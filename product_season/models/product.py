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
from openerp.osv import fields, orm


class product_template(orm.Model):
    _inherit = "product.template"
    _columns = {
        'season_id': fields.many2one(
            'product.season', 'Season', required=False),
        'brand_id': fields.many2one('product.brand', 'Brand'),
        # @todo Añadir dominio para que solo sean accesibles los partners
        # proveedores y fabricante
        'manufacturer_id': fields.many2one('res.partner', 'Manufacturer')
    }


class product_season(orm.Model):
    _name = 'product.season'
    _description = 'Product season'
    _columns = {
        'name': fields.char('Name', size=255, translate=True, required=True),
        'year': fields.char('Year', size=4),
    }


class product_brand(orm.Model):
    _name = 'product.brand'
    _description = 'Product brand'
    _columns = {
        'name': fields.char('Name', size=255, translate=True, required=True),
        # @todo Añadir dominio para que solo sean accesibles los partners
        # proveedores y fabricante
        'manufacturer_id': fields.many2one('res.partner', 'Manufacturer')
    }
