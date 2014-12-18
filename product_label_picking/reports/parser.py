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
