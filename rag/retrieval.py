from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS

chat_history = []

def build_qa_chain(vectorstore: FAISS):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2,
    )
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )
    return {"llm": llm, "retriever": retriever}


def ask(chain: dict, question: str) -> dict:
    global chat_history

    retriever = chain["retriever"]
    llm = chain["llm"]

    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)

    history_text = ""
    for human, ai in chat_history[-4:]:
        history_text += f"User: {human}\nAssistant: {ai}\n"

    prompt = f"""You are a helpful assistant. Answer based only on the context below.
If the answer is not in the context, say "I don't have that information in the document."

Context:
{context}

{history_text}User: {question}
Assistant:"""

    response = llm.invoke(prompt)
    answer = response.content

    chat_history.append((question, answer))

    pages = sorted(set(
        doc.metadata.get("page", "?") for doc in docs
    ))
    return {"answer": answer, "pages": pages}