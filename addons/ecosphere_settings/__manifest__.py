{
    'name': 'EcoSphere Settings',
    'version': '18.0.1.0.0',
    'summary': 'Configuration settings for EcoSphere',
    'category': 'ESG',
    'author': 'EcoSphere Team',
    'depends': ['ecosphere_core'],
    'data': [
        'security/ecosphere_settings_security.xml',
        'security/ir.model.access.csv',
        'views/ecosphere_settings_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
