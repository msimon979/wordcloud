from django.contrib.auth.models import User


def get_user(user_id: int) -> User:
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None


def format_user_context(request, action: str) -> dict:
    data = {
        "password": request.data.get("password"),
        "state": request.data.get("state"),
        "has_pet": request.data.get("has_pet"),
        "include_flood_coverage": request.data.get("include_flood_coverage"),
        "coverage_type": request.data.get("coverage_type"),
        "request_method": action,
    }
    return data


def create_user_context(request) -> dict:
    data = format_user_context(request, "post")

    if None in data.values():
        return None

    return data


def patch_user_context(request) -> dict:
    data = format_user_context(request, "patch")

    patch_data = {}
    for k, v in data.items():
        if v is not None:
            patch_data[k] = v

    return patch_data


def user_can_access(user_id: int, request) -> bool:
    if request.user.is_staff is False and user_id != request.user.id:
        return False

    return True
