# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.
from openerp import models, api
from functools import partial


class ProductLabelReport(models.AbstractModel):
    _inherit = 'report.product_label.label'

    @api.multi
    def render_product_picking_label(self, docargs):
        docargs.update({
            'docs': self,
            'doc_model': 'stock.move',
            'tmpl_name': 'product_label_picking.label_picking_document',
            'getPartner': partial(self.getPartner)
        })
        return docargs

    @api.model
    def getPartner(self, picking):
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
