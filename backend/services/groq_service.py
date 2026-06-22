"""
groq_service.py — Groq LLM Transcript Classification

This is the SECOND LLM in our system.
- LLM #1 (inside Vapi) handles the real-time conversation.
- LLM #2 (this one, Groq) analyzes the transcript AFTER the call.

WHY GROQ?
- It's free (generous free tier)
- It uses LLaMA 3.3-70B — a powerful open-source model
- It's fast (Groq's LPU hardware makes inference ~10x faster)

WHAT IT DOES:
- Takes the full call transcript as input
- Reads the conversation and decides:
  QUALIFIED → person wants to buy/sell
  NOT_INTERESTED → person said no
  FAILED → call was unclear or disconnected
"""

from groq import AsyncGroq
from config import settings


# The classification prompt — this is where the magic happens
CLASSIFICATION_PROMPT = """You are analyzing a real estate lead qualification call transcript.
Based on the conversation, classify the lead as exactly one of:

QUALIFIED - person expressed interest in buying or selling property
NOT_INTERESTED - person declined or showed no interest
FAILED - call was unclear, disconnected, or inconclusive

Transcript:
{transcript}

Respond with ONLY one word: QUALIFIED, NOT_INTERESTED, or FAILED"""


async def classify_transcript(transcript: str) -> str:
    """
    Send a call transcript to Groq LLaMA and get a classification.

    Args:
        transcript: The full conversation text from the Vapi call

    Returns:
        One of: "QUALIFIED", "NOT_INTERESTED", "FAILED"
    """
    # Handle empty or missing transcripts
    if not transcript or len(transcript.strip()) < 10:
        print("⚠️ Transcript too short or empty — marking as FAILED")
        return "FAILED"

    # Create the Groq client
    client = AsyncGroq(api_key=settings.GROQ_API_KEY)

    try:
        # Send the transcript to Groq's LLaMA model
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Free tier model
            messages=[
                {
                    "role": "user",
                    "content": CLASSIFICATION_PROMPT.format(transcript=transcript)
                }
            ],
            temperature=0,      # 0 = deterministic (same input → same output)
            max_tokens=10,       # We only need one word back
        )

        # Extract the classification from the response
        result = response.choices[0].message.content.strip().upper()

        # Validate the response is one of our expected values
        valid_outcomes = ["QUALIFIED", "NOT_INTERESTED", "FAILED"]
        if result not in valid_outcomes:
            print(f"⚠️ Unexpected Groq response: '{result}' — defaulting to FAILED")
            return "FAILED"

        print(f"🤖 Groq classification: {result}")
        return result

    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return "FAILED"
