# from django.contrib.auth.models import User
#
#
# class EmailAuthBackend(object):
#     def authenticate(self, request, username=None, password=None):
#         try:
#             user = User.objects.get(email=username)
#             if user.check_password(password):
#                 return user
#             return None
#         except User.DoesNotExist:
#             return None