import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import openai

# Set your OpenAI API key here
openai.api_key = 'YOUR_API_KEY'

def evaluate_disorder(answers, disorder_name):
    total_marks = sum(answers)
    result = None

    if total_marks < 4:
        result = "Slight " + disorder_name
    elif total_marks < 9:
        result = "Moderate " + disorder_name
    else:
        result = "High " + disorder_name

    return result, total_marks

def disorder_assessment(disorder_name, questions, options, scores):
    st.header(f"{disorder_name} Assessment")

    answers = []
    for i, question in enumerate(questions):
        answer = st.radio(f"{i + 1}. {question}", options, key=f'{disorder_name}_{i}')
        answers.append(options.index(answer))

    result, total_marks = evaluate_disorder(answers, disorder_name)
    st.subheader(f"Result for {disorder_name}: {result}")
    st.write("")

    # Append the total marks for visualization
    scores.append((disorder_name, total_marks))

def generate_wellness_plan(problem, medical_history, medications, age, gender, sleep_pattern, activity_level, custom,
                            plan_duration, customization_options):
    wellness_prompt = ""
    if plan_duration == "Full Week":
        wellness_prompt = f"""
        Problem: {problem}
        Medical History: {medical_history}
        Medications: {medications}
        Age: {age}
        Gender: {gender}
        Sleep Pattern: {sleep_pattern}
        Physical Activity Level: {activity_level}
        set of instructions you need to follow: {custom}

        give me a personalized mental wellness plan for a week based on the provided information in a structured tabular format.Give a special note at the end.
        """
    else:
        wellness_prompt = f"""
        Problem: {problem}
        Medical History: {medical_history}
        Medications: {medications}
        Age: {age}
        Gender: {gender}
        Sleep Pattern: {sleep_pattern}
        Physical Activity Level: {activity_level}
        set of instructions you need to follow: {custom}

        give me a personalized mental wellness plan for today based on the provided information.    
        """

    # Add customization options to the prompt
    wellness_prompt += f"\nCustomization Options: {customization_options}"

    return wellness_prompt

