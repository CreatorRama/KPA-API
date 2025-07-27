from sqlalchemy import Column,String,Date,JSON
from enum import Enum
from app.database import Base

class StatusEnum(str, Enum):
    SAVED = "saved"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    
class WheelSpecifications(Base):
    __tablename__ = 'wheel_specifications'
    
    id = Column(String(20), primary_key=True)
    form_number= Column(String(20), index=True,unique=True)
    submitted_by = Column(String(20),index=True)
    submitted_date = Column(Date,index=True)
    fields= Column(JSON)
    status = Column(String(20), default=StatusEnum.SAVED)