# GigHub API

A RESTful API built with **FastAPI** for managing freelance gigs in Nairobi. This project demonstrates CRUD operations, request validation using Pydantic, and API documentation using Swagger UI.

## Features

* View all gigs
* Search gigs by title
* Retrieve a gig by ID
* Create a new gig
* Update an existing gig
* Delete a gig
* Automatic API documentation with Swagger

## Technologies Used

* Python 3
* FastAPI
* Uvicorn
* Pydantic
* Docker

## Project Structure

```
cit-backend-course/
│── main.py
│── requirements.txt
│── Dockerfile
│── README.md
│── pyproject.toml
│── uv.lock
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/loise-maina304/cit-backend-course.git
```

2. Navigate into the project directory:

```bash
cd cit-backend-course
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

## API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

## Available Endpoints

| Method | Endpoint               | Description          |
| ------ | ---------------------- | -------------------- |
| GET    | /gigs                  | Retrieve all gigs    |
| GET    | /gigs/{gig_id}         | Retrieve a gig by ID |
| GET    | /gigs/search?q=keyword | Search gigs by title |
| POST   | /gigs                  | Create a new gig     |
| PUT    | /gigs/{gig_id}         | Update a gig         |
| DELETE | /gigs/{gig_id}         | Delete a gig         |

## Docker

Build the Docker image:

```bash
docker build -t backend-app:latest .
```

Run the Docker container:

```bash
docker run -d -p 8000:8000 --name backend-container backend-app:latest
```

## Author

**Loise Maina**

Backend Development Lab Assignment
