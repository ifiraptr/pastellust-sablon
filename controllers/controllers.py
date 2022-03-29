from odoo import http, models, fields
from odoo.http import request
import json


class PastellustSablon(http.Controller):
    @http.route('/jenisprint', auth='public', methods=['GET'], csrf=True)
    def get_print(self, **kwargs):
        print = request.env['pastellust.jenisprint'].search([])
        value = []
        for p in print:
            value.append({
                'nama' : p.name,
                'deskripsi' : p.deskripsi,
                'harga' : p.harga               
            })
        return json.dumps(value)

    @http.route('/jeniskaos', auth='public', methods=['GET'])
    def get_kaos(self, **kwargs):
        kaos = request.env['pastellust.jeniskaos'].search([])
        value = []
        for k in kaos:
            value.append({
                'nama' : k.name,
                'stok' : k.stok,
                'harga' : k.harga               
            })
        return json.dumps(value)

    @http.route('/areacetak', auth='public', methods=['GET'])
    def get_models(self, **kwargs):
        area = request.env['pastellust.areacetak'].search([])
        value = []
        for a in area:
            value.append({
                'nama' : a.name,
                'ukuran' : a.ukuran,
                'harga' : a.harga              
            })
        return json.dumps(value)

    @http.route('/akunting', auth='public', methods=['GET'])
    def get_akunting(self, **kwargs):
        akunting = request.env['pastellust.akunting'].search([])
        value = []
        for ak in akunting:
            value.append({
                'nama':ak.name,
                'tanggal':str(ak.date),
                'debet':ak.debet,
                'kredit':ak.kredit,
                'saldo':ak.saldo
            })
        return json.dumps(value)
