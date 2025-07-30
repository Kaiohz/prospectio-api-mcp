from typing import Optional
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.dto.database.base import Base


class WorkExperienceDTO(Base):
    """
    Data Transfer Object for WorkExperience.
    SQLAlchemy model for storing work experience entries in the database.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    position: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    start_date: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True
    )  # YYYY-MM format
    end_date: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True
    )  # YYYY-MM or 'Present'
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        """
        String representation of the WorkExperienceDTO object.

        Returns:
            str: A string representation showing position and company.
        """
        return f"WorkExperienceDTO(id={self.id}, position={self.position!r}, company={self.company!r})"
