from odoo import fields, models


class EcosphereCompliance(models.Model):
    _name = 'ecosphere.compliance'
    _description = 'Governance Compliance Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Compliance Name', required=True, tracking=True, help='Name of the compliance requirement.')
    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True, tracking=True, help='Company linked to the compliance record.')
    due_date = fields.Date(string='Due Date', tracking=True, help='Date by which compliance is due.')
    status = fields.Selection([('pending', 'Pending'), ('completed', 'Completed'), ('overdue', 'Overdue')], default='pending', tracking=True)
    active = fields.Boolean(default=True)
