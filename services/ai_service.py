import json
from typing import Any, Dict

import streamlit as st


CORTEX_DEFAULT_MODEL = "llama3.1-8b"

SYSTEM_PROMPT = """
You are an expert insurance AI assistant.

Your job is to analyze customer information, interactions, and transcripts
using only the evidence provided.

You must:
- Be concise and factual.
- Never invent customer information.
- Never infer missing information as fact.
- Return UNKNOWN when evidence is insufficient.
- Distinguish observed facts from recommendations.
- Use insurance terminology clearly.
"""


def _get_cortex_connection():
    return st.connection("snowflake", type="snowflake")


def query_local_llm(
    prompt: str,
    model_name: str = CORTEX_DEFAULT_MODEL,
) -> str:
    """
    Query Snowflake Cortex AI via SNOWFLAKE.CORTEX.COMPLETE.

    This replaces the previous local Ollama backend so the
    application works inside Snowflake-hosted Streamlit.
    """

    full_prompt = SYSTEM_PROMPT.strip() + "\n\n" + prompt

    try:
        conn = _get_cortex_connection()

        result = conn.query(
            "SELECT SNOWFLAKE.CORTEX.COMPLETE(?, ?) AS RESPONSE",
            params=(model_name, full_prompt),
            ttl=0,
        )

        if result.empty:
            return "UNKNOWN"

        content = result.iloc[0]["RESPONSE"]

        if not content:
            return "UNKNOWN"

        return str(content).strip()

    except Exception as e:
        return (
            f"⚠️ Snowflake Cortex AI unavailable for model "
            f"`{model_name}`. "
            f"Error: {str(e)}"
        )


def process_transcript_to_insights(
    transcript_text: str,
    model_name: str = CORTEX_DEFAULT_MODEL,
) -> Dict[str, Any]:
    """
    Transform an unstructured customer transcript into structured insights.

    Returns a dictionary with:
        sentiment
        intent
        topic
        churn_signal
        urgency
        confidence
        evidence
        status
    """

    if not transcript_text or not str(transcript_text).strip():
        return {
            "sentiment": "UNKNOWN",
            "intent": "UNKNOWN",
            "topic": "UNKNOWN",
            "churn_signal": "UNKNOWN",
            "urgency": "UNKNOWN",
            "confidence": None,
            "evidence": "Transcript is missing.",
            "status": "INSUFFICIENT_DATA",
        }

    prompt = f"""
Analyze the following insurance customer interaction transcript.

TRANSCRIPT:
{transcript_text}

Return ONLY valid JSON using exactly these fields:

{{
    "sentiment": "Positive | Neutral | Negative | UNKNOWN",
    "intent": "string or UNKNOWN",
    "topic": "string or UNKNOWN",
    "churn_signal": "High | Medium | Low | None | UNKNOWN",
    "urgency": "High | Medium | Low | UNKNOWN",
    "confidence": "number between 0 and 1, or null",
    "evidence": "short quote or factual explanation from the transcript"
}}

Rules:
1. Use only information contained in the transcript.
2. Do not hallucinate.
3. If evidence is insufficient, use UNKNOWN.
4. Confidence must be null when the assessment cannot be supported.
5. Keep evidence concise.
"""

    response = query_local_llm(
        prompt,
        model_name=model_name,
    )

    if response.startswith("⚠️"):
        return {
            "sentiment": "UNKNOWN",
            "intent": "UNKNOWN",
            "topic": "UNKNOWN",
            "churn_signal": "UNKNOWN",
            "urgency": "UNKNOWN",
            "confidence": None,
            "evidence": response,
            "status": "AI_UNAVAILABLE",
        }

    try:
        parsed = _parse_json_response(response)

        return _normalize_insight_result(parsed)

    except Exception:
        return {
            "sentiment": "UNKNOWN",
            "intent": "UNKNOWN",
            "topic": "UNKNOWN",
            "churn_signal": "UNKNOWN",
            "urgency": "UNKNOWN",
            "confidence": None,
            "evidence": "AI response could not be safely parsed.",
            "status": "INVALID_AI_RESPONSE",
        }


