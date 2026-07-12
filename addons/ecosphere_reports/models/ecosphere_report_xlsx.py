from odoo import models


class EcoSphereReportXlsx(models.AbstractModel):
    _name = 'report.ecosphere_reports.report_esg_summary_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, report_wizard):
        sheet = workbook.add_worksheet('EcoSphere ESG')
        sheet.write(0, 0, 'Organization')
        sheet.write(0, 1, report_wizard.company_id.name)
        sheet.write(1, 0, 'Report Type')
        sheet.write(1, 1, report_wizard.report_type)
