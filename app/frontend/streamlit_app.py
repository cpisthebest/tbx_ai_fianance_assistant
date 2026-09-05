import requests
import streamlit as st


# ============================================================
# CONFIG
# ============================================================

API_URL = "http://localhost:8000/api/chat"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Finance AI Assistant",
    page_icon="💰",
    layout="wide",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f8fafc;
    }

    .title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
    }

    .subtitle {
        color: #64748b;
        margin-bottom: 25px;
    }

    .intent {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 6px 12px;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">💰 Finance AI Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions about balances, accounts, banks and transactions.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Configuration")

    api_url = st.text_input(
        "FastAPI URL",
        value=API_URL,
    )

    st.divider()

    st.subheader("Example questions")

    examples = [
        "What is my total balance?",
        "How much did I spend?",
        "Show my food expenses",
        "Find transaction UTR123456",
        "Which banks do I have?",
        "How many accounts do I have?",
        "Show my travel transactions",
    ]

    for example in examples:

        if st.button(
            example,
            use_container_width=True,
        ):

            st.session_state[
                "selected_question"
            ] = example


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "selected_question" not in st.session_state:

    st.session_state.selected_question = ""


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message["role"] == "assistant":

            intent = message.get(
                "intent"
            )

            if intent:

                st.markdown(
                    f'<span class="intent">'
                    f'Intent: {intent}'
                    f'</span>',
                    unsafe_allow_html=True,
                )


# ============================================================
# INPUT
# ============================================================

selected_question = (
    st.session_state.selected_question
)

question = st.chat_input(
    "Ask a finance question..."
)


if selected_question:

    question = selected_question

    st.session_state.selected_question = ""


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # ---------------------------------------------
    # USER MESSAGE
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # ---------------------------------------------
    # ASSISTANT MESSAGE
    # ---------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing your financial data..."
        ):

            try:

                response = requests.post(

                    api_url,

                    json={
                        "question": question
                    },

                    timeout=120,
                )

                response.raise_for_status()

                data = response.json()

                answer = data.get(
                    "answer",
                    "No answer returned.",
                )

                intent = data.get(
                    "intent",
                    "UNKNOWN",
                )

                st.markdown(answer)

                st.markdown(
                    f'<span class="intent">'
                    f'Intent: {intent}'
                    f'</span>',
                    unsafe_allow_html=True,
                )

                # -----------------------------------------
                # DEBUG / DETAILS
                # -----------------------------------------

                with st.expander(
                    "🔍 View query details"
                ):

                    st.write(
                        "Detected intent:",
                        intent,
                    )

                    sql_results = data.get(
                        "sql_results",
                        [],
                    )

                    semantic_results = data.get(
                        "semantic_results",
                        [],
                    )

                    if sql_results:

                        st.subheader(
                            "SQL Results"
                        )

                        st.json(
                            sql_results
                        )

                    if semantic_results:

                        st.subheader(
                            "Semantic Results"
                        )

                        st.json(
                            semantic_results
                        )

            except requests.exceptions.ConnectionError:

                answer = (
                    "❌ Cannot connect to the "
                    "FastAPI backend. Make sure "
                    "the API is running."
                )

                intent = "ERROR"

                st.error(answer)

            except requests.exceptions.Timeout:

                answer = (
                    "⏱️ The request timed out. "
                    "Ollama may still be processing "
                    "the query."
                )

                intent = "TIMEOUT"

                st.error(answer)

            except Exception as e:

                answer = (
                    f"❌ Error processing request: "
                    f"{str(e)}"
                )

                intent = "ERROR"

                st.error(answer)

    # ---------------------------------------------
    # SAVE ASSISTANT MESSAGE
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "intent": intent,
        }
    )
