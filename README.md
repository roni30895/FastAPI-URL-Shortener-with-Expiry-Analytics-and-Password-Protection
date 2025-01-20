# FastAPI URL Shortener with Expiry, Analytics, and Password Protection

## Introduction
This project is a Python-based URL Shortener application developed using the **FastAPI** framework. It provides functionalities to shorten URLs, set expiration times, track access analytics, and optionally secure access with a password.

### Features:
1. Generate shortened URLs.
2. Set an expiration time for the URLs (default is 24 hours).
3. Log analytics for each access (timestamp and IP address).
4. Optional password protection for accessing URLs.
5. Modular and extensible code design.

---
### Directory Structure:
```
├── app/
│   ├── __init__.py        # Package initializer
│   ├── database.py        # SQLite database setup and connection
│   ├── models.py          # Pydantic models for request and response validation
│   ├── routes/            # API route definitions
│   │   ├── shortner.py    # Handles URL shortening
│   │   ├── redirect.py    # Handles URL redirection
│   │   └── analytics.py   # Handles analytics data retrieval
│   ├── utils.py           # Utility functions (hashing, expiration checks, etc.)
|   ├── main.py            # FastAPI entry point
├── requirements.txt       # Project dependencies
├── README.md              # Documentation
├── URL_shortener.db       # SQLite database file
```
---

## Prerequisites

Ensure you have the following installed on your system:

1. **Python 3.8+**
2. **pip** (Python package manager)

---

## Project Setup

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### Step 2: Install Dependencies

Use the provided `requirements.txt` file to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

The main dependencies include:
- `fastapi`: Framework for building the API.
- `uvicorn`: ASGI server for running the FastAPI app.
- `pydantic`: For data validation and serialization.
- `sqlite3`: For database management.

### Step 3: Set Up the Database

The project uses SQLite as its database. On running the application, it will automatically create the required tables (`urls` and `analytics`) if they do not already exist.

To manually inspect or modify the database:
```bash
sqlite3 URL_shortener.db
```

---

## Running the Application

Start the FastAPI application using `uvicorn`:

```bash
uvicorn main:app --reload
```

The app will run on `http://127.0.0.1:8000` by default.

### API Endpoints

#### 1. **Shorten URL**
- **Endpoint**: `POST /shorten`
- **Description**: Generates a shortened URL for a given long URL with optional expiration and password.
- **Request Body**:
  ```json
  {
    "original_url": "https://example.com",
    "exp_hour": 24,
    "password": "optionalpassword"
  }
  ```
  - `original_url` (required): The long URL to shorten.
  - `exp_hour` (optional): Expiration time in hours (default is 24).
  - `password` (optional): Password to protect the URL.
- **Response**:
  ```json
  {
    "short_url": "https://short.ly/<shortened_code>"
  }
  ```

#### 2. **Redirect URL**
- **Endpoint**: `GET /<short_url>`
- **Description**: Redirects to the original URL if the shortened URL is valid and not expired.
- **Headers**:
  ```json
  {
    "password": "optionalpassword"
  }
  ```
- **Response**:
  - On Success:
    ```json
    {
      "redirect_to": "https://example.com"
    }
    ```
  - On Expired URL:
    ```json
    {
      "detail": "Short URL has expired."
    }
    ```
  - On Invalid Password:
    ```json
    {
      "detail": "Invalid Password."
    }
    ```

#### 3. **Analytics**
- **Endpoint**: `GET /analytics/{short_url}`
- **Description**: Retrieves the analytics data for a specific shortened URL.
- **Headers**:
  ```json
  {
    "password": "optionalpassword"
  }
  ```
- **Response**:
  ```json
  {
    "short_url": "<short_url>",
    "access_count": 5,
    "logs": [
      {"access_timestamp": "2025-01-20T10:00:00", "ip_address": "192.168.1.1"},
      {"access_timestamp": "2025-01-20T12:00:00", "ip_address": "192.168.1.2"}
    ]
  }
  ```

---

## Database Structure

1. **`urls` Table**:
   - Stores information about shortened URLs.
   - Columns:
     - `id`: Auto-incrementing primary key.
     - `original_url`: The original long URL.
     - `short_url`: The shortened URL.
     - `creation_timestamp`: Time when the URL was created.
     - `expiration_timestamp`: Time when the URL will expire.
     - `password_hash`: Optional hashed password for protection.

2. **`analytics` Table**:
   - Logs information about URL access.
   - Columns:
     - `id`: Auto-incrementing primary key.
     - `short_url`: The shortened URL accessed.
     - `access_timestamp`: Time of access.
     - `ip_address`: IP address of the client.

---

## Testing the Application

You can use Postman or any API client to test the application.

### Example Workflow:
1. **Shorten a URL**:
   - Use the `POST /shorten` endpoint.
2. **Access the Shortened URL**:
   - Use the `GET /<short_url>` endpoint.
   - Verify that it redirects to the original URL.
3. **Check Analytics**:
   - Use the `GET /analytics/{short_url}` endpoint to view the access logs and counts.

---

## Extending the Application

This application is designed with modularity in mind. Future enhancements can include:
- Adding user authentication and management.
- Providing a frontend interface.
- Integrating with third-party analytics tools.

---

## Troubleshooting

1. **Database Errors**:
   - Ensure the `URL_shortener.db` file exists and is accessible.
   - Check the table structures using an SQLite client.

2. **Dependency Issues**:
   - Run `pip install -r requirements.txt` again to ensure all packages are installed.

3. **Port Conflicts**:
   - If `8000` is already in use, run the app on a different port:
     ```bash
     uvicorn main:app --reload --port 8080
     ```

---

## Author
Developed by [Rohan Nanabhau Pawar].

