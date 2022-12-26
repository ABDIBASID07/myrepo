# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hospital Management',
    'author': 'Abdibasid Ahmed',
    'version': '1.2.3',
    'category': 'Hospital sys',
    'sequence': '-100',
    'summary': 'Hospital Management System',
    'description': """Hospital h management system""",
    'depends': ['mail', 'product', 'product'],
    'data': [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/patient_tag_data.xml",
        "data/patient.tag.csv",
        "data/sequence_data.xml",
        "wizard/cancel_appointment_view.xml",
        "views/menu.xml",
        "views/patient_view.xml",
        "views/female_patient_view.xml",
        "views/appointment_view.xml",
        "views/patient_tag_view.xml",
        "views/playground_view.xml",

        # wizard should come before the views

        # data should come right after the secuirity , before the wizard

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'AGPL-3',
}
