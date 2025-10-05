# ☕ Cafe API Manager

A RESTful Flask API for managing a collection of cafés with details such as location, amenities, and coffee prices. The project uses **Flask**, **SQLAlchemy**, and **SQLite** for a lightweight and easy-to-deploy backend.

---

## 🚀 Features

- Get a **random café**
- Retrieve a **list of all cafés**
- **Search cafés** by location
- **Add a new café**
- **Update** the coffee price for a café
- **Delete** a café (requires API key)

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **Flask**
- **SQLAlchemy**
- **dotenv**
- **SQLite**

---

##### Create .env file with API_KEY variable: API_KEY='TopSecretAPIKey'

---

| Method | Endpoint                                     | Description                            |
| ------ | -------------------------------------------- | -------------------------------------- |
| GET    | `/random`                                    | Returns a random café                  |
| GET    | `/all_cafes`                                 | Returns all cafés                      |
| GET    | `/search?loc=<location>`                     | Search cafés by location               |
| POST   | `/add`                                       | Add a new café (via form data)         |
| PATCH  | `/update-price/<cafe_id>?new_price=<price>`  | Update coffee price                    |
| DELETE | `/report-closed/<cafe_id>?api_key=<API_KEY>` | Delete a café (requires valid API key) |




