# Flight API ✈

A comprehensive flight management system developed using Django REST Framework, enabling efficient management of airports, aircraft and their types, crew, routes, flights, and the entire ticket booking workflow.

## 📃 Features
- **Admin Panel** – located at /admin/
- **Flight Management** – Manage airports, aircraft and their types, crew members, routes, and flights
- **Reservation System** – Seat selection for specific flights with real-time availability validation
- **JWT Authentication** – Secure user registration and authentication using JSON Web Tokens
- **API Documentation** – Automatically generated and interactive API documentation via Swagger and ReDoc
- **Containerization** – Full support for Docker and Docker Compose for easy setup and deployment

---

## 🛠️ Prerequisites

To run this project, you will need either:

- **Docker & Docker Compose** (recommended)  
  For an easy and consistent setup across environments.

**OR**

- **Python & PostgreSQL** (local installation)  
  If you prefer running the application natively.

---

## 🚀 Run with DOCKER

This is the fastest method to get the project running with a pre-configured database in an isolated environment.

1.  **Clone the repository:**
    ```
    git clone https://github.com/Qbusik/flight-api.git
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the root directory:
    ```
    SECRET_KEY=<your secret key>
    POSTGRES_DB=<your database name>
    POSTGRES_USER=<your user name>
    POSTGRES_PASSWORD=<your password>
    DB_HOST=<your db name>
    DEBUG=True
    DB_PORT=5432
    ```

3.  **Build and Run Containers:**
    ```
    docker-compose up --build
    ```
    The application will be available at: `http://localhost:8000/`

4.  **Initialize Application:**
    Run these procedures to set up the database:
    ```
    # 1. Load sample data (fixtures)
    docker exec -it flight_app python manage.py loaddata sample_data.json

    # 2. Create an admin account
    docker exec -it flight_app python manage.py createsuperuser
    ```
---

## 📖 API Documentation

Once the server is running, the full API documentation is available here:
* **Swagger UI:** [http://localhost:8000/api/doc/swagger/](http://localhost:8000/api/doc/swagger/)
* **ReDoc:** [http://localhost:8000/api/doc/redoc/](http://localhost:8000/api/doc/redoc/)
