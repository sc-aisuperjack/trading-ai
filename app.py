import streamlit as st

from data import MANAGERS, METRICS, CITATIONS
from logic import monday_brief, chat_answer, meeting_answer
from llm import llm_provider


st.set_page_config(
    page_title="Trading AI Assistant",
    layout="wide",
)


st.title("Trading AI Assistant")

st.write(
    "Prototype for proactive trading briefs, Teams-based questions, "
    "meeting support, agent orchestration, source-grounded answers, and citation checks."
)


st.sidebar.title("Navigation")

manager_id = st.sidebar.selectbox(
    "Trading manager",
    list(MANAGERS.keys()),
    format_func=lambda x: MANAGERS[x]["name"],
)

manager = MANAGERS[manager_id]

page = st.sidebar.radio(
    "Surface",
    [
        "Dashboard",
        "Monday brief",
        "Teams chat",
        "Meeting agent",
        "Architecture",
    ],
)

st.sidebar.divider()
st.sidebar.caption(f"LLM: {llm_provider()}")


def render_result(result: dict):
    st.subheader(result["title"])
    st.info(result["summary"])

    st.markdown("### Teams-ready answer")

    st.text_area(
        label="Generated answer",
        value=result["answer"],
        height=280,
        disabled=True,
    )

    if result["passed"]:
        st.success("Citation guard passed. Numeric claims are grounded.")
    else:
        st.error(f"Citation guard blocked missing values: {', '.join(result['missing'])}")

    with st.expander("Agent trace", expanded=True):
        for step in result["trace"]:
            st.markdown(f"**{step['agent']}**")
            st.caption(step["what_it_did"])

    with st.expander("Citations", expanded=True):
        for c in CITATIONS:
            st.markdown(f"**{c['claim']}**: {c['value']}")
            st.caption(f"{c['source']} → {c['field']}")


if page == "Dashboard":
    st.header("Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Revenue",
            value=METRICS["revenue"],
            delta="-8.4%",
            delta_color="normal",
        )

    with col2:
        st.metric(
            label="Conversion",
            value=METRICS["conversion"],
            delta="-0.6 pp",
            delta_color="normal",
        )

    with col3:
        st.metric(
            label="Stock availability",
            value=METRICS["stock"],
            delta="-8.0 pp",
            delta_color="normal",
        )

    with col4:
        st.metric(
            label="Competitor price index",
            value=METRICS["competitor_index"],
            delta="+8.0%",
            delta_color="inverse",
        )

    st.divider()

    st.subheader("Current category")
    st.write(f"{METRICS['market']} {METRICS['category']}")

    st.subheader("Risk summary")
    st.write(
        f"{METRICS['category']} is under trading pressure. "
        f"Revenue is {METRICS['revenue']}, down {METRICS['revenue_change']} week on week. "
        f"Conversion has fallen from {METRICS['previous_conversion']} to {METRICS['conversion']}, "
        f"a drop of 0.6 percentage points. "
        f"Stock availability is {METRICS['stock']}, compared with the target of {METRICS['stock_target']}, "
        f"leaving a gap of {METRICS['stock_gap']}. "
        f"The competitor price index is {METRICS['competitor_index']}, meaning the category is around "
        f"{METRICS['competitor_premium']} above the competitor benchmark."
    )

    st.subheader("Next actions")
    st.write(
        "Review low-availability best sellers, assess tactical pricing options where competitor pressure is highest, "
        "and prioritise replenishment before the next trading review."
    )


elif page == "Monday brief":
    st.header("Proactive Monday brief")
    st.caption("Simulates the 07:00 Teams message generated for a trading manager.")

    if st.button("Generate Monday brief", type="primary"):
        render_result(monday_brief(manager))


elif page == "Teams chat":
    st.header("Teams chat")
    st.caption("Ask an ad-hoc trading question. The answer is checked against citations before display.")

    question = st.text_input(
        "Ask a trading question",
        "Why did dresses underperform this week?",
    )

    quick = st.selectbox(
        "Quick questions",
        [
            "Why did dresses underperform this week?",
            "Are we losing because of price or stock?",
            "Should we use markdowns and what is the margin risk?",
            "What will revenue be next week?",
        ],
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Ask custom question", type="primary"):
            render_result(chat_answer(question))

    with col2:
        if st.button("Ask quick question"):
            render_result(chat_answer(quick))


elif page == "Meeting agent":
    st.header("Meeting agent")
    st.caption("Simple simulation of a Teams meeting question answered by the assistant.")

    meeting_question = st.text_input(
        "Live meeting question",
        "Are we losing because of price or stock?",
    )

    if st.button("Answer meeting question", type="primary"):
        render_result(meeting_answer(meeting_question))


elif page == "Architecture":
    st.header("Architecture")

    st.code(
        """
Teams / Outlook
   ↓
Power Automate / Teams Bot
   ↓
Azure Function or Container App
   ↓
Small Agentic Orchestrator
   ↓
Existing trading APIs + competitor feed
   ↓
Optional OpenAI / Azure OpenAI
   ↓
Citation Guard
   ↓
Teams answer with source links
        """,
        language="text",
    )

    st.subheader("Prototype structure")

    st.write(
        "This prototype demonstrates the core workflow in a deliberately small form. "
        "In production, the same approach would run on Azure Functions or Container Apps, use Azure OpenAI, "
        "use Azure AI Search for retrieval, store audit logs in Cosmos DB, and post responses through Teams or Power Automate."
    )

    st.subheader("OpenAI setup")

    st.code(
        """
USE_OPENAI=true
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
        """,
        language="bash",
    )