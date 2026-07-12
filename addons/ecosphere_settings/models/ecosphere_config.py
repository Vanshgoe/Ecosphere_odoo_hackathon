from odoo import fields, models


class EcosphereConfig(models.TransientModel):
    _name = 'ecosphere.config'
    _description = 'EcoSphere Configuration'

    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True)
    default_reporting_period = fields.Selection([('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')], string='Reporting Period', default='monthly')
    auto_send_reports = fields.Boolean(string='Auto Send Reports', default=True)
