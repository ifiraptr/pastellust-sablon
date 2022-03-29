from odoo import api, fields, models


class SablonSelesai(models.Model):
    _name = 'pastellust.sablonselesai'
    _description = 'Penyelesaian Sablon'

    name = fields.Many2one(comodel_name='pastellust.order', string='Customer', domain=[('sablon_selesai','=', False)])
    tgl_pesan = fields.Char(compute='_compute_tgl_pesan', string='Tanggal Pesan')
    
    @api.depends('name')
    def _compute_tgl_pesan(self):
        for record in self:
            record.tgl_pesan = record.name.tanggal_pesan

    tgl_selesai = fields.Datetime('Tanggal Selesai', default=fields.Datetime.now())
    tagihan = fields.Char(compute='_compute_tagihan', string='Total Pembayaran')
    
    @api.depends('name')
    def _compute_tagihan(self):
        for record in self:
            record.tagihan = record.name.total_harga