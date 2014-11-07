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
from openerp import models, fields, api, osv
import logging

_log = logging.getLogger(__name__)


class PackAdd(models.TransientModel):
    _name = 'wiz.pack.add'
    _description = 'Add pack to sale order'

    order_id = fields.Many2one(
        comodel_name='sale.order',
        required=True,
        string='Order')
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        domain=[('is_pack', '=', True)],
        string='Pack')
    quantity = fields.Float(string="Quantity")
    order_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Order line')

    @api.one
    def button_add(self):

        ## Crea una linea por cada producto que tiene el pack,
        # pero habra que meter otra por el pack con su importe y poner dto
        # 100 % a las del pack
        products = self.env['product.product'].search([
            ('product_tmpl_id', '=', self.product_tmpl_id.id)])
        data = {
                'order_id': self._context['active_id'],
                'product_id': products.id,
                'product_uom_qty': self.quantity,
                'product_uos_qty': self.quantity,
            }
        self.env['sale.order.line'].create(data)

        for pack in self.product_tmpl_id.pack_ids:
            data = {
                    'order_id': self._context['active_id'],
                    'product_id': pack.product_id.id,
                    'product_uom_qty': pack.quantity * self.quantity,
                    'product_uos_qty': pack.quantity * self.quantity,
                    'discount': 100,
                }
            self.env['sale.order.line'].create(data)

        return {'type': 'ir.actions.act_window_close'}
