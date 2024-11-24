from rest_framework.throttling import UserRateThrottle

class RoleBasedThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            self.rate = '1000/day'
        else:
            self.rate = '100/day'  
        return super().get_cache_key(request, view)
