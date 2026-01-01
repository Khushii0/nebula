from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sketch_data = Column(Text, nullable=True)  # JSON string from canvas
    design_concept_url = Column(String, nullable=True)
    design_narrative = Column(Text, nullable=True)
    compliance_notes = Column(Text, nullable=True)
    extra_data = Column(JSON, nullable=True)  # For additional data (renamed from metadata - reserved in SQLAlchemy)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
