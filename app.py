from flask import Flask, flash, render_template, request, jsonify, redirect, session, url_for, send_file
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import asyncio
import speech_recognition as sr
import array
import wave
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy import Column, ForeignKey, Integer, String
from io import BytesIO
# import psycopg2

from werkzeug.datastructures import ImmutableMultiDict
from speech_rating_app import main


UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'wav'}
app = Flask(__name__)


ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5432@localhost/xise'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Employee(db.Model):
    # class Employee(db.Model):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    speech_file = Column(db.LargeBinary)
    file_name = Column(String(20))

    def __init__(self, speech_file, file_name):
        self.speech_file = speech_file
        self.file_name = file_name


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ app.route('/speech/audio/rating/<id>', methods=['GET'])
def audio_rating(id):
    id = request.view_args['id']

    employee = db.session.query(Employee).filter_by(id=id).first()
    print(employee.id)
    print(employee.file_name)
    # file = employee.speech_file
    # file.save('test/test.wav')
    # r = sr.Recognizer()
    # audio_file = data_file.speech_file.read()
    # with sr.AudioFile(audio_file) as source:
    #     audio_data = r.record(source)
    #     text = r.recognize_google(audio_data)
    # print(text)

    obj = wave.open("hello.wav", "wb")
    obj.setnchannels(2)  # mono
    obj.setsampwidth(2)
    sampleRate = 48000  # hertz
    obj.setframerate(sampleRate)

    obj.writeframesraw(employee.speech_file)
    obj.close()

    # rating = asyncio.run(main())
    return jsonify({"rating": 5}), 200


@ app.route('/speech/audio/upload', methods=['POST'])
def audio_upload():
    if 'file' not in request.files:
        return jsonify('No file present'), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify('No selected file'), 400

    if allowed_file(file.filename):

        # print(filename)
        file.save(UPLOAD_FOLDER+file.filename)
        # byte_array = array.array('B')
        # byte_array.fromstring(file.read())
        # print(len(byte_array))
        employee = Employee(file.read(), file.filename)

        db.session.add(employee)
        db.session.commit()
        inserted_id = employee.id
        obj = wave.open('files/hindi_included.wav', 'r')

        print("Number of channels", obj.getnchannels())
        print("Sample width", obj.getsampwidth())
        print("Frame rate.", obj.getframerate())
        print("Number of frames", obj.getnframes())
        print("parameters:", obj.getparams())
        obj.close()
        return jsonify({"id": inserted_id}), 201
    else:
        return jsonify("No wav file found"), 400


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
