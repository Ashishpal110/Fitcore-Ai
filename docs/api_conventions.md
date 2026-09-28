# FitCore — API Design Conventions

## 1. Base URL & Versioning
All application APIs are versioned under:
```text
/api/v1
```

## 2. Resource Naming Conventions
* Resource paths are lowercase and plural (e.g. `/api/v1/workouts`, `/api/v1/exercises`).
* Nested resources represent ownership hierarchy (e.g. `/api/v1/workouts/{workout_id}/exercises`).
* Actions that do not map naturally to CRUD use verbs (e.g. `/api/v1/workouts/{workout_id}/complete`).

## 3. Standard HTTP Methods & Status Codes
* `GET /resources`: Retrieve a list of resources (Status: `200 OK`)
* `GET /resources/{id}`: Retrieve a single resource by ID (Status: `200 OK` or `404 Not Found`)
* `POST /resources`: Create a new resource (Status: `201 Created`)
* `PUT /resources/{id}`: Full update / replace a resource (Status: `200 OK`)
* `PATCH /resources/{id}`: Partial update of a resource (Status: `200 OK`)
* `DELETE /resources/{id}`: Delete a resource (Status: `204 No Content` or `200 OK`)

## 4. Standard Error Response Schema
All error responses adhere to a uniform structure:
```json
{
  "error": {
    "code": "NotFoundException",
    "message": "Workout with identifier '123' was not found.",
    "details": {
      "resource": "Workout",
      "identifier": "123"
    }
  }
}
```

## 5. Security & Multi-Tenancy
* Every authenticated endpoint extracts the `current_user` from the validated JWT token.
* Route handlers must pass `current_user.id` to the service layer.
* The service layer enforces that resources can only be accessed or modified by their owner.
