import json

from odoo import http
from odoo.http import request


class EcoSphereDashboardController(http.Controller):
    @http.route(['/ecosphere/dashboard'], type='http', auth='user', website=True)
    def dashboard(self, **kwargs):
        return request.render('ecosphere_dashboard.dashboard_page', {
            'company_name': request.env.user.company_id.name,
        })

    @http.route(['/ecosphere/dashboard/data'], type='json', auth='user', website=True)
    def dashboard_data(self, **kwargs):
        company = request.env['ecosphere.company'].search([], limit=1)
        metrics = request.env['ecosphere.metric'].search([('company_id', '=', company.id)] if company else [])
        emissions = request.env['ecosphere.emission'].search([('company_id', '=', company.id)] if company else [])
        workers = request.env['ecosphere.worker'].search([('company_id', '=', company.id)] if company else [])
        policies = request.env['ecosphere.policy'].search([('company_id', '=', company.id)] if company else [])

        environmental_score = 0.0
        social_score = 0.0
        governance_score = 0.0
        if metrics:
            env_metrics = metrics.filtered(lambda m: m.category == 'environment')
            social_metrics = metrics.filtered(lambda m: m.category == 'social')
            governance_metrics = metrics.filtered(lambda m: m.category == 'governance')
            environmental_score = round(sum(m.score for m in env_metrics) / len(env_metrics), 2) if env_metrics else 0.0
            social_score = round(sum(m.score for m in social_metrics) / len(social_metrics), 2) if social_metrics else 0.0
            governance_score = round(sum(m.score for m in governance_metrics) / len(governance_metrics), 2) if governance_metrics else 0.0

        trend = []
        for item in emissions.sorted('date'):
            trend.append({'name': item.date, 'value': item.quantity})

        departments = []
        for company_item in request.env['ecosphere.company'].search([]):
            departments.append({
                'name': company_item.name,
                'score': company_item.sustainability_score,
            })

        leaderboard = []
        for worker in workers.sorted('engagement_score', reverse=True)[:5]:
            leaderboard.append({'name': worker.name, 'score': worker.engagement_score})

        return {
            'company': company.name if company else 'EcoSphere',
            'environmental_score': environmental_score,
            'social_score': social_score,
            'governance_score': governance_score,
            'department_ranking': sorted(departments, key=lambda x: x['score'], reverse=True)[:5],
            'leaderboard': leaderboard,
            'carbon_trend': trend,
            'policy_count': len(policies),
            'worker_count': len(workers),
        }
