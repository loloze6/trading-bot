"""The box reader on hand-made records whose boxes are known."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import boxes as bx  # noqa: E402


def make_data(tmp, n=1500):
    """One coin: 1,100 calm days drifting up slowly, then 400 days falling hard and swinging."""
    alt = lambda k, a: a * (-1.0) ** np.arange(k)                    # a steady swing, up one day, down the next
    r = np.r_[0.004 + alt(1100, 0.005), -0.006 + alt(n - 1100, 0.05)]
    days = pd.date_range("2019-01-01", periods=n, freq="D")
    pd.DataFrame({"timestamp": days.strftime("%Y-%m-%d"), "close": 100 * np.exp(np.cumsum(r))}).to_csv(tmp / "kraken_XUSD_1d.csv", index=False)
    return days


def test_a_book_long_only_in_the_falling_years_has_its_box_there(tmp_path):
    days = make_data(tmp_path)
    rec = tmp_path / "b_1d"; rec.mkdir()
    pos = np.where(np.arange(len(days)) >= 1160, 0.5, 0.0)          # long only once the coin is falling
    pd.DataFrame({"coin": "XUSD", "window": "w1", "timestamp": days.strftime("%Y-%m-%d"), "position": pos,
                  "value": 1000 + np.arange(len(days))}).to_csv(rec / "chart_bars.csv.gz", index=False)
    bx.profiles.cache_clear()
    res = bx.read_book(rec, data=tmp_path)
    falling_long = [k for k in res["boxes"] if k[1] == "long"]
    assert falling_long and all(k[0].startswith("falling") for k in falling_long)
    assert all(k[1] == "long" for k in res["boxes"])
    best = max(res["cells"].items(), key=lambda kv: kv[1]["presence"])
    assert best[1]["times_market"] > 1.5                             # it chooses that market
    assert res["return_in_boxes"] > 0                                 # the value grows every day


def test_a_book_always_in_has_its_boxes_wherever_the_market_is(tmp_path):
    days = make_data(tmp_path)
    rec = tmp_path / "a_1d"; rec.mkdir()
    pd.DataFrame({"coin": "XUSD", "window": "w1", "timestamp": days.strftime("%Y-%m-%d"), "position": 0.3,
                  "value": 1000.0}).to_csv(rec / "chart_bars.csv.gz", index=False)
    bx.profiles.cache_clear()
    res = bx.read_book(rec, data=tmp_path)
    for (p, s), v in res["cells"].items():
        if s == "long" and v["market"] > 0:
            assert abs(v["times_market"] - 1) < 1e-9                 # present exactly as often as the market
    assert abs(sum(v["presence"] for v in res["cells"].values()) - 1.0) < 1e-9
