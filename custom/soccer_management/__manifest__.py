# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Soccer Management',
    'version' : '1.0.0',
    'summary': 'Management soccer with friends',
    'description': """Management soccer with friends""",
    'category': 'Management',
    'website': 'https://www.odoo.com/page/billing',
    'depends' : ['base'],
    'data': [
        'views/soccer_management_view.xml',
        'views/payment_mode_view.xml',
        'views/res_partner_view.xml',
        'views/sequence.xml',

    ],
    'demo': [],
    'qweb': [],
    'application': True,
    'auto_install': False,
}
