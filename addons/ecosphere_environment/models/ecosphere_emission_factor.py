from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EcosphereEmissionFactor(models.Model):
    _name = 'ecosphere.emission.factor'
    _description = 'Emission Factor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name, company_id)', 'An emission factor with the same name already exists for this organization.'),
    ]

    name = fields.Char(string='Name', required=True, tracking=True, help='Name of the emission factor.')
    source = fields.Char(string='Source', required=True, tracking=True, help='Source of the emission factor data.')
    category = fields.Selection(
        [
            ('energy', 'Energy'),
            ('transport', 'Transport'),
            ('waste', 'Waste'),
            ('process', 'Process'),
            ('refrigerant', 'Refrigerant'),
        ],
        string='Category',
        required=True,
        tracking=True,
        help='Category of the emission factor.',
    )
    unit = fields.Char(string='Unit', required=True, tracking=True, help='Unit used for the emission factor, such as kgCO2e/kWh.')
    emission_factor = fields.Float(string='Emission Factor', required=True, tracking=True, help='Numeric value of the emission factor.')
    status = fields.Selection(
        [('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive')],
        string='Status',
        default='draft',
        tracking=True,
        help='Lifecycle status of the emission factor.',
    )
    description = fields.Text(string='Description', tracking=True, help='Additional description about the emission factor.')
    company_id = fields.Many2one(
        'ecosphere.company',
        string='Organization',
        required=True,
        tracking=True,
        help='Organization that uses this emission factor.',
    )
    active = fields.Boolean(string='Active', default=True, help='Whether this record is active.')
    emission_factor_value = fields.Float(string='Factor Value', compute='_compute_emission_factor_value', store=True, help='Normalized emission factor value.')
    factor_band = fields.Char(string='Factor Band', compute='_compute_factor_band', store=True, help='Derived band of the factor.')

    @api.depends('emission_factor')
    def _compute_emission_factor_value(self):
        for record in self:
            record.emission_factor_value = abs(record.emission_factor or 0.0)

    @api.depends('emission_factor_value')
    def _compute_factor_band(self):
        for record in self:
            if record.emission_factor_value >= 2.0:
                record.factor_band = 'High'
            elif record.emission_factor_value >= 0.5:
                record.factor_band = 'Medium'
            else:
                record.factor_band = 'Low'

    @api.onchange('emission_factor')
    def _onchange_emission_factor(self):
        if self.emission_factor < 0:
            return {'warning': {'title': 'Invalid Value', 'message': 'Emission factor cannot be negative.'}}

    @api.constrains('emission_factor', 'unit')
    def _check_emission_factor(self):
        for record in self:
            if record.emission_factor < 0:
                raise ValidationError('Emission factor cannot be negative.')
            if not record.unit:
                raise ValidationError('Unit is required.')

    def action_activate(self):
        self.write({'status': 'active'})

    def action_inactivate(self):
        self.write({'status': 'inactive'})

    def create(self, vals):
        vals = vals.copy()
        if vals.get('name'):
            vals['name'] = vals['name'].strip()
        return super().create(vals)

    def write(self, vals):
        vals = vals.copy()
        if vals.get('name'):
            vals['name'] = vals['name'].strip()
        return super().write(vals)
