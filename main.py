"""This is a Python script that processes both predetermined conditions and newly-entered inputs, then generates a subject which I have to study as the output.
Predetermined conditions: 
    > Current Grades in each subject
    > Target Grades in each subject
    > Difficulty level of the subject
    > Difficulty level of each topic in a given subject
    > Last time revised each subject
    > Last time revised each topic in a given subject
    > What revision platforms to use for each subject
Inputs:
    > A payload that contains:
        > Last time revised each subject
        > Last time revised each topic in a given subject
Outputs:
    > A subject which I have to study
    > An updated payload that contains:
        > Updated last time revised each subject
        > Updated last time revised each topic in a given subject
"""

import time
import json

"""########## Definitions ##########"""


# Defining a class so that I can create objects for each subject and store all the information about each subject in one place and in one line (reducing the read complexity).
class Subject():
    def __init__(self, name, current_grade, target_grade, subject_difficulty, last_revised_subject, revision_platforms, topics, topic_difficulties, last_revised_topic):
        self.name = name
        self.current_grade = current_grade
        self.target_grade = target_grade
        self.subject_difficulty = subject_difficulty
        self.revision_platforms = revision_platforms
        if name != "Maths":
            self.last_revised_subject = None
            self.topics = topics
            self.topic_difficulties = dict(zip(topics, topic_difficulties))
            self.last_revised_topic = dict(zip(topics, last_revised_topic))
        else:
            self.last_revised_subject = last_revised_subject
            self.topics = None
            self.topic_difficulties = None
            self.last_revised_topic = None

# Function to calculate the score for each topic in a given subject and store it in a dictionary
def get_scores(subject):
    for topic in subject.topics:
        # score = (time since last revised)^2 + difficulty level + 2 * (current grade - target grade)
        topic_score = ((time.time() - subject.last_revised_topic[topic]) ** 2) + subject.topic_difficulties[topic] + (2 * (subject.current_grade - subject.target_grade))
        scores_dict[topic] = topic_score
        topic_to_subject[topic] = subject




"""########## Main code ##########"""

# Load the payload from payload.json
with open('payload.json', 'r') as f:
    payload = json.load(f)

# Parse the payload and execute the statements in the payload to update the last revised dates for each subject and topic. 
# The payload will be in the format of a dictionary with the subject names as keys and the last revised dates as values. 
# For example: {"Maths": "27/07/2026", "Computer Science": {"Algorithms": "27/07/2026", "Programming": "27/07/2026"}, "Physics": {"Energy": "20/05/2026", "Electricity": "20/05/2026"}}
for subject, last_revised in payload.items():
    if subject == "Maths":
        maths.last_revised_subject = last_revised
    else:
        for subject_obj in [comp_sci, physics, chemistry, biology, french, history, eng_lit, eng_lang]:
            if subject_obj.name == subject:
                for topic, last_revised_topic in last_revised.items():
                    subject_obj.last_revised_topic[topic] = last_revised_topic

# An algorithm will determine which subject and topic to display based on the characteristics mentioned in the objects
scores_dict = {}
topic_to_subject = {}

# The algorithm will calculate a score for maths and each topic based on the following formula: 
# score = (time since last revised)^2 + difficulty level + 2 * (current grade - target grade)
scores_dict[maths] = ((time.time() - maths.last_revised_subject) ** 2) + maths.subject_difficulty + (2 * (maths.current_grade - maths.target_grade))
for subject in [comp_sci, physics, chemistry, biology, french, history, eng_lit, eng_lang]:
    get_scores(subject)

# Choosing the subject/topic with the highest score
scores = list(scores_dict.keys())
chosen_one = max(scores, key=lambda x: scores_dict[x])

# Displaying the subject with the highest score and accompanying information. Also displaying updated payload
if isinstance(chosen_one, Subject): # If chosen_one is a subject
    print(f"Subject: {chosen_one.name}\nLast Revised: {chosen_one.last_revised_subject}\nDifficulty Level: {chosen_one.subject_difficulty}\nRevision Platforms: {chosen_one.revision_platforms}")
    payload.update({chosen_one.name: time.time()})
else:
    print(f"Subject: {topic_to_subject[chosen_one].name}\nTopic: {chosen_one}\nLast Revised: {topic_to_subject[chosen_one].last_revised_topic[chosen_one]}\nDifficulty Level: {topic_to_subject[chosen_one].topic_difficulties[chosen_one]}\nRevision Platforms: {topic_to_subject[chosen_one].revision_platforms}")
    payload.update({topic_to_subject[chosen_one].name: {chosen_one: time.time()}})

# Write the updated payload back to payload.json
with open('payload.json', 'w') as f:
    json.dump(payload, f, indent=2)
