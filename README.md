# Theraplane AI
Demo - https://devpost.com/software/theraplane
<br>
Webapp link - https://theraplane-hlu6.onrender.com/

#Inspiration

College counselors are facing significant challenges due to the influx of incoming students, resulting in burnout, diminished therapy quality, and professionals leaving the field. Our goal is to ease the burden on college counselors by automating appointment management and prioritizing students based on their needs. By grouping students with similar mental health concerns and organizing appointments into categories, we can streamline the scheduling process. From each category, students will be selected based on the urgency of their situations, as determined by their responses to a tailored questionnaire. This focus on urgent cases allows us to maximize the effectiveness of counseling services.

#What it does

Our AI-powered scheduling platform streamlines appointment management for college counselors, addressing the challenges of increased student demand and counselor burnout. The system:

Utilizes an intelligent questionnaire to assess student needs and urgency
Employs AI to analyze responses and prioritize appointments
Integrates with existing calendar systems for real-time availability
Automates notifications for appointment reminders and confirmations
By optimizing the scheduling process, our solution enables counselors to focus on the most urgent cases, manage their caseloads effectively, and provide timely support to as many students as possible, despite limited resources.

How we built it

We leveraged OpenAI's GPT-4 model to act as a therapist assistant. We created a fine-tuned model and also used Retrieval-Augmented Generation (RAG) to ensure the model retains crucial information about the students. We used GPT-4 and some mathematical algorithms to weigh the urgency of students' psychological needs. For the front-end, we used HTML, Tailwind CSS, and JavaScript. Finally, we used Flask to link the front-end, the AI model, and the database.

