# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.


from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    season_id = fields.Many2one(
        comodel_name='product.season',
        string='Season',
        required=False
    )
    brand_id = fields.Many2one(
        comodel_name='product.brand',
        string='Brand'
    )
    # TODO: Añadir dominio para que solo sean accesibles los partners
    manufacturer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Manufacturer'
    )


class ProductSeason(models.Model):
    _name = 'product.season'
    _description = 'Product season'

    name = fields.Char(
        string='Name',
        size=255,
        translate=True,
        required=True
    )
    year = fields.Char(
        string='Year',
        size=4
    )


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product brand'

    name = fields.Char(
        string='Name',
        size=255,
        translate=True,
        required=True
    )
    # TODO: Añadir dominio para que solo sean accesibles los partners
    manufacturer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Manufacturer'
    )
