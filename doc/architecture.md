# Architecture

---

This is a description of the current architecture and design of the Ctrl-alt-budget web app.  
The application is currently a work in progress and documentation may be changed at a later date.

## Overview

---
The Ctrl-Alt-Budget application has the following capabilities:

- User Authentication
- Account Creation
- Recurring Transactions
- Transaction Input
- Transaction Categorization
- Goal Tracking
- Graph Creation

## Models

---
This sections handles part of our architecture handles user data and transports it to and from our database. 

Model ERD (Entity Relationship Diagram)

![Screenshot](../doc/images/ERD.png?raw=true "Entity_Relationship_Diagram")


## Routes
 
---
Each route file defines a Flask Blueprint. All route decorators currently use `@app.route` but will be changed in future iterations. 
 
| File | Blueprint | Routes |
|------|-----------|--------|
| `main.py` | `main_bp` | `GET /` → renders `homepage.html` |
| `auth.py` | `auth_bp` | `GET /login`, `GET /signup` → placeholder responses |
| `dashboard.py` | `dashboard_bp` | `GET /dashboard` → renders `dashboard.html` |
| `expenses.py` | `expenses_bp` | `GET /expenses`, `GET /api/transactions`, `POST /api/transactions` |
 
The `/api/transactions` endpoints currently use an **in-memory list** — data is lost on every server restart. Integration with the `Transaction` model and a real database is planned.

---

## Data Flow

---

```
Browser
  │
  ├── GET /               → homepage.html
  ├── GET /login          → login form (auth — not yet built)
  ├── GET /dashboard      → dashboard.html (loads mock data via JS)
  ├── GET /expenses       → expenses.html
  │
  ├── GET  /api/transactions   → returns transaction list as JSON
  └── POST /api/transactions   → adds a new transaction
              │
              └── Transaction model → Account balance update → Database (planned)
```




