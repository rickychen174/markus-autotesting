import json

notebook = dict()
with open("Homework_5_test.ipynb", "r") as file:
    notebook = json.load(file)

for i, cell in enumerate(notebook["cells"]):
    notebook["cells"][i]["id"] = f"cell{i}"

with open("Homework_5_test_patched.ipynb", "w+") as file:
    json.dump(notebook, file)