def _parse_json_response(response: str) -> Dict[str, Any]:
    """
    Safely parse JSON returned by the LLM.

    Handles cases where the model wraps JSON in markdown fences.
    """

    cleaned = response.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    parsed = json.loads(cleaned)

    if not isinstance(parsed, dict):
        raise ValueError("AI response is not a JSON object.")

    return parsed


def _normalize_insight_result(
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize and validate AI-generated insight values.
    """

    sentiment = str(
        result.get("sentiment", "UNKNOWN")
    ).strip()

    valid_sentiments = {
        "Positive",
        "Neutral",
        "Negative",
        "UNKNOWN",
    }

    if sentiment not in valid_sentiments:
        sentiment = "UNKNOWN"

    intent = result.get("intent", "UNKNOWN")
    topic = result.get("topic", "UNKNOWN")

    churn_signal = str(
        result.get("churn_signal", "UNKNOWN")
    ).strip()

    valid_churn = {
        "High",
        "Medium",
        "Low",
        "None",
        "UNKNOWN",
    }

    if churn_signal not in valid_churn:
        churn_signal = "UNKNOWN"

    urgency = str(
        result.get("urgency", "UNKNOWN")
    ).strip()

    valid_urgency = {
        "High",
        "Medium",
        "Low",
        "UNKNOWN",
    }

    if urgency not in valid_urgency:
        urgency = "UNKNOWN"

    confidence = result.get("confidence")

    if confidence is not None:
        try:
            confidence = float(confidence)

            if confidence > 1:
                confidence = confidence / 100

            if confidence < 0 or confidence > 1:
                confidence = None

        except (TypeError, ValueError):
            confidence = None

    evidence = result.get(
        "evidence",
        "UNKNOWN",
    )

    return {
        "sentiment": sentiment,
        "intent": intent or "UNKNOWN",
        "topic": topic or "UNKNOWN",
        "churn_signal": churn_signal,
        "urgency": urgency,
        "confidence": confidence,
        "evidence": evidence or "UNKNOWN",
        "status": "SUCCESS",
    }


def generate_customer_ai_summary(
    customer_context: str,
    model_name: str = CORTEX_DEFAULT_MODEL,
) -> str:
    """
    Generate a concise evidence-based Customer 360 summary.

    This is intentionally kept separate from transcript processing so
    customer-level summaries can later use Snowflake Customer 360 data.
    """

    if not customer_context or not customer_context.strip():
        return "UNKNOWN - No customer context is available."

    prompt = f"""
Create a concise Customer 360 summary using ONLY the information below.

CUSTOMER CONTEXT:
{customer_context}

Include:
- Customer situation
- Important policy/claim/payment signals
- Recent interaction signals
- Potential risk signals
- Recommended area of attention

Do not invent missing information.

If information is unavailable, explicitly say UNKNOWN.
"""

    return query_local_llm(
        prompt,
        model_name=model_name,
    )


def explain_next_best_action(
    customer_context: str,
    recommended_action: str,
    model_name: str = CORTEX_DEFAULT_MODEL,
) -> str:
    """
    Explain why a Next Best Action was recommended.

    The explanation must be based only on supplied evidence.
    """

    if not customer_context:
        return "UNKNOWN - Customer evidence is unavailable."

    if not recommended_action:
        return "UNKNOWN - No recommended action is available."

    prompt = f"""
Explain the following insurance Next Best Action using only the supplied
customer evidence.

CUSTOMER EVIDENCE:
{customer_context}

RECOMMENDED ACTION:
{recommended_action}

Return:
1. Why this action was recommended.
2. Which evidence supports it.
3. Any important uncertainty or missing information.

Do not invent facts.
Keep the explanation concise.
"""

    return query_local_llm(
        prompt,
        model_name=model_name,
    )
