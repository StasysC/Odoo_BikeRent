
from odoo import models, fields

class BikeProductTemplate(models.Model):
    _inherit = 'product.product'
    
    is_bike = fields.Boolean(string="Bike")
    model = fields.Char(string="Model")
    manufacturer = fields.Char(string="Manufacturer")
    
class UserRent(models.Model):
    _inherit = 'res.partner'
        
    def current_user_rents(self):
        return {
           'type': 'ir.actions.act_window',
           'view_mode': 'form',
           'view_type': 'tree, form',
           'res_model': 'bike.rent',
           'view_id ref="menu.view_tree_bike"': '',
           'nodestroy': True,
           'target':'current',

           }