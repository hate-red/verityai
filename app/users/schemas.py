from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr

    # roles
    is_admin: bool

    def __repr__(self):
        return f'username: {self.username}, email: {self.email}'


class UserFilter(BaseModel):
    id: int | None = None
    username: str | None = None
    email: EmailStr | None = None


    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username, 
            'email': self.email,
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}

        return filtered_data


class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

    def to_dict(self):
        data = {
            'username': self.username,
            'email': self.email,
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}

        return filtered_data


class UserDelete(BaseModel):
    id: int | None = None
    username: str | None = None
    email: EmailStr | None = None


    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}

        return filtered_data