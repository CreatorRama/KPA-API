# Wheel Specifications API

A FastAPI-based REST API for managing railway wheel specification forms. This API provides endpoints to create and retrieve wheel specification data with comprehensive validation and database persistence.

## Features

- **RESTful API**: Built with FastAPI for high performance and automatic API documentation
- **Data Validation**: Comprehensive input validation using Pydantic models
- **Database Integration**: SQLAlchemy ORM with support for multiple database backends
- **CORS Support**: Cross-origin resource sharing enabled for frontend integration
- **Automatic Documentation**: Interactive API docs available at `/docs` and `/redoc`
- **Form Management**: Create and retrieve wheel specification forms with filtering capabilities

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI application and route definitions
├── schemas.py           # Pydantic models for request/response validation
├── crud.py              # Database operations (Create, Read, Update, Delete)
├── models.py            # SQLAlchemy database models
├── database.py          # Database configuration and connection
└── config.py            # Application settings and environment configuration
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CreatorRama/KPA-API
   cd KPA-API
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/<your_database_name>
   APP_ENV=development
   ```

## Configuration

The application uses environment-based configuration through the `Settings` class in `config.py`:

- **DATABASE_URL**: Database connection string (supports SQLite, PostgreSQL, MySQL)
- **APP_ENV**: Application environment (development/production)

## API Endpoints

### POST `/api/forms/wheel-specifications`

Create a new wheel specification form.

**Request Body:**
```json
{
  "formNumber": "WHEEL-2025-001",
  "submittedBy": "John Doe",
  "submittedDate": "2025-01-15",
  "fields": {
    "treadDiameterNew": "915±2mm",
    "lastShopIssueSize": "905±1mm",
    "condemningDia": "850mm",
    "wheelGauge": "1435±3mm",
    "variationSameAxle": "±0.5mm",
    "variationSameBogie": "±1.0mm",
    "variationSameCoach": "±2.0mm",
    "wheelProfile": "UIC-ORE S1002",
    "intermediateWWP": "P8",
    "bearingSeatDiameter": "130±0.025mm",
    "rollerBearingOuterDia": "240±0.01mm",
    "rollerBearingBoreDia": "130±0.01mm",
    "rollerBearingWidth": "50±0.5mm",
    "axleBoxHousingBoreDia": "242±0.1mm",
    "wheelDiscWidth": "135±2mm"
  }
}
```

**Response:**
```json
{
  "data": {
    "formNumber": "WHEEL-2025-001",
    "submittedBy": "John Doe",
    "submittedDate": "2025-01-15",
    "status": "SAVED"
  },
  "message": "Wheel specification created successfully",
  "success": true
}
```

### GET `/api/forms/wheel-specifications`

Retrieve wheel specification forms with optional filtering.

**Query Parameters:**
- `formNumber` (optional): Filter by form number
- `submittedBy` (optional): Filter by submitter name
- `submittedDate` (optional): Filter by submission date

**Response:**
```json
{
  "data": [
    {
      "formNumber": "WHEEL-2025-001",
      "submittedBy": "John Doe",
      "submittedDate": "2025-01-15",
      "fields": {
        "treadDiameterNew": "915±2mm",
        "lastShopIssueSize": "905±1mm",
        "condemningDia": "850mm",
        "wheelGauge": "1435±3mm"
      },
      "status": "SAVED"
    }
  ],
  "message": "Wheel specifications retrieved successfully",
  "success": true
}
```

## Data Models

### WheelSpecificationFields

Contains all the technical specifications for railway wheels:

- **Dimensional Measurements**: Tread diameter, condemning diameter, wheel gauge
- **Tolerances**: Variations for same axle, bogie, and coach
- **Bearing Specifications**: Seat diameter, outer/bore diameters, width
- **Profile Information**: Wheel profile and wear patterns

### Validation Rules

- **Form Number**: Must start with 'WHEEL-' followed by numeric identifiers
- **Submission Date**: Cannot be in the future
- **Required Fields**: All specification fields are mandatory
- **Uniqueness**: Form numbers must be unique across the system

## Running the Application

1. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API documentation**
   - Interactive docs: http://localhost:8000/docs
   - ReDoc documentation: http://localhost:8000/redoc

3. **Health check**
   ```bash
   curl http://localhost:8000/api/forms/wheel-specifications
   ```

## Database Operations

The application uses SQLAlchemy ORM with the following key operations:

- **create_wheel_specification**: Creates new wheel specification records
- **get_wheel_specification**: Retrieves specifications with optional filtering
- **Automatic table creation**: Database tables are created on application startup
- **Connection management**: Proper database connection lifecycle management

## Error Handling

The API provides comprehensive error responses:

- **400 Bad Request**: Invalid input data or validation errors
- **409 Conflict**: Duplicate form numbers
- **500 Internal Server Error**: Server-side errors

## Development

### Adding New Fields

1. Update `WheelSpecificationFields` in `schemas.py`
2. Modify the database model in `models.py`
3. Update CRUD operations in `crud.py` if needed
4. Run database migrations

### Testing

```bash
# Install testing dependencies
pip install pytest httpx

# Run tests
pytest
```

## Production Deployment

1. **Set production environment variables**
   ```env
   DATABASE_URL=postgresql://user:password@localhost/wheel_specs
   APP_ENV=production
   ```

2. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For API support, contact: support@railops.com