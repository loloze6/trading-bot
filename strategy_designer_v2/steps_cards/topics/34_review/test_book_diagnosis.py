"""Tests of book_diagnosis.py on small records whose answers are known by construction."""
import json, subprocess, sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))
from book_diagnosis import diagnose, horizon_of  # noqa: E402
from test_idea_size import write_window  # noqa: E402


def test_no_cost_when_the_book_is_the_book_without_costs(tmp_path):
    n = 200; close = 100 * np.cumprod(np.full(n, 1.001)); fc = np.zeros(n); fc[10] = 5
    alloc = np.zeros(n); alloc[10:20] = 1.0
    write_window(tmp_path / "rec" / "BTCUSD" / "w1", close, fc, alloc)
    r = diagnose(tmp_path / "rec", 5)["whole_book"]["1_big_enough"]
    assert r["units_traded"] == pytest.approx(2.0)
    assert r["cost_per_unit_traded"] == pytest.approx(0.0, abs=1e-12)


def test_a_known_fee_is_found(tmp_path):
    n = 200; close = np.full(n, 100.0); fc = np.zeros(n); fc[10] = 5
    alloc = np.zeros(n); alloc[10:20] = 1.0
    value = np.full(n, 1000.0); value[10:20] = 999.0; value[20:] = 998.001   # 10 bps paid at open and at close
    write_window(tmp_path / "rec" / "BTCUSD" / "w1", close, fc, alloc, value)
    r = diagnose(tmp_path / "rec", 5)["whole_book"]["1_big_enough"]
    assert r["cost_per_unit_traded"] == pytest.approx(0.001, rel=1e-3)
    assert r["round_trip_cost"] == pytest.approx(0.002, rel=1e-3)


def test_move_opening_and_closing_on_a_known_path(tmp_path):
    # flat prices, except after each signal: +2 % on the signal's own bar, then +1 % on each of the next 2 bars,
    # then -1 % on the bar after (the move peaks at bar 2 and gives back). Signals every 20 bars, horizon 4.
    n, H = 400, 4
    steps = np.ones(n); fc = np.zeros(n)
    for t in range(20, n - 2 * H - 1, 20):
        fc[t] = 5; steps[t] = 1.02; steps[t + 1] = 1.01; steps[t + 2] = 1.01; steps[t + 3] = 0.99
    close = 100 * np.cumprod(steps); alloc = np.zeros(n)
    write_window(tmp_path / "rec" / "BTCUSD" / "w1", close, fc, alloc)
    res = diagnose(tmp_path / "rec", H)["whole_book"]
    d = (close[1:] / close[:-1] - 1).mean()
    assert res["bets_read"] == len(range(20, n - 2 * H - 1, 20))
    assert res["3_closing_time"]["peak_bar"] == 2
    assert res["3_closing_time"]["move_at_peak"] == pytest.approx(1.01 * 1.01 - 1 - ((1 + d) ** 2 - 1), abs=1e-9)
    assert res["1_big_enough"]["move_over_horizon"] == pytest.approx(res["3_closing_time"]["move_at_H"])
    assert res["2_opening_time"]["move_on_bar_0"] == pytest.approx(0.02 - d, abs=1e-9)


def test_every_bet_is_read_even_when_bets_overlap(tmp_path):
    n, H = 100, 10; close = np.full(n, 100.0); fc = np.zeros(n)
    fc[20], fc[21], fc[22] = 2, 4, 6        # three rises of the band inside one horizon: three bets, all read
    write_window(tmp_path / "rec" / "BTCUSD" / "w1", close, fc, np.zeros(n))
    assert diagnose(tmp_path / "rec", H)["whole_book"]["bets_read"] == 3


def test_holding_past_the_bets(tmp_path):
    # one bet at bar 10 (horizon 3); the position is held from bar 10 to bar 19: 10 bars, 3 covered, 7 past
    n = 50; close = np.full(n, 100.0); fc = np.zeros(n); fc[10:20] = 5
    alloc = np.zeros(n); alloc[10:20] = 1.0
    write_window(tmp_path / "rec" / "BTCUSD" / "w1", close, fc, alloc)
    r = diagnose(tmp_path / "rec", 3)["whole_book"]["4_holding_past_the_bets"]
    assert r["bars_in_position"] == 10
    assert r["share_past_the_bets"] == pytest.approx(0.7)


def test_a_book_always_in_a_rising_coin_is_all_market(tmp_path):
    n = 24 * 30; close = 100 * np.cumprod(np.full(n, 1.0005)); fc = np.full(n, 5.0); alloc = np.ones(n)
    write_window(tmp_path / "rec" / "BTCUSD" / "w1", close, fc, alloc)
    r = diagnose(tmp_path / "rec", 24)["whole_book"]["5_trend"]
    assert r["market_share"] == pytest.approx(1.0, rel=0.01)


def test_horizon_from_the_plan_and_the_files_written(tmp_path):
    plan = tmp_path / "plans" / "idea.md"; plan.parent.mkdir()
    plan.write_text("Horizon: 4 bars\n")
    rec = tmp_path / "bt" / "idea"
    n = 200; close = 100 * np.cumprod(np.full(n, 1.001)); fc = np.zeros(n); fc[50] = 5
    write_window(rec / "BTCUSD" / "w1", close, fc, np.zeros(n))
    (rec / "run.md").write_text("- Plan: `../../plans/idea.md`\n")
    assert horizon_of(rec) == 4
    subprocess.run([sys.executable, str(Path(__file__).parent / "book_diagnosis.py"), str(rec)], check=True,
                   capture_output=True)
    assert json.loads((rec / "diagnosis.json").read_text())["horizon"] == 4
    assert (rec / "diagnosis.md").read_text().startswith("# Diagnosis of idea")
