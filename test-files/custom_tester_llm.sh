#!/bin/bash

source ../../scripts/defaultvenv/bin/activate
cd ai-autograding-feedback
llm_output=$(../../../scripts/defaultvenv/bin/python3 main.py --submission_type jupyter --prompt image_analyze --scope image --assignment ../ --question "Question 5b" --model openai --output stdout)
escaped_llm_output=$(printf "$llm_output" | sed 's/"/\\"/g' | awk '{printf "%s\\n", $0}')
escaped_llm_output_truncated=${escaped_llm_output%\\n*}
echo "{\"overall_comment\": \"$(printf "%s" "$escaped_llm_output_truncated")\"}"