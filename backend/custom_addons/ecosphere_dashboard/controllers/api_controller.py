"""Authenticated JSON API for the separate EcoSphere frontend.

This controller deliberately uses ``request.env`` (never sudo) so normal Odoo
ACLs, record rules, active company, and allowed-company context still apply.
"""
from datetime import date, datetime

from odoo import fields, http
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.http import request


class EcoSphereAPI(http.Controller):
    """Small reusable CRUD/serialization layer for public EcoSphere resources."""

    # API name: (model, fields exposed to frontend, date field used by filters)
    RESOURCES = {
        'goals': ('ecosphere.esg.goal', ('name', 'company_id', 'category_id', 'metric_id', 'baseline_value', 'target_value', 'current_value', 'start_date', 'target_date', 'progress_percentage', 'status', 'responsible_user_id'), 'target_date'),
        'carbon': ('ecosphere.carbon.transaction', ('name', 'company_id', 'source_model', 'source_record_id', 'source_reference', 'source_type', 'activity_value', 'activity_unit', 'emission_factor_id', 'emissions_kg_co2e', 'scope', 'transaction_date', 'state'), 'transaction_date'),
        'csr': ('ecosphere.csr.activity', ('name', 'description', 'company_id', 'organizer_id', 'start_date', 'end_date', 'target_participants', 'state', 'approved_by', 'approval_date'), 'start_date'),
        'policies': ('ecosphere.esg.policy', ('name', 'code', 'description', 'company_id', 'owner_id', 'version', 'effective_date', 'review_date', 'state'), 'effective_date'),
        'compliance-issues': ('ecosphere.compliance.issue', ('name', 'company_id', 'severity', 'responsible_user_id', 'due_date', 'resolution_date', 'state', 'description'), 'due_date'),
        'risks': ('ecosphere.risk.register', ('name', 'company_id', 'category', 'probability', 'impact', 'risk_score', 'mitigation_plan', 'owner_id', 'state'), None),
        'audits': ('ecosphere.esg.audit', ('name', 'company_id', 'audit_type', 'auditor', 'start_date', 'end_date', 'findings', 'score', 'state'), 'start_date'),
        'challenges': ('ecosphere.challenge', ('name', 'company_id', 'description', 'xp_reward', 'start_date', 'end_date', 'state'), 'start_date'),
        'rewards': ('ecosphere.reward', ('name', 'xp_cost', 'active', 'company_id'), None),
        'emission-factors': ('ecosphere.emission.factor', ('name', 'code', 'source_type', 'activity_unit', 'emission_unit', 'factor_value', 'scope', 'effective_from', 'effective_to', 'active', 'company_id'), 'effective_from'),
        'product-profiles': ('ecosphere.product.esg.profile', ('product_tmpl_id', 'carbon_intensity', 'recycled_content_percentage', 'sustainability_rating', 'company_id'), None),
        'categories': ('ecosphere.esg.category', ('name', 'code', 'sequence', 'active', 'company_id'), None),
        'badges': ('ecosphere.badge', ('name', 'required_xp', 'company_id', 'unlock_rule', 'unlock_value'), None),
        'challenge-participation': ('ecosphere.challenge.participation', ('challenge_id', 'employee_id', 'state'), None),
        'csr-participation': ('ecosphere.csr.participation', ('activity_id', 'employee_id', 'company_id', 'participation_status', 'volunteer_hours', 'approved', 'approved_by'), None),
        'acknowledgements': ('ecosphere.policy.acknowledgement', ('policy_id', 'employee_id', 'company_id', 'acknowledged', 'acknowledgement_date'), None),
    }

    def _ok(self, data, pagination=None):
        result = {'success': True, 'data': data}
        if pagination is not None:
            result['pagination'] = pagination
        return result

    def _error(self, code, message):
        return {'success': False, 'error': {'code': code, 'message': str(message)}}

    def _company(self, company_id=None):
        """Return one of the session's allowed companies, or raise a safe error."""
        if company_id in (None, False, ''):
            return request.env.company
        try:
            company_id = int(company_id)
        except (TypeError, ValueError):
            raise UserError('company_id must be an integer.')
        company = request.env['res.company'].browse(company_id).exists()
        if not company or company not in request.env.companies:
            raise AccessError('The company is not available in this session.')
        return company

    def _resource(self, name):
        if name not in self.RESOURCES:
            raise UserError('Unknown API resource.')
        return self.RESOURCES[name]

    @staticmethod
    def _integer(value, name, default=None, minimum=None):
        if value in (None, ''):
            return default
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise UserError('%s must be an integer.' % name)
        if minimum is not None and value < minimum:
            raise UserError('%s must be at least %s.' % (name, minimum))
        return value

    @staticmethod
    def _date(value, name):
        """Reject malformed filter values before they reach PostgreSQL."""
        if value in (None, ''):
            return value
        if not isinstance(value, str):
            raise UserError('%s must use YYYY-MM-DD format.' % name)
        try:
            date.fromisoformat(value)
        except ValueError:
            raise UserError('%s must use YYYY-MM-DD format.' % name)
        return value

    def _record(self, model, record_id):
        record_id = self._integer(record_id, 'id', minimum=1)
        if not record_id:
            raise UserError('id is required.')
        record = request.env[model].browse(record_id).exists()
        if not record:
            return False
        record.check_access('read')
        record.check_access_rule('read')
        return record

    @staticmethod
    def _json_value(value):
        if isinstance(value, (date, datetime)):
            return fields.Datetime.to_string(value) if isinstance(value, datetime) else fields.Date.to_string(value)
        return value

    def _serialize(self, record, names):
        data = {'id': record.id}
        for name in names:
            field = record._fields[name]
            value = record[name]
            if field.type == 'many2one':
                data[name] = {'id': value.id, 'name': value.display_name} if value else None
            elif field.type in ('many2many', 'one2many'):
                data[name] = [{'id': item.id, 'name': item.display_name} for item in value]
            elif field.type == 'selection':
                data[name] = value or None
                data[name + '_label'] = dict(field._description_selection(record.env)).get(value) if value else None
            else:
                data[name] = self._json_value(value)
        return data

    def _values(self, model, exposed, payload, creating=False):
        values = payload.get('values', payload.get('data'))
        if not isinstance(values, dict):
            raise UserError('values must be an object.')
        writable = set(exposed) - {'progress_percentage', 'emissions_kg_co2e', 'scope', 'risk_score', 'approved_by', 'approval_date', 'resolution_date', 'acknowledged', 'acknowledgement_date'}
        unknown = set(values) - writable
        if unknown:
            raise UserError('Unsupported field(s): %s.' % ', '.join(sorted(unknown)))
        result = dict(values)
        has_company = 'company_id' in request.env[model]._fields
        if 'company_id' in result and has_company:
            company = self._company(result['company_id'])
            result['company_id'] = company.id
        elif creating and has_company:
            result['company_id'] = self._company(payload.get('company_id')).id
        elif 'company_id' in result and not has_company:
            del result['company_id']
        for field_name, value in list(result.items()):
            field = request.env[model]._fields[field_name]
            if field.type == 'date':
                result[field_name] = self._date(value, field_name)
            if field.type == 'many2one' and isinstance(value, dict):
                value = value.get('id')
                result[field_name] = value
            if field.type == 'many2one' and value not in (False, None, ''):
                value = self._integer(value, field_name, minimum=1)
                related = request.env[field.comodel_name].browse(value).exists()
                if not related:
                    raise UserError('%s does not reference an existing record.' % field_name)
                related.check_access('read')
                related.check_access_rule('read')
                result[field_name] = value
        return result

    def _domain(self, resource, payload):
        model, _names, date_field = self._resource(resource)
        company = self._company(payload.get('company_id'))
        domain = [('company_id', '=', company.id)] if 'company_id' in request.env[model]._fields else []
        if payload.get('status') not in (None, ''):
            state_field = 'status' if 'status' in request.env[model]._fields else 'state'
            domain.append((state_field, '=', payload['status']))
        if date_field:
            if payload.get('date_from'):
                domain.append((date_field, '>=', self._date(payload['date_from'], 'date_from')))
            if payload.get('date_to'):
                domain.append((date_field, '<=', self._date(payload['date_to'], 'date_to')))
        return domain

    def _dispatch(self, resource, action, **payload):
        try:
            model, names, _date_field = self._resource(resource)
            records = request.env[model]
            if action == 'list':
                limit = self._integer(payload.get('limit'), 'limit', 20, 1)
                if limit > 200:
                    raise UserError('limit cannot exceed 200.')
                offset = self._integer(payload.get('offset'), 'offset', 0, 0)
                domain = self._domain(resource, payload)
                total = records.search_count(domain)
                rows = records.search(domain, limit=limit, offset=offset)
                return self._ok([self._serialize(row, names) for row in rows], {'limit': limit, 'offset': offset, 'total': total})
            if action == 'get':
                record = self._record(model, payload.get('id'))
                if not record:
                    return self._error('not_found', 'Record not found.')
                return self._ok(self._serialize(record, names))
            if action == 'create':
                values = self._values(model, names, payload, creating=True)
                record = records.create(values)
                return self._ok(self._serialize(record, names))
            if action == 'update':
                record = self._record(model, payload.get('id'))
                if not record:
                    return self._error('not_found', 'Record not found.')
                record.check_access('write')
                record.check_access_rule('write')
                record.write(self._values(model, names, payload))
                return self._ok(self._serialize(record, names))
            if action == 'delete':
                record = self._record(model, payload.get('id'))
                if not record:
                    return self._error('not_found', 'Record not found.')
                record.check_access('unlink')
                record.check_access_rule('unlink')
                record.unlink()
                return self._ok({'id': self._integer(payload.get('id'), 'id'), 'deleted': True})
        except AccessError as error:
            return self._error('access_denied', error)
        except (ValidationError, UserError) as error:
            return self._error('validation_error', error)
        except (TypeError, ValueError) as error:
            return self._error('invalid_input', error)

    # Kept as concrete methods so every route is visible to Odoo's router.
    @http.route('/api/ecosphere/v1/me', type='json', auth='user', methods=['POST'])
    def me(self, **payload):
        user = request.env.user
        return self._ok({'id': user.id, 'name': user.name, 'login': user.login, 'company': {'id': request.env.company.id, 'name': request.env.company.display_name}, 'allowed_companies': [{'id': company.id, 'name': company.display_name} for company in request.env.companies]})

    @http.route('/api/ecosphere/v1/<string:resource>/<string:action>', type='json', auth='user', methods=['POST'])
    def crud(self, resource, action, **payload):
        if resource not in self.RESOURCES or action not in ('list', 'get', 'create', 'update', 'delete'):
            return self._error('not_found', 'Endpoint not found.')
        return self._dispatch(resource, action, **payload)

    @http.route('/api/ecosphere/v1/<string:resource>/summary', type='json', auth='user', methods=['POST'])
    def summary(self, resource, **payload):
        if resource not in ('carbon', 'csr'):
            return self._error('not_found', 'Endpoint not found.')
        try:
            model, _names, _date_field = self._resource(resource)
            domain = self._domain(resource, payload)
            if resource == 'carbon':
                domain.append(('state', '!=', 'cancelled'))
                groups = request.env[model].read_group(domain, ['emissions_kg_co2e:sum'], ['scope'])
                return self._ok({'total_emissions_kg_co2e': sum(row['emissions_kg_co2e'] for row in groups), 'by_scope': [{'scope': row['scope'], 'emissions_kg_co2e': row['emissions_kg_co2e']} for row in groups]})
            groups = request.env[model].read_group(domain, [], ['state'])
            return self._ok({'total': request.env[model].search_count(domain), 'by_state': [{'state': row['state'], 'count': row['__count']} for row in groups]})
        except AccessError as error:
            return self._error('access_denied', error)
        except (ValidationError, UserError, TypeError, ValueError) as error:
            return self._error('validation_error', error)

    @http.route('/api/ecosphere/v1/gamification/leaderboard', type='json', auth='user', methods=['POST'])
    def leaderboard(self, **payload):
        try:
            company = self._company(payload.get('company_id'))
            limit = self._integer(payload.get('limit'), 'limit', 20, 1)
            if limit > 200:
                raise UserError('limit cannot exceed 200.')
            groups = request.env['ecosphere.xp.ledger'].read_group([('company_id', '=', company.id)], ['xp_amount:sum'], ['employee_id'], orderby='xp_amount desc', limit=limit)
            return self._ok([{'rank': index + 1, 'employee': {'id': row['employee_id'][0], 'name': row['employee_id'][1]} if row['employee_id'] else None, 'xp': row['xp_amount']} for index, row in enumerate(groups)])
        except AccessError as error:
            return self._error('access_denied', error)
        except (ValidationError, UserError, TypeError, ValueError) as error:
            return self._error('validation_error', error)

    @http.route('/api/ecosphere/v1/dashboard', type='json', auth='user', methods=['POST'])
    def dashboard(self, **payload):
        # Delegate to the existing implementation to keep dashboard business logic identical.
        from .dashboard_controller import DashboardController
        try:
            data = DashboardController().overview(company_id=payload.get('company_id'), date_from=payload.get('date_from'), date_to=payload.get('date_to'))
            if data.get('metadata', {}).get('error'):
                return self._error('access_denied', 'The company is not available in this session.')
            return self._ok(data)
        except AccessError as error:
            return self._error('access_denied', error)
        except (ValidationError, UserError, TypeError, ValueError) as error:
            return self._error('validation_error', error)
