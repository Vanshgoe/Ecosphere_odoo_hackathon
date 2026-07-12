from odoo import http
from odoo.http import request
class DashboardController(http.Controller):
 def _company(self,company_id):
  try: company=request.env.company if not company_id else request.env['res.company'].browse(int(company_id)).exists()
  except (TypeError,ValueError): return False
  return company if company and company in request.env.companies else False
 @http.route('/ecosphere/dashboard/summary',type='json',auth='user')
 def summary(self,company_id=None,**kwargs):
  company=self._company(company_id)
  if not company: return {'labels':[],'series':[],'metadata':{'error':'company_not_allowed'}}
  score=request.env['ecosphere.esg.score'].search([('company_id','=',company.id)],limit=1)
  values=[score.environmental_score,score.social_score,score.governance_score,score.overall_score] if score else [0,0,0,0]
  return {'labels':['Environmental','Social','Governance','Overall'],'series':[{'name':'ESG score','data':values}],'metadata':{'company_id':company.id}}
 @http.route('/ecosphere/dashboard/emissions',type='json',auth='user')
 def emissions(self,company_id=None,**kwargs):
  company=self._company(company_id)
  if not company:return {'labels':[],'series':[],'metadata':{'error':'company_not_allowed'}}
  cid=company.id
  groups=request.env['ecosphere.carbon.transaction'].read_group([('company_id','=',cid),('state','!=','cancelled')],['emissions_kg_co2e:sum'],['scope'])
  return {'labels':[g['scope'] for g in groups],'series':[{'name':'kg CO2e','data':[g['emissions_kg_co2e'] for g in groups]}],'metadata':{'company_id':cid}}
 @http.route('/ecosphere/dashboard/overview',type='json',auth='user')
 def overview(self,company_id=None,date_from=None,date_to=None,**kwargs):
  company=self._company(company_id)
  if not company:return {'kpis':{},'charts':{},'metadata':{'error':'company_not_allowed'}}
  domain=[('company_id','=',company.id)]
  carbon_domain=domain.copy()
  if date_from: carbon_domain.append(('transaction_date','>=',date_from))
  if date_to: carbon_domain.append(('transaction_date','<=',date_to))
  goals=request.env['ecosphere.esg.goal'].search(domain)
  score=request.env['ecosphere.esg.score'].search(domain,limit=1)
  emissions=request.env['ecosphere.carbon.transaction'].read_group(carbon_domain+[('state','!=','cancelled')],['emissions_kg_co2e:sum'],['scope'])
  states=request.env['ecosphere.esg.goal'].read_group(domain,[],['status'])
  issues=request.env['ecosphere.compliance.issue'].read_group(domain,[],['state'])
  return {'kpis':{'total_goals':len(goals),'completed_goals':len(goals.filtered(lambda g:g.status=='achieved')),'overall_esg_progress':score.overall_score if score else 0,'total_carbon_emissions':sum(row['emissions_kg_co2e'] for row in emissions),'csr_activities':request.env['ecosphere.csr.activity'].search_count(domain),'open_compliance_issues':request.env['ecosphere.compliance.issue'].search_count(domain+[('state','in',['open','in_progress','overdue'])])},'charts':{'esg_scores':{'labels':['Environmental','Social','Governance'],'series':[{'name':'Score','data':[score.environmental_score if score else 0,score.social_score if score else 0,score.governance_score if score else 0]}]},'emissions_by_scope':{'labels':[row['scope'] for row in emissions],'series':[{'name':'kg CO2e','data':[row['emissions_kg_co2e'] for row in emissions]}]},'goal_status':{'labels':[row['status'] for row in states],'series':[{'name':'Goals','data':[row['__count'] for row in states]}]},'issue_status':{'labels':[row['state'] for row in issues],'series':[{'name':'Issues','data':[row['__count'] for row in issues]}]}},'metadata':{'company_id':company.id,'date_from':date_from,'date_to':date_to}}
