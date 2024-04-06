`main.py` which is the entry point to our server
2. This project has a few Python packages as dependencies, you can install them in your virtual environment using `requirements.txt`. 

Then install the python packages using `pip install -r requirements.txt`
#### Running the backend server

To launch the server, navigate to the `backend` directory and run:

##### `uvicorn main:app --reload`

This will start the server at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

#### How to launch the react app

1. Navigate to the `frontend` directory and run `npm install`
2. Then you can run:

   ##### `npm start`

   This will launch the app in development mode.\
   Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits. You will also see any lint errors in the console.
