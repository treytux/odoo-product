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
from openerp import models, fields, api
import logging

_log = logging.getLogger(__name__)


class PackAdd(models.TransientModel):
    _name = 'repair.wiz.pack.add'
    _description = 'Add pack to sale order'

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        domain=[('is_pack', '=', True)],
        string='Pack',
        required=True)
    quantity = fields.Float(string="Quantity", default=1)

    @api.one
    def button_add(self):
        # Crear una linea para el producto pack
        products = self.env['product.product'].search([
            ('product_tmpl_id', '=', self.product_tmpl_id.id)])
        type = 'product'
        if self.product_tmpl_id.type == 'service':
            type = 'service'
        data = {
            'workorder_id': self._context['active_id'],
            'product_id': products.id,
            'type': type,
            'description': products.name,
            'quantity': self.quantity,
            'price_unit': products.list_price,
            }
        self.env['repair.workorder.consumed'].create(data)

        # Crear una linea por cada producto que tiene el pack

        for pack in self.product_tmpl_id.pack_ids:
            type = 'product'
            if pack.product_id.type == 'service':
                type = 'service'
            data = {
                'workorder_id': self._context['active_id'],
                'product_id': pack.product_id.id,
                'type': type,
                'description': products.name,
                'quantity': pack.quantity * self.quantity,
                'price_unit': 0,
                }
            self.env['repair.workorder.consumed'].create(data)

        return {'type': 'ir.actions.act_window_close'}

