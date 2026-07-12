from odoo import api,fields,models,_
from odoo.exceptions import ValidationError
class Challenge(models.Model):
 _name='ecosphere.challenge';_description='Challenge'
 name=fields.Char(required=True);company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company);description=fields.Text();xp_reward=fields.Integer();start_date=fields.Date();end_date=fields.Date();state=fields.Selection([('draft','Draft'),('active','Active'),('closed','Closed')],default='draft')
 @api.constrains('xp_reward','start_date','end_date')
 def _challenge_valid(self):
  for r in self:
   if r.xp_reward<0: raise ValidationError(_('XP reward cannot be negative.'))
   if r.start_date and r.end_date and r.end_date<r.start_date: raise ValidationError(_('End date must follow start date.'))
 @api.model
 def cron_close_expired(self): self.search([('state','=','active'),('end_date','<',fields.Date.today())]).write({'state':'closed'})
class ChallengeParticipation(models.Model):
 _name='ecosphere.challenge.participation';_description='Challenge Participation'
 challenge_id=fields.Many2one('ecosphere.challenge',required=True);employee_id=fields.Many2one('hr.employee',required=True);state=fields.Selection([('joined','Joined'),('completed','Completed')],default='joined')
 _sql_constraints=[('challenge_employee','unique(challenge_id,employee_id)','Employee has already joined.')]
class Badge(models.Model):
 _name='ecosphere.badge';_description='Badge'
 name=fields.Char(required=True);required_xp=fields.Integer(default=0);company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company);unlock_rule=fields.Selection([('xp','XP total'),('csr_hours','CSR hours')],default='xp',required=True);unlock_value=fields.Float(default=0)
 @api.model
 def cron_award_badges(self):
  for employee in self.env['hr.employee'].search([]): self.env['ecosphere.badge.service'].evaluate(employee)
class EmployeeBadge(models.Model):
 _name='ecosphere.employee.badge';_description='Employee Badge'
 badge_id=fields.Many2one('ecosphere.badge',required=True);employee_id=fields.Many2one('hr.employee',required=True);awarded_date=fields.Date(default=fields.Date.today)
 _sql_constraints=[('employee_badge','unique(badge_id,employee_id)','Badge already awarded.')]
class Reward(models.Model):
 _name='ecosphere.reward';_description='Reward'
 name=fields.Char(required=True);xp_cost=fields.Integer(required=True);active=fields.Boolean(default=True);company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company)
 @api.constrains('xp_cost')
 def _reward_cost(self):
  if any(r.xp_cost<0 for r in self): raise ValidationError(_('XP cost cannot be negative.'))
class Redemption(models.Model):
 _name='ecosphere.reward.redemption';_description='Reward Redemption'
 reward_id=fields.Many2one('ecosphere.reward',required=True);employee_id=fields.Many2one('hr.employee',required=True);state=fields.Selection([('requested','Requested'),('approved','Approved'),('rejected','Rejected')],default='requested')
class XP(models.Model):
 _name='ecosphere.xp.ledger';_description='XP Ledger';_order='transaction_date desc'
 employee_id=fields.Many2one('hr.employee',required=True);company_id=fields.Many2one(related='employee_id.company_id',store=True);source_model=fields.Char();source_record_id=fields.Integer();reason=fields.Char(required=True);xp_amount=fields.Integer(required=True);transaction_date=fields.Datetime(default=fields.Datetime.now)
 _sql_constraints=[('xp_event_unique','unique(employee_id,source_model,source_record_id,reason)','XP event already processed.')]
class XPService(models.AbstractModel):
 _name='ecosphere.xp.service';_description='XP Ledger Service'
 def balance(self,employee): return sum(self.env['ecosphere.xp.ledger'].search([('employee_id','=',employee.id)]).mapped('xp_amount'))
 def award(self,employee,amount,source_model,source_record_id,reason):
  ledger=self.env['ecosphere.xp.ledger'].search([('employee_id','=',employee.id),('source_model','=',source_model),('source_record_id','=',source_record_id),('reason','=',reason)],limit=1)
  return ledger or self.env['ecosphere.xp.ledger'].create({'employee_id':employee.id,'source_model':source_model,'source_record_id':source_record_id,'reason':reason,'xp_amount':amount})
 def redeem(self,employee,reward):
  existing=self.env['ecosphere.reward.redemption'].search([('employee_id','=',employee.id),('reward_id','=',reward.id),('state','=','requested')],limit=1)
  if existing: return existing
  if self.balance(employee)<reward.xp_cost: raise ValidationError(_('Insufficient XP.'))
  redemption=self.env['ecosphere.reward.redemption'].create({'employee_id':employee.id,'reward_id':reward.id})
  self.award(employee,-reward.xp_cost,'ecosphere.reward.redemption',redemption.id,'Reward redemption')
  return redemption
class BadgeService(models.AbstractModel):
 _name='ecosphere.badge.service';_description='Badge Award Service'
 def evaluate(self,employee):
  balance=self.env['ecosphere.xp.service'].balance(employee)
  badges=self.env['ecosphere.badge'].search([('company_id','=',employee.company_id.id)])
  badges=badges.filtered(lambda badge: balance>=badge.unlock_value if badge.unlock_rule=='xp' else sum(self.env['ecosphere.csr.participation'].search([('employee_id','=',employee.id),('approved','=',True)]).mapped('volunteer_hours'))>=badge.unlock_value)
  existing=self.env['ecosphere.employee.badge'].search([('employee_id','=',employee.id)]).mapped('badge_id')
  awards=self.env['ecosphere.employee.badge'].create([{'employee_id':employee.id,'badge_id':badge.id} for badge in badges-existing])
  for award in awards:self.env['ecosphere.notification.service'].notify(employee.company_id,employee.user_id,'notify_badge_unlocks',_('New EcoSphere badge'),award.badge_id.name,award)
  return awards
