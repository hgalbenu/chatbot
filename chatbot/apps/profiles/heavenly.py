import datetime

from django.conf import settings


class Heavenly(object):
    def to_heavenly(self):
        import requests
        from requests.auth import HTTPBasicAuth

        def safe_cast(val, to_type, default=None):
            try:
                return to_type(val)
            except (ValueError, TypeError):
                return default

        credit_score_map = {
            'Very Important': 'high',
            'Somewhat Important': 'medium',
            'Not that important': 'low'
        }
        payload = {
            'state': self.state,
            'household-size': safe_cast(self.houseHoldSize, int),
            'credit-score-importance': credit_score_map.get(self.credit_score_importance, None),
            'incomes': [{
                    'dollar-value': safe_cast(j.income, int),
                    'consistent?': True if j.income_consistency and j.income_consistency.lower() == 'yes' else False
                } for j in self.jobs],
            'debts': [{
                    'name': d.creditor_name,
                    'dollar-value': safe_cast(d.balance, int),
                    'interest': safe_cast(d.interest_rate, float),
                    'days-behind': d.days_behind or 0
                } for d in self.debts],
        }
        try:
            r = requests.post(
                settings.HEAVENLY_URL,
                json=payload,
                auth=HTTPBasicAuth(settings.HEAVENLY_USERNAME, settings.HEAVENLY_PASSWORD)
            )
            return_data = r.json()
            outcomes = return_data.get('results', {}).get('outcomes', []) if isinstance(return_data, dict) else None
            actions = ', '.join(o.get('action', None) for o in outcomes)
            print('Heavenly', payload, return_data, actions)
            self.heavenly_request = payload
            self.heavenly_response = return_data
            self.heavenly_updated_at = datetime.now()
            self.action = actions
        except:
            pass
