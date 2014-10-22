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


class WizCreateInvoice(models.TransientModel):
    _name = 'wiz.product.label'
    _description = 'Wizard to report label'

    name = fields.Char(string="Description")

    def get_report_formats(self):
        report_ids = self.env['ir.actions.report.xml'].search([])
        return self.env['ir.actions.report.xml'].browse(report_ids)

    @api.one
    def button_print(self):
        import logging

        _log = logging.getLogger(__name__)
        _log.info(self.env.context)
        _log.info('------------------------------------------')
        _log.info('------------------------------------------')

        product = self.env['product.product'].browse(
            self.env.context['active_id'])

        datas = {
            'ids': [product.id],
            'model': 'product.product',
        }

        re = self.env['report'].get_action(
            [], 'product_label.label', data=datas)
        _log.info(re)

        return re
