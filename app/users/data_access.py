from app.data_access import BaseDA
from app.users.models import User


class UserDA(BaseDA): # type: ignore
    model = User
