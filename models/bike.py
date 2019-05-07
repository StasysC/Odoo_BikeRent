# -*- coding: utf-8 -*-
"""
Bike rent module for odoo
"""
import pdb
from datetime import datetime
from odoo import models, fields, api
from odoo import exceptions

class BikeRent(models.Model):
    """
    Versada module
    """
    _name = 'bike.rent'
    _description = 'Bike'
    _inherit_ = 'product.template'
    partner_id = fields.Many2one('res.partner')
    bike_id = fields.Many2one('bike.product.template')
    price = fields.Float()
    rent_start = fields.Date(required=True)
    rent_stop = fields.Date(required=True)
    notes = fields.Char()
    number_of_days = fields.Integer(compute='get_number_of_days')
    
    manufacturer = fields.Char()
    model = fields.Char()
        
    def get_number_of_days(self):
#        pdb.set_trace()
        rent_duration = self.rent_stop - self.rent_start
        self.number_of_days = rent_duration.days         
    
    @api.onchange('rent_start', 'rent_stop')
    def days_for_rent(self):
        """
        Calculates and shows days bike has been booked for
        """
        try:
            rent_duration = self.rent_stop - self.rent_start
            if rent_duration.days >= 0:                
                self.get_number_of_days()
            else:
                self.number_of_days = False
                self.rent_stop = False
                return {
                    'warning': {
                        'title': 'Wrong end date!',
                        'message': '"Rent stop" date cannot be before "Rent start" date',
                        }
                    }
        except AttributeError:
            pass
        except TypeError:
            pass
            