def main():
    st.title("Mental Health Disorder Assessment")

 
    # Define questions and options for each disorder
    disorders = {
        "Anxiety": [
        'How often do you feel excessive worry or fear?',
        'Do you experience physical symptoms such as restlessness or trembling when feeling anxious?',
        'How would you describe the impact of anxiety on your daily life?',
        'Have you noticed changes in your sleep patterns due to anxiety?',
    ],
    "PTSD": [
        'Do certain sounds, smells, or situations trigger vivid memories of the traumatic event?',
        'Have you experienced intense distress or physical reactions when reminded of the traumatic event?',
        'Do you actively avoid situations, places, or people that remind you of the traumatic event?',
        'Have you noticed changes in your mood or thinking patterns since the traumatic event?',
    ],
    "ADHD": [
        'Do you frequently experience racing thoughts that make it challenging to focus on one task?',
        'Are you often forgetful in daily activities, such as forgetting appointments or tasks?',
        'Do you find it difficult to follow instructions or complete tasks that require sustained mental effort?',
        'Do you often interrupt others in conversations or have difficulty waiting your turn in group situations?',
    ],
    "Bipolar": [
        'Have you ever experienced a period of abnormally elevated mood, energy, and activity (mania)?',
        'Have you ever experienced a period of abnormally low mood, energy, and activity (depression)?',
        'Do you have a family history of bipolar disorder or similar mood disorders?',
        'Have your mood swings significantly impacted your daily functioning and relationships?',
    ],
    "OCD": [
        'Do you find yourself repeatedly performing certain behaviors or having intrusive thoughts?',
        'Do you find it difficult to control or stop unwanted thoughts or images that come into your mind?',
        'How much time do you spend on rituals or repetitive behaviors to reduce anxiety or prevent a dreaded event?',
        # 'Do you avoid situations that trigger your obsessive thoughts or rituals?',
        'Do you experience significant distress if you\'re unable to perform your rituals or compulsions?',
    ],
    "Eating Disorder": [
        'Do you often engage in episodes of overeating, followed by feelings of guilt or shame?',
        'Are you preoccupied with thoughts about food, dieting, or body weight?',
        # 'Have you noticed a significant change in your eating habits, such as restricting certain foods or excessive exercising?',
        'Do you avoid social situations involving food due to concerns about your body image or eating habits?',
        'How often do you compare your body to others, either in person or through media?',
    ],
    "Depression": [
        'How often do you feel sad, hopeless, or lose interest in activities you once enjoyed?',
        'Do you experience changes in appetite or weight, such as significant weight loss or gain?',
        'Is there a persistent lack of energy or increased fatigue?',
        # 'Do you have trouble sleeping or experience excessive sleeping?',
        'Have you noticed a significant decrease or increase in your ability to think or concentrate?',
    ],
    "Stress": [
        'How often do you feel overwhelmed by the demands of your daily life?',
        'Do you experience physical symptoms like headaches or tension related to stress?',
        'How often do you find it difficult to relax and unwind?',
        'Do you often worry about future events or outcomes?',
    ],
        # Add other disorders...
    }

    options = ["Rarely or never", "Occasionally", "Frequently", "Almost all the time"]
    
    scores = []  # List to store total scores for each disorder

    for disorder_name, questions in disorders.items():
        st.subheader(f"Assessment for {disorder_name}")
        disorder_assessment(disorder_name, questions, options, scores)

    # Visualization using matplotlib
    if scores:
        disorder_names, total_scores = zip(*scores)

        # Find the index of the disorder with the highest score
        max_score_index = np.argmax(total_scores)

        # Highlight the disorder with the highest score using st.success
        st.success(f"The disorder with the highest total score is: {disorder_names[max_score_index]}")
        name = st.text_input("Name:")
        gender = st.radio("Gender:", ["Male", "Female", "Other"])
        age = st.number_input("Age:")
        
        if st.button("Generate Report"):
            # Generate the report using OpenAI API
            prompt = f"Act as a psychiatric.Use the {age}, {gender}, {disorder_names[max_score_index]} to generate a personalized Mental Health Report\n\n\nAI Instructions :\n\n1.Use the following REPORT FORMAT 'name:{name}\n \nGender:{gender}\n \nAge:{age} \nAbout the disorder you are facing: \n\nCAUSES:\n\nCURES:\n\nPrescribed Medicines:'\n\n2. Make it like a real report in a structured point for prescribed medicines\n\n3. Use the given 4 inputs to generate the report in the specified format"

            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=300
            )

            generated_report = response['choices'][0]['text']

            # Display the generated report
            st.subheader("Generated Report:")
            plt.barh(disorder_names, total_scores, color='#ff6361')
            plt.xlabel('Total Score')
            plt.title('Total Scores for Each Disorder')
            st.pyplot(plt)
            st.markdown(generated_report)

        # Get inputs for mental health wellness plan
        medical_history = st.text_area("Provide a brief medical history:")
        medications = st.text_area("List any medications you are currently taking:")
        sleep_pattern = st.text_area("describe your sleeping pattern")
        activity_level = st.selectbox("Select your physical activity level:", ["Low", "Moderate", "High"])
        personalization = st.text_area("you can add your customization")
        plan_duration = st.radio("Select plan duration:", ["Full Week", "Today"])

        if st.button("Generate Wellness Plan"):
            # Generate the wellness plan using OpenAI API
            wellness_prompt = generate_wellness_plan(disorder_name, medical_history, medications, age, gender, sleep_pattern, activity_level, personalization, plan_duration, "")
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=wellness_prompt,
                max_tokens=300
            )
            wellness_plan = response['choices'][0]['text']

            st.subheader("Generated Mental Wellness Plan:")
            st.write(wellness_plan)
                
if __name__ == "__main__":
    main()
