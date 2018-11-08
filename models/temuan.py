# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, tools
from openerp.exceptions import Warning as UserError


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

    invoice_ids=fields.Many2many(
        string="Invoice",
        comodel_name="account.invoice",
    #    inverse_name="temuan_id",
    #   relation="rel_temuan_2_invoice",
    #    column1="temuan_id",
    #    column2="invoice_id",
    #    context="{'koplak':invoice_ids}",
    )


    picking_ids = fields.Many2many(
        string="Good Receipt",
        comodel_name="stock.picking",
    #    domain="[('origin', 'in', koplak)]",
    #    domain="[('origin', 'in', ['PO00001','PO00002'])]",
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
        for picking_id in self.picking_ids:
            #raise UserError(str(picking_id.name))
            for each_line in picking_id.move_lines:
                each_line.djbc_custom_document_id.write({'name':"pib999"})
                raise UserError(str(each_line.djbc_custom_document_id.name))
                

        #self.env.cr.execute("update stock.picking set name='tes' where origin='PO00001'") 
        #self.env.cr.commit()



    #@api.onchange('invoice_ids')
    #def _onchange_invoice_ids(self):
    #   domain = {}
    #   partner_list = []
    #   if not self.invoice_ids:
    #       partner_obj = self.env['stock.picking'].search([('customer', '=', True)])
    #       for partner_ids in partner_obj:
    #           partner_list.append(partner_ids.id)
          # to assign parter_list value in domain
    #       domain = {'partner_id': [('id', '=', partner_list)]} 
    #   return {'domain': domain}

