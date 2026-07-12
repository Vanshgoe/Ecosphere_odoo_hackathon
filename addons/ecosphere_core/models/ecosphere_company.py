from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EcosphereCompany(models.Model):
    _name = 'ecosphere.company'
    _description = 'EcoSphere Company'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'Company code already exists.'),
    ]

    name = fields.Char(string='Company Name', required=True, tracking=True, help='Official name of the organization.')
    code = fields.Char(string='Code', required=True, tracking=True, help='Short unique identifier for the organization.')
    active = fields.Boolean(default=True, help='Allow archiving of company records.')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        tracking=True,
        help='The legal company linked to this ESG entity.',
    )
    sector = fields.Selection(
        [('manufacturing', 'Manufacturing'), ('finance', 'Finance'), ('retail', 'Retail'), ('technology', 'Technology'), ('energy', 'Energy')],
        string='Sector',
        default='manufacturing',
        tracking=True,
        help='Primary business sector of the company.',
    )
    description = fields.Text(string='Description', help='Brief overview of the organization.')
    website = fields.Char(string='Website', help='Company website URL.')
    total_employees = fields.Integer(string='Employees', default=0, tracking=True, help='Total number of employees.')
    sustainability_score = fields.Float(string='Sustainability Score', default=0.0, tracking=True, help='Current ESG score for the organization.')
    target_score = fields.Float(string='Target Score', default=70.0, tracking=True, help='Target sustainability score to be reached.')
    state = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('archived', 'Archived')], string='Status', default='draft', tracking=True)
    score_status = fields.Char(string='Score Status', compute='_compute_score_status', store=True, help='Derived status based on current score.')
    color = fields.Integer(string='Color Index', default=0)

    @api.depends('sustainability_score', 'target_score')
    def _compute_score_status(self):
        for record in self:
            if record.sustainability_score >= record.target_score:
                record.score_status = 'on_track'
            elif record.sustainability_score >= (record.target_score * 0.8):
                record.score_status = 'monitor'
            else:
                record.score_status = 'at_risk'

    @api.onchange('total_employees')
    def _onchange_total_employees(self):
        if self.total_employees < 0:
            return {'warning': {'title': 'Invalid Value', 'message': 'Employee count cannot be negative.'}}

    @api.constrains('sustainability_score', 'target_score')
    def _check_scores(self):
        for record in self:
            if not 0 <= record.sustainability_score <= 100:
                raise ValidationError('Sustainability score must be between 0 and 100.')
            if not 0 <= record.target_score <= 100:
                raise ValidationError('Target score must be between 0 and 100.')

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

    def action_activate(self):
        self.write({'state': 'active'})

    def action_archive(self):
        self.write({'state': 'archived'})

    def _cron_recompute_scores(self):
        for company in self.search([]):
            company.sustainability_score = min(100.0, company.sustainability_score + 0.1)
