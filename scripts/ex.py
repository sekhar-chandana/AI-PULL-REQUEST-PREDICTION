import os
import joblib

print("=" * 70)
print("CHECKING PROJECT PATHS")
print("=" * 70)

# ---------------------------------------------------
# Current Working Directory
# ---------------------------------------------------

print("\nCurrent Working Directory:")
print(os.getcwd())

# ---------------------------------------------------
# Script Directory
# ---------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("\nScript Directory:")
print(SCRIPT_DIR)

# ---------------------------------------------------
# Project Directory
# ---------------------------------------------------

PROJECT_DIR = os.path.abspath(
    os.path.join(
        SCRIPT_DIR,
        ".."
    )
)

print("\nProject Directory:")
print(PROJECT_DIR)

# ---------------------------------------------------
# Possible Model Directories
# ---------------------------------------------------

possible_dirs = [

    os.path.join(PROJECT_DIR, "Models"),

    os.path.join(SCRIPT_DIR, "Models")

]

print("\nSearching for Models Folder...\n")

for folder in possible_dirs:

    print(folder)

    if os.path.exists(folder):

        print("  FOUND")

        files = os.listdir(folder)

        if len(files):

            print("  Files:")

            for f in files:

                print("   ", f)

        else:

            print("  Folder is Empty")

    else:

        print("  NOT FOUND")

# ---------------------------------------------------
# Try Loading Files
# ---------------------------------------------------

print("\n")
print("=" * 70)
print("LOADING FILES")
print("=" * 70)

for folder in possible_dirs:

    feature_file = os.path.join(folder, "feature_names.pkl")

    background_file = os.path.join(folder, "background_data.pkl")

    if os.path.exists(feature_file):

        print("\nLoading")

        print(feature_file)

        features = joblib.load(feature_file)

        print("Feature Count :", len(features))

        print(features[:10])

    else:

        print("\nfeature_names.pkl NOT FOUND in")

        print(folder)

    if os.path.exists(background_file):

        print("\nLoading")

        print(background_file)

        background = joblib.load(background_file)

        print("Background Shape :", background.shape)

    else:

        print("\nbackground_data.pkl NOT FOUND in")

        print(folder)

print("\n")
print("=" * 70)
print("FINISHED")
print("=" * 70)