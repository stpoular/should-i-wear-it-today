# API

## Overview

* A RESTful API built using **FastAPI** that enables users to manage their accounts, add and update items, and submit comments on those items. The backend utilizes **Google Firestore** as the database, and **JWT tokens** are used for secure authentication. This system supports full CRUD (Create, Read, Update, Delete) operations for users, items, and submissions.

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

- **FastAPI**: Web framework for building the API.
- **Pydantic**: Data validation with Pydantic models.
- **Google Firestore**: NoSQL cloud database for user, item, and submission data storage.
- **JWT (JSON Web Tokens)**: Secure user authentication and token management.
- **Passlib**: Password hashing and verification.

---
# **API Documentation**

## **1. User Authentication**

### **Endpoints**
| Method | Endpoint        | Description                                       |
|--------|-----------------|---------------------------------------------------|
| `POST` | `/users/`        | Register a new user with email and password.      |
| `POST` | `/tokens/`       | Obtain authentication token (login).              |
| `GET`  | `/users/me/`     | Get current authenticated user information.       |
| `PUT`  | `/users/me/`     | Update user profile information (e.g., email, password). |
| `DELETE` | `/users/me/`   | Delete the current user's account.                |

### **Authentication**
- Uses **JWT** (JSON Web Token) for authentication.
- Protects endpoints requiring authentication by verifying the token in the `Authorization` header.

---

## **2. Item Management**

### **Endpoints**
| Method | Endpoint                       | Description                                       |
|--------|---------------------------------|---------------------------------------------------|
| `POST` | `/items/`              | Register a new item.                              |
| `GET`  | `/items/`              | View all registered items.                        |
| `GET`  | `/items/{item_id}/`     | Retrieve a specific item by ID.                   |
| `PUT`  | `/items/{item_id}/`    | Update an item’s details.                         |
| `DELETE` | `/items/{item_id}/`  | Delete an item.                                   |

### **Item Attributes**
- `name`: Name of the item (e.g., "Jacket", "Sweater").
- `color`: Color of the item (e.g., "Blue", "Red").

#### **Example Request (POST /items/)**
```json
{
  "name": "Jacket",
  "color": "Blue"
}
```

---

## **3. Submission Management**

### **Endpoints**
| Method | Endpoint                       | Description                                        |
|--------|---------------------------------|----------------------------------------------------|
| `POST` | `/submissions/`                 | Add a new submission (comment) for an item.        |
| `GET`  | `/submissions/`                 | Retrieve all submissions for the current user.     |
| `GET`  | `/submissions/{submission_id}/` | Retrieve a specific submission by ID.              |
| `GET`  | `/submissions/?item_id={item_id}` | Retrieve all submissions for a specific item.     |
| `PUT`  | `/submissions/{submission_id}/` | Update a submission (comment).                     |
| `DELETE` | `/submissions/{submission_id}/` | Delete a submission (comment).                     |

### **Submission Attributes**
- `item_id`: The ID of the item being commented on.
- `comment`: The content of the user's submission.
- `city`: The city where the item is used.
- `country`: The country where the item is used.
- `rating`: A numerical rating (0-100) given to the item.

#### **Example Request (POST /submissions/)**
```json
{
  "item_id": "abc123",
  "comment": "This jacket is very comfortable!",
  "city": "New York",
  "country": "USA",
  "rating": 90
}
```



## Installation

1. Set up **Google Cloud Firestore** and authenticate using a service account key.

2. Run the FastAPI app:
   ```bash
   uvicorn app.main:app --reload
   ```

3. The API will be accessible at `http://127.0.0.1:8000`.
