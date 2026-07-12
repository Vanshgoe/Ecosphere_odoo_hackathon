from odoo import api,fields,models,_
from odoo.exceptions import ValidationError
class Factor(models.Model):
 _name='ecosphere.emission.factor';_description='Emission Factor'
 name=fields.Char(required=True);code=fields.Char(required=True);source_type=fields.Char(required=True);activity_unit=fields.Char(required=True);emission_unit=fields.Char(default='kg CO2e');factor_value=fields.Float(required=True);scope=fields.Selection([('scope_1','Scope 1'),('scope_2','Scope 2'),('scope_3','Scope 3')],required=True);effective_from=fields.Date();effective_to=fields.Date();active=fields.Boolean(default=True);company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company)
 @api.constrains('factor_value')
 def _positive(self):
  if any(r.factor_value<0 for r in self):raise ValidationError(_('Factor must be non-negative.'))
 @api.constrains('effective_from','effective_to')
 def _dates(self):
  if any(r.effective_from and r.effective_to and r.effective_to<r.effective_from for r in self): raise ValidationError(_('Effective end date must follow start date.'))
 @api.model
 def resolve_factor(self,company,source_type,activity_unit,on_date=None):
  domain=[('company_id','=',company.id),('source_type','=',source_type),('activity_unit','=',activity_unit),('active','=',True)]
  if on_date: domain += ['|',('effective_from','=',False),('effective_from','<=',on_date),'|',('effective_to','=',False),('effective_to','>=',on_date)]
  return self.search(domain,limit=1)
class Carbon(models.Model):
 _name='ecosphere.carbon.transaction';_description='Carbon Transaction';_order='transaction_date desc'
 name=fields.Char(required=True);company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company);source_model=fields.Char();source_record_id=fields.Integer();source_reference=fields.Char();source_type=fields.Char(required=True);activity_value=fields.Float(required=True);activity_unit=fields.Char(required=True);emission_factor_id=fields.Many2one('ecosphere.emission.factor',required=True);emissions_kg_co2e=fields.Float(compute='_emissions',store=True);scope=fields.Selection(related='emission_factor_id.scope',store=True);transaction_date=fields.Date(default=fields.Date.today);state=fields.Selection([('draft','Draft'),('calculated','Calculated'),('cancelled','Cancelled')],default='calculated')
 _sql_constraints=[('carbon_source_unique','unique(company_id,source_model,source_record_id,source_type)','Duplicate carbon event.')]
 @api.depends('activity_value','emission_factor_id.factor_value')
 def _emissions(self):
  for r in self:r.emissions_kg_co2e=r.activity_value*r.emission_factor_id.factor_value
 @api.constrains('activity_value','company_id','emission_factor_id')
 def _validate_transaction(self):
  for r in self:
   if r.activity_value<0: raise ValidationError(_('Activity value cannot be negative.'))
   if r.emission_factor_id and r.emission_factor_id.company_id!=r.company_id: raise ValidationError(_('Emission factor must belong to the same company.'))
class Profile(models.Model):
 _name='ecosphere.product.esg.profile';_description='Product ESG Profile'
 product_tmpl_id=fields.Many2one('product.template',required=True);carbon_intensity=fields.Float();recycled_content_percentage=fields.Float();sustainability_rating=fields.Selection([('a','A'),('b','B'),('c','C'),('d','D')]);company_id=fields.Many2one('res.company',required=True,default=lambda s:s.env.company)
class EnvironmentalScoreService(models.AbstractModel):
 _name='ecosphere.environment.score.service';_description='Environmental Metric Provider'
 def metric_value(self,metric,company):
  Carbon=self.env['ecosphere.carbon.transaction']
  if metric.code in ('carbon_emissions','emissions_kg_co2e'):
   return sum(Carbon.search([('company_id','=',company.id),('state','=','calculated')]).mapped('emissions_kg_co2e'))
  if metric.code=='recycled_content_percentage':
   values=self.env['ecosphere.product.esg.profile'].search([('company_id','=',company.id)]).mapped('recycled_content_percentage')
   return sum(values)/len(values) if values else None
  return None
