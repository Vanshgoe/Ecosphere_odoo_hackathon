from odoo import fields, models


class EcosphereReportWizard(models.TransientModel):
    _name = 'ecosphere.report.wizard'
    _description = 'EcoSphere Report Wizard'

    company_id = fields.Many2one('ecosphere.company', string='Organization', required=True)
    report_type = fields.Selection([
        ('environment', 'Environmental Report'),
        ('social', 'Social Report'),
        ('governance', 'Governance Report'),
        ('summary', 'ESG Summary Report'),
    ], string='Report Type', required=True, default='summary')
    department = fields.Char(string='Department', help='Optional department filter for the report.')
    employee_id = fields.Many2one('ecosphere.worker', string='Employee', help='Optional employee filter for the report.')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def _get_report_action(self):
        mapping = {
            'environment': 'ecosphere_reports.action_report_environmental_pdf',
            'social': 'ecosphere_reports.action_report_social_pdf',
            'governance': 'ecosphere_reports.action_report_governance_pdf',
            'summary': 'ecosphere_reports.action_report_esg_pdf',
        }
        return self.env.ref(mapping.get(self.report_type, 'ecosphere_reports.action_report_esg_pdf'))

    def _get_report_data(self):
        emissions = self.env['ecosphere.emission'].search(self._get_emission_domain())
        resources = self.env['ecosphere.resource'].search(self._get_resource_domain())
        workers = self.env['ecosphere.worker'].search(self._get_social_domain())
        policies = self.env['ecosphere.policy'].search(self._get_policy_domain())
        compliances = self.env['ecosphere.compliance'].search(self._get_compliance_domain())
        metrics = self.env['ecosphere.metric'].search(self._get_metric_domain())

        return {
            'company_id': self.company_id.id,
            'department': self.department or '',
            'employee_id': self.employee_id.id if self.employee_id else False,
            'employee_name': self.employee_id.name if self.employee_id else '',
            'date_from': self.date_from,
            'date_to': self.date_to,
            'emission_records': emissions,
            'resource_records': resources,
            'social_records': workers,
            'policy_records': policies,
            'compliance_records': compliances,
            'metric_records': metrics,
            'emission_total': sum(record.quantity for record in emissions),
            'resource_total': sum(record.quantity for record in resources),
            'emission_count': len(emissions),
            'resource_count': len(resources),
            'social_count': len(workers),
            'policy_count': len(policies),
            'compliance_count': len(compliances),
            'metric_count': len(metrics),
            'metric_average_score': round(sum(record.score for record in metrics) / len(metrics), 2) if metrics else 0.0,
        }

    def _get_emission_domain(self):
        domain = [('company_id', '=', self.company_id.id)]
        if self.date_from:
            domain.append(('date', '>=', self.date_from))
        if self.date_to:
            domain.append(('date', '<=', self.date_to))
        if self.department:
            domain += ['|', ('name', 'ilike', self.department), ('description', 'ilike', self.department)]
        return domain

    def _get_resource_domain(self):
        domain = [('company_id', '=', self.company_id.id)]
        if self.department:
            domain += ['|', ('name', 'ilike', self.department), ('description', 'ilike', self.department)]
        return domain

    def _get_social_domain(self):
        domain = [('company_id', '=', self.company_id.id)]
        if self.employee_id:
            domain.append(('id', '=', self.employee_id.id))
        return domain

    def _get_policy_domain(self):
        domain = [('company_id', '=', self.company_id.id)]
        if self.department:
            domain += ['|', ('name', 'ilike', self.department), ('description', 'ilike', self.department)]
        return domain

    def _get_compliance_domain(self):
        domain = [('company_id', '=', self.company_id.id)]
        if self.department:
            domain += ['|', ('name', 'ilike', self.department), ('description', 'ilike', self.department)]
        return domain

    def _get_metric_domain(self):
        domain = [('company_id', '=', self.company_id.id)]
        if self.department:
            domain += ['|', ('name', 'ilike', self.department), ('description', 'ilike', self.department)]
        return domain

    def action_generate(self):
        self.ensure_one()
        return self._get_report_action().report_action(self, data=self._get_report_data())
