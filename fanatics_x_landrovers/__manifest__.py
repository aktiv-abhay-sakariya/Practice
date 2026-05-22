# -*- coding: utf-8 -*-
{
    'name': "Fanatics - LandRovers Customization",
    'summary': """""",
    'description': """  """,
    'author': "Radical Fanatics",
    'website': "www.fanatics.nl",
    'category': 'Customizations/Studio',
    'version': '18.0.47.5.13',
    # any module necessary for this one to work correctly
    'depends': [
        'project',
        'mrp',
        'sale',
        'crm',
        'stock',
        'purchase',
        'web_studio',
        'hr_recruitment',
        'quality_control',
        'knowledge',
        'mrp_workorder',
        'mail',
    ],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'views/model_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
        'views/hr_recruitment_views.xml',
        'views/quality_alert_views.xml',
        'views/project_views.xml',
        'views/mrp_views.xml',
        'views/mrp_production_views.xml',
        'views/crm_lead_views.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/vehicle_detail_views.xml',
    ],
    "icon": "fanatics_x_landrovers/static/description/icon.png",
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
    "assets": {
        'web.assets_backend': [
            'fanatics_x_landrovers/static/src/js/chatter_confirmation.js',
            'fanatics_x_landrovers/static/src/js/workorder_extension.js',
            'fanatics_x_landrovers/static/src/xml/mrp_worksheet_dialog_patch.xml',
            'fanatics_x_landrovers/static/src/xml/chatter.xml',
        ],
    }
}
