from odoo import models

class ESGXlsx(models.AbstractModel):
    _name = 'report.ecosphere_reports.esg_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'EcoSphere ESG XLSX Report'

    def generate_xlsx_report(self, workbook, data, wizards):
        title = workbook.add_format({'bold': True, 'font_size': 16})
        header = workbook.add_format({'bold': True, 'bg_color': '#D9EAD3'})
        for wizard in wizards:
            sheet = workbook.add_worksheet('ESG Report')
            sheet.write(0, 0, 'EcoSphere ESG Report', title)
            sheet.write(1, 0, 'Company', header)
            sheet.write(1, 1, wizard.company_id.name)
            sheet.write(2, 0, 'Period', header)
            sheet.write(2, 1, '%s to %s' % (wizard.date_from, wizard.date_to))
            score = self.env['ecosphere.esg.score'].search([('company_id', '=', wizard.company_id.id)], limit=1)
            sheet.write_row(4, 0, ['Environmental', 'Social', 'Governance', 'Overall'], header)
            sheet.write_row(5, 0, [score.environmental_score if score else 0, score.social_score if score else 0, score.governance_score if score else 0, score.overall_score if score else 0])
            sheet.set_column(0, 3, 20)
