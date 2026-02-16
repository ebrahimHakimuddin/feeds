# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class SubcontractorItem(models.Model):
    _name = 'subcontractor.item'
    _description = 'Subcontractor Item'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    agreement_id = fields.Many2one('subcontractor.agreement', string='Agreement', required=True, ondelete='cascade')
    partner_id = fields.Many2one(related='agreement_id.partner_id', string='Subcontractor', store=True)
    
    product_id = fields.Many2one('product.product', string='Product Variant', required=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', related='product_id.product_tmpl_id', store=True)
    
    quantity = fields.Float(string='Agreed Quantity', required=True, default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='product_id.uom_id')
    
    unit_price = fields.Float(string='Unit Price', required=True, default=0.0)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    
    # Quantity to add when balance reaches 0
    quantity_to_add = fields.Float(string='Quantity to Add on Completion', default=0.0,
                                   help='This quantity will be added to inventory when the agreement balance reaches zero')
    
    description = fields.Text(string='Description')
    
    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.quantity * record.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.standard_price
