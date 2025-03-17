import openai
from fastapi import HTTPException
import os
from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


async def summarize_text_hugging_face(text:str)->str:
    try:
       
        # Generate summary
        summary = summarizer(text, max_length=1000, min_length=2, do_sample=False)
        # print(summary[0]['summary_text'])
        return summary[0]['summary_text']
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Summarization failed: {str(e)}")

                

async def summarize_text_openAi(text: str) -> str:
    """Summarize text using OpenAI's ChatGPT."""
    try:
        
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Store the key in an environment variable

        client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Initialize the OpenAI client

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": f"Summarize this text {text}"}],
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Summarization failed: {str(e)}")
