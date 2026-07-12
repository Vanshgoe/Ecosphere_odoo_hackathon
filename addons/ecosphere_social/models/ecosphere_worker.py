from odoo import fields, models


class EcosphereWorker(models.Model):
    _name = 'ecosphere.worker'
    _description = 'Social Worker Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Employee Name', required=True, tracking=True, help='Name of the employee involved in social initiatives.')
    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True, tracking=True, help='Company linked to the employee record.')
    role = fields.Char(string='Role', help='Position or function of the employee.')
    engagement_score = fields.Float(string='Engagement Score', default=0.0, tracking=True, help='Employee engagement score.')
    active = fields.Boolean(default=True)
