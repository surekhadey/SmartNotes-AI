import streamlit as st

from pdf_processor import (
    extract_text_from_pdf,
    clean_text,
    split_text
)

from ai_generator import (
    generate_notes,
    generate_quiz
)

from database import (
    create_database,
    save_document
)


# Create database
create_database()


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SmartNotes AI",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📚 SmartNotes AI")

st.write(
    "An AI/NLP-based educational tool that converts "
    "study material into concise and structured notes."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("⚙️ Settings")


note_type = st.sidebar.selectbox(
    "Choose Note Type",
    [
        "Quick Revision",
        "Exam Preparation",
        "Detailed Notes",
        "One-Day Revision"
    ]
)


question_count = st.sidebar.slider(
    "Number of Quiz Questions",
    3,
    10,
    5
)


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload your study material",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )


    # --------------------------------------------------
    # Generate Notes Button
    # --------------------------------------------------

    if st.button(
        "🚀 Generate Smart Notes"
    ):

        with st.spinner(
            "Reading your PDF..."
        ):

            try:

                raw_text = extract_text_from_pdf(
                    uploaded_file
                )

                if not raw_text.strip():

                    st.error(
                        "No readable text was found in this PDF."
                    )

                    st.stop()


                cleaned_text = clean_text(
                    raw_text
                )


                chunks = split_text(
                    cleaned_text
                )


            except Exception as error:

                st.error(
                    f"Error reading PDF: {error}"
                )

                st.stop()


        st.info(
            f"Extracted approximately "
            f"{len(cleaned_text)} characters."
        )


        save_document(
            uploaded_file.name
        )


        # --------------------------------------------------
        # Generate notes
        # --------------------------------------------------

        all_notes = []

        progress_bar = st.progress(0)

        total_chunks = len(chunks)


        for index, chunk in enumerate(chunks):

            with st.spinner(
                f"Processing material "
                f"{index + 1}/{total_chunks}..."
            ):

                try:

                    notes = generate_notes(
                        chunk,
                        note_type
                    )

                    all_notes.append(
                        notes
                    )

                except Exception as error:

                    st.error(
                        f"Processing error: {error}"
                    )

                    st.stop()


            progress_bar.progress(
                (index + 1) / total_chunks
            )


        final_notes = (
            "\n\n---\n\n".join(
                all_notes
            )
        )


        st.session_state["notes"] = (
            final_notes
        )

        st.session_state["filename"] = (
            uploaded_file.name
        )


        st.success(
            "✅ Smart notes generated successfully!"
        )


# --------------------------------------------------
# Display Notes
# --------------------------------------------------

if "notes" in st.session_state:

    st.divider()

    st.header(
        "📝 Generated Smart Notes"
    )


    st.markdown(
        st.session_state["notes"]
    )


    # Download notes
    st.download_button(
        label="⬇️ Download Notes",
        data=st.session_state["notes"],
        file_name="smart_notes.txt",
        mime="text/plain"
    )


    # --------------------------------------------------
    # Quiz
    # --------------------------------------------------

    st.divider()

    st.header(
        "🧠 Practice Quiz"
    )


    if st.button(
        "Generate Quiz"
    ):

        with st.spinner(
            "Creating practice questions..."
        ):

            try:

                quiz = generate_quiz(
                    st.session_state["notes"],
                    question_count
                )

                st.session_state["quiz"] = quiz

            except Exception as error:

                st.error(
                    f"Quiz generation failed: {error}"
                )


    if "quiz" in st.session_state:

        st.markdown(
            st.session_state["quiz"]
        )

        st.info(
            "These questions are generated "
            "automatically from the extracted study material."
        )