
# Friendsbook Metro - Django API

A Django-based API for user profiles, preferences, and authentication.

## 🚀 Features

- JWT Authentication (Login, Logout, Token Refresh)
- User Profile Management (CRUD Operations)
- User Preferences (Height, Age, Weight, Education, Location)
- CORS Support (For Frontend Integration)
- Swagger API Documentation

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-repo/friendsbook-metro.git
cd friendsbook-metro
```

### 2️⃣ Create & Activate Virtual Environment

- For macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

- For Windows (PowerShell):

```bash
python -m venv env
env\Scriptsctivate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory and add:

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=postgres://username:password@localhost:5432/db_name
```

### 5️⃣ Apply Migrations & Create Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6️⃣ Run the Development Server

```bash
python manage.py runserver
```

Access API: `http://127.0.0.1:8000/`

## 🔐 Authentication (JWT)

### Obtain JWT Token

- **POST** `/api/token/`

Request:

```json
{
    "username": "admin",
    "password": "adminpassword"
}
```

Response:

```json
{
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}
```

### Refresh Token

- **POST** `/api/token/refresh/`

Request:

```json
{
    "refresh": "your_refresh_token"
}
```

## 📜 API Endpoints (JSON Format)

### User Profile Endpoints

| Method | Endpoint               | Description                |
|--------|------------------------|----------------------------|
| GET    | `/api/profiles/`        | List all user profiles     |
| POST   | `/api/profiles/`        | Create a new profile       |
| GET    | `/api/profiles/{id}/`   | Retrieve a profile         |
| PUT    | `/api/profiles/{id}/`   | Update a profile           |
| DELETE | `/api/profiles/{id}/`   | Delete a profile           |

### Example: Create Profile

- **POST** `/api/profiles/`
- Authorization: Bearer `your_access_token`

Request:

```json
{
    "name": "John Doe",
    "gender": "Male",
    "email": "john@example.com",
    "date_of_birth": "1990-01-01",
    "height": 175,
    "weight": 70,
    "education": "Bachelor's",
    "country": "USA",
    "address": "123 Street, NY",
    "phone_number": "+123456789",
    "language": "English",
    "religion": "Christianity"
}
```

Response:

```json
{
    "id": 1,
    "name": "John Doe",
    "gender": "Male",
    "email": "john@example.com",
    "date_of_birth": "1990-01-01",
    "height": 175,
    "weight": 70,
    "education": "Bachelor's",
    "country": "USA",
    "address": "123 Street, NY",
    "phone_number": "+123456789",
    "language": "English",
    "religion": "Christianity"
}
```

## 🛠️ Development & Debugging

### Run Tests

```bash
python manage.py test
```

### Check for Issues

```bash
python manage.py check
```

### Format Code (Black & Flake8)

```bash
black .
flake8 .
```

## 📄 API Documentation (Swagger & ReDoc)

### Install Swagger

```bash
pip install drf-yasg
```

### Access API Docs

| Type        | URL                                    |
|-------------|----------------------------------------|
| Swagger UI  | `http://127.0.0.1:8000/swagger/`       |
| ReDoc       | `http://127.0.0.1:8000/redoc/`         |

## ⚠️ Troubleshooting

- **Error: Application Labels Aren't Unique (corsheaders)**

  Open `settings.py` and remove the duplicate `corsheaders` entry from `INSTALLED_APPS`.

- **Error: Database Not Found**

  Ensure PostgreSQL is running and credentials in `.env` are correct.

- **Error: Migrations Not Applied**

  Run:

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

## 📝 License

This project is licensed under the MIT License.
