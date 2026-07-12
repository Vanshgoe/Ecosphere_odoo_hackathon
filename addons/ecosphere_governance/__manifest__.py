{
    'name': 'EcoSphere Governance',
    'version': '18.0.1.0.0',
    'summary': 'Governance policies and compliance management',
    'category': 'ESG',
    'author': 'EcoSphere Team',
    'depends': ['ecosphere_core'],
    'data': [
        'security/ecosphere_governance_security.xml',
        'security/ir.model.access.csv',
        'views/ecosphere_governance_views.xml',
        'demo/demo_data.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
