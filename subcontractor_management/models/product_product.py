# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        """Override name_get to show variant attributes more clearly in subcontractor context"""
        result = []
        for product in self:
            if self._context.get('subcontractor_item_view'):
                # Show product template name + variant attributes
                name = product.product_tmpl_id.name
                if product.product_template_attribute_value_ids:
                    variant_name = ', '.join(
                        product.product_template_attribute_value_ids.mapped('name')
                    )
                    name = f"{name} ({variant_name})"
                result.append((product.id, name))
            else:
                result.append((product.id, product.display_name))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        """Enhanced search to find products by variant attributes"""
        args = args or []
        if name and self._context.get('subcontractor_item_view'):
            # Search by product template name or attribute values
            products = self.search([
                '|', '|',
                ('name', operator, name),
                ('product_tmpl_id.name', operator, name),
                ('product_template_attribute_value_ids.name', operator, name)
            ] + args, limit=limit)
            return products.ids
        return super(ProductProduct, self)._name_search(name, args, operator, limit, name_get_uid)
