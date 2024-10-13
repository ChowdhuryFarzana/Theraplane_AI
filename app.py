import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from openai import OpenAI
from apikey import my_api as apikey
import datetime
from datetime import timedelta
import re

now = datetime.datetime.now()
app = Flask(__name__)

# Load OpenAI API key from environment variable
os.environ["OPENAI_API_KEY"] = apikey
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Define the system prompt
system_prompt = """You are a college therapist in the USA. Students are meeting you for counselling and therapy.
Ask them a variety of questions to assess for depression, anxiety, OCD, panic disorder, social anxiety disorder,
suicidal intent, substance abuse, loneliness, and bipolar disorder. Ask one question at a time. After each response, evaluate if you have 
gathered enough information to determine the student's condition and its urgency. If you have, provide an 
urgency rating on a scale of 1 to 5, with 5 being the most urgent and 1 being the least urgent. 

If at any point the student expresses suicidal thoughts or intentions, immediately provide call helpline like 911 and encourage them to seek immediate help. You must flag all suicide expressions as an urgency level 5, always provide crisis hotline numbers and emergency resources.
You must not say you are unable to help because you are the therapist helping the student.
Include [URGENCY_RATING: X] at the very end of your response when you've determined the urgency, where X is the rating. 
This will signal the end of the conversation."""

def get_ai_response(messages):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
    )
    return chat_completion.choices[0].message.content.strip()

def extract_urgency_rating(response):
    match = re.search(r'\[URGENCY_RATING: (\d+)\]', response)
    if match:
        return int(match.group(1)), response.replace(match.group(0), '').strip()
    return None, response

def schedule(name, urgent_lvl):
    if urgent_lvl == 5:  # Emergency
        appointment_time = now + timedelta(hours=1)
        description = "Emergency appointment scheduled."
    elif urgent_lvl == 4:  # Medium Emergency (within a week)
        appointment_time = now + timedelta(days=7)
        description = "Medium emergency appointment scheduled within a week."
    elif urgent_lvl == 3:  # Less Urgent (within a month)
        appointment_time = now + timedelta(days=30)
        description = "Appointment scheduled within a month."
    else:  # Regular (in 3 months)
        appointment_time = now + timedelta(days=90)
        description = "Regular appointment scheduled in 3 months."
    return appointment_time, description

@app.route('/')
def index():
    """Displays the homepage."""
    return render_template('index.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        data = request.get_json()
        
        # Check if this is a message for the AI conversation
        if 'message' in data:
            user_input = data['message']
            messages = data.get('messages', [])
            
            if not messages:
                messages = [{"role": "system", "content": system_prompt}]
            
            messages.append({"role": "user", "content": user_input})
            
            ai_response = get_ai_response(messages)
            urgency_rating, filtered_response = extract_urgency_rating(ai_response)
            
            messages.append({"role": "assistant", "content": ai_response})
            
            response_data = {
                "message": filtered_response,
                "urgency_rating": urgency_rating,
                "messages": messages
            }
            
            return jsonify(response_data)
        
        # If it's the final form submission
        elif 'name' in data:
            name = data.get('name')
            email = data.get('email')
            concern = data.get('concern')
            print(f"The data urgency is {data.get('urgency')}")
            if data.get('urgency')=='':
                urgency=5
            else:
                urgency = int(data.get('urgency'))  # Convert to int
            
            # Save data to database (implement this part)
            
            # Schedule appointment
            appointment_time, description = schedule(name, urgency)
            
            final_response = {
                'message': f'{description} Your appointment is scheduled for {appointment_time.strftime("%Y-%m-%d %H:%M")}',
                'appointment_time': appointment_time.strftime("%Y-%m-%d %H:%M")
            }
            return jsonify(final_response)
        
        else:
            return jsonify({"error": "Invalid data format"}), 400
    
    return render_template('questionnaire.html')

@app.route('/available_times')
def available_times():
    # This route should be implemented to show available appointment times
    return "Available Times Page"

if __name__ == '__main__':
    app.run(debug=True)