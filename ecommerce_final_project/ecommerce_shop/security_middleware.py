import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

logger = logging.getLogger('security')


class SecurityMiddleware(MiddlewareMixin):
    """
    Middleware для базовой защиты системы.
    """

    def process_request(self, request):
        for key, value in request.GET.items():
            if self._contains_suspicious_characters(value):
                logger.warning(f"Подозрительный запрос: {request.path} с параметром {key}={value}")
                return JsonResponse({"error": "Неверный запрос"}, status=400)

        for key, value in request.POST.items():
            if self._contains_suspicious_characters(value):
                logger.warning(f"Подозрительный POST-запрос: {request.path} с параметром {key}={value}")
                return JsonResponse({"error": "Неверный запрос"}, status=400)

    def _contains_suspicious_characters(self, value):
        """
        Проверяет строку на наличие подозрительных символов.
        """
        suspicious_characters = ["<", ">", "'", "\"", "--", ";", "/*", "*/"]
        return any(char in value for char in suspicious_characters)

    def process_response(self, request, response):
        response["Content-Security-Policy"] = "default-src 'self'"
        return response


    def process_request(self, request):
     if "<script>" in request.body.decode('utf-8').lower():
        logger.warning(f"Potential XSS detected: {request.body}")
        return JsonResponse({"error": "Suspicious input detected"}, status=403)