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
from openerp import api, models, fields, _, exceptions


class WizProductLabelFromPicking(models.TransientModel):
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

    @api.multi
    def button_print_from_picking(self):
        import logging
        _log = logging.getLogger(__name__)
        _log.info(':'*100)
        _log.info('//button_print_from_picking')
        # # _log.info('self' % self)
        # # _log.info('self.env' % self.env)
        # # _log.info('self.env.context' % self.env.context)
        _log.info('self.env.context[active_ids]: %s' % self.env.context['active_ids'])
        # # # Escribir en el campo del asistente el pedido de venta (lo
        # # # necesitaremos en el asistente print label)
        # # self.write({'order_id': self.env.context['active_id']})

        moves = self.env['stock.move'].search(
            [('picking_id', 'in', self.env.context['active_ids'])])
        _log.info('moves: %s' % moves)
        product_ids = []

        if self.quantity == 'one':
            product_ids = [m.product_id.id for m in moves]
            product_ids = list(set(product_ids))
        elif self.quantity == 'line':
            product_ids = [m.product_id.id for m in moves]
        elif self.quantity == 'total':
            for m in moves:
                product_ids = product_ids + (
                    [m.product_id.id] * int(m.product_uom_qty))

        if not self.include_service_product:
            products = self.env['product.product'].browse(
                list(set(product_ids)))
            for product in products:
                if product.type == 'service':
                    product_ids = filter(lambda x: x != product.id,
                                         product_ids)

        product_ids = filter(lambda x: x, product_ids)
        _log.info('product_ids %s' % product_ids)
        if not product_ids:
            raise exceptions.Warning(_('No labels for print'))
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': self.report_id.report_name,
                'datas': {'ids': product_ids},
            }
