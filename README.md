# Donation Campaign Site (Django Edition)

A full Crowdfunding application built with Python, Django, and Django REST Framework (DRF), backed by a PostgreSQL database. It pairs a REST API backend with server-rendered frontend pages for browsing campaigns and making donations.

---

## 🛠️ System Architecture

This version utilizes Django's built-in Object-Relational Mapper (ORM) to handle schema migrations and dynamic runtime database aggregations using Django's highly optimized `.annotate()` aggregation engine.

The frontend is built with Django templates served from the same project. The list and detail pages render campaign data directly from the database, while the donate form submits to the `POST /api/donations/` endpoint via `fetch()` — keeping the backend as the single source of truth for all validation.

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

The site becomes accessible instantly at:

* **Frontend pages:** `http://127.0.0.1:8000/`
* **REST API:** `http://127.0.0.1:8000/api/`
* **Admin panel:** `http://127.0.0.1:8000/admin/`

> 💡 The campaign list is empty until you add campaigns. Create a superuser with
> `python manage.py createsuperuser`, then add a few campaigns in the admin panel.
> Set at least one campaign's `end_date` in the future (and `is_active` on) so its
> donate form is available.

---

## 🖥️ Frontend Pages

| Page | Route | Description |
| --- | --- | --- |
| **Campaign list** | `/` | Grid of campaign cards showing title, goal vs. raised, donor count, and a progress bar. |
| **Campaign detail** | `/campaigns/<id>/` | Single campaign view with description, goal/raised/donor stats, progress bar, and a "Donate now" button. |
| **Donate form** | `/campaigns/<id>/donate/` | Collects amount, full name, email, and payment method, then submits to the donations API. |

### ✅ Validation rules

* **Minimum donation:** amounts below the campaign's `minimum_donation` are rejected. The error returned by the API (e.g. *"Minimum donation amount for this campaign is ₦1000.00"*) is shown on the form.
* **Campaign active check:** if a campaign's `end_date` has passed or `is_active` is `False`, the donate form is hidden and a **"Campaign ended"** badge is shown with the donate button disabled.

---

## 🧪 Running Tests

The test suite covers both validation rules plus a successful donation and the campaign stats annotations:

```bash
python manage.py test crowdfund
```

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

* **Validation:** the amount must be a positive number, at least the campaign's `minimum_donation`, and the target campaign must be active and not past its `end_date`. Failing requests return a `400` with an `error` message.
