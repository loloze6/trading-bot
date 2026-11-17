"""Tests of the chart files: written from a small hand-made record, only for a backtest worth a chart."""
import gzip
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chart_files as C  # noqa: E402


def record(tmp_path):
    rec = tmp_path / "rec"
    for coin, w in (("BTCUSD", "w1"), ("BTCUSD", "w2"), ("ETHUSD", "w1")):
        d = rec / coin / w
        d.mkdir(parents=True)
        pd.DataFrame({"timestamp": ["2021-01-01", "2021-01-02"], "close": [100.123456789, 101.0], "forecast": [3.14159, -2.0],
                      "postRebalance_current_allocation": [0.31, -0.2], "postRebalance_total_value": [1000.0, 1001.5],
                      "other": [1, 2]}).to_csv(d / "bars.csv.gz", index=False, compression="gzip")
        (d / "trades.json.gz").write_bytes(gzip.compress(json.dumps([{"entry_time": "2021-01-01", "exit_time": "2021-01-02",
            "side": "LONG", "entry_price": 100.0, "exit_price": 101.0, "net_profit_loss_percent": 0.9}]).encode()))
    return rec


def test_the_chart_files_hold_every_bar_and_trade(tmp_path):
    rec = record(tmp_path)
    assert C.write(rec) == (6, 3)
    bars = gzip.decompress((rec / "chart_bars.csv.gz").read_bytes()).decode().splitlines()
    assert bars[0] == "coin,window,timestamp,close,forecast,position,value"
    assert bars[1] == "BTCUSD,w1,2021-01-01,100.123,3.14,0.31,1000"
    trades = gzip.decompress((rec / "chart_trades.csv.gz").read_bytes()).decode().splitlines()
    assert trades[1] == "BTCUSD,w1,2021-01-01,2021-01-02,LONG,100,101,0.9" and len(trades) == 4
    first = (rec / "chart_bars.csv.gz").read_bytes()
    C.write(rec)
    assert (rec / "chart_bars.csv.gz").read_bytes() == first                # the same bytes again


def test_only_a_backtest_worth_a_chart(tmp_path):
    v, c = tmp_path / "v.json", tmp_path / "c.json"
    v.write_text(json.dumps({"status": "inconclusive"}))
    c.write_text(json.dumps({"status": "not profitable enough"}))
    assert not C.worth_a_chart(v, c)
    c.write_text(json.dumps({"status": "profitable enough"}))
    assert C.worth_a_chart(v, c)
    v.write_text(json.dumps({"status": "confirmed"}))
    assert C.worth_a_chart(v, tmp_path / "none.json")
    assert C.write(tmp_path / "empty") == (0, 0)


def test_each_column_lands_in_its_own_place_whatever_the_file_s_order(tmp_path):
    """The engine writes postRebalance_total_value before postRebalance_current_allocation (found by the run viewer:
    position and value were swapped in every chart file)."""
    d = tmp_path / "rec" / "BTCUSD" / "w1"
    d.mkdir(parents=True)
    pd.DataFrame({"timestamp": ["2021-01-01"], "close": [100.0], "forecast": [0.0], "postRebalance_total_value": [1000.0],
                  "postRebalance_current_allocation": [0.0]}).to_csv(d / "bars.csv.gz", index=False, compression="gzip")
    C.write(tmp_path / "rec")
    row = gzip.decompress((tmp_path / "rec" / "chart_bars.csv.gz").read_bytes()).decode().splitlines()[1].split(",")
    assert row[5] == "0" and row[6] == "1000"               # position 0, value 1000


def test_a_backtest_not_worth_a_chart_gets_the_local_names_and_one_pair_only(tmp_path):
    rec = record(tmp_path)
    C.write(rec, local=True)
    assert sorted(p.name for p in rec.glob("chart_*")) == ["chart_bars.local.csv.gz", "chart_trades.local.csv.gz"]
    C.write(rec)                                            # later worth a chart: the committed names replace them
    assert sorted(p.name for p in rec.glob("chart_*")) == ["chart_bars.csv.gz", "chart_trades.csv.gz"]
