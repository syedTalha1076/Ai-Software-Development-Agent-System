# Ai-Software-Development-Agent-System

# ⚡ DevForge AI

**An AI-powered software development team that turns a plain-English requirement into a fully planned, built, tested, reviewed, documented, and committed software project.**

Built by **Syed Talha Ali Shah** — Computer Systems Engineering, UET Peshawar

---

## Overview

DevForge AI is a multi-agent software delivery pipeline. You describe what you want built in a Streamlit UI, and a chain of specialized LLM agents — a project manager, architect, developer, execution runner, tester, debugger, code reviewer, documentation writer, Git handler, and a final critic — work through the project end to end inside an isolated workspace, with no manual handoffs between stages.

## How the Pipeline Works

Each run passes a shared `state` dict through 11 stages:

| Stage | Role | What it does |
|---|---|---|
| 1 | **Project Manager** | Turns requirements into a structured development plan (objectives, functional/non-functional requirements, tech stack, tasks, testing needs, project structure). |
| 2 | **Architect** | Designs the technical architecture: stack, folder structure, components, APIs, database design, dependencies, build sequence. |
| 3 | **Developer Agent** | Uses file tools (`create_file`, `read_file`, `update_file`, `delete_file`, `list_files`) to actually generate the project inside a sandboxed workspace. |
| 4 | **Execution Agent** | Locates the entry point and runs the app via `run_python`, capturing stdout/stderr. |
| 5 | **Testing Agent** | Runs `pytest` against the generated project and reports pass/fail. |
| 6 | **Debugging Agent** | Diagnoses failures, edits the faulty files, and iterates until tests pass or the issue is confirmed unfixable. |
| 7 | **Testing Agent (re-run)** | Re-runs the full test suite after debugging to verify the fix. |
| 8 | **Code Review Agent** | Runs `ruff` and checks code quality, bugs, and requirement coverage. |
| 9 | **Documentation Agent** | Generates full project docs: overview, features, install/config/usage, structure, testing, deployment notes. |
| 10 | **Git Agent** | Checks `git status`/`diff` and creates a local commit (`"Complete AI generated software project"`) — never pushes. |
| 11 | **Final Critic** | Scores the finished project out of 10 with strengths, problems, recommended improvements, and a final verdict. |

The Streamlit frontend visualizes the first 10 of these as an animated, theme-colored progress tracker while the pipeline runs in the background.

## Features

- 🧠 **Multi-agent pipeline** — LangChain agents (`create_agent`) backed by Groq's `openai/gpt-oss-120b` model, each scoped to only the tools it needs.
- 🔒 **Sandboxed workspace** — all agent file operations are confined to `generated_projects/` via path-traversal protection (`safe_path`).
- 🎨 **5 selectable UI themes** (Nebula Purple, Midnight Ocean, Emerald Tech, Sunset Forge, Light Studio) with animated gradients and a live, color-matched progress bar.
- 📊 **Real-time build view** — animated step tracker + percentage progress while the AI team works.
- 🗂️ **Tabbed results** — Final Review, Architecture, Development, Execution, Tests, Debugging, Code Review, Documentation, Git, and Plan, all in one place.
- 🧪 **Built-in QA loop** — tests run, failures get debugged, tests run again, before anything is reviewed or documented.

## Tech Stack

- **Frontend:** Streamlit
- **Orchestration:** LangChain (`create_agent`), LangChain Core (prompt templates, output parsers)
- **LLM:** Groq — `openai/gpt-oss-120b` via `langchain_groq.ChatGroq`
- **Tooling:** Python `subprocess` for `pytest`, `ruff`, and `git`
- **Config:** `python-dotenv`

## Project Structure

├── app.py # Streamlit frontend
├── src/
│ ├── agents/
│ │ ├── init.py
│ │ └── agents.py # Agent builders + LLM chains (manager, architect, docs, critic)
│ ├── tools/
│ │ ├── init.py
│ │ └── tools.py # File ops, run_python, run_tests, run_ruff, git tools
│ └── pipelines/
│ ├── init.py
│ └── pipeline.py # run_software_pipeline — orchestrates all 11 stages
├── generated_projects/ # Sandboxed workspace where AI-built projects are created
└── .env # GROQ_API_KEY (not committed)