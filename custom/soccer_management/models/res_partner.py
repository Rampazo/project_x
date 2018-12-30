# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from datetime import datetime, date


class ResPartner(models.Model):
    _inherit = "res.partner"

    nickname = fields.Char(string="Nickname")
    date_birth = fields.Date(string="Date of Birth")
    payment_ids = fields.One2many('payment.soccer', 'partner_id', string="Payments")
    contract = fields.Selection([('none', 'None'), ('valid', 'Valid'), ('expired', 'Expired')], compute='_compute_status_contract', string="Contract")

    def _compute_status_contract(self):

        for customer in self:

            if not customer.payment_ids:
                customer.contract = 'none'

            else:
                if len(customer.payment_ids) == 1:
                    date_maturity = datetime.strptime(customer.payment_ids.date_maturity,'%Y-%m-%d').date()

                else:
                    first = 0

                    for line in customer.payment_ids:

                        if not first:
                            date_maturity = datetime.strptime(line.date_maturity,'%Y-%m-%d').date()
                            first = 1
                            continue

                        if datetime.strptime(line.date_maturity,'%Y-%m-%d').date() > date_maturity:
                            date_maturity = datetime.strptime(line.date_maturity, '%Y-%m-%d').date()

                if date_maturity <= date.today():
                    customer.contract = 'expired'
                else:
                    customer.contract = 'valid'