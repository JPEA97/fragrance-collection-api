from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    CheckConstraint,
    Index,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Fragrance(Base):
    __tablename__ = "fragrances"

    __table_args__ = (
        UniqueConstraint("brand_id", "name", name="uq_fragrances_brand_id_name"),
        CheckConstraint(
            "release_year IS NULL OR release_year BETWEEN 1000 AND 2100",
            name="ck_fragrances_release_year_range",
        ),
        CheckConstraint(
            "gender_category IS NULL OR gender_category IN ('masculine', 'feminine', 'unisex')",
            name="ck_fragrances_gender_category_valid",
        ),
        Index("ix_fragrances_brand_id", "brand_id"),
        Index("ix_fragrances_name", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    release_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    gender_category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
