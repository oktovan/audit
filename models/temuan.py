# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, tools
from openerp.exceptions import Warning as UserError
import zeep

import logging

_logger = logging.getLogger(__name__)

class AuditTemuan(models.Model):
    _name = "audit.temuan"
    _description = "Temuan"

    name = fields.Char(
        string="# Temuan",
        required=True,
        default="/",
        copy=False,
    )

    nc = fields.Text(
        string="Ketidaksesuaian",
    )

    tgl_audit = fields.Date(
        string="Tanggal Audit",
        required=True,
    )

    auditee_ids = fields.Many2many(
        string="Auditee",
        comodel_name="hr.employee",
        relation="rel_temuan_2_employee",
        column1="temuan_id",
        column2="employee_id",
    )

    auditor_ids = fields.Many2many(
        string="Auditor",
        comodel_name="hr.employee",
        relation="rel_temuan_2_employee2",
        column1="temuan_id",
        column2="employee_id",
    )

    invoice_ids=fields.One2many(
        string="Invoice",
        comodel_name="account.invoice",
        inverse_name="temuan_id",
    #   relation="rel_temuan_2_invoice",
    #    column1="temuan_id",
    #    column2="invoice_id",
    #    context="{'koplak':invoice_ids}",
    )


    picking_ids = fields.Many2many(
        string="Good Receipt",
        comodel_name="stock.picking",
    #    domain="[('origin', 'in', koplak)]",
        domain="[('origin', 'in', ['dummies'])]",
    #    relation="rel_temuan_2_picking",
    #    column1="temuan_id",
    #    column2="picking_id",
    )


    klausul_id = fields.Many2one(
        string="Klausul",
        comodel_name="audit.klausul",
    )

    kategori = fields.Selection(
        string="Kategori",
        selection=[
            ("major", "Major"),
            ("minor", "Minor"),
            ("observation", "Observation"),
        ],
        required=True,
        default="minor",
    )

    state = fields.Selection(
        string="State",
        selection=[
            ("open", "Open"),
            ("close", "Closed"),
        ],
        required=True,
        default="open",
    )

    akar_masalah=fields.Text(
        string="Akar Masalah",
    )

    tindakan_perbaikan=fields.Text(
        string="Tindakan Perbaikan",
    )

    tindakan_korektif=fields.Text(
        string="Tindakan Korektif",
    )

    target_korektif=fields.Date(
        string="Target Waktu Korektif",
    )        

    target_perbaikan=fields.Date(
        string="Target Waktu Perbaikan",
    )

    pic_perbaikan=fields.Char(
        string="PIC Perbaikan",
    )

    pic_korektif=fields.Char(
        string="PIC Korektif",
    )



    @api.model
    def create(self, values):
        #raise UserError(str(values))
        name = values.get("name", False)
        if not name or name == "/":
                values["name"] = self.env["ir.sequence"].\
                    next_by_code('nomor.temuan')
        return super(AuditTemuan, self).create(values)

    @api.multi
    def button_open(self):
        for _state in self:
            _state.write({"state": "open"})

    @api.multi
    def button_close(self):
        for _state in self:
            _state.write({"state": "close"})

    @api.multi
    def submit_bc23(self):
        wsdl = 'http://10.1.6.86/ws/index.php?wsdl'
        client = zeep.Client(wsdl=wsdl)
        data='CAP|BC23|1|1|1|1|298|BC23_20150922_01.txt \n \
        HDR|D|99999900001920150922000025|150300|1|01|02|COSMO HONG KONG LIMITED O/B UNISTRON COM|NO. 91 KAN-HO ROAD, TAICHUNG 407 TAIWAN|TW|1|KMTC PORT KELANG|1217S|HK|IDTPP|HKHKG||987654|20150922|||GIN-FLAT|20150922|040300|150300|||||||BERD|USD|9708|1000|0|0|0|2|0|1||1000|15254860|302.5||1|1|20150922|TANGERANG|MATEUS SIGIT UTOMO|2015-09-22 00:00:00||PUSAT| 5|010020733057000|COATS REJO INDONESIA|DESA PLERET, POHJENTREK, PASURUAN, JAWA TIMUR|1|090502126-B|EXIM MANAGER\n \
        DTL|99999900001920150922000025|1|1|02|6066319000|0|BAHAN BAKU|PCE01|MERK|TIPE|SPF|1|BX|1||HK|1000|1000|15254859.96|PCE|5|10.4|0|0|\n \
        DOK|99999900001920150922000025|217|IDM121220|2012-12-20\n \
        CON|99999900001920150922000025|MRTU 2111127|20|F\n \
        KMS|99999900001920150922000025|BX|1|-\n \
        FAS|99999900001920150922000025|1|1|100||0|2|100|2|100|1|50\n \
        TRF|99999900001920150922000025|6066319000|0|1||10||||10|10\n \
        BMT|99999900001920150922000025|1|10|||\n \
        DTLDOK|99999900001920150922000025|1|1|740|BGM0004707|20170104|B0001|6'
        raise UserError(client.service.process('adminjai', '123456','pabean',data))

    @api.multi
    def button_confirm(self):
        dok=''
        for invoice_id in self.invoice_ids:
            if not invoice_id.supplier_invoice_number:
                raise UserError('supplier invoice number tidak boleh kosong')
            dok=dok+'DOK|217|'+self.name+'|'+invoice_id.supplier_invoice_number+'\n'
            dtl=''
            for product_id in invoice_id.invoice_line:
                dtl=dtl+'DTL|'+self.name+'|'+product_id.name+'\n'
        data=dtl+dok
        raise UserError(str(data))

    @api.multi
    def get_respon(self):
        respon='pib999'
        #data=self.env['stock.picking'].search([['origin', '=', 'PO00001']]).name
        #raise UserError(str(data))
        #raise UserError(self.invoice_ids.origin)
        #elf.env.cr.execute("update stock.move set djbc_custom_document_id=1")
        #_error_msg=''        
        for picking_id in self.picking_ids:
            #raise UserError(str(picking_id.name))
            for each_line in picking_id.move_lines:
                #if not each_line.djbc_custom_document_id.name:
                #    _error_msg=_error_msg+'create'+' '
                    #raise UserError("a")
                #    _logger.info(_error_msg)
                    #each_line.djbc_custom_document_id.create({'name':"pib999",'date'})

                #else:
                    #raise UserError("b")
                #result=each_line.djbc_custom_document_id.search([('name', '=', 'peb001')])
                #_logger.info(result)
                self.env['l10n_id.djbc_custom_document'].write({'id':[(12,each_line.djbc_custom_document_id.id)], })

                #each_line.djbc_custom_document_id.write({'id':'13'})
                #each_line.djbc_custom_document_id.write({'name':'pib888'})

                #each_line.djbc_custom_document_id.write({'name':"pib212"})
                #_error_msg=_each_line.djbc_custom_document_id.name+' write'+' '
                
                _logger.info(each_line.djbc_custom_document_id.id)
                _logger.info(each_line.djbc_custom_document_id.name)      
                #raise UserError(str(prev_name+each_line.djbc_custom_document_id.name))
        #raise UserError(_error_msg)        


        #self.env.cr.execute("update stock.picking set name='tes' where origin='PO00001'") 
        #self.env.cr.commit()



    @api.onchange('invoice_ids')
    def _onchange_invoice_ids(self):
        domain = {}
        origin_list = []
        #if not self.invoice_ids:
        #    partner_obj = self.env['stock.picking'].search([('customer', '=', True)])
        for invoice_id in self.invoice_ids :
            origin_list.append(invoice_id.origin)
        #to assign parter_list value in domain
        domain = {'picking_ids': [('origin', 'in', origin_list)]} 
        #return {'domain': domain}
        return {'domain': domain}
        #raise UserError('OK')


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    temuan_id = fields.Many2one(
        string="# Temuan",
        comodel_name="audit.temuan",
        )