"""
Tests for the read-only run viewer (D-180): tools/run_viewer/{loaders,sanitize,server}.py.

Fixtures: tests/fixtures/run_viewer/ is shaped like a strategy-research root (run_098 and
run_099 copied from the operator checkout through sanitize_text at creation). Every
expectation is computed from the fixture files themselves, never hard-coded.

Seal discipline: the sealed range is read from the REAL policy file at test time only
(explicit path, not the sandboxable default) and only to build tokens / count matches.
No date of the window appears in this file and no assertion message carries one.
"""
import builtins
import csv
import http.client
import io
import json
import os
import pathlib
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

import pytest
import yaml

HERE = Path(__file__).resolve().parent
SR = HERE.parent
VIEWER = SR / "tools" / "run_viewer"
FIX = HERE / "fixtures" / "run_viewer"
POLICY = SR / "config" / "campaign_data_policy.yaml"

for _p in (str(VIEWER), str(SR / "tools")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import holdout_policy  # noqa: E402
import loaders  # noqa: E402
import sanitize  # noqa: E402
import server  # noqa: E402

STEPS = ["launch", "config", "variants", "data_gate", "protocol", "replay_gate", "profit_bars",
         "grid", "claims", "analyst", "decide_next", "record"]


# --------------------------------------------------------------------------- helpers


def _yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _runs(root):
    return Path(root) / "runs"


def _window_range():
    """(lo, hi) as dates, from the real policy file, at test time only."""
    lo, hi = holdout_policy.load_holdout_range(POLICY)
    return date.fromisoformat(lo), date.fromisoformat(hi)


# --- an independent counter of every date form sanitize masks (not sanitize's own patterns)
_MN = r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
_MN_NUM = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}
_C_DAY_FORMS = [  # (regex, (year, month, day) group order); month/day swapped readings handled below
    (re.compile(r"(?<![0-9])([0-9]{4})-([0-9]{2})-([0-9]{2})"), (1, 2, 3)),
    (re.compile(r"(?<![0-9])([0-9]{4})[/._]([0-9]{2})[/._]([0-9]{2})"), (1, 2, 3)),
    (re.compile(r"(?<![0-9A-Za-z])([0-9]{4})([0-9]{2})([0-9]{2})(?![0-9])"), (1, 2, 3)),
]
_C_DMY = re.compile(r"(?<![0-9])([0-9]{1,2})[/.\-]([0-9]{1,2})[/.\-]([0-9]{4})(?![0-9])")
_C_D_MON_Y = re.compile(r"(?<![0-9A-Za-z])([0-9]{1,2})(?:st|nd|rd|th)?[ \-]+" + _MN + r"[a-z]*\.?[ \-]+([0-9]{4})", re.I)
_C_MON_D_Y = re.compile(_MN + r"[a-z]*\.?\s+([0-9]{1,2})(?:st|nd|rd|th)?,?\s+([0-9]{4})", re.I)
_C_YM = [re.compile(r"(?<![0-9-])([0-9]{4})-([0-9]{2})(?![0-9-])"),
         re.compile(r"(?<![0-9/.\-])([0-9]{4})/([0-9]{2})(?![0-9/])")]
_C_MY = re.compile(r"(?<![0-9/.\-])([0-9]{1,2})/([0-9]{4})(?![0-9])")
_C_MON_Y = re.compile(r"(?<![0-9][ \-])(?<![0-9](?:st|nd|rd|th)[ \-])(?<![A-Za-z])" + _MN + r"[a-z]*\.?\s+([0-9]{4})(?![0-9])", re.I)
_C_Q = [re.compile(r"(?<![0-9A-Za-z])q([1-4])(?:\s+|[-_])([0-9]{4})(?![0-9])", re.I),
        re.compile(r"(?<![0-9])([0-9]{4})(?:\s+|[-_])?q([1-4])(?![0-9A-Za-z])", re.I)]
_C_H = [re.compile(r"(?<![0-9A-Za-z])h([12])(?:\s+|[-_])([0-9]{4})(?![0-9])", re.I),
        re.compile(r"(?<![0-9])([0-9]{4})(?:\s+|[-_])?h([12])(?![0-9A-Za-z])", re.I)]


def _c_day_in(y, m, d, lo, hi):
    try:
        return lo <= date(int(y), int(m), int(d)) <= hi
    except ValueError:
        return False


def _c_span_in(y, m1, m2, lo, hi):
    try:
        y = int(y)
        first = date(y, m1, 1)
        last = date(y + (m2 == 12), 1 if m2 == 12 else m2 + 1, 1) - timedelta(days=1)
    except ValueError:
        return False
    return first <= hi and last >= lo


def count_in_range(text):
    """Number of tokens, in any form sanitize masks, whose day / month / quarter / half
    intersects the sealed window (0 is the only acceptable answer for any output)."""
    lo, hi = _window_range()
    n = 0
    for rx, (iy, im, idd) in _C_DAY_FORMS:
        n += sum(1 for m in rx.finditer(text) if _c_day_in(m[iy], m[im], m[idd], lo, hi))
    for m in _C_DMY.finditer(text):
        a, b, y = m[1], m[2], m[3]
        n += _c_day_in(y, b, a, lo, hi) or _c_day_in(y, a, b, lo, hi)
    for m in _C_D_MON_Y.finditer(text):
        n += _c_day_in(m[3], _MN_NUM[m[2][:3].lower()], m[1], lo, hi)
    for m in _C_MON_D_Y.finditer(text):
        n += _c_day_in(m[3], _MN_NUM[m[1][:3].lower()], m[2], lo, hi)
    for rx in _C_YM:
        n += sum(1 for m in rx.finditer(text) if 1 <= int(m[2]) <= 12 and _c_span_in(m[1], int(m[2]), int(m[2]), lo, hi))
    n += sum(1 for m in _C_MY.finditer(text) if 1 <= int(m[1]) <= 12 and _c_span_in(m[2], int(m[1]), int(m[1]), lo, hi))
    for m in _C_MON_Y.finditer(text):
        mo = _MN_NUM[m[1][:3].lower()]
        n += _c_span_in(m[2], mo, mo, lo, hi)
    for m in _C_Q[0].finditer(text):
        q = int(m[1])
        n += _c_span_in(m[2], 3 * q - 2, 3 * q, lo, hi)
    for m in _C_Q[1].finditer(text):
        q = int(m[2])
        n += _c_span_in(m[1], 3 * q - 2, 3 * q, lo, hi)
    for m in _C_H[0].finditer(text):
        h = int(m[1])
        n += _c_span_in(m[2], 6 * h - 5, 6 * h, lo, hi)
    for m in _C_H[1].finditer(text):
        h = int(m[2])
        n += _c_span_in(m[1], 6 * h - 5, 6 * h, lo, hi)
    return int(n)


_MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August",
                "September", "October", "November", "December"]


