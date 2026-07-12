from odoo.tests.common import TransactionCase


class TestEcoSphereCompany(TransactionCase):

    def test_company_score_status(self):
        company = self.env['ecosphere.company'].create({
            'name': 'Test Company',
            'code': 'TCO',
            'company_id': self.env.company.id,
            'sustainability_score': 75.0,
            'target_score': 80.0,
        })
        self.assertEqual(company.score_status, 'monitor')
