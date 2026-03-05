import streamlit as st
from app import process_pdf
from rag_engine import retrieve, generate_answer

st.title("📚 Handwritten Notes QA System")

if "index" not in st.session_state:
    st.session_state.index = None
    st.session_state.chunks = None

uploaded_file = st.file_uploader(
    "Upload handwritten PDF",
    type="pdf"
)

if uploaded_file and st.session_state.index is None:

    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Processing PDF..."):

        index, chunks = process_pdf("temp.pdf")

        st.session_state.index = index
        st.session_state.chunks = chunks

    st.success("PDF processed successfully!")

if st.session_state.index is not None:

    question = st.text_input("Ask a question about the notes")

    if question:

        with st.spinner("Thinking..."):

            contexts = retrieve(
                question,
                st.session_state.index,
                st.session_state.chunks
            )

            answer = generate_answer(
                question,
                contexts
            )

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources")

        for c in contexts:
            st.write(f"Page {c['page']}")