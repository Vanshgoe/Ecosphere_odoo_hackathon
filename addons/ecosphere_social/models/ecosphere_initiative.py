from odoo import fields, models


class EcosphereInitiative(models.Model):
    _name = 'ecosphere.initiative'
    _description = 'Social Initiative'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Initiative Name', required=True, tracking=True, help='Name of the social initiative.')
    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True, tracking=True, help='Company linked to the initiative.')
    start_date = fields.Date(string='Start Date', tracking=True, help='Initiative start date.')
    end_date = fields.Date(string='End Date', tracking=True, help='Initiative end date.')
    impact_score = fields.Float(string='Impact Score', default=0.0, tracking=True, help='Score representing initiative impact.')
    active = fields.Boolean(default=True)
