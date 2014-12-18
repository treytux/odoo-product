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
from openerp import models


class ProductLabelReport(models.AbstractModel):
    _inherit = 'report.product_label.label'

    def render_product_sale_label(self, cr, uid, ids, docargs, context=None):
        doc_model = 'sale.order.line'
        docs = self.pool[doc_model].browse(
            cr, uid, ids, context=context)
        docargs.update({
            'docs': docs,
            'doc_model': doc_model,
            'tmpl_name': 'product_label_sale.label_sale_document',

            'show_origin': context.get('show_origin', False)
        })
        return docargs
