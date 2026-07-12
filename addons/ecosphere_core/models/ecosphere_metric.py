from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EcosphereMetric(models.Model):
    _name = 'ecosphere.metric'
    _description = 'EcoSphere KPI Metric'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'Metric code already exists.'),
    ]

    name = fields.Char(string='Metric Name', required=True, tracking=True, help='Name of the ESG KPI metric.')
    code = fields.Char(string='Code', required=True, tracking=True, help='Unique shortcode for the metric.')
    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True, tracking=True, help='Organization that owns the metric.')
    category = fields.Selection([('environment', 'Environment'), ('social', 'Social'), ('governance', 'Governance')], string='Category', required=True, tracking=True)
    unit = fields.Char(string='Unit', help='Unit of the metric, such as tCO2e or %.')
    target_value = fields.Float(string='Target Value', default=0.0, tracking=True, help='Desired value for the metric.')
    current_value = fields.Float(string='Current Value', default=0.0, tracking=True, help='Current achievement for the metric.')
    score = fields.Float(string='Score', compute='_compute_score', store=True, help='Derived performance score.')
    state = fields.Selection([('draft', 'Draft'), ('in_progress', 'In Progress'), ('done', 'Done')], string='Status', default='draft', tracking=True)
    active = fields.Boolean(default=True, help='Allow archiving of metric records.')
    description = fields.Text(string='Description', help='Additional context for the metric.')

    @api.depends('target_value', 'current_value')
    def _compute_score(self):
        for record in self:
            if record.target_value:
                record.score = round((record.current_value / record.target_value) * 100, 2)
            else:
                record.score = 0.0

    @api.onchange('current_value', 'target_value')
    def _onchange_values(self):
        if self.target_value < 0:
            return {'warning': {'title': 'Invalid Value', 'message': 'Target value cannot be negative.'}}

    @api.constrains('current_value', 'target_value')
    def _check_metric_values(self):
        for record in self:
            if record.current_value < 0 or record.target_value < 0:
                raise ValidationError('Metric values cannot be negative.')

    def create(self, vals):
        vals = vals.copy()
        if vals.get('code'):
            vals['code'] = vals['code'].upper()
        return super().create(vals)

    def write(self, vals):
        vals = vals.copy()
        if vals.get('code'):
            vals['code'] = vals['code'].upper()
        return super().write(vals)
