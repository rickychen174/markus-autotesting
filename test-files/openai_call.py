import base64

from openai import OpenAI
import glob
import os

client = OpenAI()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def prompt_compare_images(submission_image_path, solution_image_path):
    submission_image_encoded = encode_image(submission_image_path)
    solution_image_encoded = encode_image(solution_image_path)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Compare these images of graphs and"
                            "provide the differences in these elements in table format:\n"
                            "- Title\n"
                            "- Axes\n"
                            "- Scale\n"
                            "- Graph Type\n"
                            "- Font\n"
                            "- Data Points"
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{submission_image_encoded}"},
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{solution_image_encoded}"},
                    },
                ],
            }
        ],
        n=1,
    )

    return completion.choices[0].message


def prompt_analyze_image(submission_image_path, question_context):
    submission_image_encoded = encode_image(submission_image_path)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "For the Python programming question below, does the image correctly solve the problem?\n"
                            f"{question_context}"
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{submission_image_encoded}"},
                    },
                ],
            }
        ],
        n=1,
    )

    return completion.choices[0].message


def prompt_compare_images_mock(submission_image_path, solution_image_path):
    return "Comparing: " + submission_image_path + " " + solution_image_path


def prompt_analyze_image_mock(submission_image_path, question_context):
    return (
        "--Prompt--\n"
        "For the Python programming question below, does the image correctly solve the problem?\n"
        f"{question_context}\n"
        "Image: " + submission_image_path
    )


output_directory = "output_images"
for question in os.listdir(output_directory):
    for image_number in os.listdir(os.path.join(output_directory, question)):
        if image_number != "context.txt":
            submission_image_path = glob.glob(os.path.join(output_directory, question, image_number, "submission.*"))[0]
            solution_image_path = glob.glob(os.path.join(output_directory, question, image_number, "solution.*"))[0]
            print(prompt_compare_images_mock(submission_image_path, solution_image_path))

for question in os.listdir(output_directory):
    with open(os.path.join(output_directory, question, "context.txt")) as file:
        context = file.read()
        print(prompt_analyze_image_mock(os.path.join(output_directory, question, "0", "submission.png"), context))
