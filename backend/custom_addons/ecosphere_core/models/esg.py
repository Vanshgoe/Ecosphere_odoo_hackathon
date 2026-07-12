from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Category(models.Model):
 _name='ecosphere.esg.category'; _description='ESG Category'; _order='sequence,name'
 name=fields.Char(required=True); code=fields.Selection([('E','Environmental'),('S','Social'),('G','Governance')],required=True); sequence=fields.Integer(default=10); active=fields.Boolean(default=True); company_id=fields.Many2one('res.company')
 _sql_constraints=[('category_code_company','unique(code,company_id)','Category code must be unique per company.')]
class ESGConfiguration(models.Model):
 _name='ecosphere.esg.configuration'; _description='EcoSphere Configuration'
 company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company)
 enable_purchase_carbon=fields.Boolean(default=True); enable_manufacturing_carbon=fields.Boolean(default=True); enable_expense_carbon=fields.Boolean(default=True); enable_fleet_carbon=fields.Boolean(default=True)
 evidence_required=fields.Boolean(string='Require evidence for CSR participation')
 notify_compliance_issues=fields.Boolean(default=True); notify_csr_decisions=fields.Boolean(default=True); notify_challenge_decisions=fields.Boolean(default=True); notify_policy_reminders=fields.Boolean(default=True); notify_badge_unlocks=fields.Boolean(default=True)
 _sql_constraints=[('configuration_company','unique(company_id)','Only one EcoSphere configuration is allowed per company.')]
 @api.model
 def for_company(self,company): return self.search([('company_id','=',company.id)],limit=1) or self.create({'company_id':company.id})
class Metric(models.Model):
 _name='ecosphere.esg.metric'; _description='ESG Metric'
 name=fields.Char(required=True); code=fields.Char(required=True); category_id=fields.Many2one('ecosphere.esg.category',required=True); description=fields.Text(); unit=fields.Char(default='%'); direction=fields.Selection([('higher_is_better','Higher is better'),('lower_is_better','Lower is better')],default='higher_is_better',required=True); weight=fields.Float(default=1); normalization_method=fields.Selection([('min_max','Min/max'),('target_based','Target'),('boolean','Boolean'),('percentage','Percentage')],default='percentage',required=True); minimum_value=fields.Float(default=0); maximum_value=fields.Float(default=100); target_value=fields.Float(); active=fields.Boolean(default=True); company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company)
 _sql_constraints=[('metric_code_company','unique(code,company_id)','Metric code must be unique per company.')]
 @api.constrains('weight','minimum_value','maximum_value')
 def _range(self):
  for r in self:
   if r.weight<0 or r.maximum_value<=r.minimum_value: raise ValidationError(_('Invalid metric range or weight.'))
class Config(models.Model):
 _name='ecosphere.scoring.config'; _description='ESG Scoring Configuration'
 name=fields.Char(required=True); environmental_weight=fields.Float(default=34); social_weight=fields.Float(default=33); governance_weight=fields.Float(default=33); scoring_period=fields.Selection([('monthly','Monthly'),('quarterly','Quarterly'),('yearly','Yearly')],default='monthly'); active=fields.Boolean(default=True); company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company)
 @api.constrains('environmental_weight','social_weight','governance_weight')
 def _weights(self):
  for r in self:
   if abs(r.environmental_weight+r.social_weight+r.governance_weight-100)>0.001: raise ValidationError(_('Weights must total 100%.'))
   if r.active and self.search_count([('company_id','=',r.company_id.id),('active','=',True),('id','!=',r.id)]): raise ValidationError(_('Only one active scoring configuration is allowed per company.'))
