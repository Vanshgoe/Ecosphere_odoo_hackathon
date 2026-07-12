from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EcosphereProgram(models.Model):
    _name = 'ecosphere.program'
    _description = 'EcoSphere ESG Program'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'Program code already exists.'),
    ]

    name = fields.Char(string='Program Name', required=True, tracking=True, help='Name of the ESG program.')
    code = fields.Char(string='Code', required=True, tracking=True, help='Unique identifier for the program.')
    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True, tracking=True, help='Organization running the program.')
    category = fields.Selection([('environment', 'Environment'), ('social', 'Social'), ('governance', 'Governance')], string='Category', required=True, tracking=True)
    start_date = fields.Date(string='Start Date', tracking=True, help='Program start date.')
    end_date = fields.Date(string='End Date', tracking=True, help='Program end date.')
    budget = fields.Float(string='Budget', default=0.0, tracking=True, help='Allocated budget for the program.')
    status = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('completed', 'Completed')], string='Status', default='draft', tracking=True)
    active = fields.Boolean(default=True, help='Allow archiving of program records.')
    description = fields.Text(string='Description', help='Context and goals for the program.')
    completion_rate = fields.Float(string='Completion Rate', compute='_compute_completion_rate', store=True, help='Derived program completion rate.')

    @api.depends('start_date', 'end_date')
    def _compute_completion_rate(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date <= record.end_date:
                record.completion_rate = 50.0
            else:
                record.completion_rate = 0.0

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            return {'warning': {'title': 'Invalid Date', 'message': 'End date cannot be before start date.'}}

    @api.constrains('budget')
    def _check_budget(self):
        for record in self:
            if record.budget < 0:
                raise ValidationError('Budget cannot be negative.')

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
