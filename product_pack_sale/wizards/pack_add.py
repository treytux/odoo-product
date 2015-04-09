# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp import models, fields, api, _, exceptions
import logging

_log = logging.getLogger(__name__)


class PackAdd(models.TransientModel):
    _name = 'wiz.pack.add'
    _description = 'Add pack to sale order'

    order_id = fields.Many2one(
        comodel_name='sale.order',
        required=True,
        string='Order'
    )
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        domain=[('is_pack', '=', True)],
        string='Pack'
    )
    quantity = fields.Float(
        string="Quantity"
    )
    price_content_pack = fields.Selection(
        selection=[
            ('show_price', 'Show price'),
            ('hide_price', 'Hide price'),
        ],
        string='Price content pack',
        default='show_price',
        help="Show or hide product prices that make the content of the pack."
    )

    @api.one
    def button_add(self):
        # Comprobar que han elegido un producto
        if not self.product_tmpl_id:
            raise exceptions.Warning(
                _('You must introduce a pack.')
            )

        # Crear una linea para el producto pack
        products = self.env['product.product'].search([
            ('product_tmpl_id', '=', self.product_tmpl_id.id)])
        data = {
            'order_id': self._context['active_id'],
            'product_id': products.id,
            'product_uom_qty': self.quantity,
            'product_uos_qty': self.quantity,
            }
        self.env['sale.order.line'].create(data)

        # Crear una linea por cada producto que tiene el pack

        if self.price_content_pack == 'show_price':
            for pack in self.product_tmpl_id.pack_ids:
                data = {
                    'order_id': self._context['active_id'],
                    'product_id': pack.product_id.id,
                    'product_uom_qty': pack.quantity * self.quantity,
                    'product_uos_qty': pack.quantity * self.quantity,
                    'discount': 100,
                    }
                self.env['sale.order.line'].create(data)

        if self.price_content_pack == 'hide_price':
            for pack in self.product_tmpl_id.pack_ids:
                data = {
                    'order_id': self._context['active_id'],
                    'product_id': pack.product_id.id,
                    'product_uom_qty': pack.quantity * self.quantity,
                    'product_uos_qty': pack.quantity * self.quantity,
                    'price_unit': 0,
                    }
                self.env['sale.order.line'].create(data)

        return {'type': 'ir.actions.act_window_close'}
