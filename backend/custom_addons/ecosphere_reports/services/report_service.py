class ReportService:
 def __init__(self,env,wizard): self.env,self.wizard=env,wizard
 def payload(self):
  company=self.wizard.company_id
  score=self.env['ecosphere.esg.score'].search([('company_id','=',company.id)],limit=1)
  emissions=self.env['ecosphere.carbon.transaction'].read_group([('company_id','=',company.id),('transaction_date','>=',self.wizard.date_from),('transaction_date','<=',self.wizard.date_to)],['emissions_kg_co2e:sum'],['scope'])
  return {'score':score,'emissions':emissions}
