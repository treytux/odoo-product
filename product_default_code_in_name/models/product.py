# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################

from openerp import models, fields, api
import logging
logger = logging.getLogger(__name__)

# class product_protuct(models.Model):
#     _inherit = "product.product"

#     display_name = fields.Char(compute='_compute_display_name')

#     @api.one
#     @api.depends('name', 'default_code')
#     def _compute_display_name(self):
#         print "*" * 80
#         print "*" * 80
#         print self.default_code
#         print "*" * 80
#         print "*" * 80

#         if self.default_code:
#             return '[%s] %s' % (self.default_code, self.name)
#         else:
#             return self.name


class product_template(models.Model):
    _inherit = "product.template"

    @api.depends(lambda self: (self._rec_name,) if self._rec_name else ())
    def _compute_display_name(self):
        for i, got_name in enumerate(self.name_get()):
            if self[i].default_code:
                self[i].display_name = u'[{}] {}'.format(self[i].default_code, got_name[1])
            else:
                self[i].display_name = got_name[1]

            # logger.info(u'*' * 20)
            # logger.info(u'display name: {} {}'.format(self[i].default_code, self[i].display_name))

#     # display_name = fields.Char(compute='_compute_display_name')

#     # @api.one
#     # @api.depends('name', 'default_code', 'future_display_name')
#     # def _compute_display_name(self):
#     #     if self.default_code:
#     #         return '[%s] %s' % (self.default_code, self.name)
#     #     else:
#     #         return self.name

#     # @api.depends(lambda self: (self._rec_name,) if self._rec_name else ())
#     def _compute_display_name(self):
#         logger.info('display name')
