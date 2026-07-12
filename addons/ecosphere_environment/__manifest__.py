{
    'name': 'EcoSphere Environment',
    'version': '18.0.1.0.0',
    'summary': 'Environmental impact and carbon management features',
    'category': 'ESG',
    'author': 'EcoSphere Team',
    'depends': ['ecosphere_core'],
    'data': [
        'security/ecosphere_environment_security.xml',
        'security/ir.model.access.csv',
        'views/ecosphere_environment_views.xml',
        'demo/demo_data.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
