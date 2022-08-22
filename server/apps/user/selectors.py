from django.db.models import QuerySet

from user.models import CustomUser

def get_user_by_id(pk=int) -> QuerySet:
    return CustomUser.objects.get(id=pk)
