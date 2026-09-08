# CR FGC Tournaments
This is full-stack, React + Flask productivity app to manage upcoming tournament events, register attendees, view standings and create new tournaments.

## Description


## Technologies Used  

**Backend**: Python, Pipenv, Flask, Flask-Migrate, Flask-Restful, Flask-Bcrypt, Flask-SQLAlchemy, Flask-JWT-Extended, Bcrypt, Marshmallow, Faker

**Frontend**: JavaScript, Node.js, Vite, React, React Router, eslint, Tailwind CSS

## Installation / Set Up Instructions

1. Fork or Clone this repository from GitHub.
    ```
    git clone <repository-url>
    cd <repository>
    ```

2. Install Dependencies.\ 
Change into the server directory `cd server`. Run `pipenv install` to create your virtual environment and install dependencies. Run `pipenv shell` to enter the virtual environment.\
Change into the client directory and install node dependencies for the frontend. Run `npm install --prefix client` OR `cd ..`, `cd client` and `npm install`

    Alternative commands:
    ```
    pipenv install && pipenv shell
    npm install --prefix client
    ```
  
3. Configure an environment variable. From the server directory, create a .env file and configure a JWT-SECRET-KEY:
    ```
    python3 -c "import secrets; print(secrets.token_hex(32))"
    ```
    ```
    JWT_SECRET_KEY=your-secret-key-here
    ```

4. Configure Flask App. Change to the server directory and configure the the Flask App environment variables:
    ```
    cd server
    export FLASK_APP=app.py
    export FLASK_RUN_PORT=5555
    ```
    Use **set** instead of export if on Window OS.
  
5. Create and seed the database. Ensure that you are in the server directory and run:
    ```
    flask db init
    flask db migrate -m "initial migration"
    flask db upgrade head
    python seed.py
    ```
  
6. To open and view the backend, ensure that you are in the server directory and run:
    ```
    python app.py
    ```

7. Run React in another terminal from the client directory:
    ```bash
    npm run dev
    ```

8. Run testing from pipenv (server-side only)
    ```
    pytest -q
    ```
  
## General Overview
1. 

## Key Features
1. 

## Known Challenges or Limitations
- Need to update server - datetime.utcnow deprecated

## Other small features to include
- 
    
## Deployment Link
-  

## Acknowledgements
- All technologies listed above.