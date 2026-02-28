import os

project_name = "churn_prediction"

# Folder structure
folders = [
    f"{project_name}/config",
    f"{project_name}/data/raw",
    f"{project_name}/data/processed",
    f"{project_name}/notebooks",
    f"{project_name}/src/data",
    f"{project_name}/src/features",
    f"{project_name}/src/models",
    f"{project_name}/src/pipeline",
    f"{project_name}/src/utils",
    f"{project_name}/tests",
    f"{project_name}/logs",
]

# Files to create
files = [
    f"{project_name}/README.md",
    f"{project_name}/requirements.txt",
    f"{project_name}/setup.py",
    f"{project_name}/.gitignore",
    f"{project_name}/.env.example",
    f"{project_name}/config/config.yaml",
    f"{project_name}/src/__init__.py",
    f"{project_name}/src/data/__init__.py",
    f"{project_name}/src/features/__init__.py",
    f"{project_name}/src/models/__init__.py",
    f"{project_name}/src/pipeline/__init__.py",
    f"{project_name}/src/utils/__init__.py",
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file in files:
    with open(file, "w") as f:
        pass

print("✅ Project structure created successfully!")