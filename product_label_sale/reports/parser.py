# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

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
