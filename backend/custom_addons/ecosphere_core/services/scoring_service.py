class ScoringService:
 def __init__(self,env,company): self.env,self.company=env,company
 @staticmethod
 def normalize(metric,value):
  if value is None:return None
  if metric.normalization_method=='boolean': value=100 if value else 0
  elif metric.normalization_method=='percentage': value=float(value)
  elif metric.normalization_method=='target_based': value=(float(value)/metric.target_value*100) if metric.target_value else 0
  else:value=(float(value)-metric.minimum_value)/(metric.maximum_value-metric.minimum_value)*100
  return max(0,min(100,100-value if metric.direction=='lower_is_better' else value))
 def _value(self,metric):
  """Ask an installed domain provider for a metric value; missing data is excluded."""
  provider={'E':'ecosphere.environment.score.service','S':'ecosphere.social.score.service','G':'ecosphere.governance.score.service'}.get(metric.category_id.code)
  return self.env[provider].metric_value(metric,self.company) if provider and provider in self.env else None
 def category_score(self,code):
  metrics=self.env['ecosphere.esg.metric'].search([('company_id','=',self.company.id),('category_id.code','=',code),('active','=',True)])
  items=[(metric,self.normalize(metric,self._value(metric))) for metric in metrics]
  items=[item for item in items if item[1] is not None and item[0].weight]
  return sum(metric.weight*value for metric,value in items)/sum(metric.weight for metric,value in items) if items else 0.0
 def calculate(self):
  config=self.env['ecosphere.scoring.config'].search([('company_id','=',self.company.id),('active','=',True)],limit=1)
  if not config:return False
  values={'environmental_score':self.category_score('E'),'social_score':self.category_score('S'),'governance_score':self.category_score('G'),'scoring_config_id':config.id}
  values['overall_score']=sum(values[field]*weight/100 for field,weight in [('environmental_score',config.environmental_weight),('social_score',config.social_weight),('governance_score',config.governance_weight)])
  current=self.env['ecosphere.esg.score'].search([('company_id','=',self.company.id)],limit=1)
  if current: current.write(values)
  else: values['company_id']=self.company.id; current=self.env['ecosphere.esg.score'].create(values)
  return current
