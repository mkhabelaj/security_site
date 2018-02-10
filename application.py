import os
import psycopg2
from flask import Flask, render_template, request, jsonify
from psycopg2.extras import RealDictCursor
from flask_bootstrap import Bootstrap

DATABASE_NAME = 'cam_config'
TABLE_NAME = 'config'
PASSWORD = 'password'
USER = os.environ['USER']
CHANNEL = 'events'
conn = psycopg2.connect(user=USER, database=DATABASE_NAME, password=PASSWORD)
cur = conn.cursor(cursor_factory=RealDictCursor)

application = Flask(__name__)
Bootstrap(application)


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


@application.route("/load_ajax", methods=['GET','POST'])
def load_ajax():
    if request.method == 'POST':

        if request.values.get('name') == 'motion-detection':
            update_database(request.values.get('stream_secret'), 'motion_detection')

        if request.values.get('name') == 'capture':
            update_database(request.values.get('stream_secret'), 'capture')

        if request.values.get('name') == 'record':
            update_database(request.values.get('stream_secret'), 'record_motion')

        return jsonify()


def update_database(stream_secret, field, switch='true'):
    cur.execute(
        "SELECT {field} FROM config WHERE stream_key='{key}'".format(
            key=stream_secret,
            field=field
        ))
    result = cur.fetchall()[0]

    if result[field]:
        switch = 'false'

    cur.execute("UPDATE config SET {field}='{switch}' WHERE stream_key='{key}'".format(
        key=stream_secret,
        switch=switch,
        field=field
    ))
    conn.commit()


