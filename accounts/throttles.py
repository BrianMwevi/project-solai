from rest_framework.throttling import UserRateThrottle, BaseThrottle


class TraderThrottle(UserRateThrottle):
    scope = 'trader'


class DeveloperThrottle(UserRateThrottle):
    scope = 'trader'


class InvestorThrottle(BaseThrottle):
    def allow_request(self, request, view):
        whitelist = "127.0.0.1:8000"
        incoming = request.META.get("HTTP_HOST")
        print(whitelist, incoming)
        if request.user.role == 'INVESTOR' and whitelist == incoming:
            return True
        return False
