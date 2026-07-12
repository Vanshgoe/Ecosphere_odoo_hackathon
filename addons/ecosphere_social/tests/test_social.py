from odoo.tests.common import TransactionCase


class TestSocialAddon(TransactionCase):
    def test_worker_creation(self):
        company = self.env['ecosphere.company'].create({
            'name': 'Social Test Company',
            'code': 'STC',
            'company_id': self.env.company.id,
        })
        worker = self.env['ecosphere.worker'].create({
            'name': 'Test Worker',
            'company_id': company.id,
            'role': 'Analyst',
            'engagement_score': 75.0,
        })
        self.assertEqual(worker.name, 'Test Worker')
