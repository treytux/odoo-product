# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 Domatix Technologies  S.L. (http://www.domatix.com)
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
from openerp import models, fields, api, _, exceptions
import logging

_log = logging.getLogger(__name__)


class PackAdd(models.TransientModel):
    _name = 'pos.wiz.pack.add'
    _description = 'Add pack to sale order'

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        domain=[('is_pack', '=', True)],
        string='Pack',
        required=False)
    quantity = fields.Float(string="Quantity", default=1)

    @api.one
    def button_add(self):
        # Comprobar que han elegido un producto
        if not self.product_tmpl_id:
            raise exceptions.Warning(
                _('You must introduce a pack.'))

        # Crear una linea para el producto pack
        products = self.env['product.product'].search([
            ('product_tmpl_id', '=', self.product_tmpl_id.id)])
        data = {
            'order_id': self._context['active_id'],
            'product_id': products.id,
            'qty': self.quantity,
            'price_unit': products.list_price,
            }
        self.env['pos.order.line'].create(data)

        # Crear una linea por cada producto que tiene el pack

        for pack in self.product_tmpl_id.pack_ids:
            data = {
                'order_id': self._context['active_id'],
                'product_id': pack.product_id.id,
                'qty': pack.quantity * self.quantity,
                'price_unit': 0,
                }
            self.env['pos.order.line'].create(data)

        return {'type': 'ir.actions.act_window_close'}


