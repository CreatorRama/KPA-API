from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query,status
from typing import Optional, AsyncIterator
from datetime import date
from app import schemas, crud, models, database
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    
    models.Base.metadata.create_all(bind=database.engine)
    yield
    
    print("Shutting down...")
    database.engine.dispose()
    

app = FastAPI(
    title="Wheel Specifications API",
    description="API for managing railway wheel specification forms",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@railops.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan
)

# CORS configuration (unchanged)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    "/api/forms/wheel-specifications",
    response_model=schemas.PostWheelSpecificationsResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Wheel Specifications"],
    summary="Create a new wheel specification form",
    responses={
        201: {"description": "Successfully created wheel specification"},
        400: {"description": "Invalid input data"},
        409: {"description": "Form number already exists"}
    }
)

def create_wheel_specification(
    specification:schemas.WheelSpecificationCreate,
    db:Session=Depends(get_db)
):
    """
    Create a new Wheel specification form with all required measurements and tolerances.
    
    - **formNumber**: Must start with 'WHEEL-' (e.g. WHEEL-2025-001)
    - **submittedBy**: Name of the person submitting the form
    - **submittedDate**: Date of submission (cannot be in the future)
    - **fields**: Contains all wheel specification measurements and tolerances
    """
    
    try:
        existing=crud.get_wheel_specification(db,formNumber=specification.formNumber)
        if(existing):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Form number already exists"
            )
            db_specs=crud.create_wheel_specification(db, specification)
            
            response_data=schemas.WheelSpecificationResponse(
                formNumber=db_specs.form_number,
                submittedBy=db_specs.submitted_by,
                submittedDate=db_specs.submitted_date,
                status=db_specs.status
            )
            
            return {
                data: response_data,
                "message": "Wheel specification created successfully",
                "Success": True
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
    @app.get(
        "/api/forms/wheel-specifications",
        response_model=schemas.GetWheelSpecificationsResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["Wheel Specifications"],
        summary="Create a new wheel specification form",
        responses={
            201: {"description": "Successfully created wheel specification"},
            400: {"description": "Invalid input data"},
            409: {"description": "Form number already exists"}
        }
    )   
    
    def get_wheel_specification(formNumber: Optional[str] = Query(None, description="Filter by form number",example="WHEEL-2025-001"),
        submittedBy: Optional[str] = Query(None, description="Filter by submitted ID",example="user_id_123"),
        submittedDate: Optional[date] = Query(None, description="Filter by submitted date",example="2025-07-03"),
        db: Session = Depends(get_db)):
        
         specs=crud.get_wheel_specification(db,formNumber=formNumber,submittedBy=submittedBy,submittedDate=submittedDate)
         response_data=[schemas.MinimalWheelSpecificationResponse.from_orm(spec) for spec in specs]
         return{
             "data": response_data,
             "message": "Wheel specifications retrieved successfully",
             "success": True
         }