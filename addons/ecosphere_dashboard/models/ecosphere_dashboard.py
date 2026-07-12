from odoo import fields, models


class EcosphereDashboard(models.Model):
    _name = 'ecosphere.dashboard'
    _description = 'EcoSphere Dashboard Summary'
    _order = 'name'

    name = fields.Char(string='Dashboard Name', default='ESG Overview', required=True)
    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True)
    total_metrics = fields.Integer(string='Total Metrics', default=0)
    total_emissions = fields.Integer(string='Total Emissions', default=0)
    average_score = fields.Float(string='Average Score', default=0.0)
