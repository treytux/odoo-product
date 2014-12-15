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
from openerp import models, fields, _


class WizProductLabelPicking(models.TransientModel):
    _name = 'wiz.product.label.picking'
    _description = 'Wizard to report label from picking'

    def _get_default_report(self):
        report_ids = self.env['ir.actions.report.xml'].search(
            [('name', 'ilike', 'label_picking')])
        return report_ids[0]

    report_id = fields.Many2one(
        comodel_name='ir.actions.report.xml',
        string='Report',
        domain=[('name', 'ilike', 'label_picking')],
        default=_get_default_report,
        required=True)
    quantity = fields.Selection(
        selection=[
            ('one', 'One label for each product'),
            ('line', 'One label for each line'),
            ('total', 'Total product quantity'),
        ],
        string='Quantity',
        default='total',
        translate=True)

    def button_print_from_picking(self, cr, uid, ids, context=None):
        wiz = self.browse(cr, uid, ids[0], context=context)

        picking_ids = context.get('active_ids', [])
        return {
            'type': 'ir.actions.report.xml',
            'report_name': wiz.report_id.report_name,
            'datas': {'ids': picking_ids},
        }
