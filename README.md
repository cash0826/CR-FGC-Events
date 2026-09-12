# CR FGC Tournaments
Currently, the CR FGC (Costa Rica Fighting Gaming Community) events and tournaments are managed through a communication channel (Whatsapp) and other external websites.   
This Single Page Application will help players, organizers and site admins visualize and keep track of events.

This is an ongoing, collaborative project with my colleague Kevin, who would like to eliminate the outsourcing of a 3rd party platform and create a brand dedicated to serving tournaments for players located in Costa Rica. The brand will serve as a mother website to advertise additional local services.

For complete status update, log, and live document, follow along with the associated [Notion](https://app.notion.com/p/CR-FGC-Tournament-Full-Stack-App-3c12c8b876328090b384c31033362ebf#3c12c8b876328020af0fd5fbaa5239af) document.

## Tech Stack  

- **Frontend**: JavaScript, Node.js, Vite, React, React Router, React-DatePicker, eslint
- **Backend**: Python, Pipenv, Flask, Flask-Migrate, Flask-Restful, Flask-Bcrypt, Flask-SQLAlchemy, Flask-JWT-Extended, Bcrypt, Marshmallow, Faker
- **Database**: SQLite

## Set Up

Note: Running the test suite in the server will delete seeded data. Delete instances and reinitialize Flask DB if running into errors.

### Backend (server)

Install server dependencies, install the database and seed the databse:
```
cd server
pipenv install
pipevn run flask db init
pipenv run flask db migrate -m "init"
pipenv run flask db upgrade head
pipenv run python seed.py
pipenv run python app.py
```

Configure an environment variable. From the server directory, create a .env file and configure a JWT-SECRET-KEY:
```
python3 -c "import secrets; print(secrets.token_hex(32))"
```
```
JWT_SECRET_KEY=your-secret-key-here
```

### Testing Suite (server)
Run testing from pipenv (server-side only)
```
pytest -q
```

### Frontend (client)
```
cd client
npm install
npm run dev
```

## Login With Seeded User

You can view and navigate the app without logging in (viewer access). Create a player account or login with a seeded user.

User | Email | Password |
|---|---|---|
| Admin | admin@email.com | adminpassword |
| Host | host1@email.com | host1password |
| Host | host2@email.com | host2password | 
| Player | amy@email.com | amypassword |

## Key Features
1. JWT-Based Authentication Flow
2. Multi-role Authorization (admin, host, player or viewer)
3. Scalable design for more roles if needed
4. Protected Pages (Create Event and Add Tournament can only be accessed by an admin or a host)

## Known Challenges or Limitations

### Server-Side Pending Updates
- Data models: datetime.utcnow deprecated
- User Data Model: create alternate gamertags into a separate data model, relating to User as a one-to-many relationship
- Tournament Data Model: create a separate data model to store games (6 so far). Additionally, serve them as options for the client to choose from on the frontend
    - Add enums to line_up_type (singles, teams)
- Event Data Model: create a separate data model to store sponsors and rules (separate exisiting rules)
- Services/Controllers: apply time logic or constraints to dates. Certain dates cannot be before start dates
    - Additionally, apply logic that Event must be either in person or online. If in person, a location is required
- Admin Assignment API Endpoint: create a resource or script that allows a user to assign atleast 1 admin role upon app deployment
- Tournament Competitor Service Layer: when a new user is registered to a tournament, add them to the event_attendees table
- Match round Data Model: Round should be integer or string?
- SSO for passwords

### Client-side Pending Features
- External API to manage Matches, Standings and Brackets
- Styling Styling Styling!
- 'Delete?' Flow
- Pictures to tournaments / served by future game data model

## Acknowledgements
- All technologies listed above.