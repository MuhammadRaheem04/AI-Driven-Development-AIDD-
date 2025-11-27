
# Role: Senior Python AI Engineer

**Objective:**
Build a **"Study Notes Summarizer & Quiz Generator Agent"** using Chainlit, the `openai-agents` SDK, and the Gemini model integrated with the Context7 MCP server.

## 1. Project Overview

The goal is to develop an **AI-powered academic assistant** that can:

* Summarize uploaded **PDF study notes** into clear, concise summaries.
* Generate **quizzes (MCQs or mixed)** based on the original study material.

**Key Features:**

* **UI:** Chainlit (modern, responsive interface for students).
* **Model:** Google Gemini model `gemini-2.0-flash` (via OpenAI Agents SDK).
* **Tools:**

  * **PyPDF** for PDF text extraction.
  * **Context7 MCP Server** to provide `openai-agents` tools.
* **Memory:** Local JSON storage for saving recent uploads, summaries, and quiz history.

## 2. Critical Technical Constraints

**You must adhere to the following strict configuration rules:**

1. **Zero-Bloat Protocol (CRITICAL):**

   * **No extra features or UI complexity** unless specified.
   * **Focus strictly on integration** between Chainlit, PyPDF, and the `openai-agents` SDK.
   * **No hallucinated code** — only use official SDK and PyPDF syntax.

2. **API Configuration:**

   * Use **OpenAI Agents SDK** configured for **Gemini**.
   * **Base URL:** `https://generativelanguage.googleapis.com/v1beta/openai/`
   * **API Key:** Load `GEMINI_API_KEY` from environment variables.
   * **Model:** `OpenaiChatCompletionModel` configured for `gemini-2.0-flash`.

3. **SDK Specificity:**
   Use the **`openai-agents` SDK**, *not* the standard `openai` package.

4. **Error Recovery Protocol:**

   * If encountering `SyntaxError`, `ImportError`, or `AttributeError`, **STOP**.
   * Do **not guess fixes** — re-run the `get-library-docs` or `resolve-library-id` MCP tool to confirm correct syntax.

5. **Dependency Management:**

   * Use **uv** for dependency management.
   * No redundant installs.
   * Verify all dependencies in `pyproject.toml` before installation.

## 3. Architecture & File Structure

*Note: The current directory is the project root. Do not create a subfolder named `summarizer`.*

```text
.
├── .env                       # Environment variables (GEMINI_API_KEY)
├── tools.py                   # Tool functions for PDF extraction, summarization, and quiz generation
├── agent.py                   # Agent setup, model configuration, and tool registration
├── app.py                     # Chainlit UI & Event Handlers
├── storage.json               # Local JSON for saving summaries and quiz data
└── pyproject.toml             # UV Config
```

## 4. Implementation Steps

### Step 1: Documentation & Pattern Analysis

**Before coding, verify SDK patterns.**

1. **Action:** Use MCP tool `get-library-docs` or `resolve-library-id` to fetch docs for:

   * `openai-agents` SDK
   * PyPDF
2. **Analyze:** Confirm correct methods for:

   * Creating and registering tools.
   * Using `OpenaiChatCompletionModel` for Gemini.
   * Extracting text from PDFs using PyPDF.
   * Handling agent responses (non-streaming).


### Step 2: Tool Implementation (`tools.py`)

Implement the following **tools** using the correct `openai-agents` SDK format (decorator or class-based depending on docs).

**Functions:**

1. `extract_text_from_pdf(file_path: str) -> str`

   * Use **PyPDF** to extract text from the uploaded PDF.
   * Handle `FileNotFoundError` and empty PDFs safely.

2. `summarize_notes(text: str) -> str`

   * Pass extracted text to the Gemini model for summarization.
   * Return a concise, academic-style summary.

3. `generate_quiz(text: str, quiz_type: str = "MCQ") -> dict`

   * Generate questions and answers from the **original PDF text**, not the summary.
   * Support:

     * `"MCQ"` quizzes (multiple choice)
     * `"mixed"` quizzes (MCQs + short answers)

4. (Optional) `save_summary_and_quiz(summary: str, quiz: dict)`

   * Save results into `storage.json` for persistence.


### Step 3: Agent Configuration (`agent.py`)

1. Initialize the Gemini client using the **Base URL**.
2. Configure the `OpenaiChatCompletionModel` for `gemini-2.0-flash`.
3. Import and **bind tools** (`extract_text_from_pdf`, `summarize_notes`, `generate_quiz`) to the agent.
4. **System Prompt:**

   ```
   You are a helpful study assistant.
   - When a user uploads a PDF, summarize it concisely.
   - When asked to create a quiz, generate questions from the full content.
   - Always maintain academic clarity and coherence.
   ```


### Step 4: UI & Application Logic (`app.py`)

Integrate the agent with **Chainlit**.

**UI Flow:**

* **File Upload Section:** User uploads a PDF.
* **Summarize Button:** Calls the `summarize_notes` tool.
* **Quiz Button:** Calls `generate_quiz` tool.
* Display results using cards or containers (based on user preference).

**Event Handlers:**

* `@cl.on_chat_start`:
  Initialize the agent and send a static welcome message —
  *"Welcome! Upload your study notes PDF to get started."*

* `@cl.on_message`:

  * Handle user inputs.
  * Route actions (Summarize / Quiz generation).
  * Await complete responses (non-streaming).
  * Display final outputs using `cl.Message().send()`.


### Step 5: Environment & Dependencies

**`.env`**

```
GEMINI_API_KEY=your_api_key_here
```

**Dependencies (to include in `pyproject.toml`):**

* `openai-agents`
* `chainlit`
* `PyPDF2`
* `uvicorn`
* `python-dotenv`
* `context7` (if needed for MCP server connection)

**Smart Install:**
If dependencies are already installed, **do not reinstall.**

## 5. Testing Scenarios

1. **PDF Upload & Summarization:**
   Upload a study notes PDF → Text extracted → Summary displayed.

2. **Quiz Generation (MCQ):**
   Click “Create Quiz” → Agent generates 5+ MCQs based on the PDF content.

3. **Mixed Quiz Generation:**
   User selects “mixed” quiz → Agent returns both MCQs and short-answer questions.

4. **Persistence Test:**
   Restart app → Previously generated summaries and quizzes remain stored in `storage.json`.