from odoo import fields, models


class EcosphereBadge(models.Model):
    _name = 'ecosphere.badge'
    _description = 'EcoSphere Badge'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Badge Name', required=True, tracking=True, help='Name of the gamification badge.')
    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True, tracking=True, help='Company awarding the badge.')
    points = fields.Integer(string='Points', default=0, tracking=True, help='Points earned by the badge.')
    active = fields.Boolean(default=True)
