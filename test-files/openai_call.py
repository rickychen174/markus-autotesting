import base64

from openai import OpenAI
import glob
import os

client = OpenAI()


# Function to encode the image
def encode_image(image_path: os.PathLike):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def prompt_compare_images(submission_image_path: os.PathLike, solution_image_path: os.PathLike):
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


def prompt_analyze_image(submission_image_paths: list[os.PathLike], question_context: str):
    content = [
        {
            "type": "text",
            "text": (
                "For the Python programming question below, do these images correctly solve the problem?\n"
                f"{question_context}"
            ),
        },
    ]
    image_attachments = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image}"},
        }
        for image in submission_image_paths
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": content + image_attachments,
            }
        ],
        n=1,
    )

    return completion.choices[0].message


def prompt_compare_images_mock(submission_image_path, solution_image_path):
    return "Comparing: " + submission_image_path + " " + solution_image_path


def prompt_analyze_image_mock(submission_image_paths: list[os.PathLike], question_context: str):
    return (
        "--Prompt--\n"
        "For the Python programming question below, do these images correctly solve the problem?\n"
        f"{question_context}\n"
        "Images: " + str(submission_image_paths)
    )


output_directory = "output_images"
for question in os.listdir(output_directory):
    for image_number in os.listdir(os.path.join(output_directory, question)):
        if image_number != "context.txt":
            submission_images = glob.glob(os.path.join(output_directory, question, image_number, "submission.*"))
            if len(submission_images) == 0:
                raise FileNotFoundError(f"Submission file for `{question}` not found")
            solution_images = glob.glob(os.path.join(output_directory, question, image_number, "solution.*"))
            if len(solution_images) == 0:
                raise FileNotFoundError(f"Solution file for `{question}` not found")

            submission_image = glob.glob(os.path.join(output_directory, question, image_number, "submission.*"))[0]
            solution_image = glob.glob(os.path.join(output_directory, question, image_number, "solution.*"))[0]
            print(prompt_compare_images_mock(submission_image, solution_image))

for question in os.listdir(output_directory):
    with open(os.path.join(output_directory, question, "context.txt")) as file:
        context = file.read()
        submission_image_paths = [
            os.path.join(output_directory, question, i, "submission.png")
            for i in os.listdir(os.path.join(output_directory, question))
            if i != "context.txt"
        ]

        print(prompt_analyze_image_mock(submission_image_paths, context))
