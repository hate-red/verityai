from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Float
from sqlalchemy.dialects.postgresql import ARRAY

from pydantic import ConfigDict

from app.database import Base
from app.users.models import User


class Sentiment(Base):
    __tablename__ = 'sentiments'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Can bu null if user is not logged in 
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    
    # TEXT field to store files contents, parsed html, plain text 
    source_text: Mapped[str]
    
    sentiments: Mapped[list[float]] = mapped_column(ARRAY(Float))

    user: Mapped[User] = relationship('User')

    model_config = ConfigDict(from_attributes=True)


    def to_dict(self) -> dict:
        return {
            'id': self.id, 
            'user_id': self.user_id, 
            'source_text': self.source_text,
            'sentiments': self.sentiments,    
        }

    def __repr__(self) -> str:
        return f'User ID: {self.user_id}\t'\
               f'Text: {self.source_text :10}...\t'\
               f'Sentiments: {self.sentiments[0]}'
