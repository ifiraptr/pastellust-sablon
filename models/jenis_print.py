from odoo import api, fields, models


class JenisPrint(models.Model):
    _name = 'pastellust.jenisprint'
    _description = 'Jenis Print Yang Tersedia'

    name = fields.Char(string='Name')
    deskripsi = fields.Char(string='Deskripsi Jenis Print')
    harga = fields.Integer(string='Harga Print')
    
    
