class AnalyticsService:
 """Read-group based, company-scoped dashboard aggregation helper."""
 def __init__(self,env,company): self.env,self.company=env,company
 def emissions_by_scope(self):
  rows=self.env['ecosphere.carbon.transaction'].read_group([('company_id','=',self.company.id),('state','!=','cancelled')],['emissions_kg_co2e:sum'],['scope'])
  return {'labels':[row['scope'] for row in rows],'series':[{'name':'kg CO2e','data':[row['emissions_kg_co2e'] for row in rows]}]}
