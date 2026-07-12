from odoo import fields, models


class EcospherePolicy(models.Model):
    _name = 'ecosphere.policy'
    _description = 'Governance Policy'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Policy Name', required=True, tracking=True, help='Name of the governace policy.')
    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True, tracking=True, help='Company linked to the policy.')
    policy_type = fields.Selection([('ethics', 'Ethics'), ('compliance', 'Compliance'), ('risk', 'Risk')], string='Type', required=True, tracking=True)
    effective_date = fields.Date(string='Effective Date', tracking=True, help='Date the policy becomes effective.')
    status = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('expired', 'Expired')], default='draft', tracking=True)
    active = fields.Boolean(default=True)
