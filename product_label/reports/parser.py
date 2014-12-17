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
from openerp import models, exceptions, _
from functools import partial
from reportlab.graphics.barcode import createBarcodeDrawing


class ProductLabelReport(models.AbstractModel):
    _name = 'report.product_label.label'

    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        product_obj = self.pool['product.product']
        report = report_obj._get_report_from_name(
            cr, uid, 'product_label.label')
        selected_orders = product_obj.browse(cr, uid, ids, context=context)

        docargs = {
            'doc_ids': ids,
            'doc_model': report.model,
            'docs': selected_orders,
            'formatCurrency': self.formatCurrency,
            'printBarcode': partial(self.printBarcode, cr,
                                    uid, context=context),
            'getDataContext': partial(self.getDataContext, cr,
                                      uid, context=context),
            'getFieldValue': partial(self.getFieldValue, cr,
                                     uid, context=context)
        }

        return report_obj.render(
            cr, uid, ids,
            'product_label.label', docargs,
            context=context)

    def formatCurrency(self, value):
        return str('%.2f' % value).replace('.', ',')

    def printBarcode(self, cr, uid, value, width, height, context=None):
        try:
            width, height = int(width), int(height)
            barcode = createBarcodeDrawing(
                'EAN13', value=value, format='png', width=width, height=height)
            barcode = barcode.asString('png')
            barcode = barcode.encode('base64', 'strict')
        except (ValueError, AttributeError):
            # raise exceptions.HTTPException(
            #     description='Cannot convert into barcode.')
            raise exceptions.Warning(_('Cannot convert into barcode.'))
        return barcode

    def getDataContext(self, cr, uid, context=None):
        return context['data']

    def getFieldValue(self, cr, uid, product_id, field, context=None):
        return context['data'][product_id][field]


