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
from openerp import models, api, _
import logging
_log = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.one
    def action_pack_add(self):
        _log.info('x'*100)
        _log.info(self.id)

        cr, uid, context = self.env.args
        wiz_id = self.env['wiz.pack.add'].with_context(context).create({
            'order_id': self.id
        })
        _log.info(context)
        _log.info('x'*100)
        return {
            'name': _('Add pack'),
            'type': 'ir.actions.act_window',
            'res_model': 'wiz.pack.add',
            'view_type': 'form',
            'view_mode': 'form',
            'nodestroy': True,
            'context': context,
            'res_id': wiz_id.id,
            'target': 'new',
        }
