requirements:
    pip install -r "{{invocation_directory()}}\requirements.txt"

start:
    python "{{invocation_directory()}}\src\main.py"
