import os
import sys

if __name__ == "__main__":
    current_folder = os.path.dirname(__file__)
    print(f"Project root: {current_folder}")
    sys.path.insert(0,current_folder)
    print(sys.path)