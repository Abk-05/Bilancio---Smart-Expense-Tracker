import os
import sys

if __name__ == "__main__":

    root_folder = os.path.dirname(os.path.dirname(__file__))

    print(f"Project root: {root_folder}")
    sys.path.insert(0, root_folder)
    print(sys.path)