class Score(models.Model):
 _name='ecosphere.esg.score'; _description='Current ESG Score'
 company_id=fields.Many2one('res.company',required=True); environmental_score=fields.Float(); social_score=fields.Float(); governance_score=fields.Float(); overall_score=fields.Float(); calculation_date=fields.Datetime(default=fields.Datetime.now); scoring_config_id=fields.Many2one('ecosphere.scoring.config',required=True)
 _sql_constraints=[('score_company','unique(company_id)','One current score per company.')]
 @api.constrains('environmental_score','social_score','governance_score','overall_score')
 def _scores(self):
  for r in self:
   if any(x<0 or x>100 for x in [r.environmental_score,r.social_score,r.governance_score,r.overall_score]): raise ValidationError(_('Scores must be 0–100.'))
 @api.model
 def cron_recalculate(self):
  from ..services.scoring_service import ScoringService
  for company in self.env['res.company'].search([]): ScoringService(self.env,company).calculate()
 @api.model
 def cron_snapshot(self):
  Snapshot=self.env['ecosphere.esg.score.snapshot']
  for score in self.search([]):
   Snapshot.create({'company_id':score.company_id.id,'environmental_score':score.environmental_score,'social_score':score.social_score,'governance_score':score.governance_score,'overall_score':score.overall_score,'scoring_config_id':score.scoring_config_id.id})
class Snapshot(models.Model):
 _name='ecosphere.esg.score.snapshot'; _description='ESG Score Snapshot'; _order='snapshot_date desc'
 company_id=fields.Many2one('res.company',required=True,index=True); environmental_score=fields.Float(); social_score=fields.Float(); governance_score=fields.Float(); overall_score=fields.Float(); snapshot_date=fields.Datetime(default=fields.Datetime.now,index=True); scoring_config_id=fields.Many2one('ecosphere.scoring.config')
class Goal(models.Model):
 _name='ecosphere.esg.goal'; _description='ESG Goal'; _inherit=['mail.thread','mail.activity.mixin']
 name=fields.Char(required=True); company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company); category_id=fields.Many2one('ecosphere.esg.category',required=True); metric_id=fields.Many2one('ecosphere.esg.metric',required=True); baseline_value=fields.Float(); target_value=fields.Float(); current_value=fields.Float(); start_date=fields.Date(default=fields.Date.today); target_date=fields.Date(required=True); progress_percentage=fields.Float(compute='_progress',store=True); status=fields.Selection([('draft','Draft'),('active','Active'),('achieved','Achieved'),('failed','Failed'),('cancelled','Cancelled')],default='draft'); responsible_user_id=fields.Many2one('res.users',default=lambda s:s.env.user)
 @api.depends('baseline_value','target_value','current_value')
 def _progress(self):
  for r in self:
   d=r.target_value-r.baseline_value; r.progress_percentage=max(0,min(100,((r.current_value-r.baseline_value)/d*100) if d else 0))
 @api.constrains('start_date','target_date','metric_id','category_id','company_id')
 def _validate_goal(self):
  for r in self:
   if r.start_date and r.target_date and r.target_date<r.start_date: raise ValidationError(_('Target date must not be before start date.'))
   if r.metric_id and r.category_id and r.metric_id.category_id!=r.category_id: raise ValidationError(_('The metric must belong to the selected ESG category.'))
   if r.metric_id and r.metric_id.company_id!=r.company_id: raise ValidationError(_('Goal and metric must belong to the same company.'))
 def action_activate(self): self.write({'status':'active'})
 def action_cancel(self): self.write({'status':'cancelled'})
 @api.model
 def cron_update_goals(self):
  for r in self.search([('status','=','active')]):
   if r.progress_percentage>=100:r.status='achieved'
   elif r.target_date<fields.Date.today():r.status='failed'
class NotificationService(models.AbstractModel):
 _name='ecosphere.notification.service'; _description='EcoSphere Notification Service'
 def notify(self,company,user,setting,summary,note,record=None):
  config=self.env['ecosphere.esg.configuration'].for_company(company)
  if not getattr(config,setting) or not user: return False
  return self.env['mail.activity'].create({'res_model_id':self.env['ir.model']._get_id(record._name if record else 'res.company'),'res_id':record.id if record else company.id,'user_id':user.id,'summary':summary,'note':note,'activity_type_id':self.env.ref('mail.mail_activity_data_todo').id})
