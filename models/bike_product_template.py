# -*- coding: utf-8 -*-

from odoo import models, fields

class BikeProductTemplate(models.Model):
    _name = 'bike.product.template'
    _inherit = ['product.product']
    
    is_bike = fields.Boolean(string="Dviratukas")