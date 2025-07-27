from datetime import date
from typing import Optional,List
from pydantic import BaseModel, Field,field_validator,ConfigDict

class WheelSpecificationFields(BaseModel):
    treadDiameterNew:str=Field(..., description="New Tread diameter with acceptable range")
    lastShopIssueSize:str=Field(..., description="Last shop issue size with acceptable range")
    condemningDia:str=Field(..., description="Condemning diameter with acceptable range")
    wheelGauge:str=Field(..., description="Wheel gauge with tolerance")
    variationSameAxle:str=Field(..., description="Variation on same axle")
    variationSameBogie:str=Field(..., description="Variation on same bogie")
    variationSameCoach:str=Field(..., description="Variation on same coach")
    variationSameAxle:str=Field(..., description="Variation on same axle")
    wheelProfile:str=Field(..., description="Wheel profile specification")
    intermediateWWP:str=Field(..., description="Intermediate wheel wear profile")
    bearingSeatDiameter: str = Field(..., description="Bearing seat diameter with tolerance")
    rollerBearingOuterDia:str=Field(..., description="Roller bearing outer diameter with tolerance")
    rollerBearingBoreDia:str=Field(..., description="Roller bearing bore diameter with tolerance")
    rollerBearingWidth:str=Field(..., description="Roller bearing width  with tolerance")
    axleBoxHousingBoreDia:str=Field(..., description="Axle box housing bore diameter with tolerance")
    wheelDiscWidth: str = Field(..., description="Wheel disc width with tolerance")
    
    
class WheelSpecificationCreate(BaseModel):
    formNumber: str = Field(..., min_length=5, max_length=50)
    submittedBy: str = Field(..., min_length=3, max_length=50)
    submittedDate: date
    fields: WheelSpecificationFields
    
    @field_validator('formNumber')
    @classmethod
    def validate_form_number(cls, v: str) -> str:
        v = v.strip().upper()
        if not v.startswith('WHEEL-'):
            raise ValueError('Form number must start with WHEEL-')
        if not v[6:].isdigit(): 
            raise ValueError('After WHEEL- must be numbers')
        return v
    
    @field_validator('submittedDate')
    @classmethod
    def validate_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('Submitted date cannot be in the future')
        return v

class WheelSpecificationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    formNumber: str = Field(..., alias="form_number")
    submittedBy: str = Field(..., alias="submitted_by")
    submittedDate: date = Field(..., alias="submitted_date")
    status: Optional[str] = None  

    
class PostWheelSpecificationsResponse(BaseModel):
    data: WheelSpecificationResponse
    message: str
    success: bool
    
class MinimalWheelSpecificationFields(BaseModel):
    treadDiameterNew: Optional[str] = None
    lastShopIssueSize: Optional[str] = None
    condemningDia: Optional[str] = None
    wheelGauge: Optional[str] = None

class MinimalWheelSpecificationResponse(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: date
    fields: MinimalWheelSpecificationFields
    status: Optional[str] = None

    @classmethod
    def from_orm(cls, db_spec):
        return cls(
            formNumber=db_spec.form_number,
            submittedBy=db_spec.submitted_by,
            submittedDate=db_spec.submitted_date,
            fields={
                "treadDiameterNew": db_spec.fields.get("treadDiameterNew", ""),
                "lastShopIssueSize": db_spec.fields.get("lastShopIssueSize", ""),
                "condemningDia": db_spec.fields.get("condemningDia", ""),
                "wheelGauge": db_spec.fields.get("wheelGauge", "")
            },
            status=db_spec.status
        )

class GetWheelSpecificationsResponse(BaseModel):
    data: List[MinimalWheelSpecificationResponse]
    message: str
    success: bool

class WheelSpecificationFilter(BaseModel):
    formNumber: Optional[str] = None
    submittedBy: Optional[str] = None
    submittedDate: Optional[date] = None
