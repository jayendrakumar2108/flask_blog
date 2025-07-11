# BlogiVerse – A Flask Blogging Platform
BlogiVerse is a secure, responsive, and feature-rich blogging platform built with Flask, JWT, and Flask-Login. It supports full blog CRUD operations, user authentication with role-based access (admin, publisher), password reset via email, search and filter functionality, and modern UI with Bootstrap.
---

## 🚀 Features

- 🔐 **User Authentication**: Login, Register, Forgot & Reset Password
- 👥 **Role Management**: Admin and Publisher roles
- 📝 **Post CRUD**: Create, Edit, View, and Delete blogs
- 📌 **Search & Tag Filter**: Easily find relevant blogs
- 📈 **Blog Views Counter**
- 📬 **Email Notifications**: Password reset via email
- 🎨 **Responsive UI**: Built with Bootstrap 5, FontAwesome, and animations
- 🧪 **API Support**: Secure RESTful APIs with JWT
- 📊 **Dashboard**: View stats of posts, views, and publish status

---

## 📁 Project Structure

blogiverse/
│
├── app/
│ ├── templates/
│ │ ├── base.html
│ │ ├── dashboard.html
│ │ ├── login.html, register.html, ...
│ ├── static/
│ │ └── images/
│ ├── models/
│ │ └── user.py, post.py
│ ├── routes/
│ │ └── auth.py, posts.py
│ ├── forms/
│ │ └── auth_forms.py
│ ├── controllers/
│ │ └── auth_controller.py
│ └── extensions.py
│
├── config.py
├── run.py
└── README.md

yaml
Copy
Edit

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/blogiverse-flask.git
cd blogiverse-flask
2. Create & Activate Virtual Environment
bash
Copy
Edit
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Setup Environment Variables (Optional)
Create a .env file or configure in config.py:

env
Copy
Edit
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
5. Initialize Database
bash
Copy
Edit
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
6. Run the App
bash
Copy
Edit
python run.py
Visit the app at: http://127.0.0.1:5000/

🧑‍💻 Roles & Access
Role	Access Level
Publisher	Can create, edit, and delete own posts
Admin	Can access/edit/delete all user posts

📦 API Endpoints (JWT Auth Required)
Method	Endpoint	Description
POST	/posts/api	Create blog post
GET	/posts/api	List all posts
PUT	/posts/api/<id>	Update post by ID
DELETE	/posts/api/<id>	Delete post by ID

💡 Admin Access
To create a default admin user:

sql
Copy
Edit
INSERT INTO user (username, email, password_hash, role, is_active, created_at)
VALUES (
  'admin',
  'admin@blog.com',
  '<hashed_password>',
  'admin',
  1,
  NOW()
);
👉 Use Python to hash password:

python
Copy
Edit
from werkzeug.security import generate_password_hash
print(generate_password_hash("yourpassword"))


🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to modify or improve.
