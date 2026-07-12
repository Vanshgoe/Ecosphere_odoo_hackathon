{
    'name': 'EcoSphere Reports',
    'version': '18.0.1.0.0',
    'summary': 'QWeb and XLSX reporting for ESG data',
    'category': 'ESG',
    'author': 'EcoSphere Team',
    'depends': ['ecosphere_core', 'ecosphere_environment', 'ecosphere_social', 'ecosphere_governance', 'report_xlsx'],
    'data': [
        'security/ecosphere_reports_security.xml',
        'security/ir.model.access.csv',
        'views/ecosphere_reports_views.xml',
        'report/report_template.xml',
        'report/report_action.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
