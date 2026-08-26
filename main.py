from src.tools.tools import create_file

path = "test2/new_test.py"
result = create_file.invoke({
    "path":path,
    "content":"print('Checking again😃')"
})

print(result)