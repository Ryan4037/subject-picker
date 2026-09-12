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

# Defining all Subjects
maths = Subject("Maths", 8, 9, 2, 0.0, "Sparx Maths: https://maths.sparx-learning.com", None, None, None)
comp_sci = Subject("Computer Science", 8, 9, 3, None, ["Microsoft Teams", "Anki", "revise2"], ["Algorithms", "Programming", "Data Representation", "Computer Systems", "Cyber Security", "SQL", "Ethics"], [2+3, 1+3, 3+3, 5+3, 4+3, 6+3, 7+3], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
physics = Subject("Physics", 9, 9, 1, None, ["PMT: https://www.physicsandmathstutor.com/physics-revision/gcse-aqa/", "PMT Practical: https://www.physicsandmathstutor.com/physics-revision/gcse-aqa/practical-skills/", "revise2: https://www.revise2.com/"], ["Energy", "Electricity", "Particle Model of Matter", "Atomic Structure", "Forces", "Waves", "Magnetism and Electromagnetism", "Space Physics"], [3+2, 4+2, 2+2, 1+2, 7+2, 8+2, 6+2, 5+2], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
chemistry = Subject("Chemistry", 8, 9, 4, None, ["PMT: https://www.physicsandmathstutor.com/chemistry-revision/gcse-aqa/", "PMT Practical: https://www.physicsandmathstutor.com/chemistry-revision/gcse-aqa/practical-skills/", "revise2: https://www.revise2.com/"], ["Atomic Structure", "Bonding", "Quantitative Chemistry", "Chemical Changes", "Energy Changes", "The Rate and Extent of Chemical Change", "Organic Chemistry", "Chemical Analysis", "Chemistry of the Atmosphere", "Using Resources"], [1+0, 5+0, 2+0, 8+0, 3+0, 4+0, 9+0, 10+0, 6+0, 7+0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
biology = Subject("Biology", 8, 9, 8, None, ["PMT: https://www.physicsandmathstutor.com/biology-revision/gcse-aqa/", "PMT Practical: https://www.physicsandmathstutor.com/biology-revision/gcse-aqa/practical-skills/", "revise2: https://www.revise2.com/", "Textbook: IRL"], ["Cell Biology", "Organisation", "Infection and Response", "Bioenergetics", "Homeostasis", "Inheritance, Variation and Evolution", "Ecology"], [2+3, 3+3, 4+3, 1+3, 7+3, 5+3, 6+3], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
french = Subject("French", 8, 9, 5, None, ["For Vocab: ***Anki***", "Anything Else - Languagenut: https://www.languagenut.com/resources/", "Miscellaneous - BBC Bitesize: https://www.bbc.co.uk/bitesize/examspecs/zhkvkhv"], ["Module 1", "Module 2", "Module 3", "Module 4", "Module 5", "Module 6", "Module 7", "Module 8"], [5+2, 2+2, 3+2, 4+2, 1+2, 6+2, 7+2, 8+2], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
history = Subject("History", 5, 7, 9, None, ["Padlet: https://padlet.com/jmurray165/gcse-history-derby-moor-ai4oohu5z5qjqqvx", "revise2: https://www.revise2.com/", "Seneca: https://app.senecalearning.com/classroom/course/67b0ecb0-38be-11e8-977a-0db134efd493", "BBC Bitesize: https://www.bbc.co.uk/bitesize/examspecs/zw4bv4j", "Textbooks: IRL"], ["Paper 1: Medicine", "Paper 1: Western Front", "Paper 2: Elizabeth", "Paper 2: American West", "Paper 3: Nazi Germany"], [2+5, 1+5, 3+5, 4+5, 5+5], [0.0, 0.0, 0.0, 0.0, 0.0])
eng_lit = Subject("English Literature", 8, 9, 7, None, ["C:\\Users\\Owner\\.vscode\\Workspace\\In Progress\\Revision\\eng_lit.html"], ["Paper 1: Macbeth", "Paper 1: A Christmas Carol", "Paper 2: An Inspector Calls", "Paper 2: Power and Conflict Poetry"], [1+6, 3+6, 2+6, 4+6], [0.0, 0.0, 0.0, 0.0])
eng_lang = Subject("English Language", 9, 9, 6, None, ["BBC Bitesize: https://www.bbc.co.uk/bitesize/examspecs/zcbchv4", "Youtube - Mr. Salles: https://www.youtube.com/@MrSallesTeachesEnglish", "Youtube - Mr. Everything English: https://www.youtube.com/@MrEverythingEnglish", "Youtube - Mr. Bruff: https://www.youtube.com/@mrbruff", "Textbook: IRL"], ["Paper 1: Section A", "Paper 1: Section B", "Paper 2: Section A", "Paper 2: Section B"], [3, 2, 4, 1], [0.0, 0.0, 0.0, 0.0])


"""########## Main code ##########"""
# Analysing the payload
payload = eval(input("Enter the payload: "))

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
    print(f"Subject: {chosen_one.name}\n Last Revised: {chosen_one.last_revised_subject}\n Difficulty Level: {chosen_one.subject_difficulty}\n Revision Platforms: {chosen_one.revision_platforms}")
    payload.update({chosen_one.name: time.time()})
else:
    print(f"Subject: {topic_to_subject[chosen_one].name}\n Topic: {chosen_one}\n Last Revised: {topic_to_subject[chosen_one].last_revised_topic[chosen_one]}\n Difficulty Level: {topic_to_subject[chosen_one].topic_difficulties[chosen_one]}\n Revision Platforms: {topic_to_subject[chosen_one].revision_platforms}")
    payload.update({topic_to_subject[chosen_one].name: {chosen_one: time.time()}})
print(f"Updated Payload: {payload}")