
from odoo import models, fields, api
from datetime import datetime, timedelta

class BikeProductTemplate(models.Model):
    _inherit = 'product.product'
    
    is_bike = fields.Boolean(string='Bike')
    model = fields.Char(string='Model')
    manufacturer = fields.Char(string='Manufacturer')
 
class UserRent(models.Model):
    _inherit = 'res.partner'
    _compute_rent_count = fields.Integer(compute='get_rent_count')
    partner_ids = fields.One2many('bike.rent', 'partner_id')
    backwards = fields.One2many(comodel_name='bike.rent',
                                inverse_name='partner_id')

    def current_user_rents(self):
        return {
           'name': 'Rents',
           'type': 'ir.actions.act_window',
           'view_mode': 'tree,form',
           'view_type': 'form',
           'res_model': 'bike.rent',
           'nodestroy': True,
           'target':'current',
           'domain': [('partner_id','in',[self.name])]
           }
        
    @api.multi
    def get_rent_count(self):
        for record in self:
            record._compute_rent_count = len(record.partner_ids)
            print(record._compute_rent_count)

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    return_date = fields.Date(string='Bike return date')
    
    @api.multi
    def return_date(self):
        bike_rent_obj = self.env['sale.order']
        self.return_date = bike_rent_obj.rent_stop

class SaleOrder(models.Model):
    _inherit = 'sale.order'
  
    rent_start = fields.Date(string='Rent start', required=True)
    rent_stop = fields.Date(string='Rent stop', required=True)
    rent_duration = fields.Integer(string='Rent duration')
    
    @api.multi
    @api.depends('rent_duration')
    def rent_dates(self):
        for record in self:
            record.rent_start = datetime.today().strftime('%Y-%m-%d')
            record.rent_stop = record.rent_start + timedelta(record.rent_duration)
        
    @api.multi
    def action_confirm(self):
        self.rent_dates()
        def filter_rests(record):
            return record.product_id.is_bike and record.product_id.type == 'service'
                   
        for record in self.order_line.filtered(filter_rests):
            self.env['bike.rent'].create({
                'price': record.price_subtotal,
                'rent_start': self.rent_start,
                'rent_stop': self.rent_stop,
                'partner_id': record.order_partner_id.id,
                'bike_id': record.product_id.id,
            })
        return super(SaleOrder, self).action_confirm()