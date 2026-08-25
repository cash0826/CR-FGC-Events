from config import app, db, bcrypt, jwt, api

__all__ = ["app", "db", "bcrypt", "jwt", "api"]

if __name__ == "__main__":
    app.run(debug=True, port=5555)
