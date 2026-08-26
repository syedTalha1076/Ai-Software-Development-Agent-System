# ============================================================
# AI SOFTWARE DEVELOPMENT PIPELINE
# ============================================================

from src.agents.agents import (
    build_developer_agent,
    build_execution_agent,
    build_testing_agent,
    build_debugging_agent,
    build_code_review_agent,
    build_git_agent,
    manager_chain,
    architect_chain,
    documentation_chain,
    critic_chain,
)


def run_software_pipeline(requirements: str) -> dict:

    # ========================================================
    # STATE
    # ========================================================

    state = {}

    # ========================================================
    # STEP 1 - PROJECT MANAGER
    # ========================================================

    print("\n" + "=" * 60)
    print("STEP 1 - PROJECT MANAGER IS CREATING DEVELOPMENT PLAN...")
    print("=" * 60)

    state["plan"] = manager_chain.invoke({
        "requirements": requirements
    })

    print("\nDevelopment Plan:\n")
    print(state["plan"])


    # ========================================================
    # STEP 2 - ARCHITECT
    # ========================================================

    print("\n" + "=" * 60)
    print("STEP 2 - ARCHITECT IS DESIGNING THE PROJECT...")
    print("=" * 60)

    state["architecture"] = architect_chain.invoke({
        "requirements": requirements,
        "plan": state["plan"]
    })

    print("\nArchitecture:\n")
    print(state["architecture"])


    # ========================================================
    # STEP 3 - DEVELOPER AGENT
    # ========================================================

    print("\n" + "=" * 60)
    print("STEP 3 - DEVELOPER AGENT IS BUILDING THE PROJECT...")
    print("=" * 60)

    developer_agent = build_developer_agent()

    developer_prompt = f"""
You are the main Developer Agent.

Build the software project according to the requirements,
development plan, and architecture below.

USER REQUIREMENTS:
{requirements}

DEVELOPMENT PLAN:
{state["plan"]}

ARCHITECTURE:
{state["architecture"]}

Instructions:

1. Inspect the current project workspace.
2. Create the required folders and files.
3. Implement the application.
4. Write clean and maintainable code.
5. Do not skip important files.
6. Use the available file tools to actually create the project.
7. Do not just describe the code. Actually create the files.
"""

    developer_result = developer_agent.invoke({
        "messages": [
            ("user", developer_prompt)
        ]
    })

    state["development_result"] = (
        developer_result["messages"][-1].content
    )

    print("\nDeveloper Result:\n")
    print(state["development_result"])


    # ========================================================
    # STEP 4 - CODE EXECUTION
    # ========================================================

    print("\n" + "=" * 60)
    print("STEP 4 - EXECUTION AGENT IS RUNNING THE APPLICATION...")
    print("=" * 60)

    execution_agent = build_execution_agent()

    execution_prompt = f"""
Inspect the generated project.

Requirements:
{requirements}

Architecture:
{state["architecture"]}

Your task:

1. Inspect the project files.
2. Identify the main Python entry point.
3. Run the application using the available tools.
4. Capture stdout and stderr.
5. Report whether the application starts successfully.
6. If an error occurs, clearly report the error.

Do not modify the code.
"""

    execution_result = execution_agent.invoke({
        "messages": [
            ("user", execution_prompt)
        ]
    })

    state["execution_result"] = (
        execution_result["messages"][-1].content
    )

    print("\nExecution Result:\n")
    print(state["execution_result"])


    # ========================================================
    # STEP 5 - TESTING
    # ========================================================

    print("\n" + "=" * 60)
    print("STEP 5 - TESTING AGENT IS RUNNING TESTS...")
    print("=" * 60)

    testing_agent = build_testing_agent()

    testing_prompt = f"""
You are the Testing Agent.

Inspect the generated project and run the test suite.

Project Requirements:
{requirements}

Architecture:
{state["architecture"]}

Developer Result:
{state["development_result"]}

Execution Result:
{state["execution_result"]}

Instructions:

1. Inspect the project.
2. Check whether tests exist.
3. Run pytest.
4. Analyze the test output.
5. Clearly report PASS or FAIL.
6. Include important errors if tests fail.
"""

    testing_result = testing_agent.invoke({
        "messages": [
            ("user", testing_prompt)
        ]
    })

    state["test_results"] = (
        testing_result["messages"][-1].content
    )

    print("\nTest Results:\n")
    print(state["test_results"])


    # ========================================================
    # STEP 6 - DEBUGGING
    # ========================================================

    print("\n" + "=" * 60)
    print("STEP 6 - DEBUGGING AGENT IS ANALYZING THE RESULTS...")
    print("=" * 60)

    debugging_agent = build_debugging_agent()

    debugging_prompt = f"""
You are the Debugging Agent.

Analyze the generated project and fix problems if necessary.

Requirements:
{requirements}

Test Results:
{state["test_results"]}

Execution Results:
{state["execution_result"]}

Instructions:

1. Inspect the relevant source files.
2. Analyze errors and failed tests.
3. If there are errors, identify their root cause.
4. Modify the faulty files.
5. Run the tests again.
6. Continue fixing the code until the problem is resolved
   or you determine that it cannot be fixed.

If everything already works, do not unnecessarily modify
the project.
"""

    debugging_result = debugging_agent.invoke({
        "messages": [
            ("user", debugging_prompt)
        ]
    })

    state["debugging_result"] = (
        debugging_result["messages"][-1].content
    )

    print("\nDebugging Result:\n")
    print(state["debugging_result"])


    # ========================================================
    # STEP 7 - RUN TESTS AGAIN
    # ========================================================

    print("\n" + "=" * 60)
    print("STEP 7 - TESTING AGENT IS VERIFYING THE FIX...")
    print("=" * 60)

    testing_result_after_debug = testing_agent.invoke({
        "messages": [
            (
                "user",
                """
Run the complete test suite again after the debugging changes.

Report:

- Number of tests passed
- Number of tests failed
- Important errors
- Final test status
"""
            )
        ]
    })

    state["final_test_results"] = (
        testing_result_after_debug["messages"][-1].content
    )

    print("\nFinal Test Results:\n")
    print(state["final_test_results"])


    # ========================================================
    # STEP 8 - CODE REVIEW
    # ========================================================

    print("\n" + "=" * 60)
    print("STEP 8 - CODE REVIEW AGENT IS REVIEWING THE PROJECT...")
    print("=" * 60)

    code_review_agent = build_code_review_agent()

    review_prompt = f"""
You are the Code Review Agent.

Review the completed project.

Requirements:
{requirements}

Final Test Results:
{state["final_test_results"]}

Debugging Result:
{state["debugging_result"]}

Instructions:

1. Inspect the project files.
2. Run Ruff.
3. Look for code-quality issues.
4. Look for obvious bugs.
5. Check maintainability.
6. Check whether the implementation satisfies the requirements.
7. Report all important issues.

Do not modify the code.
"""

    review_result = code_review_agent.invoke({
        "messages": [
            ("user", review_prompt)
        ]
    })

    state["code_review"] = (
        review_result["messages"][-1].content
    )

    print("\nCode Review:\n")
    print(state["code_review"])


    # ========================================================
    # STEP 9 - DOCUMENTATION
    # ========================================================

    print("\n" + "=" * 60)
    print("STEP 9 - DOCUMENTATION AGENT IS GENERATING DOCUMENTATION...")
    print("=" * 60)

    state["documentation"] = documentation_chain.invoke({
        "requirements": requirements,
        "architecture": state["architecture"],
        "test_results": state["final_test_results"],
        "code_review": state["code_review"]
    })

    print("\nDocumentation:\n")
    print(state["documentation"])


    # ========================================================
    # STEP 10 - GIT
    # ========================================================

    print("\n" + "=" * 60)
    print("STEP 10 - GIT AGENT IS SAVING THE PROJECT...")
    print("=" * 60)

    git_agent = build_git_agent()

    git_prompt = f"""
You are the Git Agent.

The software project has now been developed and reviewed.

Your tasks:

1. Check Git status.
2. Inspect the Git diff.
3. If the project contains valid changes, create a commit.
4. Use this commit message:

"Complete AI generated software project"

Do not push to GitHub.
Only create the local commit.
"""

    git_result = git_agent.invoke({
        "messages": [
            ("user", git_prompt)
        ]
    })

    state["git_result"] = (
        git_result["messages"][-1].content
    )

    print("\nGit Result:\n")
    print(state["git_result"])


    # ========================================================
    # STEP 11 - FINAL CRITIC
    # ========================================================

    print("\n" + "=" * 60)
    print("STEP 11 - FINAL CRITIC IS EVALUATING THE PROJECT...")
    print("=" * 60)

    state["final_review"] = critic_chain.invoke({
        "requirements": requirements,
        "architecture": state["architecture"],
        "test_results": state["final_test_results"],
        "code_review": state["code_review"],
        "documentation": state["documentation"]
    })

    print("\nFinal Project Review:\n")
    print(state["final_review"])


    # ========================================================
    # FINAL STATE
    # ========================================================

    print("\n" + "=" * 60)
    print("AI SOFTWARE DEVELOPMENT PIPELINE COMPLETED")
    print("=" * 60)

    return state