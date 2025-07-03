
# 📝 BlogiVerse – A Flask Blogging Platform

BlogiVerse is a secure, responsive, and feature-rich blogging platform built with **Flask**, **JWT**, and **Flask-Login**. It supports full blog CRUD operations, user authentication with role-based access (admin, publisher), password reset via email, search and filter functionality, and modern UI with Bootstrap.

---

## 🚀 Features

- 🔐 **User Authentication**: Login, Register, Forgot & Reset Password
- 👥 **Role Management**: `admin` and `publisher`
- 📝 **Post CRUD**: Create, Edit, View, Delete blogs
- 📌 **Search & Tag Filter**: Easily find relevant blogs
- 📈 **Blog Views Counter**
- 📬 **Email Notification**: Password reset via email
- 🎨 **Responsive UI**: Bootstrap 5, FontAwesome, Animations
- 🧪 **API Support**: Secure RESTful APIs with JWT
- 📊 **Dashboard**: View stats of posts, views, and publish status

---

## 📁 Project Structure

```
blogiverse/
│
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── login.html, register.html ...
│   ├── static/
│   │   └── images/
│   ├── models/
│   │   └── user.py, post.py
│   ├── routes/
│   │   └── auth.py, posts.py
│   ├── forms/
│   │   └── auth_forms.py
│   ├── controllers/
│   │   └── auth_controller.py
│   └── extensions.py
│
├── config.py
├── run.py
└── README.md
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/blogiverse-flask.git
cd blogiverse-flask
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables (Optional)

```bash
# In .env or config.py
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### 5. Initialize Database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the App

```bash
python run.py
```

Visit: `http://127.0.0.1:5000/`

---

## 🧑‍💻 Roles & Access

| Role       | Access Level                     |
|------------|----------------------------------|
| Publisher  | Can create, edit, and delete own posts |
| Admin      | Can access/edit/delete all posts |

---

## 📦 APIs

| Method | Endpoint             | Description              |
|--------|----------------------|--------------------------|
| POST   | `/posts/api`         | Create blog post         |
| GET    | `/posts/api`         | List all published posts |
| PUT    | `/posts/api/<id>`    | Update post by ID        |
| DELETE | `/posts/api/<id>`    | Delete post by ID        |

> Uses JWT Auth — must login to get token.

---

## 💡 Admin Access

To create a default admin:

```sql
INSERT INTO user (username, email, password_hash, role, is_active, created_at)
VALUES ('admin', 'admin@blog.com', '<hashed_password>', 'admin', 1, NOW());
```

Use `werkzeug.security.generate_password_hash('yourpassword')` to generate the hash.

---

## ✨ Screenshots

> Add screenshots of dashboard, post creation, and reset password features here for better presentation.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📃 License

MIT License – free to use, modify, and distribute.

---

## 🧠 Acknowledgements

- Flask
- Flask-Login
- Flask-JWT-Extended
- Bootstrap 5
- FontAwesome

---

## 📫 Contact

**Danthuluri Sai Hemanth Varma**  
📧 [saihemanthdanthuluri03@gmail.com](mailto:saihemanthdanthuluri03@gmail.com)  
🌐 [GitHub](https://github.com/danthulurisaihemanth)
