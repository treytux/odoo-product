# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp import models, exceptions, _
from functools import partial
from reportlab.graphics.barcode import createBarcodeDrawing


class ProductLabelReport(models.AbstractModel):
    _name = 'report.product_label.label'

    def render_product_label(self, cr, uid, ids, docargs, context=None):
        docs = self.pool['product.product'].browse(
            cr, uid, ids, context=context)
        docargs.update({
            'docs': docs,
            'tmpl_name': 'product_label.label_document',
        })
        return docargs

    def render_html(self, cr, uid, ids, data=None, context=None):
        docargs = {
            'doc_ids': ids,
            'doc_model': 'product.product',
            'formatCurrency': self.formatCurrency,
            'printBarcode': partial(self.printBarcode, cr,
                                    uid, context=context),
            'formatSize': partial(self.formatSize, cr,
                                  uid, context=context),
        }

        if 'render_func' in context and hasattr(self, context['render_func']):
            fnc = getattr(self, context['render_func'])
            fnc(cr, uid, ids, docargs, context=context)
        else:
            raise exceptions.Warning(_('Don\'t have render func'))

        return self.pool['report'].render(
            cr, uid, ids,
            context.get('report_name', 'product_label.label'),
            docargs,
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

    def formatSize(self, cr, uid, value, size, context=None):
        try:
            return value[:size]
        except:
            return value
