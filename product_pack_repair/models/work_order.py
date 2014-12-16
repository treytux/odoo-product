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
from openerp import models, api, _


class WorkOrder(models.Model):
    _inherit = 'repair.workorder'

    @api.multi
    def action_pack_add(self):
        wiz_obj = self.env['repair.wiz.pack.add']
        wiz_values = {}
        wiz = wiz_obj.create(wiz_values)
        return {'name': _('Add pack'),
                'type': 'ir.actions.act_window',
                'res_model': 'repair.wiz.pack.add',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': wiz.id,
                'target': 'new',
                }
