import json
import subprocess

marks = {
    "name": "Custom Test 4",
    "output": "Perfect!",
    "marks_earned": 100,
    "marks_total": 100,
    "status": "pass",
    "time": 1,
}

llm_process = subprocess.run(
    [
        "python3",
        "main.py",
        "--submission_type jupyter",
        "--prompt image_analyze",
        "--scope image",
        "--assignment ./",
        '--question "Question 5b"',
        "--model openai",
        "--output stdout",
    ],
    stdout=subprocess.PIPE,
    text=True,
)

llm_output = llm_process.stdout

comments = {"overall_comment": llm_output}

print(json.dumps(marks) + json.dumps(comments))
