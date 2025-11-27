import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel
from tools import extract_text_from_pdf, summarize_notes, generate_quiz
from agents import enable_verbose_stdout_logging

enable_verbose_stdout_logging()

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

agent = Agent(
    name="Study Notes Assistant",
    model=model,
    tools=[extract_text_from_pdf, summarize_notes, generate_quiz],
    instructions="""
You are a study notes assistant.
Use extract_text_from_pdf tool when user uploads a document and return the extracted text and: 
- if user asks for summary use summarize_notes tool and
- if user asks to generate the quiz use generate_quiz tool .
""",
)

