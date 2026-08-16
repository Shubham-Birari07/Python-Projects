# Django Tweet App

A simple full-stack social-media style web application built with **Python and Django**. Users can create, view, edit, and delete their own tweets, attach optional images, search tweets, and manage their accounts through Django authentication.

This project was originally built as a Django learning/college project and was later improved through an iterative AI-assisted development workflow using **OpenAI Codex**.

---

## 📌 Project Overview

The Django Tweet App provides a compact implementation of a tweet-style feed with authentication and image uploads.

The application currently supports:

- User registration and login/logout
- Public tweet feed
- Creating tweets
- Editing your own tweets
- Deleting your own tweets
- Optional tweet image uploads
- Case-insensitive tweet search
- Search query preservation
- Empty-feed and no-search-results states
- Owner-based authorization for tweet editing/deletion
- Responsive Bootstrap navigation
- Automated Django tests for core functionality
- Django admin integration

The project intentionally keeps a simple architecture so that the Django request → view → model → template flow remains easy to understand.

---

## ✨ Features

### 👤 Authentication

- User registration using Django's built-in authentication system
- Login and logout
- Password-related Django authentication views
- Authentication-protected tweet creation
- Authentication and ownership protection for editing and deleting tweets

### 📝 Tweet Management

Authenticated users can:

- Create tweets up to **280 characters**
- Optionally attach an image
- Edit their own tweets
- Delete their own tweets

Users cannot edit or delete tweets belonging to another user.

### 🔎 Tweet Search

The navbar includes a GET-based tweet search.

Search behavior:

- Searches tweet text
- Case-insensitive matching
- Uses whitespace trimming
- Keeps the search query in the input after submission
- Displays matching tweets using the existing feed
- Shows a no-results message when a non-empty search has no matches
- An empty search returns the normal feed

The search uses the existing `/tweet/` route rather than introducing a separate search page.

### 🖼️ Image Uploads

Tweets can optionally contain an uploaded image.

The feed safely handles both:

- Tweets with images
- Tweets without images

### 🧭 Navigation

The project includes:

- Home/root navigation
- Tweet feed navigation
- Authentication navigation
- Bootstrap-based navbar interactions
- Responsive navbar behavior

### 🧪 Automated Testing

The project includes Django tests covering important application behavior such as:

- Feed behavior
- Tweet creation
- Editing
- Deletion
- Ownership restrictions
- Search
- Empty/no-result behavior
- Tweets with and without photos
- Authentication-related access restrictions

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Backend programming language |
| **Django** | Web framework |
| **SQLite** | Development database |
| **HTML5** | Page structure |
| **CSS3** | Styling |
| **Bootstrap** | UI and responsive layout |
| **Django ORM** | Database interaction |
| **Django Authentication** | User accounts and authentication |
| **OpenAI Codex** | AI-assisted development and code review |

---

## 🏗️ Project Architecture

The project uses a simple Django architecture:

```text
Browser
   │
   ▼
Django Project URLconf
   │
   ▼
Tweet App URLconf / Django Auth
   │
   ▼
Views
   │
   ├── Forms
   │
   └── Models / Django ORM
           │
           ▼
        SQLite
           │
           ▼
       Templates
           │
           ▼
        Browser
```

### Request Flow

For a typical tweet-related request:

```text
Browser
  → URL
  → Django View
  → Model / QuerySet
  → Template
  → Browser
```

For search:

```text
Search Form
  → GET ?q=...
  → /tweet/
  → tweet_list()
  → Tweet.objects.filter(text__icontains=q)
  → tweet_list.html
```

---

## 📁 Project Structure

The main project structure is:

```text
chaicenter/
│
├── manage.py
│
├── chaicenter/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tweet/
│   ├── migrations/
│   │   └── 0001_initial.py
│   │
│   ├── templates/
│   │   ├── index.html
│   │   └── tweet/
│   │       ├── tweet_list.html
│   │       ├── tweet_form.html
│   │       └── tweet_confirm_delete.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── layouts.html
│   └── registration/
│       ├── login.html
│       ├── register.html
│       └── logged_out.html
│
├── media/
│   └── tweets/
│       └── photos/
│
├── static/
│
└── requirements.txt
```

> The exact files in your working tree may vary slightly as the project evolves. The structure above reflects the application's Django organization used during the current development milestone.

---

## 🗄️ Data Model

The application currently uses one custom model: `Tweet`.

### Tweet

| Field | Type | Description |
|---|---|---|
| `user` | ForeignKey | User who owns the tweet |
| `text` | TextField | Tweet content, limited to 280 characters |
| `photo` | ImageField | Optional uploaded image |
| `created_at` | DateTimeField | Automatically records creation time |
| `updated_at` | DateTimeField | Automatically records last update time |

### Relationship

```text
User
  │
  └─── 1 ──────── * ─── Tweet
```

One user can own multiple tweets, while each tweet belongs to one user.