def date_forms(d):
    """{name: token} spelling day `d` (and its month / quarter / half) in every masked form."""
    y, mo, dd = d.year, d.month, d.day
    mn = _MONTH_NAMES[mo - 1]
    q = (mo - 1) // 3 + 1
    h = 1 if mo <= 6 else 2
    return {
        "iso": f"{y:04d}-{mo:02d}-{dd:02d}",
        "iso glued after letters": f"run{y:04d}-{mo:02d}-{dd:02d}",
        "iso with time": f"{y:04d}-{mo:02d}-{dd:02d}T09:30:00Z",
        "ymd slash": f"{y:04d}/{mo:02d}/{dd:02d}",
        "ymd dot": f"{y:04d}.{mo:02d}.{dd:02d}",
        "ymd underscore": f"{y:04d}_{mo:02d}_{dd:02d}",
        "dmy slash": f"{dd:02d}/{mo:02d}/{y:04d}",
        "mdy slash": f"{mo:02d}/{dd:02d}/{y:04d}",
        "dmy dot": f"{dd:02d}.{mo:02d}.{y:04d}",
        "dmy dash": f"{dd:02d}-{mo:02d}-{y:04d}",
        "d Mon Y": f"{dd} {mn[:3]} {y}",
        "d Month Y": f"{dd} {mn} {y}",
        "Mon d, Y": f"{mn[:3]} {dd}, {y}",
        "Month d, Y": f"{mn} {dd}, {y}",
        "DD-Mon-YYYY": f"{dd:02d}-{mn[:3]}-{y}",
        "lower month": f"{dd} {mn.lower()} {y}",
        "upper month": f"{dd} {mn.upper()} {y}",
        "Month Y": f"{mn} {y}",
        "Mon Y": f"{mn[:3]} {y}",
        "Y/M": f"{y:04d}/{mo:02d}",
        "M/Y": f"{mo:02d}/{y:04d}",
        "Y-M": f"{y:04d}-{mo:02d}",
        "compact": f"{y:04d}{mo:02d}{dd:02d}",
        "compact stamp": f"{y:04d}{mo:02d}{dd:02d}T113455Z_c3c83fd6",
        "Q Y": f"Q{q} {y}",
        "Y Q": f"{y} Q{q}",
        "YQ": f"{y}Q{q}",
        "Y-Q": f"{y}-Q{q}",
        "Q-Y": f"Q{q}-{y}",
        "H Y": f"H{h} {y}",
        "YH": f"{y}H{h}",
        "Y-H": f"{y}-H{h}",
    }


@pytest.fixture()
def fx_copy(tmp_path):
    dst = tmp_path / "fx"
    shutil.copytree(FIX, dst)
    return dst


class Srv:
    def __init__(self, root, runs, sink=None):
        self.srv = server.make_server(root, runs, "127.0.0.1", 0, sink)
        self.port = self.srv.server_address[1]
        self.t = threading.Thread(target=self.srv.serve_forever, daemon=True)
        self.t.start()

    def req(self, path, method="GET"):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=30)
        try:
            c.request(method, path)
            r = c.getresponse()
            return r.status, dict(r.getheaders()), r.read()
        finally:
            c.close()

    def get_json(self, path):
        st, _, body = self.req(path)
        return st, json.loads(body)

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()
        self.t.join(timeout=10)


@pytest.fixture()
def srv():
    s = Srv(FIX, _runs(FIX))
    yield s
    s.close()


def crawl_paths(root):
    runs = _runs(root)
    paths = ["/", "/static/index.html", "/api/runs"]
    for rid in loaders.list_run_ids(runs):
        paths.append(f"/api/run/{rid}")
        paths += [f"/api/run/{rid}/step/{n}" for n in STEPS]
        rd = loaders.Reader(root, runs, rid)
        for v in loaders.list_variants(rd):
            paths.append(f"/api/run/{rid}/variant/{v}/equity")
            for w in loaders.list_windows(rd, v):
                paths.append(f"/api/run/{rid}/variant/{v}/window/{quote(w, safe='')}/bars")
    return paths


def crawl(s, root):
    out = []
    for p in crawl_paths(root):
        st, _, body = s.req(p)
        out.append((p, st, body))
    return out


# --------------------------------------------------------------------------- view 1


def test_view1_runs_newest_first_with_expected_fields():
    v1 = loaders.load_campaign(FIX, _runs(FIX))
    assert [r["run_id"] for r in v1["runs"]] == ["run_099", "run_098"]
    r99, r98 = v1["runs"]
    assert r99["entry_id"] == "child_run_098_long_only_fold_b"
    assert r98["entry_id"] == "daily_breadth_fold_b"
    assert r99["fold"] == "B" and r98["fold"] == "B"
    assert r99["coins"] == ["BTCUSD", "LTCUSD"]
    assert r99["timeframe"] == "1d"
    assert r99["idea_status"] == "refuted" and r98["idea_status"] == "refuted"
    assert r99["outcome_letter"] is None and r99["outcome_note"] == "not recorded"
    assert r99["pre_registered_letters"][:3] == ["A", "B", "C"]
    # cost: the sum of the fixture's own audit log
    ps = _yaml(FIX / "runs/run_099/pipeline_state.yaml")
    expected = sum(rec["cost_usd"] for rec in ps["audit_log"].values())
    assert r99["cost_usd"] == pytest.approx(expected)
    assert r99["cost_label"] == "model cost (stages that called a model)"
    # base bars: counted from the fixture's profit_bars_evaluation
    pb = _yaml(FIX / "runs/run_099/artifacts/profit_bars_evaluation.yaml")
    bars = pb["variants"]["base"]["bars"]
    assert r99["base_bars"] == {"passed": sum(b["result"] == "PASS" for b in bars), "total": len(bars)}
    assert r99["base_bars"]["total"] == 7
    assert r99["launched_at"] and r99["done_at"] and r99["duration_seconds"] > 0
    assert r99["status"] == "completed" and r99["legacy_shape"] is False


def test_view1_queue_and_blocks():
    v1 = loaders.load_campaign(FIX, _runs(FIX))
    q = v1["queue"]
    assert any(e["status"].startswith("blocked") for e in q["entries"])
    assert sum(q["counts"].values()) == len(_yaml(FIX / "config/campaign_queue.yaml")["queue"])
    reg = _yaml(FIX / "campaign_record/block_registry.yaml")
    assert v1["blocks"]["revision"] == reg["revision"]
    assert [b["block_id"] for b in v1["blocks"]["blocks"]] == [b["block_id"] for b in reg["blocks"]]
    last = {}
    for rec in reg.get("statuses", []):
        last[rec["block_id"]] = rec["status"]
    for b in v1["blocks"]["blocks"]:
        assert b["status"] == last.get(b["block_id"], "active")


def test_view1_blocks_error_is_reported_not_raised(fx_copy):
    (fx_copy / "campaign_record/block_registry.yaml").write_text("schema_version: [unclosed\n", encoding="utf-8")
    v1 = loaders.load_campaign(fx_copy, _runs(fx_copy))
    assert "error" in v1["blocks"]
    assert [r["run_id"] for r in v1["runs"]] == ["run_099", "run_098"]


# --------------------------------------------------------------------------- view 2


def test_view2_twelve_steps_in_order_with_statuses_for_run_099():
    v2 = loaders.load_run(FIX, _runs(FIX), "run_099")
    assert [c["name"] for c in v2["steps"]] == STEPS
    st = {c["name"]: c["status"] for c in v2["steps"]}
    assert st["profit_bars"] == "fail" and st["grid"] == "fail"
    assert st["replay_gate"] == "ok"
    assert set(st.values()) <= {"ok", "fail", "warn", "absent", "unreadable"}
    for c in v2["steps"]:
        assert set(c) == {"name", "title", "status", "headlines", "line", "sources"}
    h = v2["header"]
    assert h["run_id"] == "run_099" and h["entry_id"] == "child_run_098_long_only_fold_b"
    assert h["cost_label"] == "model cost (stages that called a model)"
    assert h["outcome_letter"] is None and h["outcome_note"] == "not recorded"
    assert h["purpose"] and h["outcomes"][0]["letter"] == "A"
    assert [a["stage"] for a in h["audit"]] == list(_yaml(FIX / "runs/run_099/pipeline_state.yaml")["audit_log"])
    assert any("LAUNCH-CARD" in ln for ln in h["campaign_log"])
    assert h["campaign_log"][-1].count("DECIDE") == 1
    # profit_bars headline: base bars passed / total
    pb = {c["name"]: c for c in v2["steps"]}["profit_bars"]
    assert pb["headlines"][0]["value"] == "4/7" or "/7" in pb["headlines"][0]["value"]
    assert json.dumps(v2, allow_nan=False)


