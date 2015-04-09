# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

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
