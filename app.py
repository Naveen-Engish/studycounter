# app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Float)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_session', methods=['POST'])
def save_session():
    data = request.get_json()
    session = StudySession(
        subject=data['subject'],
        start_time=datetime.fromisoformat(data['start_time']),
        end_time=datetime.fromisoformat(data['end_time']),
        duration=data['duration']
    )
    db.session.add(session)
    db.session.commit()
    return jsonify({'message': 'Session saved!'})

@app.route('/get_sessions')
def get_sessions():
    sessions = StudySession.query.all()
    return jsonify([{
        'subject': s.subject,
        'date': s.start_time.date().isoformat(),
        'duration': s.duration
    } for s in sessions])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)