# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AuditKlausul(models.Model):
    _name = "audit.klausul"
    _description = "Klausul"

    name = fields.Char(
        string="Klausul",
        required=True,
        copy=False,
    )

    kode = fields.Char(
        string="Kode",
        required=True,
    )

    keterangan = fields.Text(
        string="Keterangan",
        required=True,
    )



