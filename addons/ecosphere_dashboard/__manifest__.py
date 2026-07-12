{
    'name': 'EcoSphere Dashboard',
    'version': '18.0.1.0.0',
    'summary': 'Analytics dashboard for ESG KPIs',
    'category': 'ESG',
    'author': 'EcoSphere Team',
    'depends': ['ecosphere_core', 'ecosphere_environment', 'ecosphere_social', 'ecosphere_governance'],
    'data': [
        'security/ecosphere_dashboard_security.xml',
        'security/ir.model.access.csv',
        'views/ecosphere_dashboard_views.xml',
        'views/ecosphere_dashboard_page.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ecosphere_dashboard/static/src/components/dashboard/esg_dashboard.css',
            'ecosphere_dashboard/static/src/components/dashboard/esg_dashboard.js',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
