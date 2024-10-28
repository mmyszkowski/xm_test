import os
import subprocess
output_dir = os.path.join("../static")
test_suite = os.path.join("tests/robot", "test_api.robot")
os.system("pytest -v")
os.makedirs(output_dir, exist_ok=True)
subprocess.run([
    "robot",
    "--outputdir", output_dir,
    test_suite
])