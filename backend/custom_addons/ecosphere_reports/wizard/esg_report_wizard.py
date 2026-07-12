import base64
import csv
from io import StringIO
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
class ReportWizard(models.TransientModel):
 _name='ecosphere.report.wizard';_description='ESG Report Wizard'
 company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company);date_from=fields.Date(required=True);date_to=fields.Date(required=True);category=fields.Selection([('E','Environmental'),('S','Social'),('G','Governance')]);sections=fields.Char(default='scores,emissions,goals,social,governance')
 department_id=fields.Many2one('hr.department');employee_id=fields.Many2one('hr.employee');challenge_id=fields.Many2one('ecosphere.challenge');module=fields.Selection([('environment','Environmental'),('social','Social'),('governance','Governance'),('summary','ESG Summary')],default='summary')
 @api.constrains('date_from','date_to')
 def _date_range(self):
  if any(record.date_from and record.date_to and record.date_to<record.date_from for record in self): raise ValidationError(_('End date must be on or after start date.'))
 def action_pdf(self): return self.env.ref('ecosphere_reports.action_esg_report').report_action(self)
 def action_xlsx(self): return self.env.ref('ecosphere_reports.action_esg_xlsx').report_action(self)
 def action_csv(self):
  self.ensure_one(); output=StringIO(); writer=csv.writer(output); writer.writerow(['Metric','Value'])
  score=self.env['ecosphere.esg.score'].search([('company_id','=',self.company_id.id)],limit=1)
  writer.writerows([['Environmental score',score.environmental_score if score else 0],['Social score',score.social_score if score else 0],['Governance score',score.governance_score if score else 0],['Overall score',score.overall_score if score else 0]])
  attachment=self.env['ir.attachment'].create({'name':'ecosphere_report.csv','type':'binary','datas':base64.b64encode(output.getvalue().encode()),'mimetype':'text/csv'})
  return {'type':'ir.actions.act_url','url':'/web/content/%s?download=true' % attachment.id,'target':'self'}
