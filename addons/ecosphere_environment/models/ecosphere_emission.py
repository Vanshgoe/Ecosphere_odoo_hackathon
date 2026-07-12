from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EcosphereEmission(models.Model):
    _name = 'ecosphere.emission'
    _description = 'Environmental Emission Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char(string='Emission Name', required=True, tracking=True, help='Short label for the emission event.')
    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True, tracking=True, help='Company linked to this emission record.')
    date = fields.Date(string='Date', required=True, default=fields.Date.today, tracking=True, help='Emission date.')
    emission_type = fields.Selection([('scope1', 'Scope 1'), ('scope2', 'Scope 2'), ('scope3', 'Scope 3')], string='Type', required=True, tracking=True)
    quantity = fields.Float(string='Quantity', default=0.0, tracking=True, help='Amount emitted.')
    unit = fields.Char(string='Unit', default='tCO2e', help='Unit of measurement.')
    description = fields.Text(string='Description', help='Details about the emission source.')
    state = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved')], default='draft', tracking=True)
    active = fields.Boolean(default=True)

    @api.onchange('quantity')
    def _onchange_quantity(self):
        if self.quantity < 0:
            return {'warning': {'title': 'Invalid value', 'message': 'Quantity cannot be negative.'}}

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity < 0:
                raise ValidationError('Quantity cannot be negative.')
