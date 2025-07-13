from typing import List, Optional
from sqlalchemy import ARRAY, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from infrastructure.dto.database.base import Base


class Company(Base):
    """
    Represents a company with optional fields to match frontend requirements.
    SQLAlchemy model for database persistence.
    """

    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        doc="Unique identifier for the company",
    )
    name: Mapped[Optional[str]] = mapped_column(String(255), doc="Name of the company")
    industry: Mapped[Optional[str]] = mapped_column(
        String(255), doc="Industry sector of the company"
    )
    compatibility: Mapped[Optional[str]] = mapped_column(
        String(50),
        doc="Compatibility rate with the prospect (e.g., '95% compatibility')",
    )
    source: Mapped[Optional[str]] = mapped_column(
        String(255), doc="Source of the information (e.g., 'LinkedIn Sales Navigator')"
    )
    location: Mapped[Optional[str]] = mapped_column(
        String(255), doc="Location of the company"
    )
    size: Mapped[Optional[str]] = mapped_column(
        String(100), doc="Company size (e.g., '50-200 employees')"
    )
    revenue: Mapped[Optional[str]] = mapped_column(
        String(100), doc="Company revenue (e.g., '5-10M€')"
    )
    website: Mapped[Optional[str]] = mapped_column(String(500), doc="Company website")
    description: Mapped[Optional[str]] = mapped_column(
        Text, doc="Description of the company ('About')"
    )
    opportunities: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String),
        doc="List of opportunities or keywords associated with the company",
    )

    def __repr__(self) -> str:
        """
        String representation of the Company object.

        Returns:
            str: A string representation showing id, name, and industry.
        """
        return (
            f"Company(id={self.id!r}, name={self.name!r}, industry={self.industry!r})"
        )


# Type alias for a list of companies
CompanyList = List[Company]
