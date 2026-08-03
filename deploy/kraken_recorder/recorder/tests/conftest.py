import sys
from pathlib import Path

# Put the bundle root (this file's parents[2]: tests/ -> recorder/ -> bundle)
# on the path so `recorder.*` imports resolve without an installed package.
# The recorder is standalone: every test below builds its own fixtures under
# tmp_path, and no test reads any recorded or archived capture data.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
