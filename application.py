import os
import psycopg2
from flask import Flask, render_template, request, jsonify
from psycopg2.extras import RealDictCursor
from flask_bootstrap import Bootstrap
import glob
import time
import atexit
import subprocess

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

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


@application.route("/images", methods=['GET','POST'])
def images():
    """Image detail"""
    image_paths = []
    [image_paths.append(filename) for filename in glob.iglob('static/media/**/*.jpg')]
    return render_template('images.html', results=image_paths)


@application.route("/videos", methods=['GET','POST'])
def videos():
    """Image detail"""
    video_paths = []
    [video_paths.append(filename) for filename in glob.iglob('static/media/**/*.mp4')]
    return render_template('videos.html', results=video_paths)


@application.route("/load_ajax", methods=['GET','POST'])
def load_ajax():
    if request.method == 'POST':

        if request.values.get('name') == 'motion-detection':
            update_database(request.values.get('stream_secret'), 'motion_detection')

        if request.values.get('name') == 'capture':
            update_database(request.values.get('stream_secret'), 'capture')

        if request.values.get('name') == 'record':
            update_database(request.values.get('stream_secret'), 'record_motion')

        if request.values.get('name') == 'capture_image':
            update_database(request.values.get('stream_secret'), 'capture_image')

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


def convert_videos():
    """Image detail"""
    print('converting videos')

    for filename in glob.iglob('static/media/**/*.avi'):
        print(filename)
        original_filename = filename

        subprocess.check_call(['ffmpeg', '-i', original_filename, filename.replace('avi', 'mp4')])
        subprocess.check_call(['rm', original_filename])


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=convert_videos,
    trigger=IntervalTrigger(minutes=20),
    id='video converter',
    name='convert avi to mp4',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())