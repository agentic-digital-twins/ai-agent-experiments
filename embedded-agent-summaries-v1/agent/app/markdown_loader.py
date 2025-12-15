import os


def load_markdown(base_dir: str, doc_name: str) -> str:
    path = os.path.join(base_dir, doc_name)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Markdown file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
