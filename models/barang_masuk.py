from odoo import api, fields, models


class BarangMasuk(models.Model):
    _name = 'pastellust.barangmasuk'
    _description = 'Barang Masuk dari Supplier'

    name = fields.Many2one(comodel_name='pastellust.pesan', string='Name', domain=[('sudah_masuk','=', False)])
    tgl_pesan = fields.Char(compute='_compute_tgl_pesan', string='Tanggal Pemesanan')
    
    @api.depends('name')
    def _compute_tgl_pesan(self):
        for record in self:
            record.tgl_pesan = record.name.tanggal_pesan

    tgl_datang = fields.Datetime(string='Tanggal Barang Datang', default = fields.Datetime.now())
    tagihan = fields.Float(compute='_compute_tagihan', string='Tagihan')
    
    @api.depends('name')
    def _compute_tagihan(self):
        for record in self:
            record.tagihan = record.name.tagihan_supplier

    supplier = fields.Char(compute='_compute_supplier', string='Supplier')
    
    @api.depends('name')
    def _compute_supplier(self):
        for record in self:
            record.supplier = record.name.supplier
    
