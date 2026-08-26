from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

from src.tools.tools import (
    create_file,
    read_file,
    update_file,
    delete_file,
    list_files,
    run_python,
    run_tests,
    run_ruff,
    git_status,
    git_diff,
    git_commit,
)


load_dotenv()


# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# ============================================================
# 1st Agent : Developer Agent
# ============================================================

def build_developer_agent():

    return create_agent(
        model=llm,
        tools=[
            create_file,
            read_file,
            update_file,
            delete_file,
            list_files,
        ],
    )


# ============================================================
# 2nd Agent : Code Execution Agent
# ============================================================

def build_execution_agent():

    return create_agent(
        model=llm,
        tools=[
            list_files,
            read_file,
            run_python,
        ],
    )


# ============================================================
# 3rd Agent : Testing Agent
# ============================================================

def build_testing_agent():

    return create_agent(
        model=llm,
        tools=[
            list_files,
            read_file,
            run_tests,
        ],
    )


# ============================================================
# 4th Agent : Debugging Agent
# ============================================================

def build_debugging_agent():

    return create_agent(
        model=llm,
        tools=[
            list_files,
            read_file,
            update_file,
            run_python,
            run_tests,
        ],
    )


# ============================================================
# 5th Agent : Code Review Agent
# ============================================================

def build_code_review_agent():

    return create_agent(
        model=llm,
        tools=[
            list_files,
            read_file,
            run_ruff,
        ],
    )


# ============================================================
# 6th Agent : Git Agent
# ============================================================

def build_git_agent():

    return create_agent(
        model=llm,
        tools=[
            git_status,
            git_diff,
            git_commit,
        ],
    )


# ============================================================
# Project Manager Chain
# ============================================================

manager_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an experienced software project manager.

Your job is to analyze the user's software requirements
and create a clear development plan.

Break the project into small, logical tasks.

Include:

- Project objective
- Functional requirements
- Non-functional requirements
- Required technologies
- Development tasks
- Testing requirements
- Expected project structure

Do NOT write implementation code.
Focus only on planning.
"""
    ),

    (
        "human",
        """
Create a development plan for the following software project:

{requirements}
"""
    ),
])


manager_chain = (
    manager_prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# Architect Chain
# ============================================================

architect_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a senior software architect.

Design a complete architecture based on the project
requirements and development plan.

Include:

- Technology stack
- Project architecture
- Folder structure
- Components
- APIs if required
- Database design if required
- Dependencies
- Implementation sequence

Do NOT write the complete implementation.

Your output will be given to a Developer Agent.
"""
    ),

    (
        "human",
        """
PROJECT REQUIREMENTS:

{requirements}


DEVELOPMENT PLAN:

{plan}


Create an implementation-ready architecture.
"""
    ),
])


architect_chain = (
    architect_prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# Documentation Chain
# ============================================================

documentation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a professional software documentation engineer.

Generate clear documentation for the completed software.

Include:

- Project overview
- Features
- Technology stack
- Installation
- Configuration
- Usage
- Project structure
- Testing
- Deployment
- Important notes
"""
    ),

    (
        "human",
        """
PROJECT REQUIREMENTS:

{requirements}


ARCHITECTURE:

{architecture}


TEST RESULTS:

{test_results}


CODE REVIEW:

{code_review}


Generate the final project documentation.
"""
    ),
])


documentation_chain = (
    documentation_prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# Final Review / Critic Chain
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a strict senior software engineer and code reviewer.

Evaluate the completed software project.

Check:

- Requirement completion
- Architecture
- Implementation
- Testing
- Code quality
- Maintainability
- Security
- Documentation

Respond in the following format:

Score: X/10

Strengths:
- ...
- ...

Problems:
- ...
- ...

Recommended Improvements:
- ...
- ...

Final Verdict:
...
"""
    ),

    (
        "human",
        """
PROJECT REQUIREMENTS:

{requirements}


ARCHITECTURE:

{architecture}


TEST RESULTS:

{test_results}


CODE REVIEW:

{code_review}


DOCUMENTATION:

{documentation}

Evaluate the project strictly.
"""
    ),
])


critic_chain = (
    critic_prompt
    | llm
    | StrOutputParser()
)