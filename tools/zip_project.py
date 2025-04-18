import os
import zipfile

def zip_project(source_dir, zip_filename="project_export.zip", exclude=None):
    if exclude is None:
        exclude = [
            ".git", "__pycache__", ".DS_Store", ".env", ".venv",
            "*.pyc", "*.pyo", "*.log", "*.sqlite3", "*.vtt"
        ]

    def should_exclude(path):
        for pattern in exclude:
            if pattern.startswith("*.") and path.endswith(pattern[1:]):
                return True
            if pattern in path.split(os.sep):
                return True
        return False

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, start=source_dir)
                if not should_exclude(rel_path):
                    zipf.write(full_path, arcname=rel_path)

    print(f"✅ Project zipped to: {zip_filename}")

if __name__ == "__main__":
    zip_project(source_dir=".")
