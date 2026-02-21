from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class User(Base):
    """
    Database model for storing users
    """
    __tablename__ = 'users'
    # __table_args__ = {'extend_existing': True}

    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    def __str__(self) -> str:
        return f'Email: {self.email}'
