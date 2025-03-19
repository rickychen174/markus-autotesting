#!/bin/bash

source ../../scripts/defaultvenv/bin/activate
cd ai-autograding-feedback
llm_output=$(../../../scripts/defaultvenv/bin/python3 main.py --submission_type jupyter --prompt image_analyze --scope image --assignment ../ --question "Question 5b" --model openai --output stdout)
escaped_llm_output=$(echo "$llm_output" | sed 's/"/\\"/g')
echo {\"overall_comment\": \"${escaped_llm_output}\"}