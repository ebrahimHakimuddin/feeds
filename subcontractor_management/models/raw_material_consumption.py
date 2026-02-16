# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class RawMaterialConsumption(models.Model):
    _name = 'raw.material.consumption'
    _description = 'Raw Material Consumption'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'consumption_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    consumption_date = fields.Date(string='Consumption Date', required=True, default=fields.Date.context_today, tracking=True)
    
    agreement_id = fields.Many2one('subcontractor.agreement', string='Related Agreement', tracking=True)
    partner_id = fields.Many2one('res.partner', string='Subcontractor', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    # Material lines
    line_ids = fields.One2many('raw.material.consumption.line', 'consumption_id', string='Materials')
    
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True)
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('raw.material.consumption') or 'New'
        return super(RawMaterialConsumption, self).create(vals)

    @api.depends('line_ids.total_cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(record.line_ids.mapped('total_cost'))

    def action_confirm(self):
        """Confirm the consumption"""
        self.write({'state': 'confirmed'})

    def action_done(self):
        """Mark as done and consume materials from inventory"""
        for record in self:
            for line in record.line_ids:
                line._consume_material()
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})


class RawMaterialConsumptionLine(models.Model):
    _name = 'raw.material.consumption.line'
    _description = 'Raw Material Consumption Line'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    consumption_id = fields.Many2one('raw.material.consumption', string='Consumption', required=True, ondelete='cascade')
    
    product_id = fields.Many2one('product.product', string='Material', required=True, domain=[('detailed_type', '=', 'product')])
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='product_id.uom_id')
    
    unit_cost = fields.Float(string='Unit Cost', required=True)
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True)
    
    description = fields.Text(string='Description')

    @api.depends('quantity', 'unit_cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * record.unit_cost

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_cost = self.product_id.standard_price

    def _consume_material(self):
        """Create stock move to consume material"""
        if self.quantity <= 0:
            return
        
        stock_location = self.env.ref('stock.stock_location_stock')
        # Using production location as destination for consumed materials
        production_location = self.env.ref('stock.location_production', raise_if_not_found=False)
        if not production_location:
            # Fallback to inventory loss if production location doesn't exist
            production_location = self.env.ref('stock.stock_location_scrapped')
        
        move_vals = {
            'name': f'Material Consumption: {self.product_id.name}',
            'product_id': self.product_id.id,
            'product_uom': self.uom_id.id,
            'product_uom_qty': self.quantity,
            'location_id': stock_location.id,
            'location_dest_id': production_location.id,
            'origin': f'{self.consumption_id.name}',
        }
        
        move = self.env['stock.move'].create(move_vals)
        move._action_confirm()
        move._action_done()
