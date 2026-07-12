class FleetCarbonAdapter:
 @staticmethod
 def activity_values(record): return {'source_type':'fleet','activity_value':getattr(record,'distance',0.0)}
