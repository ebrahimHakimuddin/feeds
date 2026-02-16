# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SubcontractorPayment(models.Model):
    _name = 'subcontractor.payment'
    _description = 'Subcontractor Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'payment_date desc'

    name = fields.Char(string='Payment Reference', required=True, copy=False, readonly=True, default='New')
    agreement_id = fields.Many2one('subcontractor.agreement', string='Agreement', required=True, ondelete='cascade', tracking=True)
    partner_id = fields.Many2one(related='agreement_id.partner_id', string='Subcontractor', store=True)
    
    payment_date = fields.Date(string='Payment Date', required=True, default=fields.Date.context_today, tracking=True)
    amount = fields.Float(string='Payment Amount', required=True, tracking=True)
    
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('subcontractor.payment') or 'New'
        return super(SubcontractorPayment, self).create(vals)

    def action_confirm(self):
        """Confirm payment and check if balance reached zero"""
        self.write({'state': 'confirmed'})
        
        # Check if agreement balance reached zero
        for payment in self:
            agreement = payment.agreement_id
            if agreement.balance <= 0.01:  # Small threshold for floating point comparison
                # Trigger inventory update for all items
                for item in agreement.item_ids:
                    if item.quantity_to_add > 0:
                        self._update_inventory(item)

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

    def _update_inventory(self, item):
        """Update inventory when agreement is fully paid"""
        if item.quantity_to_add <= 0:
            return
        
        # Create stock move to increase inventory
        stock_location = self.env.ref('stock.stock_location_stock')
        move_vals = {
            'name': _('Subcontractor Completion: %s') % item.product_id.name,
            'product_id': item.product_id.id,
            'product_uom': item.uom_id.id,
            'product_uom_qty': item.quantity_to_add,
            'location_id': self.env.ref('stock.stock_location_suppliers').id,
            'location_dest_id': stock_location.id,
            'origin': f'{item.agreement_id.name}',
        }
        
        move = self.env['stock.move'].create(move_vals)
        move._action_confirm()
        move._action_done()
