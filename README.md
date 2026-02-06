# Flight API ✈

A comprehensive flight management system developed using Django REST Framework, enabling efficient management of airports, aircraft and their types, crew, routes, flights, and the entire ticket booking workflow.

## 📃 Features
- **Flight Management** – Manage airports, aircraft and their types, crew members, routes, and flights.
- **Reservation System** – Seat selection for specific flights with real-time availability validation across different aircraft types.
- **JWT Authentication** – Secure user registration and authentication using JSON Web Tokens.
- **API Documentation** – Automatically generated and interactive API documentation via Swagger and ReDoc.
- **Containerization** – Full support for Docker and Docker Compose for easy setup and deployment.

---

## 🛠️ Prerequisites

To run this project, you will need either:

- **Docker & Docker Compose** (recommended)  
  For an easy and consistent setup across environments.

**OR**

- **Python & PostgreSQL** (local installation)  
  If you prefer running the application natively.

---

## 🚀 Getting Started with DOCKER

This is the fastest method to get the project running with a pre-configured database in an isolated environment.

1.  **Clone the repository:**
    ```
    git clone https://github.com/Qbusik/flight-api.git
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the root directory:
    ```
    SECRET_KEY="your_private_secret_key"
    DEBUG=True
    POSTGRES_DB=database
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    DB_HOST=db
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
