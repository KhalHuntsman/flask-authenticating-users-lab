# Cookies, Sessions, and Authentication API

## Overview

This project is a Flask-based backend API that demonstrates **session-based authentication** and **session-backed content access control**. It combines two core pieces of functionality:

1. **User authentication using sessions**
   - Users can log in, log out, and remain logged in across requests.
   - Authentication state is stored securely using Flask’s session system.

2. **Article access with a backend-enforced paywall**
   - Users may view up to **three articles per session**.
   - After the limit is exceeded, further access is blocked at the API level.

All stateful logic is enforced on the backend to prevent frontend or browser-based bypassing.

## File Structure

The project follows a standard Flask application layout.

server/app.py
server/models.py
server/seed.py
server/app.db
client/src/index.js
client/src/App.js
client/package.json
README.md

pgsql
Copy code

### Key Files

- `server/app.py`  
  Main Flask application. Defines API resources, session logic, authentication, and article routes.

- `server/models.py`  
  SQLAlchemy models and Marshmallow schemas for `User` and `Article`.

- `server/seed.py`  
  Seeds the database with initial users and articles.

- `server/app.db`  
  SQLite database used for development.

- `client/src/App.js`  
  React frontend that consumes the API (no changes required for this lab).

---

## Functionality

### Authentication

Authentication is handled using Flask sessions and RESTful resources.

- A user logs in by submitting a username.
- The user’s `id` is stored in `session['user_id']`.
- Subsequent requests use the session to determine login state.
- Logging out removes the session data.

### Session Persistence

- Session data persists across page refreshes.
- Each browser session is tracked independently.
- Clearing cookies or calling `/clear` resets the session.

### Article Paywall

- Article views are tracked using `session['page_views']`.
- The counter increments on every request to `/articles/<id>`.
- Users may view **up to three articles per session**.
- On the fourth request, the API returns a `401 Unauthorized` response.

## API Endpoints

### Authentication Routes

#### `POST /login`

Logs a user in using their username.

**Behavior**
- Retrieves the user by username
- Stores `user_id` in the session
- Returns the user as JSON

**Response**
- `200 OK` with user data
- `401 Unauthorized` if login fails

#### `DELETE /logout`

Logs the user out.

**Behavior**
- Removes `user_id` from the session

**Response**
- `204 No Content` (empty response body)

#### `GET /check_session`

Checks whether a user is currently logged in.

**Behavior**
- If `user_id` exists in the session, returns the user
- Otherwise returns unauthorized

**Response**
- `200 OK` with user data
- `401 Unauthorized` with empty JSON body

### Article Routes

#### `GET /articles`

Returns all articles.

#### `GET /articles/<int:id>`

Returns a single article if the page view limit has not been exceeded.

**Behavior**
- Initializes and increments `session['page_views']`
- Allows first three views
- Blocks subsequent views

**Blocked Response**
{
  "message": "Maximum pageview limit reached"
}

Status Code: 401 Unauthorized

Utility Routes
GET /clear
DELETE /clear

Clears all session data, including login state and page view count.

Intended for testing and development use.

### Features

- Session-based authentication
- Backend-enforced authorization checks
- Secure session cookie signing via app.secret_key
- Stateless frontend with API-driven auth state
- RESTful route design using Flask-RESTful
- SQLite-backed persistence for users and articles
- Test-driven development with Pytest

## How to Use
Setup:
- pipenv install && pipenv shell
- npm install --prefix client
- cd server
- flask db upgrade
- python seed.py

Run the Backend
- python app.py

Run the Frontend
- In a separate terminal: npm start --prefix client

## Testing
pytest

Reset Session

Navigate to:

http://localhost:5555/clear

## Notes

Authentication and paywall logic are intentionally enforced on the backend.

Session data is signed but readable by the client; sensitive data should not be stored directly.

This project demonstrates foundational session-based auth concepts that translate to larger systems.

## License

Educational use only. Intended for learning Flask sessions, authentication, and backend access control.