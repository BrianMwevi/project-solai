from rest_framework.throttling import UserRateThrottle, BaseThrottle


class TraderThrottle(UserRateThrottle):
    scope = 'trader'


class DeveloperThrottle(UserRateThrottle):
    scope = 'trader'



