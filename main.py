"""
Subject Picker — Streamlit app

Recommends whichever subject/topic is most in need of revision, based on:
    score = (time since last revised)^2 + difficulty + 2 * (target grade- current grade)

Click "I've revised this" once you've actually studied it — that's the only
thing that updates payload.json. Just viewing the page (or any other widget
interaction) does NOT mark anything as revised.
"""

import json
import os
import time

import streamlit as st

PAYLOAD_PATH = os.path.join(os.path.dirname(__file__), "payload.json")


class Subject:
    def __init__(self, name, current_grade, target_grade, subject_difficulty,
                 last_revised_subject, revision_platforms, topics,
                 topic_difficulties, last_revised_topic):
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


def build_subjects():
    """Predetermined conditions for every subject/topic (from MAINOG.py)."""
    subjects = {}
    subjects["Maths"] = Subject(
        "Maths", 8, 9, 2, 0.0,
        "Sparx Maths: https://maths.sparx-learning.com",
        None, None, None,
    )
    subjects["Computer Science"] = Subject(
        "Computer Science", 8, 9, 3, None,
        ["Microsoft Teams", "Anki", "revise2"],
        ["Algorithms", "Programming", "Data Representation", "Computer Systems",
         "Cyber Security", "SQL", "Ethics"],
        [2 + 3, 1 + 3, 3 + 3, 5 + 3, 4 + 3, 6 + 3, 7 + 3],
        [0.0] * 7,
    )
    subjects["Physics"] = Subject(
        "Physics", 9, 9, 1, None,
        ["PMT: https://www.physicsandmathstutor.com/physics-revision/gcse-aqa/",
         "PMT Practical: https://www.physicsandmathstutor.com/physics-revision/gcse-aqa/practical-skills/",
         "revise2: https://www.revise2.com/"],
        ["Energy", "Electricity", "Particle Model of Matter", "Atomic Structure",
         "Forces", "Waves", "Magnetism and Electromagnetism", "Space Physics"],
        [3 + 2, 4 + 2, 2 + 2, 1 + 2, 7 + 2, 8 + 2, 6 + 2, 5 + 2],
        [0.0] * 8,
    )
    subjects["Chemistry"] = Subject(
        "Chemistry", 8, 9, 4, None,
        ["PMT: https://www.physicsandmathstutor.com/chemistry-revision/gcse-aqa/",
         "PMT Practical: https://www.physicsandmathstutor.com/chemistry-revision/gcse-aqa/practical-skills/",
         "revise2: https://www.revise2.com/"],
        ["Atomic Structure", "Bonding", "Quantitative Chemistry", "Chemical Changes",
         "Energy Changes", "The Rate and Extent of Chemical Change", "Organic Chemistry",
         "Chemical Analysis", "Chemistry of the Atmosphere", "Using Resources"],
        [1 + 0, 5 + 0, 2 + 0, 8 + 0, 3 + 0, 4 + 0, 9 + 0, 10 + 0, 6 + 0, 7 + 0],
        [0.0] * 10,
    )
    subjects["Biology"] = Subject(
        "Biology", 8, 9, 8, None,
        ["PMT: https://www.physicsandmathstutor.com/biology-revision/gcse-aqa/",
         "PMT Practical: https://www.physicsandmathstutor.com/biology-revision/gcse-aqa/practical-skills/",
         "revise2: https://www.revise2.com/", "Textbook: IRL"],
        ["Cell Biology", "Organisation", "Infection and Response", "Bioenergetics",
         "Homeostasis", "Inheritance, Variation and Evolution", "Ecology"],
        [2 + 3, 3 + 3, 4 + 3, 1 + 3, 7 + 3, 5 + 3, 6 + 3],
        [0.0] * 7,
    )
    subjects["French"] = Subject(
        "French", 8, 9, 5, None,
        ["For Vocab: ***Anki***",
         "Anything Else - Languagenut: https://www.languagenut.com/resources/",
         "Miscellaneous - BBC Bitesize: https://www.bbc.co.uk/bitesize/examspecs/zhkvkhv"],
        ["Module 1", "Module 2", "Module 3", "Module 4", "Module 5", "Module 6",
         "Module 7", "Module 8"],
        [5 + 2, 2 + 2, 3 + 2, 4 + 2, 1 + 2, 6 + 2, 7 + 2, 8 + 2],
        [0.0] * 8,
    )
    subjects["History"] = Subject(
        "History", 5, 7, 9, None,
        ["Padlet: https://padlet.com/jmurray165/gcse-history-derby-moor-ai4oohu5z5qjqqvx",
         "revise2: https://www.revise2.com/",
         "Seneca: https://app.senecalearning.com/classroom/course/67b0ecb0-38be-11e8-977a-0db134efd493",
         "BBC Bitesize: https://www.bbc.co.uk/bitesize/examspecs/zw4bv4j",
         "Textbooks: IRL"],
        ["Paper 1: Medicine", "Paper 1: Western Front", "Paper 2: Elizabeth",
         "Paper 2: American West", "Paper 3: Nazi Germany"],
        [2 + 5, 1 + 5, 3 + 5, 4 + 5, 5 + 5],
        [0.0] * 5,
    )
    subjects["English Literature"] = Subject(
        "English Literature", 8, 9, 7, None,
        ["C:\\Users\\Owner\\.vscode\\Workspace\\In Progress\\Revision\\eng_lit.html"],
        ["Paper 1: Macbeth", "Paper 1: A Christmas Carol", "Paper 2: An Inspector Calls",
         "Paper 2: Power and Conflict Poetry"],
        [1 + 6, 3 + 6, 2 + 6, 4 + 6],
        [0.0] * 4,
    )
    subjects["English Language"] = Subject(
        "English Language", 9, 9, 6, None,
        ["BBC Bitesize: https://www.bbc.co.uk/bitesize/examspecs/zcbchv4",
         "Youtube - Mr. Salles: https://www.youtube.com/@MrSallesTeachesEnglish",
         "Youtube - Mr. Everything English: https://www.youtube.com/@MrEverythingEnglish",
         "Youtube - Mr. Bruff: https://www.youtube.com/@mrbruff",
         "Textbook: IRL"],
        ["Paper 1: Section A", "Paper 1: Section B", "Paper 2: Section A",
         "Paper 2: Section B"],
        [3, 2, 4, 1],
        [0.0] * 4,
    )
    return subjects


