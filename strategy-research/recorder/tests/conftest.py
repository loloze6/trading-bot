import sys
from pathlib import Path

# strategy-research/ on the path so `recorder.*` imports resolve without an
# installed package. The recorder is standalone: nothing here touches
# trading-bot/, and no test reads any recorded, archived or holdout data.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
