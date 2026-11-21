"""bets.py: the bets of a forecast, on a series whose answer is known."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bets import bets  # noqa: E402


def test_bets_are_rises_of_at_least_the_band_on_their_side():
    fc = np.array([0, 2, 2, 5, 3, 0, -1, -3, 4, 4.5, 6, 0], float)
    # 2 from 0: a bet; 5 (3 above 2): a bet; -1 is below the band, -3: a bet; 4 after a change of side: a bet;
    # 4.5 is noise; 6 (2 above 4): a bet
    assert bets(fc).tolist() == [1, 3, 7, 8, 10]
