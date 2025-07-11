from app import create_app

app = create_app()  # ✅ This makes `app` available at module level for gunicorn

if __name__ == '__main__':
    app.run(debug=True)
