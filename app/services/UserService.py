from ..model.Users import Users


class UserService:
    @staticmethod
    def get_user(user_id) -> Users:
        user = Users.query.get(user_id)
        if user is None:
            raise ValueError(f"User with id {user_id} not found")
        return user

    @staticmethod
    def get_all_users():
        users = Users.query.all()
        return users
