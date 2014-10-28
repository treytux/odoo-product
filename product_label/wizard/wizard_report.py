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


class WizProductLabel(models.TransientModel):
    _name = 'wiz.product.label'
    _description = 'Wizard to report label'

    name = fields.Char(string="DescriptionXXX")

    @api.one
    def get_report_formats(self):
        report_ids = self.env['ir.actions.report.xml'].search(
            [('key', '=', 'product_label')])
        reports = self.env['ir.actions.report.xml'].browse(report_ids)
        _log.info('------------------------------------------')
        _log.info(reports)
        _log.info('------------------------------------------')
        return reports

    @api.one
    def button_print(self):
        _log.info('XXXXXXXXXXXXXXXXXXXXXXXXXXX')
        datas = {
            'ids': [self.env.context['active_id']],
            'model': 'product.product',
        }
        _log.info(datas)
        re = self.env['report'].get_action(
            [], 'product_label.label', data=datas)
        return re
