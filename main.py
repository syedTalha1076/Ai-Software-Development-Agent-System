# from src.tools.tools import create_file

# path = "test2/new_test.py"
# result = create_file.invoke({
#     "path":path,
#     "content":"print('Checking again😃')"
# })

# print(result)


from src.pipelines.pipeline import run_software_pipeline


def main():

    print("=" * 60)
    print("      AI SOFTWARE DEVELOPMENT TEAM")
    print("=" * 60)

    requirements = input(
        "\nEnter your software requirements:\n> "
    )

    if not requirements.strip():
        print("Please provide software requirements.")
        return

    result = run_software_pipeline(requirements)

    print("\n" + "=" * 60)
    print("FINAL PROJECT REVIEW")
    print("=" * 60)

    print(result["final_review"])


if __name__ == "__main__":
    main()