from odoo import api,fields,models,_
from odoo.exceptions import ValidationError
class Activity(models.Model):
 _name='ecosphere.csr.activity';_description='CSR Activity';_inherit=['mail.thread']
 name=fields.Char(required=True);description=fields.Text();company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company);organizer_id=fields.Many2one('res.users',default=lambda s:s.env.user);start_date=fields.Date();end_date=fields.Date();target_participants=fields.Integer();state=fields.Selection([('draft','Draft'),('submitted','Submitted'),('approved','Approved'),('completed','Completed'),('cancelled','Cancelled')],default='draft');approved_by=fields.Many2one('res.users');approval_date=fields.Date()
 @api.constrains('start_date','end_date','target_participants')
 def _activity_validation(self):
  for r in self:
   if r.start_date and r.end_date and r.end_date<r.start_date: raise ValidationError(_('End date must follow start date.'))
   if r.target_participants<0: raise ValidationError(_('Target participants cannot be negative.'))
 def action_submit(self): self.write({'state':'submitted'})
 def action_approve(self): self.write({'state':'approved','approved_by':self.env.user.id,'approval_date':fields.Date.today()})
 def action_complete(self): self.write({'state':'completed'})
 def action_cancel(self): self.write({'state':'cancelled'})
class Participation(models.Model):
 _name='ecosphere.csr.participation';_description='CSR Participation'
 activity_id=fields.Many2one('ecosphere.csr.activity',required=True);employee_id=fields.Many2one('hr.employee',required=True);company_id=fields.Many2one(related='activity_id.company_id',store=True);participation_status=fields.Selection([('registered','Registered'),('attended','Attended'),('cancelled','Cancelled')],default='registered');volunteer_hours=fields.Float();approved=fields.Boolean();approved_by=fields.Many2one('res.users')
 _sql_constraints=[('csr_employee_unique','unique(activity_id,employee_id)','Employee already participates.')]
 @api.constrains('volunteer_hours')
 def _hours(self):
  if any(r.volunteer_hours<0 for r in self): raise ValidationError(_('Volunteer hours cannot be negative.'))
 def action_approve(self):
  for record in self:
   record.write({'approved':True,'approved_by':self.env.user.id,'participation_status':'attended'})
   if 'ecosphere.xp.service' in self.env: self.env['ecosphere.xp.service'].award(record.employee_id,10,record._name,record.id,'Approved CSR participation')
   self.env['ecosphere.notification.service'].notify(record.company_id,record.employee_id.user_id,'notify_csr_decisions',_('CSR participation approved'),record.activity_id.name,record)
class Diversity(models.Model):
 _name='ecosphere.diversity.metric';_description='Diversity Metric'
 name=fields.Char(required=True);company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company);department_id=fields.Many2one('hr.department');period_date=fields.Date(required=True);value=fields.Float(required=True);unit=fields.Char(default='%')
class Training(models.Model):
 _name='ecosphere.training.metric';_description='Training Metric'
 employee_id=fields.Many2one('hr.employee',required=True);department_id=fields.Many2one(related='employee_id.department_id',store=True);company_id=fields.Many2one(related='employee_id.company_id',store=True);name=fields.Char(required=True);state=fields.Selection([('planned','Planned'),('completed','Completed')],default='planned');training_hours=fields.Float();completion_date=fields.Date()
class DepartmentScore(models.Model):
 _name='ecosphere.department.score';_description='Department ESG Score';_order='calculation_date desc'
 department_id=fields.Many2one('hr.department',required=True);company_id=fields.Many2one(related='department_id.company_id',store=True);environmental_score=fields.Float();social_score=fields.Float();governance_score=fields.Float();overall_score=fields.Float();calculation_date=fields.Datetime(default=fields.Datetime.now)
 _sql_constraints=[('department_score_unique','unique(department_id,calculation_date)','Department score snapshot already exists.')]
 @api.model
 def cron_calculate_department_scores(self):
  for department in self.env['hr.department'].search([]):
   employees=self.env['hr.employee'].search([('department_id','=',department.id)])
   if not employees: continue
   hours=sum(self.env['ecosphere.training.metric'].search([('department_id','=',department.id),('state','=','completed')]).mapped('training_hours'))
   csr=sum(self.env['ecosphere.csr.participation'].search([('employee_id','in',employees.ids),('approved','=',True)]).mapped('volunteer_hours'))
   social=min(100,(hours+csr)/max(len(employees),1)*10)
   self.create({'department_id':department.id,'environmental_score':0,'social_score':social,'governance_score':0,'overall_score':social})
class SocialScoreService(models.AbstractModel):
 _name='ecosphere.social.score.service';_description='Social Metric Provider'
 def metric_value(self,metric,company):
  if metric.code=='volunteer_hours': return sum(self.env['ecosphere.csr.participation'].search([('company_id','=',company.id),('approved','=',True)]).mapped('volunteer_hours'))
  if metric.code=='training_hours': return sum(self.env['ecosphere.training.metric'].search([('company_id','=',company.id),('state','=','completed')]).mapped('training_hours'))
  return None
