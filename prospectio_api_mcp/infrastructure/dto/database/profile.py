from typing import List, Optional, Any
from sqlalchemy import Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.dto.database.base import Base


class ProfileDTO(Base):
    """
    Data Transfer Object for Profile.
    SQLAlchemy model for storing user profiles in the database.
    """

    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    work_experience: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        """
        String representation of the ProfileDTO object.

        Returns:
            str: A string representation showing last_name and job_title.
        """
        return f"ProfileDTO(id={self.id}, job_title={self.job_title!r})"
