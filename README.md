# Fragrance Collection API

## Project Overview

This project is a backend API designed to recommend fragrances from a user’s personal collection based on contextual inputs such as season, occasion, time of day, weather, and location type.

Instead of recommending arbitrary products, the system focuses on helping users decide **what to wear next from what they already own**. The recommendation engine evaluates each fragrance in the user’s collection using a weighted scoring system that considers contextual matches, personal rating, and usage frequency.

The API is built with a structured backend architecture, including authentication, relational data modeling, and a service-based recommendation engine.

## Core Features

- User authentication with JWT-based login
- Personal fragrance collection management (CRUD)
- Context-aware recommendation engine
- Weighted scoring system with:
  - context matching (season, occasion, weather, time of day...)
  - personal rating influence
  - usage penalty (times worn)
- Top 3 recommendations per request
- Explanation for each recommendation
- Filtering and pagination for collection endpoints
- Consistent API response structure using data envelopes
- Integration test coverage for:
  - authentication
  - collection ownership
  - collection lifecycle
  - recommendation logic

## Architecture Overview

The backend follows a layered architecture to separate concerns and maintain scalability:

- **Routes (`api/routes`)**
  - Handle HTTP requests and responses
  - Perform request validation and dependency injection

- **Schemas (`schemas`)**
  - Define request and response contracts using Pydantic
  - Enforce validation and response consistency

- **Models (`models`)**
  - Represent database tables using SQLAlchemy
  - Define relationships and constraints

- **Services (`services`)**
  - Contain business logic (e.g., recommendation scoring engine)
  - Keep route handlers thin and focused

- **Core (`core`)**
  - Configuration and security (JWT, hashing, settings)

- **Database (`db`)**
  - Session management and base model setup

This separation ensures that business logic, data access, and API concerns remain decoupled and maintainable.
