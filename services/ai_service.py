'''import ollama

def query_local_llm(prompt: str, model_name: str = "llama3") -> str:
    """
    Sends a prompt to the local Ollama LLM and returns the response.
    Make sure Ollama is running on your machine.
    """
    try:
        response = ollama.chat(
            model=model_name, 
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert insurance AI assistant. You help employees and customers understand customer risk profiles, churn signals, policy details, and next best actions clearly and concisely based on evidence."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"⚠️ **Ollama Connection Error:** Could not connect to local model (`{model_name}`). Ensure Ollama is open and running on your PC. Error details: `{str(e)}`"

def process_transcript_to_insights(transcript_text: str, model_name: str = "llama3"):
    """
    Transforms unstructured text into structured insights as required by Section 3.
    """
    prompt = f"""
    Analyze the following customer interaction transcript and return a structured assessment:
    Transcript: "{transcript_text}"
    
    Provide your output clearly with:
    - Sentiment (Positive / Neutral / Negative / UNKNOWN)
    - Intent (e.g., Billing Inquiry, Claim Status, Cancellation Threat)
    - Topic
    - Churn Signal (High / Medium / Low / None)
    - Urgency (High / Medium / Low)
    - Confidence (Percentage)
    
    If information is missing, explicitly return UNKNOWN instead of hallucinating.
    """
    return query_local_llm(prompt, model_name=model_name)'''

import json
from typing import Any, Dict, Optional

try:
    import ollama
except ImportError:
    ollama = None


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


def query_local_llm(
    prompt: str,
    model_name: str = "llama3"
) -> str:
    """
    Query the optional local Ollama LLM.

    Ollama is treated as an optional development/local AI provider.
    The application should not fail if Ollama is unavailable.
    """

    if ollama is None:
        return (
            "⚠️ Local AI provider is unavailable. "
            "The Ollama Python package is not installed."
        )

    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        message = response.get("message", {})
        content = message.get("content")

        if not content:
            return "UNKNOWN"

        return content.strip()

    except Exception as e:
        return (
            f"⚠️ Local AI provider unavailable for model "
            f"`{model_name}`. "
            f"Error: {str(e)}"
        )


def process_transcript_to_insights(
    transcript_text: str,
    model_name: str = "llama3"
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
    Safely parse JSON returned by the local LLM.

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
    result: Dict[str, Any]
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
    model_name: str = "llama3"
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
    model_name: str = "llama3"
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