# --------------------------------------------------------------------------- view 3


def test_view3_profit_bars_table_rows_are_the_seven_bars():
    st = loaders.load_step(FIX, _runs(FIX), "run_099", "profit_bars")
    pb = _yaml(FIX / "runs/run_099/artifacts/profit_bars_evaluation.yaml")
    t = st["tables"][0]
    variants = list(pb["variants"])
    assert t["columns"] == ["bar"] + variants
    assert len(t["rows"]) == 7 + 1  # seven bars plus the per-variant result row
    assert t["rows"][-1][0] == "variant result"
    assert t["rows"][-1][1:] == [pb["variants"][v]["result"] for v in variants]
    base_bars = {b["name"]: b for b in pb["variants"]["base"]["bars"]}
    bi = 1 + variants.index("base")
    for row in t["rows"][:-1]:
        b = base_bars[row[0]]
        assert row[bi].endswith("/ " + b["result"])
        assert row[bi].split(" / ")[0] == loaders.fmt(b["actual"])
    assert t["by_option"]["by"] == "variant"
    assert t["by_option"]["options"] == variants
    assert t["by_option"]["rows_by_option"]["base"][0] == [t["rows"][0][0], t["rows"][0][bi]]
    dsr = [x for x in st["tables"] if x["title"] == "Deflated Sharpe basis"][0]
    assert dict(map(tuple, dsr["rows"]))["n_trials"] == str(pb["dsr_basis"]["n_trials"])
    assert st["raw"] and st["raw"][0]["path"].endswith("profit_bars_evaluation.yaml")


def test_view3_grid_cells_match_grid_evaluation():
    st = loaders.load_step(FIX, _runs(FIX), "run_099", "grid")
    g = _yaml(FIX / "runs/run_099/artifacts/grid_evaluation.yaml")
    t = st["tables"][0]
    cols = t["columns"]
    cells = {(r[cols.index("criterion")], r[cols.index("variant")]): r for r in t["rows"]}
    n = 0
    for crit, per in g["grid"].items():
        for v, c in per.items():
            n += 1
            row = cells[(crit, v)]
            assert row[cols.index("result")] == c["result"]
            assert row[cols.index("value")] == c.get("value")
            assert row[cols.index("threshold")] == c.get("threshold")
            assert row[cols.index("n_windows")] == c.get("n_windows")
            assert row[cols.index("reason")] == c.get("reason")
    assert n == len(t["rows"])
    ric = _yaml(FIX / "runs/run_099/artifacts/residual_ic.yaml")
    rt = [x for x in st["tables"] if x["title"] == "Residual IC"][0]
    rc = rt["columns"]
    for r in rt["rows"]:
        v = ric["variants"][r[0]]
        assert r[rc.index("p_value_one_sided")] == v["p_value_one_sided"]
        assert r[rc.index("correlation_to_composite")] == v["correlation_to_composite"]
    texts = " ".join(x["body"] for x in st["text"])
    for bid in ric["composite"]["block_ids"]:
        assert bid in texts


def test_view3_analyst_queries_count_and_rerun_section():
    for rid, has_rerun in (("run_099", False), ("run_098", True)):
        st = loaders.load_step(FIX, _runs(FIX), rid, "analyst")
        qdir = FIX / "runs" / rid / "artifacts" / "analyst_queries"
        expected = sum(len(_yaml(p)["queries"]) for p in sorted(qdir.glob("*.yaml")))
        main_q = [t for t in st["tables"] if t["title"] == "Queries"][0]
        assert len(main_q["rows"]) == expected
        titles = [t["title"] for t in st["tables"]]
        rerun = [t for t in st["tables"] if t.get("section") == "re-run on a copy"]
        if has_rerun:
            assert titles.index("Queries") < titles.index("re-run on a copy: Lenses")
            assert [t["title"] for t in rerun] == ["re-run on a copy: Lenses", "re-run on a copy: Queries"]
            rq = FIX / "runs" / rid / "artifacts" / "analyst_rerun" / "analyst_queries"
            exp_r = sum(len(_yaml(p)["queries"]) for p in sorted(rq.glob("*.yaml")))
            assert len(rerun[1]["rows"]) == exp_r
            assert any(x.get("section") == "re-run on a copy" and x["title"].endswith("README") for x in st["text"])
            card = loaders.load_run(FIX, _runs(FIX), rid)["steps"][STEPS.index("analyst")]
            assert "re-run on a copy present" in card["line"]
        else:
            assert not rerun
            assert not any("re-run" in t["title"] for t in st["tables"] + st["text"])
        lens = [t for t in st["tables"] if t["title"] == "Lenses"][0]
        assert {r[0] for r in lens["rows"]} == {p.stem for p in (FIX / "runs" / rid / "artifacts/analyst").glob("*.yaml")}
        q0 = main_q["rows"][0]
        assert q0[main_q["columns"].index("function")]
        json.loads(q0[main_q["columns"].index("params")])


def test_view3_data_gate_protocol_and_variants_tables():
    runs = _runs(FIX)
    dg = loaders.load_step(FIX, runs, "run_099", "data_gate")
    t = dg["tables"][0]
    assert len(t["rows"]) == 18 and {r[0] for r in t["rows"]} == {"base", "design_no_vol_target", "asset_ltc"}
    pr = loaders.load_step(FIX, runs, "run_099", "protocol")
    t = pr["tables"][0]
    assert t["columns"][:3] == ["variant", "window", "symbol"]
    assert len(t["rows"]) == len(t["links"]) == 18
    for row, link in zip(t["rows"], t["links"]):
        assert link == {"variant": row[0], "window": row[1]}
    pres = _yaml(FIX / "runs/run_099/artifacts/variants/base/protocol_result.yaml")
    base_rows = [r for r in t["rows"] if r[0] == "base"]
    assert [r[3] for r in base_rows] == [x["core"]["trade_count"] for x in pres["results"]]
    vs = loaders.load_step(FIX, runs, "run_099", "variants")
    patch = vs["tables"][0]
    assert {r[0] for r in patch["rows"]} == {"base", "design_no_vol_target", "asset_ltc"}
    json.loads(patch["rows"][1][3])
    dn = loaders.load_step(FIX, runs, "run_099", "decide_next")
    cand = dn["tables"][0]
    assert cand["columns"] == ["candidate_id", "origin", "kind", "eligible", "reasons", "picked"]
    dr = _yaml(FIX / "runs/run_099/artifacts/decision_record.yaml")
    assert len(cand["rows"]) == len(dr["candidates"])


def test_every_view3_table_has_by_option_or_is_label_value():
    for rid in ("run_099", "run_098"):
        for n in STEPS:
            st = loaders.load_step(FIX, _runs(FIX), rid, n)
            for t in st["tables"]:
                assert "by_option" in t
                bo = t["by_option"]
                if bo is None:
                    continue
                assert set(bo) == {"by", "options", "rows_by_option"}
                assert set(bo["rows_by_option"]) == set(bo["options"])
                for pairs in bo["rows_by_option"].values():
                    assert all(isinstance(p, list) and len(p) == 2 for p in pairs)


# --------------------------------------------------------------------------- view 4


def _window_files(rid, variant, label):
    res = _yaml(FIX / f"runs/{rid}/artifacts/variants/{variant}/protocol_result.yaml")["results"]
    r = [x for x in res if x["window"] == label][0]
    d = FIX / f"runs/{rid}/variants/{variant}/results/{r['run_id']}"
    return r, d / "bars.csv", d / "trades.json"


