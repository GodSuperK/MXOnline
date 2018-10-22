__author__ = "GodSuperK"
__date__ = "18-10-22 上午7:59"

from operation.models import UserStar


def has_star(user, org_id, fav_type=3):
    if user.is_authenticated:
        is_existed = UserStar.objects.filter(user_id=user.id, id_of_staring=org_id, type_of_staring=fav_type)
        if is_existed:
            return True
        else:
            return False
    return False
