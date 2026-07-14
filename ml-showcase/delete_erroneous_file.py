import os

erroneous_file = "python iris_predictor.py"

if os.path.exists(erroneous_file):
    try:
        os.remove(erroneous_file)
        print(f"Successfully deleted: {erroneous_file}")
    except OSError as e:
        print(f"Error deleting {erroneous_file}: {e}")
else:
    print(f"File not found: {erroneous_file}")
