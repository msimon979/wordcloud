from users.models import UserInformation

class UserService:
    
    @staticmethod
    def create_user_information(user, state):
        UserInformation.objects.create(user=user, state=state)

    @staticmethod
    def update_user_state(user, state):
        user = UserInformation.objects.get(user=user)
        user.state = state
        user.save()

    @staticmethod
    def get_user_state(user):
        try:
            user = UserInformation.objects.get(user=user)
        except UserInformation.DoesNotExist:
            return None
        return user.state