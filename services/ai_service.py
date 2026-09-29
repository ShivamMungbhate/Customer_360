import ollama

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
    return query_local_llm(prompt, model_name=model_name)