from odoo import fields, models


class EcosphereResource(models.Model):
    _name = 'ecosphere.resource'
    _description = 'Environmental Resource Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Resource Name', required=True, tracking=True, help='Name of the resource.')
    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True, tracking=True, help='Company linked to this resource record.')
    resource_type = fields.Selection([('water', 'Water'), ('energy', 'Energy'), ('waste', 'Waste')], string='Type', required=True, tracking=True)
    quantity = fields.Float(string='Quantity', default=0.0, tracking=True, help='Available or used quantity.')
    unit = fields.Char(string='Unit', default='m3', help='Unit of the resource quantity.')
    description = fields.Text(string='Description', help='Additional details about the resource.')
    active = fields.Boolean(default=True)
