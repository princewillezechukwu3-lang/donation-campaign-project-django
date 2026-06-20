# Donation Campaign Backend API (Django Edition)

A robust Crowdfunding API built using Python, Django, and Django REST Framework (DRF), backed by a PostgreSQL database instance.

---

## 🛠️ System Architecture

This version utilizes Django's built-in Object-Relational Mapper (ORM) to handle schema migrations and dynamic runtime database aggregations using Django's highly optimized `.annotate()` aggregation engine.

---

## 🚀 Getting Started

### 1. Installation
Clone this repository to your local architecture, then install the required core packages via the Python package manager manifest:
```bash
pip install -r requirements.txt
```
### 2. Environmental Configuration

Create a `.env` file in the root directory of the project and populate it with your local PostgreSQL environment variables:

```env
DEBUG=True
SECRET_KEY=your-django-secret-key-here
DB_NAME=donation_campaign
DB_USER=postgres
DB_PASSWORD=Prince5045#
DB_HOST=localhost
DB_PORT=5432

```

### 3. Database Initialization

Ensure your local PostgreSQL service is running with the database specified above. Execute the following automated migration routines to build the data structures seamlessly:

```bash
python manage.py migrate

```

### 4. Execution

To launch the Django development web service engine locally:

```bash
python manage.py runserver

```

The endpoint ecosystem will become accessible instantly at `http://127.0.0.1:8000/api/`

---

## 🗺️ API Endpoints Index

### 📋 Campaigns Segment

#### 🔹 Create a Campaign

* **Endpoint:** `POST /api/campaigns/`
* **Payload Requirements (JSON):**
```json
{
  "title": "Clean Water Initiative",
  "description": "Building sustainable solar-powered water wells.",
  "goal_amount": "75000.00",
  "minimum_donation": "500.00",
  "end_date": "2026-12-31T00:00:00Z"
}

```



#### 🔹 Get All Campaigns

* **Endpoint:** `GET /api/campaigns/`
* **Success Response (200 OK):** An array containing all active campaign objects along with their dynamic runtime stats (`total_raised` and `donor_count`).

---

### 💳 Donations Segment

#### 🔹 Submit a Donation

* **Endpoint:** `POST /api/donations/`
* **Payload Requirements (JSON):**
```json
{
  "campaign": 1,
  "amount": "2500.00",
  "donor_name": "Jane Doe",
  "donor_email": "jane@example.com"
}

```



```