Deleting a user cascades to their tweet records through the model relationship.

---

## 🔐 Security & Access Control

The project uses Django's built-in authentication and standard web security mechanisms.

Implemented protections include:

- CSRF-protected POST forms
- Login-required tweet creation
- Login-required tweet editing
- Login-required tweet deletion
- Owner-only edit access
- Owner-only delete access
- Django's built-in password hashing
- Django's standard authentication views

Ownership checks are performed at the queryset level so a logged-in user cannot simply change a URL ID to modify another user's tweet.

---

## 🔗 Main Routes

| Route | Purpose | Access |
|---|---|---|
| `/` | Home/root page | Public |
| `/tweet/` | Tweet feed and search | Public |
| `/tweet/create/` | Create tweet | Authenticated |
| `/tweet/<id>/edit/` | Edit own tweet | Owner only |
| `/tweet/<id>/delete/` | Delete own tweet | Owner only |
| `/tweet/register/` | Register account | Public |
| `/accounts/login/` | Login | Public |
| `/accounts/logout/` | Logout | Authenticated |
| `/accounts/password_*` | Django password management | Based on view |

> The application also exposes `/admin/` through Django's administration interface.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin account

```bash
python manage.py createsuperuser
```

Follow the prompts.

### 6. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 🧪 Running Tests

Run Django's complete test suite:

```bash
python -B manage.py test --verbosity 2
```

Run Django system checks:

```bash
python -B manage.py check
```

Check that no new migrations are required:

```bash
python -B manage.py makemigrations --check --dry-run
```

These checks were used during the iterative improvement process to verify that changes did not break the existing application.

---

## 🔍 Example Search Behavior

A normal feed request:

```text
/tweet/
```

A search request:

```text
/tweet/?q=django
```

The search uses Django ORM case-insensitive matching:

```python
Tweet.objects.filter(text__icontains=q)
```

This keeps the implementation simple while reusing the existing tweet feed.

---

## 🧠 Development Approach

Rather than rewriting the application, the project was improved incrementally.

The development process followed this pattern:

```text
Analyze
   ↓
Identify one issue
   ↓
Implement a focused fix
   ↓
Run Django checks/tests
   ↓
Manually verify the application
   ↓
Review the result
   ↓
Move to the next improvement
```

This approach helped preserve the existing architecture while reducing the risk of introducing regressions.

---

## 🤖 AI-Assisted Development

This project was improved using **OpenAI Codex** as an AI coding assistant.

Codex was used to:

- Analyze and understand the existing Django codebase
- Trace application functionality and request flow
- Identify bugs and small improvement opportunities
- Implement the tweet search functionality
- Fix optional image rendering behavior
- Add focused automated tests
- Improve root/home navigation
- Enable Bootstrap navbar interactions
- Make small HTML/UI improvements
- Perform safe code-quality cleanup

The AI-generated changes were **reviewed, tested, and manually verified** before being retained in the project.

AI was used as a development assistant rather than as a replacement for understanding the application. The development process remained iterative, with each change intentionally scoped and validated before moving to the next improvement.

---

## 📚 What I Learned

Through this project, I practiced:

- Django project and app structure
- URL routing
- Function-based views
- Django models and relationships
- Django ORM queries
- ModelForms
- User authentication
- Authorization and ownership checks
- File/image uploads
- Templates and template inheritance
- Bootstrap integration
- GET-based search
- Django testing
- Debugging existing applications
- Incremental code improvement
- Git and GitHub-based version control
- AI-assisted software development workflows

---

## 🔮 Possible Future Improvements

The current version is intentionally kept simple. Possible future enhancements include:

- Pagination for larger tweet feeds
- More optimized database queries
- Tweet timestamps in the feed
- Better image handling and validation
- Improved profile/user pages
- Tweet likes or favorites
- Comments/replies
- User search
- Hashtag support
- More advanced filtering
- Production-ready environment configuration
- Deployment to a cloud platform
- More extensive automated test coverage

These are intentionally future enhancements rather than requirements for the current milestone.

---

## ⚠️ Development vs Production

This repository is primarily a learning/development project.

Before deploying publicly, production hardening would be required, including:

- Proper secret management
- `DEBUG=False`
- Appropriate `ALLOWED_HOSTS`
- Production-grade database configuration
- Production static/media handling
- Secure deployment configuration
- HTTPS
- Proper logging and monitoring
- Dependency/version management

Do not use development settings as-is for a production deployment.

---

## 📄 License

Add your preferred license here.

Example:

```text
MIT License
```

If this project is for a college assignment or portfolio, you can also replace this section with the licensing terms you choose.

---

## 👨‍💻 Author

**Shubham Birari**

GitHub: `https://github.com/<your-username>`

LinkedIn: `https://www.linkedin.com/in/<your-profile>/`

---

## ⭐ Acknowledgment

Built as a Django learning and portfolio project, with iterative improvements and AI-assisted development using OpenAI Codex.
