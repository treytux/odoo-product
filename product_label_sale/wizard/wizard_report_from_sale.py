# -*- coding: utf-8 -*-
###############################################################################
#
#    Trey, Kilobytes de Soluciones
#    Copyright (C) 2014-Today Trey, Kilobytes de Soluciones <www.trey.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from openerp import models, fields, exceptions, _


class WizProductLabelFromSale(models.TransientModel):
    _inherit = 'wiz.product.label'

    quantity = fields.Selection(
        selection=[
            ('one', 'One label for each product'),
            ('line', 'One label for each line'),
            ('total', 'Total product quantity'),
        ],
        string='Quantity',
        default='total',
        translate=True)
    include_service_product = fields.Boolean(
        string='Include service products',
        default=False)

    def button_print_from_sale(self, cr, uid, ids, context=None):
        wiz = self.browse(cr, uid, ids[0], context=context)
        move_ids = self.pool['sale.order.line'].search(
            cr, uid, [('order_id', 'in', context.get('active_ids', []))])
        moves = self.pool['sale.order.line'].browse(cr, uid, move_ids)

        product_ids = []
        if wiz.quantity == 'one':
            product_ids = [m.product_id.id for m in moves]
            product_ids = list(set(product_ids))
        elif wiz.quantity == 'line':
            product_ids = [m.product_id.id for m in moves]
        elif wiz.quantity == 'total':
            for m in moves:
                product_ids = product_ids + (
                    [m.product_id.id] * int(m.product_uom_qty))

        if not wiz.include_service_product:
            products = self.pool['product.product'].browse(
                cr, uid, list(set(product_ids)))
            for product in products:
                if product.type == 'service':
                    product_ids = filter(lambda x: x != product.id,
                                         product_ids)

        product_ids = filter(lambda x: x, product_ids)

        if not product_ids:
            raise exceptions.Warning(_('No labels for print'))

        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': wiz.report_id.report_name,
                'datas': {'ids': product_ids},
            }
