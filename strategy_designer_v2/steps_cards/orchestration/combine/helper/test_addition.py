"""What a run adds to the portfolio (addition.py) on hand-made records: the two portfolios, the same coin-days, the
strategies that entered, nothing written in portfolios/, the same file on a second call."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import addition as ad  # noqa: E402
import combine as cb  # noqa: E402
import update as up  # noqa: E402
from test_update import world, chart, N  # noqa: E402,F401


def book(w, run, n, coins=("AUSD", "BUSD")):
    rid = f"{n:03d}-01_book-{n}_1d"
    rng = np.random.default_rng(100 + n)
    chart(w, "common", run, rid, lambda c: 1000 * np.cumprod(1 + 0.002 + 0.01 * rng.standard_normal(N)), coins=list(coins))
    j = w["root"] / "orchestration" / "common_record" / run; j.mkdir(parents=True, exist_ok=True)
    (j / f"{rid}.json").write_text("{}")
    books = json.loads((w["reg"] / "books.json").read_text())
    books.append({"key": f"{run}__{rid}", "run": run, "id": rid, "kind": "paying", "side": "long", "made_utc": f"2026-11-0{n}T00:00:00"})
    (w["reg"] / "books.json").write_text(json.dumps(books))
    return f"{run}__{rid}"


def test_with_and_without_a_runs_candidates_on_the_same_coin_days(world):
    a, b = book(world, "old_run", 1, coins=("AUSD",)), book(world, "old_run", 2, coins=("AUSD",))
    c = book(world, "night1_x_run", 3)                       # the run's book also trades BUSD
    before = sorted(p for p in (world["func"] / "portfolios").rglob("*"))
    out = ad.addition(["night1_*"], world["data"])
    assert out["runs"] == ["night1_x_run"] and out["candidates"] == {"with": 3, "without": 2}
    assert out["entered"] == [c] and out["left"] == [] and out["strategies"]["without"] == sorted([a, b])
    assert out["coin_days"] == N - 1                         # AUSD only: BUSD's days exist with the run only
    whole = out["periods"][0][1]
    assert whole["with"]["days"] == whole["without"]["days"] == N - 1
    rows = {r["key"]: r for r in json.loads((world["reg"] / "books.json").read_text())}
    alone = cb.per_coin(out["weights"]["without"], rows, up.COMMON)[0].groupby(level="day").mean()
    assert whole["without"]["sharpe"] == cb.stats(alone)["sharpe"]
    assert [p for p, _ in out["periods"]][1:] == ["2019", "2020", "2021", "2022", "2023"]
    y = out["periods"][1][1]["with"]
    assert y["scale"] == whole["with"]["scale"] and y["days"] == 364          # a year at the whole period's scale
    assert sorted(p for p in (world["func"] / "portfolios").rglob("*")) == before     # nothing written there


def test_the_same_candidates_give_the_same_text_and_a_run_without_candidates_changes_nothing(world):
    book(world, "old_run", 1); book(world, "night1_x_run", 2)
    one, two = ad.text("night1", ad.addition(["night1_x_run"], world["data"])), ad.text("night1", ad.addition(["night1_x_run"], world["data"]))
    assert one == two and "| all years |" in one and "Entered the portfolio with these runs (1):" in one
    none = ad.addition(["no_such_run"], world["data"])
    assert none["runs"] == [] and none["entered"] == [] and none["left"] == []
    assert none["periods"][0][1]["with"] == none["periods"][0][1]["without"]
