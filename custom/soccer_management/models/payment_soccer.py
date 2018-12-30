# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError


class PaymentSoccer(models.Model):
    _name = "payment.soccer"
    _description = "Payment Soccer"

    @api.returns('self')
    def _payment_mode_default(self):
        return self.env['payment.mode.soccer'].search([], limit=1)

    name = fields.Char(string="Refence", readonly=True)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True, domain="[('customer', '=', True)]")
    payment_type = fields.Selection([('monthly', 'Monthly'), ('loose', 'Loose')], string="Payment Type", default='monthly', required=True)
    payment_mode_id = fields.Many2one('payment.mode.soccer', string="Payment Mode", default=_payment_mode_default)
    date = fields.Date(string="Payment Date", default=fields.Date.today, required=True)
    date_maturity = fields.Date(string="Date Maturity")
    amount = fields.Float(string="Amount", required=True)
    paid = fields.Float(string="Paid")
    state = fields.Selection([('open', 'Open'), ('paid', 'Paid')], string="State", default='open')
    observation = fields.Text(string="Observation")

    @api.onchange('date','payment_type')
    def _onchange_date_maturity(self):

        if self.date and self.payment_type:
            if self.payment_type == 'monthly':
                s = datetime.strptime(self.date,'%Y-%m-%d').date() + timedelta(days=28)
                self.date_maturity = s
            else:
                s = datetime.strptime(self.date, '%Y-%m-%d').date()
                self.date_maturity = s
        else:
            self.date_maturity = False

    @api.onchange('partner_id', 'payment_type')
    def _onchange_amount(self):

        if self.partner_id and self.payment_type:
            if self.partner_id.date_birth:
                days_live = date.today() - datetime.strptime(self.partner_id.date_birth, '%Y-%m-%d').date()
                age = days_live.days / 365

                if self.payment_type == 'monthly' and age > 16:
                    self.amount = 40
                elif self.payment_type == 'monthly' and age <= 16:
                    self.amount = 30
                elif self.payment_type == 'loose' and age > 16:
                    self.amount = 15
                elif self.payment_type == 'loose' and age <= 16:
                    self.amount = 10
                else:
                    self.amount = 0


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('payment.soccer') or _('Unknown Pack')
        res = super(PaymentSoccer, self).create(vals)
        return res

    def action_close_payment(self):

        if self.paid == self.amount:
            self.state = 'paid'
        else:
            raise ValidationError(_('Total paid is not equal to the total payable'))

class PaymentModeSoccer(models.Model):
    _name = "payment.mode.soccer"
    _description = "Payment Mode Soccer"

    name = fields.Char(string="Name")
    amount = fields.Float(compute='_compute_amount', string="Amount")
    payment_mode_default = fields.Boolean(string="Payment Mode Default")
    payment_ids = fields.One2many('payment.soccer', 'payment_mode_id', string="Payments")

    def _compute_amount(self):

        amount = 0

        for line in self.payment_ids:
            amount += line.paid

        self.amount = amount


