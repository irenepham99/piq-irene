
# PIQ Energy Take Home 
This is a development only application that allows users to run and view results of an energy study. Data is not being persisted on the back end past the existing session.

## Running Locallys

### Server Set Up
 1. Navigate to `server` 
 2. Create a virtual environment `python3 -m venv venv`
 3. Actiate the virtual environment `source venv/bin/activate`
 4. Install requirements `pip install -r requirements.txt`
 5. Run the server in dev mode `fastapi dev main.py `

The server should run on `http://127.0.0.1:8000`


### Client Set Up 
1. Navigate to `client` directory 
2. Run `npm install`
3. Run `npm run dev` 
4. The client should run at `http://localhost:5173/` but double check the terminal output to see which port is being used in case port 5173 is already taken. 



