# # -*- coding: utf-8 -*-
# ###############################################################################
# #
# #    Trey, Kilobytes de Soluciones
# #    Copyright (C) 2014-Today Trey, Kilobytes de Soluciones <www.trey.es>
# #
# #    This program is free software: you can redistribute it and/or modify
# #    it under the terms of the GNU Affero General Public License as
# #    published by the Free Software Foundation, either version 3 of the
# #    License, or (at your option) any later version.
# #
# #    This program is distributed in the hope that it will be useful,
# #    but WITHOUT ANY WARRANTY; without even the implied warranty of
# #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #    GNU Affero General Public License for more details.
# #
# #    You should have received a copy of the GNU Affero General Public License
# #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# #
# ###############################################################################
# from openerp import models, exceptions, _
# from functools import partial
# from reportlab.graphics.barcode import createBarcodeDrawing

# import logging

# _log = logging.getLogger(__name__)


# class ProductLabelReport(models.AbstractModel):
#     _inherit = 'report.product_label.label'

#     def render_html(self, cr, uid, ids, data=None, context=None):
#         return super(ProductLabelReport, self).render_html(
#             cr, uid, ids, data, context)

#     def getPricelist(self, cr, uid, product, context=None):
#         _log.info('/'*100)
#         _log.info('//getPricelist--product_label_sale')
#         _log.info('context %s' % context)
#         _log.info('context[active_id] %s' % context['active_id'])

#         # Necesito el id del pedido de venta!!
#         # Se lo paso al wiz pero aqui no conozco el id del wiz

#         # _log.info('self %s' % self)
#         # _log.info('self.quantity %s' % self.quantity)
#         # _log.info('self.order_id %s' % self.order_id)




#         return super(ProductLabelReport, self).getPricelist(
#             cr, uid, product, context)

#         # # Cargar la tarifa del pedido de venta
#         # order = self.pool.get('sale.order').browse(
#         #     cr, uid, context['active_id'], context=context)
#         # if order.pricelist_id:
#         #     prices = self.pool.get('product.pricelist').price_get(
#         #         cr, uid, [order.pricelist_id],
#         #         product.id, 1, context=context)
#         #     price_unit = prices[order.pricelist_id][0]
#         #     price = self.pool.get('account.tax').compute_all(
#         #         cr, uid, product.taxes_id, price_unit, 1)
#         #     return price['total_included']
#         # else:
#         #     return 0.00


