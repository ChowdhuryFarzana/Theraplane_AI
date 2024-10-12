import openai
import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Returns a service object for interacting with the Google Calendar API."""
    creds = Credentials.from_authorized_user_file('credentials.json', SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service

# Function to schedule based on urgency level
def schedule_appointment(name, email, urgency_level):
    service = get_calendar_service()
    
    # Determine appointment time based on urgency
    now = datetime.utcnow()
    
    if urgency_level == "5":  # Emergency
        appointment_time = now + timedelta(hours=1)
        description = "Emergency appointment scheduled."
    elif urgency_level == "4":  # Medium Emergency (within a week)
        appointment_time = now + timedelta(days=7)
        description = "Medium emergency appointment scheduled within a week."
    elif urgency_level == "3":  # Less Urgent (within a month)
        appointment_time = now + timedelta(days=30)
        description = "Appointment scheduled within a month."
    else:  # Regular (in 3 months)
        appointment_time = now + timedelta(days=90)
        description = "Regular appointment scheduled in 3 months."

    # Set appointment start and end times (1-hour duration)
    start_time = appointment_time.isoformat() + 'Z'  # 'Z' indicates UTC time
    end_time = (appointment_time + timedelta(hours=1)).isoformat() + 'Z'
    
    # Create the calendar event
    event = {
        'summary': f'Counseling Appointment for {name}',
        'location': 'Online',
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/New_York',
        },
        'attendees': [{'email': email}],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # Send email reminder 1 day before
                {'method': 'popup', 'minutes': 10},       # Popup reminder 10 minutes before
            ],
        },
    }

    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return event_result.get('htmlLink')  # Return the event link
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

# Root route to display the homepage
@app.route('/')
def index():
    """Displays the homepage."""
    return render_template('index.html')

# Route to handle questionnaire submission
@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        # Retrieve data from form
        data = request.get_json()
        name = data['name']
        email = data['email']
        concern = data['concern']
        urgency = data['urgency']  # Urgency score from 1 to 5
        
        # Save the user data in the database
        conn = sqlite3.connect('scheduling.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, email, concern, urgency_level) VALUES (?, ?, ?, ?)", (name, email, concern, urgency))
        conn.commit()
        conn.close()

        # Schedule the appointment based on urgency level
        appointment_link = schedule_appointment(name, email, urgency)

        if appointment_link:
            return jsonify({"status": "success", "appointment_link": appointment_link})
        else:
            return jsonify({"status": "error", "message": "Error scheduling appointment. Please try again."})
    
    return render_template('questionnaire.html')

if __name__ == '__main__':
    app.run(debug=True)
