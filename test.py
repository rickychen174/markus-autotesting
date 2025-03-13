from server.autotest_server.utils import loads_partial_json
import subprocess

result = subprocess.run(["sh", "test-files/custom_tester_llm.sh"], capture_output=True, text=True)
stdout = result.stdout

json, malformed = loads_partial_json(stdout)
print(json)
print(malformed)
