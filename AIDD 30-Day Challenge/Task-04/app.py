import chainlit as cl
import json
import os
from agent import agent
from agents import Runner

STORAGE_FILE = "storage.json"


def load_data():
    if not os.path.exists(STORAGE_FILE):
        return {"summaries": [], "quizzes": []}
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"summaries": [], "quizzes": []}


def save_data(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)


@cl.on_chat_start
async def on_chat_start():
    await cl.Message("Upload your study notes PDF to begin.").send()


@cl.on_message
async def on_message(message: cl.Message):

    # ==================================================
    # CASE 1: PDF UPLOADED
    # ==================================================
    if message.elements:
        for element in message.elements:
            if "pdf" in element.mime:
                pdf_path = element.path

                prompt = f"""
The user uploaded a PDF:

FILE PATH: {pdf_path}

1. FIRST call extract_text_from_pdf tool.
2. Then call summarize_notes tool.
3. Do NOT return raw text.  
4. Only return the final summary to the user.

IMPORTANT:
After extracting, store the text exactly as: {{ "extracted_text": "<text>" }}
"""

                result = await Runner.run(agent, input=prompt)

                summary = result.final_output or "No summary returned."

                # Save extracted text and summary
                cl.user_session.set("pdf_text", result.final_output)  # raw_output contains tool responses
                data = load_data()
                data["summaries"].append(summary)
                save_data(data)

                await cl.Message(f"**Summary:**\n{summary}").send()
                return

    # ==================================================
    # CASE 2: USER ASKS FOR QUIZ
    # ==================================================
    text = message.content.lower()

    if "quiz" in text:
        pdf_text = cl.user_session.get("pdf_text")
        data = load_data()

        if pdf_text:
            # Use extracted text (BEST)
            prompt = f"""
Create a quiz from the extracted text below.
You MUST call generate_quiz tool.

Extracted Text:
{pdf_text}
"""
        elif data["summaries"]:
            # Fallback to summary
            last_summary = data["summaries"][-1]
            prompt = f"""
Create a quiz from this summary.
You MUST call generate_quiz tool.

Summary:
{last_summary}
"""
        else:
            return await cl.Message(
                "No PDF text or summary found. Upload a PDF first."
            ).send()

        result = await Runner.run(agent, input=prompt)

        quiz = result.final_output or "No quiz generated."

        data["quizzes"].append(quiz)
        save_data(data)

        await cl.Message(f"**Quiz:**\n{quiz}").send()
        return

    # ==================================================
    # CASE 3: DEFAULT CHAT
    # ==================================================
    result = await Runner.run(agent, input=message.content)
    await cl.Message(result.final_output).send()

