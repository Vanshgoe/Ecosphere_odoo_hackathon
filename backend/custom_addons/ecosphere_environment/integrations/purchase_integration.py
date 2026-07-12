class PurchaseCarbonAdapter:
 """Optional adapter: callers pass extracted activity data after purchase confirmation."""
 @staticmethod
 def create_transaction(env,order,activity_value,factor):
  return env['ecosphere.carbon.transaction'].create({'name':order.name,'company_id':order.company_id.id,'source_model':'purchase.order','source_record_id':order.id,'source_reference':order.name,'source_type':'purchase','activity_value':activity_value,'activity_unit':factor.activity_unit,'emission_factor_id':factor.id})
