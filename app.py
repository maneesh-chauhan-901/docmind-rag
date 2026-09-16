"""Streamlit user interface for DocMind."""

import streamlit as st

from rag import answer_question_stream, clear_index, get_document_names, index_pdf


st.set_page_config(page_title="DocMind", page_icon="📄", layout="centered")

st.title("DocMind")
st.caption("AI research and document intelligence assistant")
st.write("Upload research PDFs, then ask questions grounded in their content.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type="pdf",
        accept_multiple_files=True,
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                chunk_count, added = index_pdf(
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                )
                if added and chunk_count:
                    st.success(f"Indexed {uploaded_file.name}")
                elif added:
                    st.warning(f"No text found in {uploaded_file.name}")
            except Exception as error:
                st.error(f"Could not process {uploaded_file.name}: {error}")

    document_names = get_document_names()
    st.subheader("Indexed documents")
    if document_names:
        for name in document_names:
            st.write(f"- {name}")
    else:
        st.caption("No documents indexed yet.")

    if st.button("Clear document index", use_container_width=True):
        clear_index()
        st.session_state.chat_history = []
        st.rerun()

st.divider()

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask a question about your documents")
if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            _, answer_stream = answer_question_stream(question)
            answer = st.write_stream(answer_stream)
            if not answer:
                answer = "The model returned no answer. Please try the question again."
                st.warning(answer)
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )
        except Exception as error:
            error_message = f"I could not answer the question: {error}"
            st.error(error_message)
            st.session_state.chat_history.append(
                {"role": "assistant", "content": error_message}
            )
