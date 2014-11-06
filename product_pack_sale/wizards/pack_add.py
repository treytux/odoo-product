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
from openerp import models, fields, api
import logging

_log = logging.getLogger(__name__)


class PackAdd(models.TransientModel):
    _name = 'wiz.pack.add'
    _description = 'Add pack to sale order'

    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Order')
    product_id = fields.Many2one(
        comodel_name='product.template',
        string='Pack')
    quantity = fields.Float(string="Quantity")

    @api.one
    def button_add(self):
        _log.info('~'*100)
        _log.info(self.env.context)
        return {'type': 'ir.actions.act_window_close'}
