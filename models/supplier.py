from odoo import api, fields, models


class Supplier(models.Model):
    _name = 'pastellust.supplier'
    _description = 'Supplier Bahan dan Alat Pastellust Sablon'

    name = fields.Char(string='Supplier')
    alamat = fields.Char(string='Alamat')
    cp = fields.Char(string='Contact Person')
    bahanalat = fields.One2many(comodel_name='pastellust.perlengkapan', inverse_name='suppliernya', string='Bahan Supply')
    
    
    
