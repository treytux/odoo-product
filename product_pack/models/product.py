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


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pack_ids = fields.One2many(
        comodel_name='product.pack',
        inverse_name='product_tmpl_id',
        string='Pack')
    is_pack = fields.Boolean(
        compute='_compute_is_pack',
        string='Is a pack',
        store=True)

    @api.one
    @api.depends('pack_ids')
    def _compute_is_pack(self):
        self.is_pack = bool(self.pack_ids)
