import streamlit as st
from dotenv import load_dotenv
from rag.ingestion import load_and_index_pdf, load_existing_index
from rag.retrieval import build_qa_chain, ask

load_dotenv()

st.set_page_config(
    page_title="DocChat — AI Document Q&A",
    page_icon="📄",
    layout="centered",
)

st.title("DocChat")
st.caption("Upload a PDF and ask questions — powered by RAG + Groq + LLaMA 3")

# ── Sidebar: PDF upload ───────────────────────────────────────────────────────
with st.sidebar:
    st.header("Your document")
    uploaded = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded:
        with st.spinner("Indexing document..."):
            vectorstore = load_and_index_pdf(uploaded.read())
            st.session_state["chain"] = build_qa_chain(vectorstore)
        st.success(f"Ready! Ask anything about **{uploaded.name}**")

    st.divider()
    if st.button("Clear conversation"):
        st.session_state.pop("messages", None)
        st.session_state.pop("chain", None)
        st.rerun()

# ── Chat history init ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ── Render previous messages ──────────────────────────────────────────────────
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Handle new question ───────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question about your document..."):

    if "chain" not in st.session_state:
        st.warning("Please upload a PDF first.")
        st.stop()

    # Show user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask(st.session_state["chain"], prompt)

        st.markdown(result["answer"])

        if result["pages"]:
            page_list = ", ".join(f"p.{p}" for p in result["pages"])
            st.caption(f"Sources: {page_list}")

    st.session_state["messages"].append({
        "role": "assistant",
        "content": result["answer"],
    })