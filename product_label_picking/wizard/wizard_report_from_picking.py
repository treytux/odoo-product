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
        moves = self.env['stock.move'].search(
            [('picking_id', 'in', self.env.context['active_ids'])])

        if self.quantity == 'line':
            move_ids = [
                m.id for m in moves
                if self.include_service_product
                or (not self.include_service_product
                    and m.product_id.type not in ('service'))
            ]
        elif self.quantity == 'total':
            move_ids = []
            for m in moves:
                if self.include_service_product or (not
                   self.include_service_product and m.product_id.type
                   not in ('service')):
                    move_ids = move_ids + (
                        [m.id] * int(m.product_uom_qty))

        if not move_ids:
            raise exceptions.Warning(_('No labels for print'))
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': self.report_id.report_name,
                'datas': {'ids': move_ids},
                'context': {
                    'render_func': 'render_product_picking_label',
                    'report_name': self.report_id.report_name
                }
            }