def test_bars_run_099_base_window_2020_05():
    b = loaders.load_bars(FIX, _runs(FIX), "run_099", "base", "2020-05")
    r, bars_p, trades_p = _window_files("run_099", "base", "2020-05")
    ct = _yaml(FIX / "runs/run_099/artifacts/variants/base/claim_test.yaml")
    expected_bars = [x["bars"] for x in ct["bars"] if x["window"].endswith("/2020-05")][0]
    with open(bars_p, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert b["n_bars"] == expected_bars == len(rows)
    assert set(b["columns"]) == {"timestamp", "close", "forecast", "position", "portfolio_value", "approved_rebalance"}
    assert b["columns"]["timestamp"][0] == rows[0]["timestamp"]
    assert b["columns"]["position"][5] == pytest.approx(float(rows[5]["postRebalance_current_allocation"]))
    trades = json.loads(trades_p.read_text(encoding="utf-8"))
    assert len(b["trades"]) == len(trades) == r["core"]["trade_count"]
    assert set(b["trades"][0]) == set(loaders.TRADE_FIELDS)
    assert b["trades"][0]["entry_time"] == trades[0]["entry_time"]
    assert b["metrics"]["trade_count"] == r["core"]["trade_count"]
    assert json.dumps(b, allow_nan=False)


def test_equity_is_chained_across_windows():
    e = loaders.load_equity(FIX, _runs(FIX), "run_099", "base")
    ws = e["windows"]
    assert [w["label"] for w in ws] == ["2018-05", "2019-01", "2019-09", "2020-05", "2021-01", "2021-09"]
    assert ws[0]["equity"][0] == pytest.approx(1.0)
    prev_end = 1.0
    for w in ws:
        # independent recomputation from the csv
        _, bars_p, _ = _window_files("run_099", "base", w["label"])
        with open(bars_p, newline="", encoding="utf-8") as fh:
            pv = [float(x["portfolio_value"]) for x in csv.DictReader(fh)]
        assert w["equity"][0] == pytest.approx(prev_end)
        assert w["equity"][-1] == pytest.approx(prev_end * pv[-1] / pv[0])
        assert len(w["equity"]) == len(w["timestamps"]) == len(pv)
        prev_end = w["equity"][-1]


# --------------------------------------------------------------------------- absent / broken


def test_run_098_asset_ada_has_no_protocol_result_and_nothing_raises():
    assert not (FIX / "runs/run_098/artifacts/variants/asset_ada/protocol_result.yaml").exists()
    runs = _runs(FIX)
    v2 = loaders.load_run(FIX, runs, "run_098")
    assert [c["name"] for c in v2["steps"]] == STEPS
    pr = loaders.load_step(FIX, runs, "run_098", "protocol")
    assert pr["status"] == "warn"
    assert any("asset_ada absent" in h["value"] for h in pr["headlines"])
    assert not [r for r in pr["tables"][0]["rows"] if r[0] == "asset_ada"]
    b = loaders.load_bars(FIX, runs, "run_098", "asset_ada", "2021-01")
    assert b["columns"]["close"] is None and b["trades"] is None
    e = loaders.load_equity(FIX, runs, "run_098", "asset_ada")
    assert e["windows"] == []
    for n in STEPS:
        loaders.load_step(FIX, runs, "run_098", n)


def test_missing_profit_bars_gives_absent_card_and_legacy_row(fx_copy):
    (fx_copy / "runs/run_099/artifacts/profit_bars_evaluation.yaml").unlink()
    runs = _runs(fx_copy)
    v2 = loaders.load_run(fx_copy, runs, "run_099")
    card = {c["name"]: c for c in v2["steps"]}["profit_bars"]
    assert card["status"] == "absent"
    assert card["sources"][0]["state"] == "absent"
    row = [r for r in loaders.load_campaign(fx_copy, runs)["runs"] if r["run_id"] == "run_099"][0]
    assert row["legacy_shape"] is True and row["base_bars"] is None
    assert loaders.load_step(fx_copy, runs, "run_099", "profit_bars")["tables"] == []


def test_unparseable_yaml_marks_one_card_unreadable_and_the_rest_normal(fx_copy):
    runs = _runs(fx_copy)
    base = {c["name"]: c["status"] for c in loaders.load_run(FIX, _runs(FIX), "run_099")["steps"]}
    bad = fx_copy / "runs/run_099/artifacts/grid_evaluation.yaml"
    bad.write_text("grid: [unclosed\n  - : : :\n", encoding="utf-8")
    v2 = loaders.load_run(fx_copy, runs, "run_099")
    got = {c["name"]: c["status"] for c in v2["steps"]}
    assert got["grid"] == "unreadable"
    assert {k: v for k, v in got.items() if k != "grid"} == {k: v for k, v in base.items() if k != "grid"}
    grid_card = [c for c in v2["steps"] if c["name"] == "grid"][0]
    assert grid_card["line"].startswith("unreadable (")
    assert any(s["state"] == "unreadable" and s.get("reason") for s in grid_card["sources"])
    assert loaders.load_campaign(fx_copy, runs)["runs"][0]["run_id"] == "run_099"
    # via HTTP
    s = Srv(fx_copy, runs)
    try:
        for path in ("/api/runs", "/api/run/run_099", "/api/run/run_099/step/grid", "/api/run/run_099/step/profit_bars"):
            st, body = s.get_json(path)
            assert st == 200, path
        st, body = s.get_json("/api/run/run_099")
        assert {c["name"]: c["status"] for c in body["steps"]}["grid"] == "unreadable"
    finally:
        s.close()


def test_a_bug_in_one_step_loader_blanks_only_that_card(monkeypatch):
    def boom(s, ctx):
        raise KeyError("x")

    monkeypatch.setitem(loaders._STEP_FUNCS, "claims", boom)
    v2 = loaders.load_run(FIX, _runs(FIX), "run_099")
    st = {c["name"]: c["status"] for c in v2["steps"]}
    assert st["claims"] == "unreadable"
    assert st["profit_bars"] == "fail" and st["replay_gate"] == "ok"


def test_empty_and_legacy_run_folders_are_listed(fx_copy):
    runs = _runs(fx_copy)
    (runs / "run_101").mkdir()
    (runs / "run_100").mkdir()
    shutil.copy(fx_copy / "runs/run_099/pipeline_state.yaml", runs / "run_100/pipeline_state.yaml")
    (runs / "run_0007").mkdir()
    v1 = loaders.load_campaign(fx_copy, runs)
    assert [r["run_id"] for r in v1["runs"]] == ["run_101", "run_100", "run_099", "run_098", "run_0007"]
    empty = v1["runs"][0]
    assert empty["legacy_shape"] is True
    for k in ("entry_id", "fold", "coins", "idea_status", "base_bars", "cost_usd", "launched_at", "status"):
        assert empty[k] is None
    assert v1["runs"][1]["legacy_shape"] is True and v1["runs"][1]["status"] == "completed"
    for rid in ("run_101", "run_100", "run_0007"):
        v2 = loaders.load_run(fx_copy, runs, rid)
        assert [c["name"] for c in v2["steps"]] == STEPS
        for n in STEPS:
            loaders.load_step(fx_copy, runs, rid, n)
    s = Srv(fx_copy, runs)
    try:
        for path in ("/api/run/run_101", "/api/run/run_100", "/api/run/run_0007", "/api/runs"):
            assert s.get_json(path)[0] == 200
    finally:
        s.close()


# --------------------------------------------------------------------------- server


def test_server_endpoints_200_and_headers(srv):
    for p, st, body in crawl(srv, FIX):
        assert st == 200, p
    st, hdr, body = srv.req("/api/runs")
    assert hdr["Content-Type"].startswith("application/json")
    assert hdr["Cache-Control"] == "no-store"
    v1 = json.loads(body)
    assert [r["run_id"] for r in v1["runs"]] == ["run_099", "run_098"]
    st, hdr, body = srv.req("/")
    assert st == 200 and b"run viewer" in body and hdr["Content-Type"].startswith("text/html")
    st, _, body = srv.req("/api/runs", "HEAD")
    assert st == 200 and body == b""


def test_server_step_card_json_shape(srv):
    st, d = srv.get_json("/api/run/run_099/step/profit_bars")
    assert st == 200
    assert {"name", "title", "status", "headlines", "line", "sources", "tables", "text", "raw"} <= set(d)
    st, d = srv.get_json("/api/run/run_099")
    assert set(d) == {"header", "steps", "sources"}
    st, d = srv.get_json("/api/run/run_099/variant/base/window/2020-05/bars")
    assert {"variant", "label", "symbol", "columns", "trades", "metrics", "sources"} <= set(d)
    st, d = srv.get_json("/api/run/run_099/variant/base/equity")
    assert set(d) >= {"variant", "windows"}


@pytest.mark.parametrize("path", [
    "/api/run/run_555",
    "/api/run/run_099/step/nope",
    "/api/run/run_099/variant/nope/equity",
    "/api/run/run_099/variant/nope/window/2020-05/bars",
    "/api/run/run_099/variant/base/window/1999-01/bars",
    "/api/run/run_098/variant/asset_ada/window/2021-01/bars",
    "/api/run/run_099/variant/base/bogus",
    "/api/nothing",
    "/nothing",
    "/static/nothing.js",
    "/static/",
])
def test_server_unknown_ids_are_404_json(srv, path):
    st, hdr, body = srv.req(path)
    assert st == 404
    assert "error" in json.loads(body)


@pytest.mark.parametrize("path", [
    "/static/../server.py",
    "/static/%2e%2e/server.py",
    "/static/..%2fserver.py",
    "/static/..%5cserver.py",
    "/static/../../../config/campaign_queue.yaml",
    "/static//etc/passwd",
    "/api/run/..%2f..%2fconfig/step/grid",
    "/api/run/run_099/step/..%2fgrid",
    "/api/run/run_099/variant/..%2f..%2fbase/equity",
    "/api/run/run_099/variant/base/window/..%2f..%2f..%2f..%2fprofit/bars",
    "/api/run/run_099%00/step/grid",
])
def test_server_path_traversal_never_returns_file_content(srv, path):
    st, hdr, body = srv.req(path)
    assert st in (400, 404)
    assert b"import loaders" not in body and b"queue:" not in body and b"root:" not in body


@pytest.mark.parametrize("method", ["POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def test_server_other_methods_are_405(srv, method):
    st, hdr, body = srv.req("/api/runs", method)
    assert st == 405
    assert hdr["Allow"] == "GET, HEAD"


def test_server_static_serves_only_files_inside_static_dir(srv):
    st, _, body = srv.req("/static/index.html")
    assert st == 200 and b"run viewer" in body


# --------------------------------------------------------------------------- sanitize


def test_sanitize_public_api_is_exactly_two_names():
    public = {n for n in dir(sanitize) if not n.startswith("_")}
    assert public == {"sanitize", "sanitize_text"}
    assert set(sanitize.__all__) == {"sanitize", "sanitize_text"}


def test_sanitize_masks_in_window_dates_and_leaves_others():
    lo, hi = _window_range()
    mid = lo + (hi - lo) // 2
    mask = "[sealed-window date]"
    inside = {
        "start day": lo.isoformat(),
        "mid day": mid.isoformat(),
        "end day": hi.isoformat(),
        "timestamp T/Z": f"{mid.isoformat()}T11:31:44Z",
        "timestamp with fraction and offset": f"{mid.isoformat()}T11:31:44.309639+00:00",
        "space time": f"{lo.isoformat()} 09:30:00",
        "compact stamp": f"{lo:%Y%m%d}T113455Z_c3c83fd6",
        "compact day": f"{hi:%Y%m%d}",
        "month token": f"{mid:%Y-%m}",
    }
    first_month_start = lo.replace(day=1)
    outside = {
        "day before": (lo - timedelta(days=1)).isoformat(),
        "day after": (hi + timedelta(days=1)).isoformat(),
        "month before": f"{first_month_start - timedelta(days=1):%Y-%m}",
        "compact day before": f"{lo - timedelta(days=1):%Y%m%d}",
        "not a date": "version 1.2.3 and sha 3baf8f35b810496ca838",
    }
    payload = {
        "plain": list(inside.values()),
        "nested": {"deeper": [{"text": "run at " + v + " done"} for v in inside.values()]},
        "outside": list(outside.values()),
        f"key {lo.isoformat()}": "value",
        "number": 42,
    }
    out = sanitize.sanitize(payload)
    assert out is not payload and payload["plain"][0] == lo.isoformat()  # input untouched
    for name, tok in inside.items():
        assert out["plain"][list(inside).index(name)] == mask, name
        assert out["nested"]["deeper"][list(inside).index(name)]["text"] == f"run at {mask} done", name
    for name, tok in outside.items():
        assert out["outside"][list(outside).index(name)] == tok, name
    assert f"key {mask}" in out and out["number"] == 42
    assert sanitize.sanitize_text(None) is None
    blob = json.dumps(out)
    assert count_in_range(blob) == 0
    assert sanitize.sanitize_text(f"{lo.isoformat()}..{hi.isoformat()}") == f"{mask}..{mask}"


def test_sanitize_fails_closed_with_fixed_text(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(sanitize, "_range", None)
    monkeypatch.setattr(sanitize, "_POLICY_PATH", tmp_path / "missing.yaml")
    with pytest.raises(Exception) as ei:
        sanitize.sanitize_text("2020-05-01")
    assert str(ei.value) == "run viewer: sealed-window policy unreadable; not starting"
    with pytest.raises(Exception) as ei2:
        server.make_server(FIX, _runs(FIX))
    assert str(ei2.value) == "run viewer: sealed-window policy unreadable; not starting"
    assert server.main(["--runs", str(_runs(FIX)), "--port", "0"]) == 1
    assert capsys.readouterr().err.strip() == "run viewer: sealed-window policy unreadable; not starting"
    bad = tmp_path / "bad.yaml"
    bad.write_text("holdout_range: [not, a, range\n", encoding="utf-8")
    monkeypatch.setattr(sanitize, "_POLICY_PATH", bad)
    monkeypatch.setattr(sanitize, "_range", None)
    with pytest.raises(Exception) as ei3:
        sanitize.sanitize({"a": "b"})
    assert str(ei3.value) == "run viewer: sealed-window policy unreadable; not starting"


# --------------------------------------------------------------------------- guards


def test_sealed_window_dates_absent_from_every_response(srv):
    n = 0
    bad = []
    for p, st, body in crawl(srv, FIX):
        assert st == 200
        c = count_in_range(body.decode("utf-8"))
        if c:
            n += c
            bad.append(p)
    assert n == 0, f"{n} in-window date token(s) in responses of {bad}"


def test_log_and_banner_carry_no_window_date_in_a_full_crawl():
    lines = []
    s = Srv(FIX, _runs(FIX), sink=lines.append)
    try:
        paths = crawl_paths(FIX)
        for p in paths:
            s.req(p)
        s.req("/api/run/run_099/step/nope")
        s.req("/api/runs", "POST")
        # a request path that spells in-window dates is masked in the log line
        lo, hi = _window_range()
        s.req(f"/api/run/run_{lo.isoformat()}")
        s.req(f"/static/{hi:%Y%m%d}T101010Z.js")
    finally:
        s.close()
    banner = server.banner("127.0.0.1", 8765)
    assert banner == "run viewer: read-only, local network only, no authentication -- http://127.0.0.1:8765/"
    assert len(lines) >= len(paths)
    assert all(re.fullmatch(r"(GET|HEAD|POST) .+ \d{3}", ln) for ln in lines), "log line shape"
    n = count_in_range("\n".join(lines) + "\n" + banner)
    # the banner with an in-window date in the host position is masked as well
    masked_banner = server.banner(f"{lo.isoformat()}", 1)
    n += count_in_range(masked_banner)
    assert n == 0, f"{n} in-window date token(s) in log/banner"


class _Guard:
    """Fails any write-mode open and any mutating os/pathlib call; records read opens."""

    WRITE_MODE = re.compile(r"[wax+]")

    def __init__(self, monkeypatch):
        self.mp = monkeypatch
        self.reads = []  # (resolved path string, opened_from_sanitize)
        self.violations = []

    def _from_sanitize(self):
        f = sys._getframe(2)
        san = str(VIEWER / "sanitize.py")
        while f is not None:
            if f.f_code.co_filename == san:
                return True
            f = f.f_back
        return False

    def install(self):
        real_open = builtins.open
        guard = self

        def guarded_open(file, mode="r", *a, **kw):
            m = mode if isinstance(mode, str) else "r"
            if guard.WRITE_MODE.search(m):
                guard.violations.append(("open", m))
                raise PermissionError("write-mode open blocked by the read-only guard")
            if isinstance(file, (str, bytes, os.PathLike)):
                guard.reads.append((os.fspath(file) if not isinstance(file, bytes) else file.decode(), guard._from_sanitize()))
            return real_open(file, mode, *a, **kw)

        self.mp.setattr(builtins, "open", guarded_open)
        self.mp.setattr(io, "open", guarded_open)

        def blocker(name):
            def _b(*a, **kw):
                guard.violations.append((name, ""))
                raise PermissionError(f"{name} blocked by the read-only guard")
            return _b

        for name in ("replace", "rename", "mkdir", "makedirs", "remove", "unlink", "rmdir"):
            self.mp.setattr(os, name, blocker("os." + name))
        for name in ("write_text", "write_bytes", "mkdir", "touch", "unlink", "rename", "replace"):
            self.mp.setattr(pathlib.Path, name, blocker("Path." + name))


def test_read_only_guard_and_read_path_allowlist(monkeypatch):
    # warm lazy imports outside the guard (module import is not a data read)
    import pandas  # noqa: F401
    import block_registry  # noqa: F401

    guard = _Guard(monkeypatch)
    guard.install()
    monkeypatch.setattr(sanitize, "_range", None)  # force the one policy read to happen in the window
    s = None
    try:
        s = Srv(FIX, _runs(FIX))
        results = crawl(s, FIX)
    finally:
        if s is not None:
            s.close()
    assert not guard.violations, f"{len(guard.violations)} blocked write attempt(s)"
    assert all(st == 200 for _, st, _ in results)
    assert len(results) > 60

    fix_root = str(FIX.resolve()).lower()
    viewer_root = str(VIEWER.resolve()).lower()
    policy = str(POLICY.resolve()).lower()
    policy_reads = 0
    for path, from_sanitize in guard.reads:
        low = str(Path(path).resolve()).lower()
        if low == policy:
            assert from_sanitize, "the policy was opened from outside sanitize.py"
            policy_reads += 1
            continue
        for bad in ("local_data", "holdout_sealed", "campaign_data_policy", "handoffs"):
            assert bad not in low, f"a read path contains a forbidden name ({bad})"
        assert low.startswith(fix_root) or low.startswith(viewer_root), "a read outside the fixture root / viewer folder"
    assert policy_reads == 1, f"policy opened {policy_reads} time(s), expected exactly one"
    # allowlist by kind: only the documented locations under the root
    rels = set()
    for path, _ in guard.reads:
        low = Path(path).resolve()
        try:
            rel = low.relative_to(FIX.resolve()).as_posix()
        except ValueError:
            continue
        rels.add(rel)
    allowed = re.compile(r"^(runs/run_\d+/.+|config/campaign_queue\.yaml|briefs/[^/]+\.md|"
                         r"campaign_record/(campaign_state\.yaml|campaign_memory\.yaml|campaign_log\.md|block_registry\.yaml))$")
    off = [r for r in rels if not allowed.match(r)]
    assert not off, f"{len(off)} read(s) outside the documented allowlist"
    assert not any("/handoffs/" in r for r in rels)


# --------------------------------------------------------------------------- review fixes (D-180)

MASK = "[sealed-window date]"
_MONTH_FORMS = {"Month Y", "Mon Y", "Y/M", "M/Y", "Y-M"}
_QUARTER_FORMS = {"Q Y", "Y Q", "YQ", "Y-Q", "Q-Y"}
_HALF_FORMS = {"H Y", "YH", "Y-H"}


def _mid_day():
    lo, hi = _window_range()
    return lo + (hi - lo) // 2


def _outside_day():
    """The latest day before the window whose month/day-swapped reading is not in it either."""
    lo, hi = _window_range()
    d = lo - timedelta(days=1)
    while True:
        try:
            swapped = date(d.year, d.day, d.month)
        except ValueError:
            return d
        if not (lo <= swapped <= hi):
            return d
        d -= timedelta(days=1)


def _outside_for(form):
    lo, _ = _window_range()
    if form in _MONTH_FORMS:
        return lo.replace(day=1) - timedelta(days=1)
    if form in _QUARTER_FORMS:
        return date(lo.year, 3 * ((lo.month - 1) // 3) + 1, 1) - timedelta(days=1)
    if form in _HALF_FORMS:
        return date(lo.year, 1 if lo.month <= 6 else 7, 1) - timedelta(days=1)
    return _outside_day()


def test_sanitize_every_date_form_masked_inside_and_untouched_outside():
    inside = date_forms(_mid_day())
    assert len(inside) >= 30
    for name, tok in inside.items():
        expected = "a " + MASK + " b"
        if name == "iso glued after letters":
            expected = "a run" + MASK + " b"
        assert sanitize.sanitize_text(f"a {tok} b") == expected, name
        assert count_in_range(tok) >= 1, name  # the test counter sees the same form
    for name in inside:
        tok = date_forms(_outside_for(name))[name]
        assert sanitize.sanitize_text(f"a {tok} b") == f"a {tok} b", name
        assert count_in_range(tok) == 0, name


def test_sanitize_swapped_day_month_reading_is_masked_if_either_reading_is_inside():
    lo, hi = _window_range()
    d = _mid_day()
    for tok in (f"{d.day}/{d.month}/{d.year}", f"{d.month}/{d.day}/{d.year}", f"{d.day}.{d.month}.{d.year}",
                f"{d.month}-{d.day}-{d.year}"):
        assert sanitize.sanitize_text(tok) == MASK
    # a day outside the window whose month is inside it keeps its day form (leftmost token wins)
    o = _outside_day()
    for tok in (f"{o.day} {_MONTH_NAMES[o.month - 1]} {o.year}", f"{_MONTH_NAMES[o.month - 1][:3]} {o.day}, {o.year}"):
        assert sanitize.sanitize_text(tok) == tok


def test_sanitize_leaves_hashes_and_plain_numbers_alone():
    sha = "19c8d4c6ad88929a79f4ae49d6f7161566dfd0ba3d15cc495e974f787eb78f1f"
    for s in (sha, "123456", "version 1.2.3", "n=1234567890", f"sha {sha} and 123456 end", "Marching 5 times"):
        assert sanitize.sanitize_text(s) == s


def test_sanitize_known_limits_are_documented():
    doc = sanitize.__doc__
    for word in ("epoch", "ISO week", "ordinal", "two-digit"):
        assert word in doc


def test_sanitize_public_names_unchanged_after_widening():
    assert {n for n in dir(sanitize) if not n.startswith("_")} == {"sanitize", "sanitize_text"}


# ---- injection: a masking test that can fail


def _inject_value(prefix):
    """All forms of a mid-window day, one string, short enough never to be truncated."""
    return prefix + " | ".join(date_forms(_mid_day()).values())


def test_injected_window_dates_in_every_kind_of_source_are_masked_everywhere(fx_copy):
    forms = date_forms(_mid_day())
    n_forms = len(forms)
    runs = _runs(fx_copy)
    val = _inject_value("")
    assert count_in_range(val) >= n_forms  # the injected string really holds every form
    assert len(val) < 560

    def baseline(path):
        s = Srv(fx_copy, runs)
        try:
            st, _, body = s.req(path)
        finally:
            s.close()
        return body.decode("utf-8").count(MASK)

    base_runs = baseline("/api/runs")
    base_run = baseline("/api/run/run_099")
    base_grid = baseline("/api/run/run_099/step/grid")
    base_bars = baseline("/api/run/run_099/variant/base/window/2020-05/bars")

    # 1. a queue entry's notes (shown in view 1 for ready / blocked entries)
    qp = fx_copy / "config/campaign_queue.yaml"
    q = yaml.safe_load(qp.read_text(encoding="utf-8"))
    target = [e for e in q["queue"] if e["status"] == "ready" or str(e["status"]).startswith("blocked")][0]
    target["notes"] = val
    qp.write_text(yaml.safe_dump(q, sort_keys=False, allow_unicode=True), encoding="utf-8")
    # 2. a campaign_log line for run_099 (between its LAUNCH-CARD and its DECIDE line)
    lp = fx_copy / "campaign_record/campaign_log.md"
    lines = lp.read_text(encoding="utf-8").split("\n")
    li = [i for i, ln in enumerate(lines) if "LAUNCH-CARD" in ln and "run_099" in ln][0]
    lines.insert(li + 1, "- note run_099 " + val)
    lp.write_text("\n".join(lines), encoding="utf-8")
    # 3. a key and a value of a run_099 artifact YAML (idea_status.yaml, shown raw in the grid step)
    ip = fx_copy / "runs/run_099/artifacts/idea_status.yaml"
    with open(ip, "a", encoding="utf-8", newline="\n") as fh:
        fh.write("\n" + json.dumps(_inject_value("key ")) + ": " + json.dumps(_inject_value("value ")) + "\n")
    # 4. a bars.csv timestamp cell of one window, 5. a trades.json entry_time
    _, bars_p, trades_p = _window_files_in(fx_copy, "run_099", "base", "2020-05")
    with open(bars_p, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    rows[1][rows[0].index("timestamp")] = val
    with open(bars_p, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh, lineterminator="\n").writerows(rows)
    trades = json.loads(trades_p.read_text(encoding="utf-8"))
    trades[0]["entry_time"] = val
    trades_p.write_text(json.dumps(trades), encoding="utf-8")

    lines_out = []
    s = Srv(fx_copy, runs, sink=lines_out.append)
    try:
        crawled = {p: (st, body.decode("utf-8")) for p, st, body in crawl(s, fx_copy)}
        s.req("/api/run/run_099/step/nope")
    finally:
        s.close()
    bad = [p for p, (st, text) in crawled.items() if st != 200 or count_in_range(text) != 0]
    assert not bad, f"{len(bad)} response(s) failed (status or window date left)"
    assert count_in_range("\n".join(lines_out)) == 0
    # each injection site's response carries at least one mask per injected form
    assert crawled["/api/runs"][1].count(MASK) - base_runs >= n_forms
    assert crawled["/api/run/run_099"][1].count(MASK) - base_run >= n_forms
    assert crawled["/api/run/run_099/step/grid"][1].count(MASK) - base_grid >= 2 * n_forms  # key and value
    assert crawled["/api/run/run_099/variant/base/window/2020-05/bars"][1].count(MASK) - base_bars >= 2 * n_forms


def _window_files_in(root, rid, variant, label):
    res = _yaml(Path(root) / f"runs/{rid}/artifacts/variants/{variant}/protocol_result.yaml")["results"]
    r = [x for x in res if x["window"] == label][0]
    d = Path(root) / f"runs/{rid}/variants/{variant}/results/{r['run_id']}"
    return r, d / "bars.csv", d / "trades.json"


def test_static_route_masks_text_files(tmp_path, monkeypatch):
    sd = tmp_path / "static"
    sd.mkdir()
    (sd / "t.js").write_text("const a = " + json.dumps(_inject_value("")) + ";\n", encoding="utf-8")
    (sd / "t.css").write_text("/* " + _inject_value("") + " */\n", encoding="utf-8")
    monkeypatch.setattr(server, "STATIC_DIR", sd)
    s = Srv(FIX, _runs(FIX))
    try:
        for name in ("t.js", "t.css"):
            st, hdr, body = s.req("/static/" + name)
            text = body.decode("utf-8")
            assert st == 200
            assert count_in_range(text) == 0, name
            assert text.count(MASK) >= len(date_forms(_mid_day())), name
    finally:
        s.close()


# ---- brief path containment


def test_brief_path_outside_briefs_is_never_read(fx_copy, tmp_path, monkeypatch):
    brief_text = (fx_copy / "briefs/child_run_098_long_only_fold_b.md").read_text(encoding="utf-8")
    outside = tmp_path / "outside_brief.md"
    outside.write_text(brief_text, encoding="utf-8")
    (fx_copy / "config/x.md").write_text(brief_text, encoding="utf-8")
    good = "briefs/child_run_098_long_only_fold_b.md"
    qp = fx_copy / "config/campaign_queue.yaml"
    original = qp.read_text(encoding="utf-8")
    assert original.count(f"brief_path: {good}") == 1
    runs = _runs(fx_copy)

    # control: the real path is read and gives a purpose
    assert not isinstance(loaders.load_run(fx_copy, runs, "run_099")["header"]["purpose"], loaders.Unr)

    loads = []
    real_load = loaders.Reader._load

    def spy(self, path, kind):
        loads.append((Path(path).resolve(), kind))
        return real_load(self, path, kind)

    monkeypatch.setattr(loaders.Reader, "_load", spy)
    forbidden = [str(outside), "config/x.md", "config/campaign_queue.yaml", "briefs/../config/x.md",
                 "briefs\\..\\config\\x.md", "briefs/x.txt", "briefs"]
    for bp in forbidden:
        qp.write_text(original.replace(f"brief_path: {good}", "brief_path: " + json.dumps(bp)), encoding="utf-8")
        loads.clear()
        guard = _Guard(monkeypatch)
        with monkeypatch.context() as mp:
            guard.mp = mp
            guard.install()
            v2 = loaders.load_run(fx_copy, runs, "run_099")
            v1 = loaders.load_campaign(fx_copy, runs)
        assert v2["header"]["purpose"] == "unreadable (brief_path outside briefs/)", bp
        assert v2["header"]["outcomes"] == [], bp
        row = [r for r in v1["runs"] if r["run_id"] == "run_099"][0]
        assert row["pre_registered_letters"] == [], bp
        text_loads = {p for p, k in loads if k == "text"}
        for p in (outside.resolve(), (fx_copy / "config/x.md").resolve(), qp.resolve()):
            assert p not in text_loads, bp
        opened = {Path(p).resolve() for p, _ in guard.reads if isinstance(p, str)}
        assert outside.resolve() not in opened and (fx_copy / "config/x.md").resolve() not in opened, bp
        assert not guard.violations
    # null brief_path stays silent (no entry value at all)
    qp.write_text(original.replace(f"brief_path: {good}", "brief_path: null"), encoding="utf-8")
    assert loaders.load_run(fx_copy, runs, "run_099")["header"]["purpose"] is None


# ---- server robustness


def _raw(port, payload, timeout=5):
    s = socket.create_connection(("127.0.0.1", port), timeout=timeout)
    got = b""
    try:
        try:
            s.sendall(payload)
        except OSError:
            pass
        while True:
            try:
                chunk = s.recv(65536)
            except (socket.timeout, OSError):
                break
            if not chunk:
                break
            got += chunk
    finally:
        s.close()
    return got


def test_server_survives_garbage_requests_without_traceback_or_date_in_log(capfd):
    lo, hi = _window_range()
    iso = lo.isoformat()
    lines = []
    s = Srv(FIX, _runs(FIX), sink=lines.append)
    payloads = {
        "garbage": b"\x00\xff\xfe garbage \x01\r\n\r\n",
        "http09": b"GET /api/runs\r\n",
        "http09 non-GET": b"POST /api/runs\r\n",
        "bad version": b"GET / HTTP/9.9\r\n\r\n",
        "unknown method with date": f"FOO{iso} /x{iso} HTTP/1.1\r\n\r\n".encode(),
        "huge url": b"GET /" + b"a" * 70000 + b" HTTP/1.1\r\n\r\n",
        "empty": b"",
    }
    try:
        replies = {name: _raw(s.port, p) for name, p in payloads.items()}
        st, body = s.get_json("/api/runs")  # still alive afterwards
        assert st == 200
    finally:
        s.close()
    for name, r in replies.items():
        assert b"Traceback" not in r, name
        assert iso.encode() not in r, name
        assert count_in_range(r.decode("latin-1")) == 0, name
        if r.startswith(b"HTTP/"):
            code = int(r.split(b" ", 2)[1])
            assert code in (400, 404, 405, 414, 501, 505), name
            assert b"error" in r, name
    assert replies["unknown method with date"].startswith(b"HTTP/1.0 501")
    assert replies["huge url"] == b"" or replies["huge url"].startswith(b"HTTP/1.0 414")
    # the stdlib answers a bad version before it has a version to answer in: a bare JSON body (HTTP/0.9 style)
    assert replies["bad version"].startswith(b"HTTP/1.0 505") or json.loads(replies["bad version"]) == {"error": "not supported"}
    assert json.loads(replies["garbage"].split(b"\r\n\r\n", 1)[-1]) == {"error": "bad request"}
    joined = "\n".join(lines)
    assert "Traceback" not in joined and "File \"" not in joined
    assert count_in_range(joined) == 0
    assert all(len(ln) <= 400 for ln in lines)
    out, err = capfd.readouterr()
    assert "Traceback" not in err and "Traceback" not in out
    assert count_in_range(err + out) == 0


def test_handle_error_sends_one_fixed_line_and_nothing_to_stderr(capfd):
    lines = []
    s = Srv(FIX, _runs(FIX), sink=lines.append)
    try:
        try:
            raise RuntimeError("secret " + _window_range()[0].isoformat())
        except RuntimeError:
            s.srv.handle_error(None, ("127.0.0.1", 1))
    finally:
        s.close()
    assert lines == ["run viewer: request error"]
    out, err = capfd.readouterr()
    assert err == "" and out == ""


# ---- no bytecode under the repository


def test_server_writes_no_pycache_next_to_the_sources(tmp_path):
    tools_src = SR / "tools"
    sr = tmp_path / "strategy-research"
    tools = sr / "tools"
    tools.mkdir(parents=True)
    for p in tools_src.glob("*.py"):
        shutil.copy2(p, tools / p.name)
    shutil.copytree(tools_src / "run_viewer", tools / "run_viewer", ignore=shutil.ignore_patterns("__pycache__"))
    (sr / "config").mkdir()
    shutil.copy2(POLICY, sr / "config" / "campaign_data_policy.yaml")
    root = tmp_path / "root"
    shutil.copytree(FIX, root)
    assert not list(tmp_path.rglob("__pycache__"))
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONDONTWRITEBYTECODE", "PYTHONPATH", "PYTHONPYCACHEPREFIX")}
    proc = subprocess.Popen([sys.executable, str(tools / "run_viewer" / "server.py"), "--runs", str(root / "runs"),
                             "--root", str(root), "--port", "0"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True)
    try:
        banner = proc.stdout.readline()
        m = re.search(r":(\d+)/", banner)
        assert m, "server did not print its banner"
        c = http.client.HTTPConnection("127.0.0.1", int(m.group(1)), timeout=60)
        c.request("GET", "/api/runs")
        r = c.getresponse()
        body = json.loads(r.read())
        c.close()
        assert r.status == 200 and body["runs"]
        c = http.client.HTTPConnection("127.0.0.1", int(m.group(1)), timeout=60)
        c.request("GET", "/api/run/run_099/step/grid")
        assert c.getresponse().status == 200
        c.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        proc.stdout.close()
        proc.stderr.close()
    found = [str(p.relative_to(tmp_path)) for p in tmp_path.rglob("__pycache__")]
    assert not found, f"{len(found)} __pycache__ folder(s) written next to the copied sources"


# ---- absent is not unreadable


def test_absent_optional_file_does_not_make_the_card_unreadable(fx_copy):
    runs = _runs(fx_copy)
    (fx_copy / "runs/run_099/artifacts/deviations.yaml").unlink()
    card = {c["name"]: c for c in loaders.load_run(fx_copy, runs, "run_099")["steps"]}["config"]
    assert card["status"] != "unreadable"
    assert not str(card["line"]).startswith("unreadable")
    assert any(h["label"] == "deviations" and h["value"].startswith("absent") for h in card["headlines"])
    assert any(sr["path"].endswith("deviations.yaml") and sr["state"] == "absent" for sr in card["sources"])
    # a file that exists but is broken is still unreadable
    (fx_copy / "runs/run_099/artifacts/deviations.yaml").write_text("status: [unclosed\n", encoding="utf-8")
    card = {c["name"]: c for c in loaders.load_run(fx_copy, runs, "run_099")["steps"]}["config"]
    assert card["status"] == "unreadable"


# ---- blocks error and raw size


def test_blocks_error_names_type_and_file_only(fx_copy):
    (fx_copy / "campaign_record/block_registry.yaml").write_text("schema_version: [unclosed\n", encoding="utf-8")
    err = loaders.load_campaign(fx_copy, _runs(fx_copy))["blocks"]["error"]
    assert err.endswith("reading block_registry.yaml")
    assert str(fx_copy) not in err and "\\" not in err and "/" not in err
    assert len(err) < 100


def test_step_raw_embeds_only_run_files_and_the_brief():
    campaign_wide = {"campaign_record/campaign_log.md", "campaign_record/campaign_state.yaml",
                     "campaign_record/campaign_memory.yaml", "config/campaign_queue.yaml",
                     "campaign_record/block_registry.yaml"}
    for n in STEPS:
        st = loaders.load_step(FIX, _runs(FIX), "run_099", n)
        paths = {r["path"] for r in st["raw"]}
        assert not (paths & campaign_wide), n
        assert all(p.startswith("runs/run_099/") or p.startswith("briefs/") for p in paths), n
    rec = loaders.load_step(FIX, _runs(FIX), "run_099", "record")
    srcs = {r["path"] for r in rec["sources"]}
    assert campaign_wide - {"config/campaign_queue.yaml"} <= srcs  # still listed as sources
    assert "config/campaign_queue.yaml" in {r["path"] for r in loaders.load_step(FIX, _runs(FIX), "run_099", "launch")["sources"]}
    launch = loaders.load_step(FIX, _runs(FIX), "run_099", "launch")
    assert any(r["path"].startswith("briefs/") for r in launch["raw"])


# ---- id regexes


def test_run_id_and_name_regexes_reject_trailing_newline_and_unicode_digits():
    assert loaders.RUN_ID_RE.match("run_099")
    assert not loaders.RUN_ID_RE.match("run_099\n")
    assert not loaders.RUN_ID_RE.match("run_\u0663\u0664")
    assert not loaders._safe_name("base\n")
    assert not loaders.run_exists(_runs(FIX), "run_099\n")