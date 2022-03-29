from odoo import api, fields, models


class AreaCetak(models.Model):
    _name = 'pastellust.areacetak'
    _description = 'Area Cetak Sablon'

    name = fields.Char(string='Name')
    ukuran = fields.Char(string='Ukuran Area Cetak')
    harga = fields.Integer(string='Harga Per-Ukuran')
    
    
