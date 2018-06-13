# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


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
        # raise UserError(str(values))
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

    