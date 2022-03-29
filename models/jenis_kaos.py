from odoo import api, fields, models


class JenisKaos(models.Model):
    _name = 'pastellust.jeniskaos'
    _description = 'Jenis Kaos Yang Tersedia'

    name = fields.Char(string='Name')
    stok = fields.Integer(string='Stok Kaos')
    harga = fields.Integer(string='Harga Kaos')
    
