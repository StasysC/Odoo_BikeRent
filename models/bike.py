"""
This file is part of Odoo. The COPYRIGHT file at the top level of
this module contains the full copyright notices and license terms.
"""
from odoo import models, fields, api
from datetime import datetime

class BikeRent(models.Model):
    """
    Defining custom fields on module
    """
    _name = 'bike.rent'
    _inherit = 'mail.thread'
    _description = 'Bike'
    partner_id = fields.Many2one(comodel_name='res.partner',
                                 string='Partner',
                                 select=True)
    bike_id = fields.Many2one('product.product', string='Bike')
    price = fields.Float(string='Price')
    rent_start = fields.Date(string='Rent start', required=True)
    rent_stop = fields.Date(string='Rent stop', required=True)
    notes = fields.Char(string='Notes')
    today = fields.Date(default=datetime.today().strftime('%Y-%m-%d'))

    _compute_number_of_days = fields.Integer(string='Number of days',
                                    compute='get_number_of_days')    
    
#    @api.multi
#    @api.depends ('rent_stop')
#    def set_color(self):
#        today = datetime.today().strftime('%Y-%m-%d')
#        for record in self:
#            if str(record.rent_stop) < today:
#                record.color = "grey"
#            elif str(record.rent_start) < today and str(record.rent_stop) > today:
#                record.color = "green"
#            else:
#                record.color = "neveikia"
#
#            
    
    @api.multi
    @api.depends('rent_stop', 'rent_start')
    def get_number_of_days(self):
        """
        Passes the difference between rent end and start dates
        to _compute_number_of_days variable
        """
        for record in self:
            try:
                rent_duration = record.rent_stop - record.rent_start            
                record._compute_number_of_days = rent_duration.days
            except (AttributeError, TypeError):
                pass
    
    @api.onchange('_compute_number_of_days')        
    def days_is_negative(self):
        """
        If number of days are negative, clears rent_stop and 
        _compute_number_of_days fields
        """
        if self._compute_number_of_days < 0:                
            self._compute_number_of_days = False
            self.rent_stop = False
            return {
                'warning': {
                    'title': 'Wrong end date!',
                    'message': '"Rent stop" date cannot be before "Rent start" date',
                    }
                }
    