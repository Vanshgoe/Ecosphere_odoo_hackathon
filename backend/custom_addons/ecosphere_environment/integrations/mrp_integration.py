class ManufacturingCarbonAdapter:
 @staticmethod
 def activity_values(record): return {'source_type':'manufacturing','activity_value':getattr(record,'qty_produced',0.0)}
