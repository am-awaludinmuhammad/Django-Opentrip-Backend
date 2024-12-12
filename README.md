# Open Trip API

This is a public API built using **Django** and **Django Rest Framework (DRF)**, designed for managing and accessing trip data. The project supports account management, trip listings, orders, review, and payments. The API is secured with **JWT** authentication and supports detailed filtering and pagination of trip data.

## Features
- **User authentication**: Token-based authentication using **SimpleJWT**.
- **Trip Management**: View, create, update, and delete trips.
- **Order & Payment**: Manage orders and payments with a one-to-one relationship.
- **Bank Information**: Includes bank details using short names for Indonesian banks.
- **Public Trip Access**: Some trip data is publicly accessible without authentication.
- **Custom API Responses**: API responses are wrapped inside a `data` object for consistency.
- **Pagination Support**: Paginated responses for list views, with data inside a `result` object.

## Project Structure
├── account/  
├── trip/  
├── order/  
├── general/  
└── project/  

## Requirements
- All required dependencies for this project are listed in requirements.txt

## Setup Instructions
**1. Clone the repository:**
```bash
git clone https://github.com/am-awaludinmuhammad/Django-Opentrip-Backend
```

**2. Clone the repository:**
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables:** 
- You can copy .env.example file into .env
```bash
cp .env.example .env # On windows copy .env.example .env
```
-  Or manualy create a .env file in the root of your project and add the necessary variables:

```makefile
SECRET_KEY=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

APP_DEBUG="False"
DJANGO_LOG_LEVEL="DEBUG"

# in minutes
ACCESS_TOKEN_LIFETIME=
# in days
REFRESH_TOKEN_LIFETIME=1

EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USE_TLS="True"
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_TIMEOUT=10

FRONTEND_URL="http://localhost:3000"
```

**5. Database migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Create a superuser:** There are some endpoints that required superuser role
```bash
python manage.py createsuperuser
```


**7. Run the development server:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**7. Seed provinces, regencies, and districts data:**
```bash
python manage.py seed_locations
```

## API Documentation
The API documentation is available at /api/schema/swagger-ui/ or /api/schema/redoc/

## Testing
**To run tests:**
```bash
python manage.py test
```

## Contributing
Contributions are welcome! Feel free to open issues or pull requests.

