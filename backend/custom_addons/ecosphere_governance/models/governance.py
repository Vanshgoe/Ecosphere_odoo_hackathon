from odoo import api,fields,models, _
from odoo.exceptions import ValidationError
class Policy(models.Model):
 _name='ecosphere.esg.policy';_description='ESG Policy';_inherit=['mail.thread']
 name=fields.Char(required=True);code=fields.Char(required=True);description=fields.Text();company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company);owner_id=fields.Many2one('res.users');version=fields.Char(default='1.0');effective_date=fields.Date();review_date=fields.Date();attachment_ids=fields.Many2many('ir.attachment');state=fields.Selection([('draft','Draft'),('published','Published'),('archived','Archived')],default='draft')
 _sql_constraints=[('policy_code_company','unique(code,company_id)','Policy code must be unique per company.')]
 @api.constrains('effective_date','review_date')
 def _review_date(self):
  if any(r.effective_date and r.review_date and r.review_date<r.effective_date for r in self): raise ValidationError(_('Review date must follow effective date.'))
 def action_publish(self):
  self.write({'state':'published','effective_date':self.effective_date or fields.Date.today()})
  for policy in self:
   policy.message_post(body=_('Policy published. Please acknowledge it.'))
 def action_archive(self): self.write({'state':'archived'})
class Ack(models.Model):
 _name='ecosphere.policy.acknowledgement';_description='Policy Acknowledgement'
 policy_id=fields.Many2one('ecosphere.esg.policy',required=True);employee_id=fields.Many2one('hr.employee',required=True);company_id=fields.Many2one(related='policy_id.company_id',store=True);acknowledged=fields.Boolean();acknowledgement_date=fields.Date()
 _sql_constraints=[('policy_ack_unique','unique(policy_id,employee_id)','Policy acknowledgement already exists.')]
 def action_acknowledge(self): self.write({'acknowledged':True,'acknowledgement_date':fields.Date.today()})
class Audit(models.Model):
 _name='ecosphere.esg.audit';_description='ESG Audit'
 name=fields.Char(required=True);company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company);audit_type=fields.Char();auditor=fields.Char();start_date=fields.Date();end_date=fields.Date();findings=fields.Text();score=fields.Float();state=fields.Selection([('draft','Draft'),('in_progress','In Progress'),('completed','Completed')],default='draft')
class Issue(models.Model):
 _name='ecosphere.compliance.issue';_description='Compliance Issue'
 name=fields.Char(required=True);company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company);severity=fields.Selection([('low','Low'),('medium','Medium'),('high','High'),('critical','Critical')],default='medium');responsible_user_id=fields.Many2one('res.users');due_date=fields.Date();resolution_date=fields.Date();state=fields.Selection([('open','Open'),('in_progress','In Progress'),('resolved','Resolved'),('overdue','Overdue'),('cancelled','Cancelled')],default='open');description=fields.Text()
 @api.model
 def cron_mark_overdue(self): self.search([('state','in',['open','in_progress']),('due_date','<',fields.Date.today())]).write({'state':'overdue'})
 def action_start(self): self.write({'state':'in_progress'})
 def action_resolve(self): self.write({'state':'resolved','resolution_date':fields.Date.today()})
 @api.model_create_multi
 def create(self,vals_list):
  records=super().create(vals_list)
  for record in records:
   self.env['ecosphere.notification.service'].notify(record.company_id,record.responsible_user_id,'notify_compliance_issues',_('New compliance issue'),record.name,record)
  return records
class Risk(models.Model):
 _name='ecosphere.risk.register';_description='Risk Register'
 name=fields.Char(required=True);company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company);category=fields.Char();probability=fields.Float();impact=fields.Float();risk_score=fields.Float(compute='_risk',store=True);mitigation_plan=fields.Text();owner_id=fields.Many2one('res.users');state=fields.Selection([('open','Open'),('mitigated','Mitigated'),('closed','Closed')],default='open')
 @api.depends('probability','impact')
 def _risk(self):
  for r in self:r.risk_score=r.probability*r.impact
 @api.constrains('probability','impact')
 def _risk_range(self):
  if any(r.probability<0 or r.impact<0 for r in self): raise ValidationError(_('Probability and impact cannot be negative.'))
class GovernanceScoreService(models.AbstractModel):
 _name='ecosphere.governance.score.service';_description='Governance Metric Provider'
 def metric_value(self,metric,company):
  if metric.code=='policy_acknowledgement_rate':
   acks=self.env['ecosphere.policy.acknowledgement'].search([('company_id','=',company.id)])
   return (sum(acks.mapped('acknowledged'))/len(acks)*100) if acks else None
  if metric.code=='open_compliance_issues': return self.env['ecosphere.compliance.issue'].search_count([('company_id','=',company.id),('state','in',['open','in_progress','overdue'])])
  return None
