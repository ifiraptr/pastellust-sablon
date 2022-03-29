from odoo import api, fields, models


class Perlengkapan(models.Model):
    _name = 'pastellust.perlengkapan'
    _description = 'Alat dan Bahan Pastellust Sablon'

    name = fields.Char(string='Name')
    harga = fields.Integer(string='Harga Satuan')
    stok = fields.Integer(string='Stok')
    suppliernya = fields.Many2one(comodel_name='pastellust.supplier', string='Supplier')
    telp = fields.Char(compute='_compute_telp', string='No. Telp')
    
    @api.depends('suppliernya')
    def _compute_telp(self):
        for record in self:
            record.telp = record.suppliernya.cp
    
    
    

