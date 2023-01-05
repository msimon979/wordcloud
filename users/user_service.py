from users.models import UserInformation


class UserService:
    @staticmethod
    def create_user_information(user, context):
        query_args = {
            "user": user,
            "state": context["state"],
            "has_pet": context["has_pet"],
            "include_flood_coverage": context["include_flood_coverage"],
            "coverage_type": context["coverage_type"],
        }

        user_information = UserInformation.objects.create(**query_args)
        return user_information

    @staticmethod
    def update_user_information(user, context):
        user = UserInformation.objects.get(user=user)

        for col, value in context.items():
            if hasattr(user, col):
                setattr(user, col, value)

        user.save()
        return user

    @staticmethod
    def get_user_state(user):
        try:
            user = UserInformation.objects.get(user=user)
        except UserInformation.DoesNotExist:
            return None
        return user.state

    @staticmethod
    def get_user_information(user):
        try:
            user = UserInformation.objects.get(user=user)
        except UserInformation.DoesNotExist:
            return {}

        user_info = {
            "state": user.state,
            "has_pet": user.has_pet,
            "include_flood_coverage": user.include_flood_coverage,
            "coverage_type": user.coverage_type,
        }

        return user_info
