import pytest
from pathlib import Path

# Points at the demo wiki bundled with the starter kit
DEMO_WIKI = Path(__file__).resolve().parent.parent.parent / "demo" / "wiki"


@pytest.fixture
def wiki_root():
    return DEMO_WIKI
