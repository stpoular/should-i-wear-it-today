# should-i-wear-it-today

## Overview

**should-i-wear-it-today** is a weather-based clothing recommender app, offering personalised recommendations to users based on their historical data.

**Note: development is still in progress.**

## Features

- **User Authentication:**
  - Register new users with a unique username, email, and password.
  - Login and authenticate via JWT tokens.
  - View and update current user information.
  - Delete user accounts.
  
- **Item Management:**
  - Add new items with attributes such as name and color.
  - Retrieve all items belonging to the authenticated user.
  - Update or delete items.

- **Submission System:**
  - Add comments (submissions) related to items.
  - View, update, and delete submissions for the authenticated user.

## Tech stack
### Backend
- **FastAPI**: Web framework for building the API.
- **Pydantic**: Data validation with Pydantic models.
- **Google Firestore**: NoSQL cloud database for user, item, and submission data storage.
- **JWT (JSON Web Tokens)**: Secure user authentication and token management.
- **Passlib**: Password hashing and verification.

---
# **API Documentation**
See [API Documentation](backend/API.md)

---

## Installation

1. Clone this repository:
   ```bash
   git https://github.com/stpoular/should-i-wear-it-today
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up **Google Cloud Firestore** and authenticate using a service account key.

4. Run the backend app:
   ```bash
   uvicorn app.main:app --reload
   ```

5. The API will be accessible at `http://127.0.0.1:8000`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
