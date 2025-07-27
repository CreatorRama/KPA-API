from sqlalchemy.orm import Session
from app import models,schemas

from datetime import date
from typing import Optional

def create_wheel_specification(db: Session, wheel_spec: schemas.WheelSpecificationResponse):
    existing=db.query(models.WheelSpecification).filter(
        models.WheelSpecification.form_number == wheel_spec.formNumber).first()
    if existing:
        raise ValueError("form number already exists")
    
    db_spec = models.WheelSpecification(
        id=wheel_spec.formNumber,
        form_number=wheel_spec.formNumber,
        submitted_by=wheel_spec.submittedBy,
        submitted_date=wheel_spec.submittedDate,
        status=models.StatusEnum.SAVED.value
    )
    
    db.add(db_spec)
    db.commit()
    db.refresh(db_spec)
    return db_spec

def get_wheel_specification(db:Session,formNumber:Optional[str]=None,
    submittedBy:Optional[str]=None,
    submittedDate:Optional[date]=None):
    query = db.query(models.WheelSpecification)
    
    if formNumber:
        query = query.filter(models.WheelSpecification.form_number == formNumber)
    if submittedBy:
        query = query.filter(models.WheelSpecification.submitted_by == submittedBy)
    if submittedDate:
        query = query.filter(models.WheelSpecification.submitted_date == submittedDate)
    
    return query.all()