from odoo.tests.common import TransactionCase
from ..services.scoring_service import ScoringService

class TestScoring(TransactionCase):
 def test_normalization_percentage(self):
  metric=self.env['ecosphere.esg.metric'].new({'name':'Metric','code':'test_normal','category_id':self.env.ref('ecosphere_core.category_environmental').id,'normalization_method':'percentage','direction':'higher_is_better','company_id':self.env.company.id})
  self.assertEqual(ScoringService.normalize(metric,120),100)
 def test_lower_is_better(self):
  metric=self.env['ecosphere.esg.metric'].new({'name':'Metric','code':'test_lower','category_id':self.env.ref('ecosphere_core.category_environmental').id,'normalization_method':'percentage','direction':'lower_is_better','company_id':self.env.company.id})
  self.assertEqual(ScoringService.normalize(metric,20),80)
