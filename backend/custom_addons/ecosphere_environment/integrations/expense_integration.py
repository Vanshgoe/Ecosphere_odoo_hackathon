class ExpenseCarbonAdapter:
 @staticmethod
 def activity_values(record): return {'source_type':'expense','activity_value':getattr(record,'quantity',0.0)}