def load_payload():
    if os.path.exists(PAYLOAD_PATH):
        with open(PAYLOAD_PATH, "r") as f:
            return json.load(f)
    return {}


def save_payload(payload):
    with open(PAYLOAD_PATH, "w") as f:
        json.dump(payload, f, indent=2)


def apply_payload(subjects, payload):
    """Overlay saved last-revised times onto the freshly-built subject objects."""
    for name, last_revised in payload.items():
        subj = subjects.get(name)
        if subj is None:
            continue
        if name == "Maths":
            subj.last_revised_subject = last_revised
        else:
            for topic, ts in last_revised.items():
                if subj.last_revised_topic is not None and topic in subj.last_revised_topic:
                    subj.last_revised_topic[topic] = ts


def compute_scores(subjects):
    """
    score = (time since last revised)^2 + difficulty + 2 * (target grade - current grade)

    Keyed by (subject_name, topic_or_None) rather than raw topic name — several
    topic names repeat across subjects (e.g. "Atomic Structure" is both a
    Physics and a Chemistry topic) and a flat topic-name key would silently
    let one overwrite the other.
    """
    scores = {}
    maths = subjects["Maths"]
    scores[("Maths", None)] = (
        (time.time() - maths.last_revised_subject) ** 2
        + maths.subject_difficulty
        + 2 * (maths.target_grade - maths.current_grade)
    )
    for name, subj in subjects.items():
        if name == "Maths":
            continue
        for topic in subj.topics:
            last = subj.last_revised_topic[topic]
            score = (
                (time.time() - last) ** 2
                + subj.topic_difficulties[topic]
                + 2 * (subj.target_grade - subj.current_grade)
            )
            scores[(name, topic)] = score
    return scores


def fmt_ts(ts):
    if not ts:
        return "Never"
    return time.strftime("%d %b %Y, %H:%M", time.localtime(ts))


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Subject Picker", page_icon="📚")
st.title("📚 Subject Picker")
st.caption("Picks whatever's most overdue for revision.")

subjects = build_subjects()
payload = load_payload()
apply_payload(subjects, payload)

scores = compute_scores(subjects)
chosen_name, chosen_topic = max(scores, key=lambda k: scores[k])
chosen_subject = subjects[chosen_name]

st.subheader(f"Subject: {chosen_subject.name}")
if chosen_topic is None:
    st.write(f"**Last revised:** {fmt_ts(chosen_subject.last_revised_subject)}")
    st.write(f"**Difficulty level:** {chosen_subject.subject_difficulty}")
else:
    st.write(f"**Topic:** {chosen_topic}")
    st.write(f"**Last revised:** {fmt_ts(chosen_subject.last_revised_topic[chosen_topic])}")
    st.write(f"**Difficulty level:** {chosen_subject.topic_difficulties[chosen_topic]}")
st.write(f"**Revision platform(s):** {chosen_subject.revision_platforms}")

if st.button("✅ I've revised this — mark as done"):
    now = time.time()
    if chosen_topic is None:
        payload["Maths"] = now
    else:
        # setdefault + update merges into the existing per-subject dict instead
        # of replacing it, so other topics' saved times aren't wiped out.
        payload.setdefault(chosen_subject.name, {})[chosen_topic] = now
    save_payload(payload)
    st.rerun()
