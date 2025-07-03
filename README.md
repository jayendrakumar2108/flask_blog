```markdown
# Flask Blogging Website

A complete mini blogging platform built with Flask, featuring authentication, post management, and REST APIs.

## Features

- User registration and authentication (web + JWT API)
- Role-based access control (Admin, Publisher, Visitor)
- Post creation, editing, and deletion
- Draft and published post status
- RESTful API endpoints
- Responsive web interface
- Error handling
- Database migrations

## Quick Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up MySQL database:
```bash
# Create database
mysql -u root -p
CREATE DATABASE flask_blog;
```

3. Update database URI in config.py if needed:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/flask_blog'
```

4. Run the application:
```bash
python app.py
```

5. Access the application:
- Web interface: http://localhost:5000
- API endpoints: http://localhost:5000/api/posts

## Default Admin Account
- Email: admin@blog.com
- Password: admin123

## API Endpoints

### Authentication
- POST /auth/register - Register new user
- POST /auth/login - Login user

### Posts (REST API)
- GET /api/posts - Get all published posts
- POST /api/posts - Create new post (requires JWT)
- GET /api/posts/{id} - Get specific post
- PUT /api/posts/{id} - Update post (requires JWT)
- DELETE /api/posts/{id} - Delete post (requires JWT)

### Example API Usage

#### Register User
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "role": "publisher"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### Create Post (with JWT token)
```bash
curl -X POST http://localhost:5000/api/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "summary": "A brief summary",
    "status": "published",
    "tags": "flask,python,web"
  }'
```