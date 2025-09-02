# from django.conf import settings
# from rest_framework import status
# from django.http import JsonResponse


# class TokenAuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.exluded_paths = ["/", "/admin/"]

#     def __call__(self, request):
#         if request.path in self.exluded_paths:
#             return self.get_response(request)
#         auth_header = request.headers.get("Authorization")

#         if not auth_header:
#             return JsonResponse(
#                 {"error": "Invalid or missing token"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         auth_bearer_and_token = auth_header.split(" ", 1)

#         if (
#             not len(auth_bearer_and_token) == 2
#             or not auth_bearer_and_token[0] == "Bearer"
#         ):
#             return JsonResponse(
#                 {"error": "Invalid or missing token"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         token = auth_bearer_and_token[1]
#         if token != settings.SECRET_TOKEN:
#             return JsonResponse(
#                 {"error": "Invalid or missing token"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         return self.get_response(request)
