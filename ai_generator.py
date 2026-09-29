import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer


# --------------------------------------------------
# Split text into sentences
# --------------------------------------------------

def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip()) > 30
    ]

    return sentences


# --------------------------------------------------
# Extract important keywords using TF-IDF
# --------------------------------------------------

def extract_keywords(text, number_of_keywords=10):

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=number_of_keywords
        )

        matrix = vectorizer.fit_transform([text])

        keywords = vectorizer.get_feature_names_out()

        return list(keywords)

    except Exception:
        return []


# --------------------------------------------------
# Select important sentences
# --------------------------------------------------

def get_important_sentences(text, number_of_sentences=8):

    sentences = split_sentences(text)

    if not sentences:
        return []

    if len(sentences) <= number_of_sentences:
        return sentences

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        matrix = vectorizer.fit_transform(sentences)

        scores = matrix.sum(axis=1)

        sentence_scores = []

        for index, score in enumerate(scores):
            sentence_scores.append(
                (index, float(score))
            )

        sentence_scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

        selected_indexes = [
            index
            for index, score in
            sentence_scores[:number_of_sentences]
        ]

        selected_indexes.sort()

        return [
            sentences[index]
            for index in selected_indexes
        ]

    except Exception:

        return sentences[:number_of_sentences]


# --------------------------------------------------
# Generate smart notes
# --------------------------------------------------

def generate_notes(text, note_type):

    important_sentences = get_important_sentences(
        text,
        number_of_sentences=8
    )

    keywords = extract_keywords(
        text,
        number_of_keywords=10
    )

    notes = []

    notes.append("# SmartNotes AI")

    notes.append(
        f"\n## Note Type: {note_type}"
    )

    notes.append(
        "\n## Important Points"
    )

    for sentence in important_sentences:

        sentence = sentence.strip()

        if sentence:
            notes.append(
                f"- {sentence}"
            )

    if keywords:

        notes.append(
            "\n## Important Keywords"
        )

        for keyword in keywords:

            notes.append(
                f"- **{keyword.title()}**"
            )

    notes.append(
        "\n## Quick Revision"
    )

    if important_sentences:

        for sentence in important_sentences[:5]:

            notes.append(
                f"- {sentence}"
            )

    notes.append(
        "\n## Study Tip"
    )

    notes.append(
        "Revise the important points and keywords first, "
        "then read the original study material for deeper understanding."
    )

    return "\n".join(notes)


# --------------------------------------------------
# Generate local quiz
# --------------------------------------------------

def generate_quiz(notes, number_of_questions=5):

    sentences = split_sentences(notes)

    if len(sentences) < 2:

        return (
            "Not enough information available to "
            "generate a quiz."
        )

    keywords = extract_keywords(
        notes,
        number_of_keywords=20
    )

    questions = []

    question_number = 1

    for sentence in sentences:

        if question_number > number_of_questions:
            break

        words = re.findall(
            r'\b[A-Za-z][A-Za-z-]{4,}\b',
            sentence
        )

        if not words:
            continue

        answer = None

        # Try to find a keyword appearing in the sentence
        for keyword in keywords:

            if keyword.lower() in sentence.lower():

                answer = keyword
                break

        if answer is None:
            answer = words[0]

        question_text = sentence.replace(
            answer,
            "_____",
            1
        )

        question_text = question_text.replace(
            answer.title(),
            "_____",
            1
        )

        question_text = question_text.replace(
            answer.upper(),
            "_____",
            1
        )

        # Create options
        other_words = [
            word
            for word in words
            if word.lower() != answer.lower()
        ]

        distractors = []

        for word in other_words:

            if word.lower() not in [
                x.lower() for x in distractors
            ]:

                distractors.append(word)

            if len(distractors) == 3:
                break

        # If fewer than 3 distractors are available
        while len(distractors) < 3:

            distractors.append(
                "None of these"
            )

        options = [
            answer,
            distractors[0],
            distractors[1],
            distractors[2]
        ]

        # Shuffle options without using random
        # so the project remains predictable
        options = options[1:] + options[:1]

        correct_position = options.index(answer)

        letters = ["A", "B", "C", "D"]

        questions.append(
            f"QUESTION {question_number}:\n"
            f"{question_text}\n\n"
            f"A) {options[0]}\n"
            f"B) {options[1]}\n"
            f"C) {options[2]}\n"
            f"D) {options[3]}\n\n"
            f"ANSWER:\n"
            f"{letters[correct_position]}\n\n"
            f"EXPLANATION:\n"
            f"The correct answer is {answer} because "
            f"it is directly related to the study material.\n"
        )

        question_number += 1

    if not questions:

        return "Unable to generate quiz questions."

    return "\n".join(questions)