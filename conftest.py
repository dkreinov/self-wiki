import sys
from pathlib import Path

# Allow `from tools.web.renderer import ...` style imports when running pytest
sys.path.insert(0, str(Path(__file__).parent))
