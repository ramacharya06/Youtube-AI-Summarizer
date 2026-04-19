import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage
from dotenv import load_dotenv
from get_transcript import get_transcript

load_dotenv()

MAX_CHARS = 12000  # keep within free-tier token limits


def summarize(video_url: str) -> tuple[str, str, bool]:
    """Fetch transcript and return an AI summary.

    Returns:
        summary (str)       – the generated summary text
        transcript (str)    – the (possibly truncated) transcript
        truncated (bool)    – True if the transcript was truncated
    """
    transcript = get_transcript(video_url)
    truncated = False
    if len(transcript) > MAX_CHARS:
        transcript = transcript[:MAX_CHARS]
        truncated = True

    prompt = f"""Summarize this YouTube video transcript in a clear, structured format.

Transcript:
{transcript}

Provide:
1. A concise 2-3 paragraph summary
2. Key topics covered (bullet points)
3. Main takeaways (numbered list)
4. Whether the video is worth watching and for whom

Keep it concise but informative."""

    api_key = os.getenv("YOUR_GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        google_api_key=api_key,
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    summary = response.content[0]["text"] if isinstance(response.content, list) else response.content
    return summary, transcript, truncated


def main():
    """CLI entrypoint — asks for a URL and prints the summary."""
    video_url = input("Enter the video URL: ")
    print("Fetching transcript…")
    summary, _, truncated = summarize(video_url)
    if truncated:
        print(f"(Transcript truncated to {MAX_CHARS:,} chars)")
    print("\n── Summary ──────────────────────────────────────────")
    print(summary)


if __name__ == "__main__":
    main()
