from odoo import fields, models


class EcosphereChallenge(models.Model):
    _name = 'ecosphere.challenge'
    _description = 'EcoSphere Challenge'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Challenge Name', required=True, tracking=True, help='Name of the ESG challenge.')
    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True, tracking=True, help='Company hosting the challenge.')
    points = fields.Integer(string='Points', default=0, tracking=True, help='Points awarded when completing the challenge.')
    deadline = fields.Date(string='Deadline', tracking=True, help='Challenge deadline date.')
    active = fields.Boolean(default=True)
