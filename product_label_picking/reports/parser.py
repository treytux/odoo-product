# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp import models
from functools import partial


class ProductLabelReport(models.AbstractModel):
    _inherit = 'report.product_label.label'

    def render_product_picking_label(self, cr, uid, ids, docargs,
                                     context=None):
        doc_model = 'stock.move'
        docs = self.pool[doc_model].browse(
            cr, uid, ids, context=context)
        docargs.update({
            'docs': docs,
            'doc_model': doc_model,
            'tmpl_name': 'product_label_picking.label_picking_document',
            'getPartner': partial(self.getPartner, cr, uid, context=context)
        })
        return docargs

    def getPartner(self, cr, uid, picking, context=None):
        partner = None

        # Si el albaran es de entrada
        if picking.picking_type_id and \
           picking.picking_type_id.code == 'incoming':

            # Obtener el cliente a traves del grupo de abastecimiento del alb
            # de entrada (si partner_id es cliente, proviene del pedido de un
            # cliente, por lo que sera bajo demanda)
            if picking.group_id and picking.group_id.partner_id and \
               picking.group_id.partner_id.customer is True:
                partner = picking.group_id.partner_id

        return partner
