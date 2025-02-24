import json
import base64
import os

input_notebook = "Homework_5_submission_patched.ipynb"
output_directory = "output_images"

with open(input_notebook, "r") as file:
    notebook = json.load(file)
    os.makedirs(output_directory, exist_ok=True)
    for cell_number, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] == "code":
            # Choosing the saved image's name
            source = cell["source"]
            if len(source) > 0 and source[0].startswith("# Question"):
                # Cell header for file names
                question_name = source[0][2:-1].replace(" ", "_")
            elif "markus_saved_image" in cell["metadata"]:
                # Cell metadata tag for saved image file name
                question_name = cell["metadata"]["markus_saved_image"]
            else:
                continue

            # Find images and save them
            image_count = 0
            for output in cell["outputs"]:
                for file_type, data in output["data"].items():
                    if "image/" in file_type:
                        ext = file_type.split("/")[-1]
                        image_filename = f"submission.{ext}"
                        os.makedirs(os.path.join(output_directory, question_name, str(image_count)), exist_ok=True)
                        image_path = os.path.join(output_directory, question_name, str(image_count), image_filename)
                        image_count += 1

                        image_data = base64.b64decode(data)
                        with open(image_path, "wb") as img_file:
                            img_file.write(image_data)

            # Save question context (source of previous cell)
            if cell_number >= 1 and notebook["cells"][cell_number - 1]["cell_type"] == "markdown":
                question_context_data = "".join(notebook["cells"][cell_number - 1]["source"])
                question_context_filename = "context.txt"
                os.makedirs(os.path.join(output_directory, question_name), exist_ok=True)
                question_context_path = os.path.join(output_directory, question_name, question_context_filename)
                with open(question_context_path, "w") as txt_file:
                    txt_file.write(question_context_data)
