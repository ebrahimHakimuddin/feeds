# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class SubcontractorAgreement(models.Model):
    _name = 'subcontractor.agreement'
    _description = 'Subcontractor Agreement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc'

    name = fields.Char(string='Agreement Reference', required=True, copy=False, readonly=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Subcontractor', required=True, tracking=True)
    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.context_today, tracking=True)
    date_end = fields.Date(string='End Date', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    # Financial fields
    total_value = fields.Float(string='Total Agreement Value', compute='_compute_total_value', store=True)
    total_paid = fields.Float(string='Total Paid', compute='_compute_total_paid', store=True)
    balance = fields.Float(string='Balance Unpaid', compute='_compute_balance', store=True)
    
    # Relations
    item_ids = fields.One2many('subcontractor.item', 'agreement_id', string='Subcontracted Items')
    payment_ids = fields.One2many('subcontractor.payment', 'agreement_id', string='Payments')
    
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('subcontractor.agreement') or 'New'
        return super(SubcontractorAgreement, self).create(vals)

    @api.depends('item_ids.total_price')
    def _compute_total_value(self):
        for record in self:
            record.total_value = sum(record.item_ids.mapped('total_price'))

    @api.depends('payment_ids.amount', 'payment_ids.state')
    def _compute_total_paid(self):
        for record in self:
            record.total_paid = sum(record.payment_ids.filtered(lambda p: p.state == 'confirmed').mapped('amount'))

    @api.depends('total_value', 'total_paid')
    def _compute_balance(self):
        for record in self:
            record.balance = record.total_value - record.total_paid

    def action_activate(self):
        self.write({'state': 'active'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
