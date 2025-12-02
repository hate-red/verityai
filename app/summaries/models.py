from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from pydantic import ConfigDict
from typing import Optional

from app.database import Base
from app.users.models import User


class Summary(Base):
    __tablename__ = 'summaries'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Can bu null if user is not logged in 
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True, default=None) # type: ignore
    
    # Just TEXT field to store files contents, parsed html, plain text 
    source_text: Mapped[str]
    
    # Also a TEXT filed for processed source_text
    summarized_text: Mapped[str]
    
    user: Mapped[User] = relationship('User') # type: ignore # noqa: F821

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'source_text': self.source_text,
            'summarized_text': self.summarized_text,
        }


    def __repr__(self) -> str:
        return f'User ID: {self.user_id} | {self.source_text :10}... | {self.summarized_text :10}...'
