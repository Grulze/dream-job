# Dream job

## Getting Started

### Prerequisites
Make sure you have the following installed on your local machine:
- [Docker](https://www.docker.com/)

### Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-repo-url.git
   cd your-repo
   ```

2. **Build Docker containers**:
   Run the following command to build the Docker containers for the app, PostgreSQL, and Redis.
   ```sh
   docker compose build
   ```

3. **Start the services**:
   Bring up the application and the associated services (PostgreSQL and Redis) using Docker Compose.
   ```sh
   docker compose up
   ```

   The application will now be accessible at `http://127.0.0.1:8000`.

4. **Access API documentation**:
   FastAPI provides interactive API documentation, which can be accessed at:
   - **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Stopping the services
To stop the application and services, press `Ctrl+C` in the terminal where Docker is running, or run:
```sh
docker compose down
```