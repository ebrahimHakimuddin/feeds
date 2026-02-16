# -*- coding: utf-8 -*-
{
    'name': 'Subcontractor Management',
    'version': '1.0',
    'category': 'Operations',
    'summary': 'Manage subcontractor agreements, items, and payments',
    'description': """
        Subcontractor Management Module
        ================================
        This module allows you to:
        * Create subcontractor agreements with partners
        * Assign subcontracted items with variants
        * Track payments on a weekly basis
        * View payment history and balance for each agreement
        * Automatically update inventory when balance reaches zero
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'product', 'stock'],
    'data': [
        'data/sequence_data.xml',
        'security/ir.model.access.csv',
        'views/subcontractor_agreement_views.xml',
        'views/subcontractor_item_views.xml',
        'views/subcontractor_payment_views.xml',
        'views/raw_material_consumption_views.xml',
        'wizard/weekly_payment_wizard_views.xml',
        'views/menu_items.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
