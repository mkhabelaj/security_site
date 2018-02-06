import os
import psycopg2
from flask import Flask, render_template, request
from psycopg2.extras import RealDictCursor

DATABASE_NAME = 'cam_config'
TABLE_NAME = 'config'
PASSWORD = 'password'
USER = os.environ['USER']
CHANNEL = 'events'
conn = psycopg2.connect(user=USER, database=DATABASE_NAME, password=PASSWORD)
cur = conn.cursor(cursor_factory=RealDictCursor)

application = Flask(__name__)


@application.route("/")
def index():
    """Video streaming home page."""
    try:
        cur.execute('select * from port_map;')
        # Fetch a dictionary with the database
        port_map = cur.fetchall()
    except Exception as ex:
        print(ex)
    return render_template('index.html', results=port_map)


@application.route("/video_stream", methods=['GET','POST'])
def video_stream():
    """Video streaming detail"""
    return render_template('video_stream.html', result=request.args)



