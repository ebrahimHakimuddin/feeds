# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WeeklyPaymentWizard(models.TransientModel):
    _name = 'weekly.payment.wizard'
    _description = 'Weekly Payment Wizard'

    partner_id = fields.Many2one('res.partner', string='Subcontractor', required=True)
    payment_date = fields.Date(string='Payment Date', required=True, default=fields.Date.context_today)
    
    agreement_line_ids = fields.One2many('weekly.payment.wizard.line', 'wizard_id', string='Unpaid Agreements')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Load all agreements with unpaid balance for selected partner"""
        if self.partner_id:
            agreements = self.env['subcontractor.agreement'].search([
                ('partner_id', '=', self.partner_id.id),
                ('state', '=', 'active')
            ])
            
            lines = []
            for agreement in agreements:
                if agreement.balance > 0:
                    lines.append((0, 0, {
                        'agreement_id': agreement.id,
                        'total_value': agreement.total_value,
                        'total_paid': agreement.total_paid,
                        'balance': agreement.balance,
                        'payment_amount': 0.0,
                    }))
            
            self.agreement_line_ids = lines

    def action_create_payments(self):
        """Create payment records for selected agreements"""
        payment_obj = self.env['subcontractor.payment']
        
        for line in self.agreement_line_ids:
            if line.payment_amount > 0:
                payment_obj.create({
                    'agreement_id': line.agreement_id.id,
                    'payment_date': self.payment_date,
                    'amount': line.payment_amount,
                    'state': 'draft',
                    'notes': f'Weekly payment via wizard on {self.payment_date}'
                })
        
        return {'type': 'ir.actions.act_window_close'}


class WeeklyPaymentWizardLine(models.TransientModel):
    _name = 'weekly.payment.wizard.line'
    _description = 'Weekly Payment Wizard Line'

    wizard_id = fields.Many2one('weekly.payment.wizard', string='Wizard', required=True, ondelete='cascade')
    agreement_id = fields.Many2one('subcontractor.agreement', string='Agreement', required=True)
    
    total_value = fields.Float(string='Total Agreement Value', readonly=True)
    total_paid = fields.Float(string='Amount Paid', readonly=True)
    balance = fields.Float(string='Balance', readonly=True)
    payment_amount = fields.Float(string='Payment Amount')
    
    @api.onchange('payment_amount')
    def _onchange_payment_amount(self):
        """Ensure payment amount doesn't exceed balance"""
        if self.payment_amount > self.balance:
            self.payment_amount = self.balance
