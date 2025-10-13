# 💰 Personal Budget Tracker Application

**Frontend Deployed Link:**  
🔗 [https://business-frontend-ten.vercel.app/](https://business-frontend-ten.vercel.app/)

**Backend API Root:**  
🔗 [https://business-backend-chi.vercel.app/api](https://business-backend-chi.vercel.app/api)

---

## 🧾 Test Credentials

| Username | Password |
|-----------|-----------|
| test_user | test@12345 |

## Admin Credentials
🔗 [https://business-backend-chi.vercel.app/admin](https://business-backend-chi.vercel.app/admin)

| Username | Password |
|-----------|-----------|
| admin | admin@12345 |

---

## 🧾 Overview

The **Personal Budget Tracker** is a full-stack web application built using **React (Vite)** for the frontend and **Django REST Framework (DRF)** for the backend.  
It allows users to securely track their income, expenses, and monthly budgets — complete with **data visualization via D3.js**.

Users can:
- Log in securely (JWT / Token-based authentication)
- Add, edit, and delete transactions
- Categorize transactions ( salary, Groceries)
- Set a monthly budget and compare it with actual expenses
- View visual summaries using **D3.js Donut and Bar charts**

---

## ⚙️ Tech Stack

### Frontend
- **Framework:** React + Vite  
- **Styling:** Tailwind CSS  
- **Charts:** D3.js (Bar and Donut)  
- **State Management:** React Hooks  
- **API Communication:** Fetch API  

### Backend
- **Framework:** Django + Django REST Framework (DRF)
- **Authentication:** Token-based Auth (DRF Auth)
- **Database:** SQLite (development)
- **Deployment:** Vercel (backend + frontend)

---

## 🗂️ Folder Structure

### 🖥️ Backend (`backend/`)
```
backend/
│
├── budget_backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── finance/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── vercel.json
```

### 🌐 Frontend (`frontend/`)
```
frontend/
│
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── D3Bar.jsx
│   │   ├── D3Donut.jsx
│   │   ├── Pagination.jsx
│   │   └── TransactionForm.jsx
│   ├── pages/
│   │   ├── Budget.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Login.jsx
│   │   └── Transactions.jsx
│   ├── api.js
│   ├── auth.js
│   ├── App.jsx
│   ├── main.jsx
│   ├── styles.css
│   └── .env
│
├── vite.config.js
├── package.json
├── README.md
└── index.html
```

---

## 🧩 API Integration Code (`src/api.js`)

```javascript
const API_BASE = import.meta.env.VITE_API_BASE || 'https://business-backend-chi.vercel.app/api';

export async function login(username, password) {
  const res = await fetch(`${API_BASE}/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!res.ok) throw new Error('Login failed');
  return res.json(); // {token}
}

function authHeaders() {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Token ${token}` } : {};
}

export async function getSummary() {
  const r = await fetch(`${API_BASE}/summary/`, { headers: authHeaders() });
  return r.json();
}

export async function listCategories() {
  const r = await fetch(`${API_BASE}/categories/`, { headers: authHeaders() });
  return r.json();
}

export async function createCategory(data) {
  const r = await fetch(`${API_BASE}/categories/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(data)
  });
  return r.json();
}

export async function listTransactions(params = {}) {
  const qs = new URLSearchParams(params).toString();
  const r = await fetch(`${API_BASE}/transactions/${qs ? `?${qs}` : ''}`, { headers: authHeaders() });
  return r.json();
}

export async function createTransaction(data) {
  const r = await fetch(`${API_BASE}/transactions/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(data)
  });
  return r.json();
}

export async function updateTransaction(id, data) {
  const r = await fetch(`${API_BASE}/transactions/${id}/`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(data)
  });
  return r.json();
}

export async function deleteTransaction(id) {
  return fetch(`${API_BASE}/transactions/${id}/`, { method: 'DELETE', headers: authHeaders() });
}

export async function listBudgets() {
  const r = await fetch(`${API_BASE}/budgets/`, { headers: authHeaders() });
  return r.json();
}

export async function createBudget(data) {
  const r = await fetch(`${API_BASE}/budgets/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(data)
  });
  return r.json();
}

export async function currentBudget() {
  const r = await fetch(`${API_BASE}/budgets/current/`, { headers: authHeaders() });
  return r.json();
}
```

---

## 🔒 Authentication
- Implemented using **DRF Token Authentication**
- Tokens are stored in localStorage for secure session management
- Only authenticated users can:
  - Add, edit, or delete transactions
  - View budget and summaries

---

## 📊 D3.js Charts
- **Bar Chart (`D3Bar.jsx`)**: Visualizes income vs expenses over time.
- **Donut Chart (`D3Donut.jsx`)**: Displays expense distribution by category.

Both charts update dynamically based on user’s financial data.

---

## 🧠 Features Summary

| Feature | Description |
|----------|--------------|
| **User Login** | Token-based authentication (DRF) |
| **Dashboard** | D3.js charts summarizing income & expenses |
| **Transactions** | Add, edit, delete with filters and pagination |
| **Budgets** | Monthly budget setup & tracking |
| **Responsive Design** | Fully mobile and desktop friendly |

---

## 🧩 API Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/api/auth/login/` | POST | Obtain authentication token |
| `/api/transactions/` | GET, POST | List or create transactions |
| `/api/transactions/<id>/` | PUT, DELETE | Update or delete a transaction |
| `/api/categories/` | GET, POST | Manage income/expense categories |
| `/api/budgets/` | GET, POST | Manage monthly budgets |
| `/api/summary/` | GET | Get total income, expense, and balance summary |

---

## 🧮 Environment Variables (`.env`)
```
VITE_API_BASE=https://business-backend-chi.vercel.app/api
```

---

## 🚀 Deployment
- **Frontend:** Vercel (`business-frontend-ten.vercel.app`)
- **Backend:** Vercel (`business-backend-chi.vercel.app`)
- **Database:** SQLite (persistent for demo)

---

## 🧱 Installation Guide

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

App runs locally on `http://localhost:5173`

---

## 🧩 Assumptions
- Each user manages only their own financial data.
- Password reset & registration are out of scope (per instructions).
- SQLite database used for simplicity during deployment.

---

## 🧠 Attribution
Assistance was taken from **ChatGPT (OpenAI GPT-5)** for:
- Documentation formatting
- D3.js integration examples
- API fetch template structure

All business logic, testing, and deployment were manually implemented.

---

## ✅ Deliverables Summary

| Deliverable | Link |
|--------------|------|
| **Frontend** | [https://business-frontend-ten.vercel.app/](https://business-frontend-ten.vercel.app/) |
| **Backend API Root** | [https://business-backend-chi.vercel.app/api](https://business-backend-chi.vercel.app/api) |
| **Test Login** | `test_user / test@12345` |
| **Frontend Repo** | *(https://github.com/aman99951/business-frontend)* |
| **Backend Repo** | *(https://github.com/aman99951/business-backend)* |

---

**Author:** Aman Kumar  
**Email:** aman9995199@gmail.com  
**Date:** 13 October 2025  
**Confidential Technical Assessment Submission**
