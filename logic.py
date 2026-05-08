from data import METRICS, CITATIONS
from guard import citation_guard, allowed_values
from llm import ask_openai, openai_enabled


def agent_trace(surface: str) -> list[dict]:
    return [
        {
            "agent": "Orchestrator",
            "what_it_did": f"Selected the {surface} workflow.",
        },
        {
            "agent": "Retrieval Agent",
            "what_it_did": "Loaded business rules and source metadata.",
        },
        {
            "agent": "Metric Agent",
            "what_it_did": "Read approved trading metrics from existing API mock.",
        },
        {
            "agent": "Root Cause Agent",
            "what_it_did": "Detected stock gap, conversion decline, and competitor price pressure.",
        },
        {
            "agent": "Action Agent",
            "what_it_did": "Generated practical trading actions.",
        },
        {
            "agent": "Citation Guard",
            "what_it_did": "Checked numeric claims before the answer is shown.",
        },
    ]


def monday_brief(manager: dict) -> dict:
    answer = (
        f"Good morning {manager['name']},\\n\\n"
        f"Here is your Monday trading brief for {METRICS['market']} {METRICS['category']}.\\n\\n"
        f"Headline:\\n"
        f"Revenue is {METRICS['revenue']}, down {METRICS['revenue_change']} week on week. "
        f"Conversion fell from {METRICS['previous_conversion']} to {METRICS['conversion']}. "
        f"Stock availability is {METRICS['stock']} against a target of {METRICS['stock_target']}.\\n\\n"
        f"Likely root cause:\\n"
        f"The issue appears to be a combination of stock availability and competitor pricing pressure. "
        f"Stock is {METRICS['stock_gap']} below target. "
        f"The competitor price index is {METRICS['competitor_index']}, meaning the category is around "
        f"{METRICS['competitor_premium']} above competitor benchmark.\\n\\n"
        f"Suggested actions:\\n"
        f"1. Review low-availability best sellers before the mid-week trade review.\\n"
        f"2. Check tactical markdowns where competitor pressure is strongest.\\n"
        f"3. Protect margin because current gross margin is {METRICS['gross_margin']} and markdown rate is {METRICS['markdown_rate']}."
    )

    passed, missing = citation_guard(answer, CITATIONS)

    return {
        "title": "Monday proactive brief",
        "summary": f"{METRICS['category']} needs action. Revenue is {METRICS['revenue']} and down {METRICS['revenue_change']}.",
        "answer": answer,
        "passed": passed,
        "missing": missing,
        "trace": agent_trace("Monday brief"),
    }


def chat_answer(question: str) -> dict:
    q = question.lower()

    if openai_enabled():
        draft = ask_openai(
            task="Teams chat answer",
            question=question,
            metrics=METRICS,
            allowed_values=allowed_values(CITATIONS),
        )
        if draft:
            answer = draft
        else:
            answer = fallback_answer(q)
    else:
        answer = fallback_answer(q)

    passed, missing = citation_guard(answer, CITATIONS)

    return {
        "title": "Teams chat answer",
        "summary": "Grounded answer generated from approved metric values.",
        "answer": answer,
        "passed": passed,
        "missing": missing,
        "trace": agent_trace("Teams chat"),
    }


def meeting_answer(question: str) -> dict:
    result = chat_answer(question)
    result["title"] = "Meeting agent answer"
    result["summary"] = "Meeting agent answered using the same grounded tool route."
    result["trace"] = agent_trace("Meeting agent")
    return result


def fallback_answer(q: str) -> str:
    if "forecast" in q or "next week" in q:
        return (
            "I cannot give a reliable revenue forecast from the approved sources. "
            "A future revenue number requires an approved forecasting model."
        )

    if "price" in q and "stock" in q:
        return (
            f"Both are contributing, but stock is the first operational fix. "
            f"Stock availability is {METRICS['stock']} against a target of {METRICS['stock_target']}. "
            f"The competitor price index is {METRICS['competitor_index']}, around {METRICS['competitor_premium']} above benchmark. "
            f"Conversion also fell from {METRICS['previous_conversion']} to {METRICS['conversion']}."
        )

    if "margin" in q or "markdown" in q:
        return (
            f"Markdowns should be selective. Gross margin is {METRICS['gross_margin']} and markdown rate is {METRICS['markdown_rate']}. "
            f"Because the competitor price index is {METRICS['competitor_index']}, tactical markdowns may help, "
            f"but only on high-traffic SKUs where conversion is weak."
        )

    return (
        f"{METRICS['category']} underperformed because revenue is {METRICS['revenue']}, down {METRICS['revenue_change']}, "
        f"while conversion fell from {METRICS['previous_conversion']} to {METRICS['conversion']}. "
        f"The likely drivers are stock availability at {METRICS['stock']} and competitor price index at {METRICS['competitor_index']}."
    )
