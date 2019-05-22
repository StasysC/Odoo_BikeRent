
from odoo import models, fields, api

class BikeProductTemplate(models.Model):
    _inherit = 'product.product'
    
    is_bike = fields.Boolean(string='Bike')
    model = fields.Char(string='Model')
    manufacturer = fields.Char(string='Manufacturer')


 
class UserRent(models.Model):
    _inherit = 'res.partner'
    _compute_rent_count = fields.Integer(compute='get_rent_count')
    
    def current_user_rents(self):
        return {
           'name': 'Rents',
           'type': 'ir.actions.act_window',
           'view_mode': 'tree',
           'view_type': 'form',
           'res_model': 'bike.rent',
           'nodestroy': True,
           'target':'current',
           'domain': [('partner_id','in',[self.name])]
           }
        
    @api.multi
    def get_rent_count(self):
        data_obj = self.env['bike.rent']
        print("*****************************************")
        print(data_obj.partner_id.name)
        print("*****************************************")

        for record in self:

            print("*****************************************")
#            record._compute_rent_count = data_obj.search_count(['record.active', '=', True])
            record._compute_rent_count = data_obj.search_count(['record.name', '=', data_obj.partner_id])
#            list_data = data_obj.search(['record.name', '=', data_obj.partner_id])
#            print(len(list_data))
            print("*****************************************")
    
class Chatter(models.Model):
    _name = 'user.chatter'
    _inherit = 'mail.thread'