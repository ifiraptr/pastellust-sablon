from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Order(models.Model):
    _name = 'pastellust.order'
    _description = 'Daftar Order Pastellust Sablon'

    name = fields.Char(string='Kode Order', required=True)
    pemesan = fields.Many2one(comodel_name='res.partner', string='Customer', domain=[('is_customernya','=', True)])
    phone = fields.Char(compute='_compute_phone', string='No. Telp')
    
    @api.depends('pemesan')
    def _compute_phone(self):
        for record in self:
            record.phone = record.pemesan.phone
    
    tanggal_pesan = fields.Datetime('Tanggal Pemesanan', default=fields.Datetime.now())
    tanggal_selesai = fields.Datetime(compute='_compute_tanggal', string='Tanggal Selesai') 

    @api.model
    def _compute_tanggal(self):        
        for record in self:           
            tgl = self.env['pastellust.sablonselesai'].search([('name','=', record.id)]).mapped('tgl_selesai')
            if tgl:
                record.tanggal_selesai = tgl[0]   
                record.sablon_selesai= True
            else:
                record.tanggal_selesai = 0
                record.sablon_selesai= False
                
    sablonselesai_ids = fields.One2many(comodel_name='pastellust.sablonselesai', inverse_name='name', string='Penyelesaian Sablon')
    detailkaos_ids = fields.One2many(comodel_name='pastellust.detailkaos', inverse_name='order_id', string='Detail Order')
    jenis_print = fields.Many2one(comodel_name='pastellust.jenisprint', string='Jenis Print')
    area_cetak = fields.Many2one(comodel_name='pastellust.areacetak', string='Area Cetak')
    ukuran = fields.Selection(string='Ukuran Kaos', selection=[('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL'), ('xxl', 'XXL')])
    warna = fields.Selection(string='Warna Kaos', 
                            selection=[
                                ('putih', 'Putih'), 
                                ('hitam', 'Hitam'),
                                ('merah', 'Merah'),
                                ('abu misty', 'Abu Misty'),
                                ('kuning muda', 'Kuning Muda'),
                                ('biru muda', 'Biru Muda'),
                                ('pink', 'Pink'),
                                ('coklat tua', 'Coklat Muda'),
                                ('navy', 'Navy'),
                                ('royal', 'Royal'),
                                ('abu gelap', 'Abu Gelap'),
                                ('hijau', 'Hijau'),
                                ('maroon', 'Maroon')])
    img = fields.Binary(string='Design')
    
    jml_pesanan = fields.Integer(compute='_compute_jml_pesanan', string='Jumlah Pesanan')
    sablon_selesai = fields.Boolean(string='Sudah Selesai')
    
    
    @api.depends('detailkaos_ids')
    def _compute_jml_pesanan(self):
        for record in self:
            record.jml_pesanan +=len(record.detailkaos_ids)

    total_harga = fields.Integer(compute='_compute_total_harga', string='Total Tagihan')
    
    @api.depends('jenis_print', 'area_cetak')
    def _compute_total_harga(self):
        for record in self:           
                total = sum(self.env['pastellust.detailkaos'].search([('order_id','=', record.id)]).mapped('harga'))
                record.total_harga = total + record.jenis_print.harga + record.area_cetak.harga

    des_print = fields.Char(compute='_compute_des_print', string='Deskripsi Jenis Print')
    
    @api.depends('jenis_print')
    def _compute_des_print(self):
        for record in self:
            record.des_print = record.jenis_print.deskripsi

    ukuran_cetak = fields.Char(compute='_compute_ukuran_cetak', string='Ukuran Area Cetak')
    
    @api.depends('area_cetak')
    def _compute_ukuran_cetak(self):
        for record in self:
            record.ukuran_cetak = record.area_cetak.ukuran

    masuk_akunting = fields.Boolean(string='Masuk Akunting')

    def confirm(self):
        for record in self:
            if record.tanggal_selesai:
                record.masuk_akunting=True
                self.env['pastellust.akunting'].create({'kredit':record.total_harga,'name':record.pemesan.display_name})
            else:
                raise ValidationError("Yang belum selesai disablon tidak bisa masuk.")
    def cancel(self):
        for record in self:
            record.masuk_akunting=False
            data = self.env['pastellust.akunting'].search([('name','=',record.pemesan.display_name)])
            data.unlink()
    
class DetailKaos(models.Model):
    _name = 'pastellust.detailkaos'
    _description = 'New Description'

    order_id = fields.Many2one(comodel_name='pastellust.order', string='Kode Order')
    jenis_kaos = fields.Many2one(comodel_name='pastellust.jeniskaos', string='Jenis Kaos')

    name = fields.Char(string='Name')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='Harga Satuan')
    
    @api.depends('jenis_kaos')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.jenis_kaos.harga

    qty = fields.Integer(string='Quantity')

    @api.constrains('qty')
    def _check_stok(self):
        for record in self:
            bahan = self.env['pastellust.jeniskaos'].search([('stok', '<',record.qty),('id', '!=',record.id)])
            if bahan:
                raise ValidationError("Stok kaos yang dipilih tidak cukup.")

    harga = fields.Integer(compute='_compute_harga', string='Harga')
    
    @api.depends('qty', 'harga_satuan')
    def _compute_harga(self):
        for record in self:
            record.harga = record.harga_satuan * record.qty
    
    @api.model
    def create(self,vals):
        record = super(DetailKaos, self).create(vals) 
        if record.qty:
            self.env['pastellust.jeniskaos'].search([('id','=',record.jenis_kaos.id)]).write({'stok':record.jenis_kaos.stok-record.qty})
            return record
    
    
  
    
