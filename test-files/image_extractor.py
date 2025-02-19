import json
import base64
import os

input_notebook = "Homework_5_submission_patched.ipynb"
output_directory = "output_images"

with open(input_notebook, "r") as file:
    notebook = json.load(file)
    os.makedirs(output_directory, exist_ok=True)
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            source = cell["source"]
            if len(source) > 0 and source[0].startswith("# Question"):
                # Cell header for file names
                image_name = source[0][2:-1].replace(" ", "_")
            elif "markus_saved_image" in cell["metadata"]:
                # Cell metadata tag for saved image file name
                image_name = cell["metadata"]["markus_saved_image"]
            else:
                image_name = "image"

            image_count = 0
            for output in cell["outputs"]:
                for file_type, data in output["data"].items():
                    if "image/png" in file_type:
                        ext = file_type.split("/")[-1]
                        image_filename = f"{image_name}_{image_count}.{ext}"
                        image_path = os.path.join(output_directory, image_filename)
                        image_count += 1

                        image_data = base64.b64decode(data)
                        with open(image_path, "wb") as img_file:
                            img_file.write(image_data)
