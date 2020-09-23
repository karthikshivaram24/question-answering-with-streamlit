from typing import Dict

import streamlit as st  # type: ignore
import wikipedia    # type: ignore
from transformers import Pipeline, pipeline  # type: ignore

NUM_SENT = 10


def get_qa_pipeline() -> Pipeline:
    qa = pipeline("question-answering", framework="tf")
    return qa


def answer_question(pipeline: Pipeline, question: str, paragraph: str) -> Dict:
    input = {"question": question, "context": paragraph}
    return pipeline(input)


def get_wiki_paragraph(query: str) -> str:
    results = wikipedia.search(query)
    try:
        summary = wikipedia.summary(results[0], sentences=NUM_SENT)
    except wikipedia.DisambiguationError as e:
        ambiguous_terms = e.options
        return wikipedia.summary(ambiguous_terms[0], sentences=NUM_SENT)
    return summary


def format_text(paragraph: str, start_idx: int, end_idx: int) -> str:
    return (
        paragraph[:start_idx]
        + "**"
        + paragraph[start_idx:end_idx]
        + "**"
        + paragraph[end_idx:]
    )


if __name__ == "__main__":
    """
    # Wikipedia Article
    """
    paragraph_slot = st.empty()
    wiki_query = st.text_input("WIKIPEDIA SEARCH TERM", "")
    question = st.text_input("QUESTION", "")

    if wiki_query:
        wiki_para = get_wiki_paragraph(wiki_query)
        paragraph_slot.markdown(wiki_para)
        # Execute question against paragraph
        if question != "":
            pipeline = get_qa_pipeline()
            try:
                answer = answer_question(pipeline, question, wiki_para)
                start_idx = answer["start"]
                end_idx = answer["end"]
                st.success(answer["answer"])
                print(f"QUESTION: {question}\nRESPONSE: {answer}")
            except Exception as e:
                print(e)
                st.warning("You must provide a valid wikipedia paragraph")
