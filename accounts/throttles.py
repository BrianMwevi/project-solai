from rest_framework.throttling import UserRateThrottle


class TraderThrottle(UserRateThrottle):
    scope = 'trader'


class DeveloperThrottle(UserRateThrottle):
    scope = 'developer'


class InvestorThrottle(UserRateThrottle):
    scope = 'investor'



