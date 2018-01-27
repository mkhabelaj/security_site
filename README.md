# security_site
Displays a stream of images

#### Things to consider
I built this project using:
  1. This project runs hand to hand with this project [security](https://github.com/mkhabelaj/security)
     1. This project is the frontend, and [security](https://github.com/mkhabelaj/security) is the backend.
  1. Python 3.4 
  1. Ubuntu 14.04
  
#### Usage 
1. Create and initiate a virtual environment
1. Install the following Python modules.
 1. Flask, psycopg2, gunicorn
1. run the following project [security](https://github.com/mkhabelaj/security)
1. ```cd``` into this project and run ```gunicorn --bind 0.0.0.0:8000 wsgi -w 1 --threads 50```
1. Then in use browser in enter the following address ```http://0.0.0.0:8000```
1. Click on the stream you want to view
