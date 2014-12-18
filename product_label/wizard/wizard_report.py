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


class WizProductLabel(models.TransientModel):
    _name = 'wiz.product.label'
    _description = 'Wizard to report label'

    def _get_default_report(self):
        report_ids = self.env['ir.actions.report.xml'].search(
            [('name', 'ilike', '(product_label)')])
        return report_ids[0]

    report_id = fields.Many2one(
        comodel_name='ir.actions.report.xml',
        string='Report',
        domain=[('name', 'ilike', '(product_label)')],
        default=_get_default_report,
        required=True)

    def getPrice(self, product):
        cr, uid, context = self.env.args
        pricelists = self.env['product.pricelist'].search([
            ('type', '=', 'sale')])

        if len(pricelists) > 1:
            pricelists = self.env['product.pricelist'].search([
                ('name', 'ilike', 'Public Pricelist'), ('type', '=', 'sale')])
        if pricelists:
            prices = pricelists[0].price_get(product.id, 1)
            price_unit = prices[pricelists[0].id]
            price = product.taxes_id.compute_all(price_unit, 1)

            return price['total_included']
        else:
            return 0.00

    @api.multi
    def button_print(self):
        datas = {'ids': self.env.context['active_ids']}

        return {
            'type': 'ir.actions.report.xml',
            'report_name': self.report_id.report_name,
            'datas': datas,
            'context': {
                'render_func': 'render_product_label',
                'report_name': self.report_id.report_name
            },
        }
