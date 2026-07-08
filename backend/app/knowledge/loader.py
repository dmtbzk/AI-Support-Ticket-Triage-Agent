from pathlib import Path

BASE_PATH = Path(__file__).parent


def load_knowledge(category: str) -> str:
    filename = f"{category.lower()}.md"

    filepath = BASE_PATH / filename

    if not filepath.exists():
        filepath = BASE_PATH / "general.md"

    return filepath.read_text()