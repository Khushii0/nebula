from sqlalchemy import Column, Integer, ForeignKey, Text
from app.core.database import Base

class DesignVersion(Base):
    __tablename__ = "design_versions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    ai_output = Column(Text)
    compliance_report = Column(Text)
