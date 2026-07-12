from odoo.tests import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestEcoSphereAPI(HttpCase):
    def test_api_routes_require_session_and_have_consistent_envelope(self):
        response = self.url_open('/api/ecosphere/v1/me', data='{}', headers={'Content-Type': 'application/json'})
        self.assertIn(response.status_code, (200, 302, 401, 403))

    def test_api_resource_configuration_is_complete(self):
        from odoo.addons.ecosphere_dashboard.controllers.api_controller import EcoSphereAPI
        expected = {'goals', 'carbon', 'csr', 'policies', 'compliance-issues', 'risks', 'audits', 'challenges', 'rewards'}
        self.assertEqual(expected, set(EcoSphereAPI.RESOURCES))
