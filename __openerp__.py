# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Audit ISO27001-2013",
    "version": "8.0.1.0.0",
    "website": "https://edi-indonesia.co.id",
    "author": "Oktovan Rezman",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "hr",
        "stock",
        "account_accountant",
        "purchase",
    ],
    "data": [
        "reports/ncr.xml",
        "security/res_groups_data.xml",
        "views/klausul_views.xml",
        "views/temuan_views.xml",
        "views/invoice_tree_inherit.xml",
        "views/menu.xml"
    ],
}
