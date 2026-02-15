from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a financial research analyst. Summarize concall or business documents clearly."},
                {"role": "user", "content": f"Summarize the following document:\n\n{text[:12000]}"}
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI SUMMARY ERROR:", str(e))
        return "AI summary failed. Check backend logs."
