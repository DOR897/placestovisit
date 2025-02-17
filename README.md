# places to visit App
an app where u can add create update and delete cool places in the world.

Best Places to Visit API
This is a REST API built with FastAPI that provides information about the cool places to visit in various countries.

## HOW TO RUN THE APP
this app using fastapi,streamlit and docker so make sure u have these three. 
To run the APP in  using Docker, you need these following commands:


You need to clone the repository:`` git clone https://github.com/EASS-HIT-PART-A-2022-CLASS-III/placestovisit.git ``

then go the app name 'cd placestovisit'

after that u can use docker to run the up with those two commands:
``docker-compose build`` first and then `` docker compose up``
and u will see the up running at "http://localhost:8501" where u can add places to the DB and delete also.
u can see a map which can show u countries and places u think about adding to the app DB.

## A demo for the app 

## HOW TO CREATE,UPDATE AND DELETE PLACES VIA THE RUNNING ONLY BACKEND
if u want to edit the places and update u can navgite to the backend:
U need to use the command 'cd cool-places-backend' after u clone the app.
after that ``docker build -t my-fa -f./nginx.Dockerfile`` and ``docker build -t my-fastapi-app .`` This assumes that your FastAPI application is in the current directory and that your dependencies are listed in a requirements.txt file in the same directory. You may need to modify the COPY and pip install commands if your application has different requirements or file locations.

Once the image is built, you can run it using the docker run command:

``docker run -p 8800:8800 my-fastapi-app`` This will start the FastAPI application in a container and map port 8800 on the container to port 8800 on the host machine. You can then access the application by navigating to http://localhost:8800/docs in a web browser or making requests to it programmatically.
and that's it u can create,update and delete and also view the current locations in the appAPI.

``python -m pytest test.py``
