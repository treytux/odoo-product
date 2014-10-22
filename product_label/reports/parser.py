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
import logging

_log = logging.getLogger(__name__)


class ProductLabelReport(models.AbstractModel):
    _name = 'report.product_label.label'

    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        purchase_obj = self.pool['product.product']
        report = report_obj._get_report_from_name(
            cr, uid, 'product_label.label')
        selected_orders = purchase_obj.browse(cr, uid, ids, context=context)

        docargs = {
            'doc_ids': ids,
            'doc_model': report.model,
            'docs': selected_orders,
            'formatCurrency': self.formatCurrency,
            'get_pricelist': partial(self.get_pricelist, cr,
                                     uid, context=context)
        }

        return report_obj.render(
            cr, uid, ids,
            'product_label.label', docargs,
            context=context)

    def formatCurrency(self, value):
        return str('%.2f' % value).replace('.', ',')

    def get_pricelist(self, cr, uid, product, context=None):
        pricelist_ids = self.pool['product.pricelist'].search(
            cr, uid, [('type', '=', 'sale')])

        if len(pricelist_ids) > 1:
            pricelist_ids = self.pool.get('product.pricelist').search(
                cr, uid,
                [('name', 'ilike', 'Public Pricelist'), ('type', '=', 'sale')])

        if pricelist_ids:
            prices = self.pool.get('product.pricelist').price_get(
                cr, uid, pricelist_ids,
                product.id, 1, context=context)
            price_unit = prices[pricelist_ids[0]]
            price = self.pool.get('account.tax').compute_all(
                cr, uid, product.taxes_id, price_unit, 1)
            return price['total_included']
        else:
            return 0.00
