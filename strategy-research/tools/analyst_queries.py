"""E-075 PR-4 (CUL-422, D-088): the analyst's query engine -- six fixed functions
over ONE saved run's own bars and trades. A pure module: no SDK, no model call,
no network, and nothing in the pipeline imports it yet (PR-5 wires it).

Design: engineering/delivery_plan_readers.md (Amendment 1, Step 11, A1.8 draft v2
item 7, A1.11 items 5 and 7); engineering/roadmap/E-075/PHASE_A.md section 2
(the six functions) as cut by ITERATIVE_PLAN_JUDGEMENT.md section 4 (PR-4: no
placebo arm, no outcome layer, no exploration/confirmation split -- the run is
read as it is, its folds being the only windows it has).

The six functions (all take `variant="base"`, last but for conditional_effect's floor)
--------------------------------------------------
  list_columns()
  describe(column, by=None)
  distribution(column, by=None, bins=10)
  conditional_effect(condition, horizons=None, outcome=None, baseline=None,
                     statistic="mean_diff", direction="greater", by=None, floor=None)
  trade_slice(filter, agg, by=None)
  event_study(trade_filter, bars_before, bars_after)

`floor` (D-094) is written into the returned `test` block (default {min_events: 1}),
so a claim can carry the floor it will be graded with and still be the test that ran.
The floor never changes a measured number (claim_tests.effect_sizes does not read it).

`conditional_effect` is expressed in the claim-test slots: its condition is one
bar selector (claim_tests.SELECTORS plus the gated `trailing_vol` field) or the
PR-3 `trade` selector, and it calls claim_tests.effect_sizes with the TestSpec
built from the slots, so its numbers ARE what claim_measure.measure_test reads
(equality is tested for every selector / outcome / baseline / statistic
combination the slots allow). Its result carries the exact `test` block, ready
to paste into a claim, and whether claim_card accepts it with the trade family
on (`compiles_as_claim`: the analyst's own proposal check, check_claim with
trade_tests=True; a bar test with the gated `trailing_vol` field is still
refused there). D-090: "today" in D-088 meant that check, not the pipeline's
other check_claim calls, which do not pass trade_tests yet.

What it can read (and cannot)
-----------------------------
  * ONE run directory, passed in. Every file read is `bars.csv` or `trades.json`
    of a window named by the variant's `protocol_result.yaml`, plus the variant's
    `trade_diagnostics.json`, all resolved and refused unless they sit inside the
    run directory (no `..`, no symlink out, no absolute run id). Never
    `trading-bot/local_data/` (claim_tests.load_variant_bars is called with no
    cache, so no warm-up rows exist), never another run, never a path given by
    the caller: the functions take typed values from closed vocabularies only
    (a column name from the data dictionary, a selector from the claim engine, a
    trade field from claim_tests.TRADE_FIELDS), never a path, a regex or code.
  * A run directory whose resolved path has a `local_data` or `holdout_sealed`
    component is refused, and any bar at or after the holdout start (read from
    config/campaign_data_policy.yaml; unreadable = refuse everything) is refused
    (claim_measure.check_before_holdout).
  * It writes only the query log (default `<run>/artifacts/analyst_queries.yaml`).

Why this cannot leak (no lookahead)
-----------------------------------
  * Conditions are the claim engine's: bar-t fields only (check_spec refuses any
    other field), trade selectors read the lot's own entry stamp and the exit
    descriptors the PR-3 guide labels as such.
  * `describe` / `distribution` read columns the data dictionary marks `close` or
    `fill` (known at the bar's close, before or at the decision), plus the
    derived `past_return_<n>` / `trailing_vol_<n>` (rows t-n..t only). A column
    marked `exit` / `after` is outcome-only and refused here; `meta` is a label
    (usable as `by` only); `run` / `end` are never offered (finding A1: the
    end-of-run balances repeated on every row are a real lookahead).
  * Outcomes (`fwd_return` ..., `trade_net_return`, `post_exit_return`) are
    matched by timestamp inside one window by the claim engine; event_study's
    "after" half is an outcome, labelled as such in the result.

Comparisons (the look counter)
------------------------------
One comparison is one returned number that relates a condition or a group to an
outcome. Feature-only results count 0.
  conditional_effect  horizons x groups (groups = 1 without `by`, else the number
                      of windows / coins returned; the pooled number returned
                      beside a `by` is not counted again)
  trade_slice         groups x (aggregates of trade_net_return / post_exit_return
                      whose stat is not `count`)
  event_study         the number of "after" checkpoints returned
  describe, distribution  the number of groups when grouped by hour, weekday or
                      regime, whatever the column: past_return_1 at bar t+1 IS
                      fwd_return h=1 at bar t, and the difference of two bucket
                      means of a price level is the mean move between the buckets,
                      so a mean by hour is a calendar effect, and by a persistent
                      regime label nearly a regime effect (D-090); else 0
  list_columns  0
A session may spend COMPARISON_BUDGET (150); a call that would count more than
what is left is refused with "comparison budget spent".

The log
-------
Every call -- refused ones included -- is appended to the query log BEFORE its
result is returned: a sequential id (q1, q2, ...), the function, the parameters,
the status, a short digest, the result itself and its hash, the comparisons it
counts and the cumulative total. The id is in the returned dict. An unexpected
error is logged as status `error` and re-raised; a refusal is returned, not
raised.

Caps per call: at most MAX_GROUPS groups, MAX_HORIZONS horizons, and a result of
at most MAX_RESULT_CHARS characters; over any of them the call is refused with
the reason and counts 0.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
from pathlib import Path

import numpy as np
import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import claim_measure as cmeas  # noqa: E402
import claim_tests as ct  # noqa: E402

SCHEMA_VERSION = 1
LOG_REL = "artifacts/analyst_queries.yaml"
DICTIONARY_PATH = Path(_HERE).parent / "docs" / "DATA_DICTIONARY.md"

MAX_GROUPS = 12
MAX_HORIZONS = 6
MAX_RESULT_CHARS = 4000
COMPARISON_BUDGET = 150
MAX_AGGS = 4
MAX_TRADE_CLAUSES = ct.MAX_TRADE_CLAUSES
MAX_FIELD_BARS = 1000                     # past_return_<n> / trailing_vol_<n>
BINS_RANGE = (2, 20)
# the "after"/"before" checkpoints of event_study, per cadence (PHASE_A 2.2)
CHECKPOINTS = {"hourly": (1, 2, 3, 6, 12, 24), "daily": (1, 2, 3, 5, 10)}

BY_BARS = ("window", "coin", "regime", "weekday", "hour")
BY_EFFECT = ("window", "coin")
BY_TRADES = ("window", "direction", "regime_at_entry", "weekday", "hour")
AGG_FIELDS = ("trade_net_return", "post_exit_return", "holding_bars", "entry_forecast")
AGG_STATS = ("mean", "median", "share_positive", "count")
# an aggregate relates a group to an outcome only for these fields
_OUTCOME_AGG_FIELDS = ("trade_net_return", "post_exit_return")
DERIVED_COLUMNS = ("past_return", "trailing_vol")
_DERIVED_RE = re.compile(r"(past_return|trailing_vol)_([0-9]+)")
_SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.\-]*")
_WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
FORBIDDEN_PARTS = ("local_data", ct.HOLDOUT_DIR_NAME)
DAY = ct.DAY

ROLE_OF_WHEN = {"close": "feature", "fill": "feature", "exit": "outcome", "after": "outcome",
                "meta": "label", "run": "never", "end": "never"}


# describe / distribution grouped by these labels relate a calendar or regime group to an
# outcome (past_return_1 at t+1 == fwd_return h=1 at t; a price level's bucket means differ
# by the move between the buckets): one comparison per group, whatever the column (D-090)
_CALENDAR_BY = ("hour", "weekday", "regime")


def _nonfinite(v) -> bool:
    """True when a parameter holds a NaN or an infinite number anywhere (JSON allows
    `NaN` / `Infinity` / 1e999; the log would show None and the test block would not be
    the one that ran)."""
    if isinstance(v, dict):
        return any(_nonfinite(x) for x in v.values())
    if isinstance(v, (list, tuple)):
        return any(_nonfinite(x) for x in v)
    return isinstance(v, (float, np.floating)) and not math.isfinite(float(v))


class QueryRefused(Exception):
    """A call the engine will not run (bad parameter, cap, budget, path). Logged
    with its reason and returned, never raised to the caller."""


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def _py(v):
    """JSON/YAML-safe copy: numpy scalars -> python, non-finite floats -> None."""
    if isinstance(v, dict):
        return {str(k): _py(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_py(x) for x in v]
    if isinstance(v, (np.bool_,)):
        return bool(v)
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        f = float(v)
        return f if math.isfinite(f) else None
    return v


def r8(v):
    """A number rounded to 8 significant digits (None for None / non-finite)."""
    if v is None:
        return None
    f = float(v)
    return float(f"{f:.8g}") if math.isfinite(f) else None


def _canon_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _inside(path: Path, root: Path) -> bool:
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
        return True
    except (ValueError, OSError):
        return False


def _to_float(s) -> float:
    if s is None:
        return float("nan")
    t = str(s).strip()
    if t == "":
        return float("nan")
    if t in ("True", "true"):
        return 1.0
    if t in ("False", "false"):
        return 0.0
    try:
        return float(t)
    except ValueError:
        return float("nan")


# ---------------------------------------------------------------------------
# The data dictionary: the closed vocabulary of columns
# ---------------------------------------------------------------------------

_BARS_OPEN = "<!-- data-dictionary: bars.csv -->"
_TABLE_CLOSE = "<!-- /data-dictionary -->"


def load_bars_dictionary(path=None) -> list:
    """The bars.csv table of docs/DATA_DICTIONARY.md as [{field, meaning, unit,
    when, role, pattern}]. `pattern`: a compiled regex for a field with a
    `<placeholder>` (a component id, an asset, ...), else None. Raises
    ValueError on a row that is not 5 cells or a `when` it does not know."""
    text = Path(path or DICTIONARY_PATH).read_text(encoding="utf-8")
    start = text.index(_BARS_OPEN) + len(_BARS_OPEN)
    block = text[start:text.index(_TABLE_CLOSE, start)]
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Field"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 5:
            raise ValueError(f"data dictionary row is not 5 cells: {line[:80]!r}")
        field_ = cells[0].strip("`")
        when = cells[4].strip("`")
        if when not in ROLE_OF_WHEN:
            raise ValueError(f"data dictionary: {field_!r} has unknown 'when known' {when!r}")
        pattern = None
        # a field that is ONLY a placeholder (`<reserved feed>`) would match every column
        # name: it stays unmatchable, so an unknown column is never taken for it
        if "<" in field_ and re.sub(r"<[^>]+>", "", field_).strip("."):
            pattern = re.compile("".join(
                "[^.]+" if seg.startswith("<") else re.escape(seg)
                for seg in re.split(r"(<[^>]+>)", field_) if seg))
        rows.append({"field": field_, "meaning": cells[1], "unit": cells[2], "when": when,
                     "role": ROLE_OF_WHEN[when], "pattern": pattern})
    if not rows:
        raise ValueError("data dictionary: the bars.csv table is empty")
    return rows


def dictionary_row(rows: list, column: str):
    """The dictionary row a bars.csv column belongs to (exact name first, then a
    placeholder pattern), or None."""
    for r in rows:
        if r["pattern"] is None and r["field"] == column:
            return r
    for r in rows:
        if r["pattern"] is not None and r["pattern"].fullmatch(column):
            return r
    return None


# ---------------------------------------------------------------------------
# The log
# ---------------------------------------------------------------------------

_YAML_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
_YAML_DUMPER = getattr(yaml, "CSafeDumper", yaml.SafeDumper)


class QueryLog:
    """artifacts/analyst_queries.yaml: one entry per call, rewritten atomically
    on every append. `append` returns only after the file holds the entry.

    One writer at a time (a session). The file is read once and kept in memory;
    it is read again if its size or modification time is not what this object
    last wrote (another engine on the same file, a resumed session)."""

    def __init__(self, path):
        self.path = Path(path)
        self._cache = None
        self._sig = None

    def _signature(self):
        st = self.path.stat()
        return (st.st_mtime_ns, st.st_size)

    def entries(self) -> list:
        if not self.path.exists():
            self._cache, self._sig = None, None
            return []
        sig = self._signature()
        if self._cache is None or sig != self._sig:
            doc = yaml.load(self.path.read_text(encoding="utf-8"), Loader=_YAML_LOADER) or {}
            qs = doc.get("queries") if isinstance(doc, dict) else None
            if not isinstance(qs, list):
                raise ValueError(f"{self.path}: not an analyst query log (no `queries` list)")
            self._cache, self._sig = qs, sig
        return self._cache

    def cumulative_comparisons(self) -> int:
        # a negative count in a hand-edited log never gives budget back (D-090)
        return int(sum(max(0, int(q.get("n_comparisons") or 0)) for q in self.entries()
                       if q.get("status") == "ok"))

    def append(self, entry: dict) -> dict:
        entries = list(self.entries())
        entry = dict(entry)
        entry["id"] = f"q{len(entries) + 1}"
        entry["cumulative_comparisons"] = self.cumulative_comparisons() + int(
            entry.get("n_comparisons") or 0)
        ordered = {k: entry[k] for k in ("id", "function", "params", "status", "reason",
                                          "n_comparisons", "cumulative_comparisons", "digest",
                                          "result_sha256", "result") if k in entry}
        entries.append(_py(ordered))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_name(self.path.name + ".tmp")
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            yaml.dump({"schema_version": SCHEMA_VERSION,
                       "note": ("every call of the analyst's query tools, in order, written "
                                "before the result was returned; n_comparisons counts the "
                                "numbers that relate a condition or group to an outcome"),
                       "queries": entries}, f, Dumper=_YAML_DUMPER, sort_keys=False,
                      allow_unicode=True, width=120)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, self.path)
        self._cache, self._sig = entries, self._signature()
        return entry


# ---------------------------------------------------------------------------
# The engine
# ---------------------------------------------------------------------------

class QueryEngine:
    """The six query functions over one run directory.

    `run_dir`: the saved run (must exist; its resolved path may not contain a
    `local_data` or `holdout_sealed` component). `log_path`: where the query log
    goes (default `<run_dir>/artifacts/analyst_queries.yaml`). `holdout_start`:
    an ISO day; default read from config/campaign_data_policy.yaml on the first
    data load (unreadable: every data call is refused, never guessed).
    `comparison_budget`: comparisons a session may spend."""

    def __init__(self, run_dir, *, log_path=None, holdout_start: str | None = None,
                 comparison_budget: int = COMPARISON_BUDGET):
        self.run_dir = Path(run_dir).resolve()
        if not self.run_dir.is_dir():
            raise ValueError(f"run directory {str(run_dir)!r} does not exist")
        bad = [p for p in self.run_dir.parts if p in FORBIDDEN_PARTS]
        if bad:
            raise ValueError(f"refusing a run directory under {bad[0]!r}: {self.run_dir}")
        self.log = QueryLog(log_path if log_path is not None else self.run_dir / LOG_REL)
        self._holdout_start = holdout_start
        self.budget = int(comparison_budget)
        self._dictionary = None
        self._bars: dict = {}
        self._trades: dict = {}
        self._cols: dict = {}

    # -- the public functions ------------------------------------------------

    def list_columns(self, variant: str = "base"):
        return self._run("list_columns", {"variant": variant},
                         lambda: self._list_columns(variant))

    def describe(self, column, by=None, variant: str = "base"):
        return self._run("describe", {"column": column, "by": by, "variant": variant},
                         lambda: self._describe(column, by, variant))

    def distribution(self, column, by=None, bins: int = 10, variant: str = "base"):
        return self._run("distribution",
                         {"column": column, "by": by, "bins": bins, "variant": variant},
                         lambda: self._distribution(column, by, bins, variant))

    def conditional_effect(self, condition, horizons=None, outcome=None, baseline=None,
                           statistic: str = "mean_diff", direction: str = "greater", by=None,
                           variant: str = "base", floor=None):
        params = {"condition": condition, "horizons": horizons, "outcome": outcome,
                  "baseline": baseline, "statistic": statistic, "direction": direction,
                  "by": by, "variant": variant}
        if floor is not None:
            # logged only when given: a call without it logs exactly as before
            params["floor"] = floor
        return self._run("conditional_effect", params,
                         lambda: self._conditional_effect(condition, horizons, outcome, baseline,
                                                          statistic, direction, by, variant,
                                                          floor))

    def trade_slice(self, filter, agg, by=None, variant: str = "base"):  # noqa: A002
        return self._run("trade_slice",
                         {"filter": filter, "agg": agg, "by": by, "variant": variant},
                         lambda: self._trade_slice(filter, agg, by, variant))

    def event_study(self, trade_filter, bars_before, bars_after, variant: str = "base"):
        return self._run("event_study",
                         {"trade_filter": trade_filter, "bars_before": bars_before,
                          "bars_after": bars_after, "variant": variant},
                         lambda: self._event_study(trade_filter, bars_before, bars_after, variant))

    # -- the call wrapper: log BEFORE returning -------------------------------

    def _run(self, name: str, params: dict, compute):
        try:
            logged_params = _py(json.loads(_canon_json(_py(params))))
        except (TypeError, ValueError):
            logged_params = {"unserialisable": repr(params)[:500]}
        entry = {"function": name, "params": logged_params}
        result = None
        try:
            if "unserialisable" in logged_params:
                raise QueryRefused("parameters must be plain JSON values")
            if _nonfinite(params):
                raise QueryRefused("parameters must be finite numbers (no NaN or infinity)")
            result, n = compute()
            result = _py(result)
            size = len(_canon_json(result))
            if size > MAX_RESULT_CHARS:
                raise QueryRefused(
                    f"the result is {size} characters, over the {MAX_RESULT_CHARS} cap: ask for "
                    f"fewer groups, horizons, bins or aggregates")
            entry.update(status="ok", n_comparisons=int(n), result=result,
                         digest=self._digest(name, result),
                         result_sha256=hashlib.sha256(_canon_json(result).encode()).hexdigest())
        except QueryRefused as exc:
            result = None
            entry.update(status="refused", reason=str(exc), n_comparisons=0)
        except Exception as exc:  # noqa: BLE001 -- logged, then re-raised
            entry.update(status="error", reason=f"{type(exc).__name__}: {exc}"[:500],
                         n_comparisons=0)
            self.log.append(entry)
            raise
        logged = self.log.append(entry)          # the entry is on disk from here on
        return self._package(logged, result)

    def _package(self, logged: dict, result):
        out = {"query_id": logged["id"], "status": logged["status"],
               "n_comparisons": logged["n_comparisons"],
               "cumulative_comparisons": logged["cumulative_comparisons"]}
        if logged["status"] == "ok":
            out["result"] = result
        else:
            out["reason"] = logged.get("reason")
        return out

    def _charge(self, n: int) -> None:
        """Refuse a call that would spend more comparisons than are left."""
        if n <= 0:
            return
        spent = self.log.cumulative_comparisons()
        if spent + n > self.budget:
            raise QueryRefused(
                f"comparison budget spent ({spent} of {self.budget} used, this call needs {n}): "
                f"write your proposal")

    @staticmethod
    def _digest(name: str, result: dict) -> str:
        if name == "conditional_effect":
            parts = [f"h={h}: effect {c['effect']} n={c['n_events']}"
                     for h, c in list(result["horizons"].items())[:3]]
            return f"{result['unit']}; " + "; ".join(parts)
        if name == "describe":
            return "; ".join(f"{g}: n={v['n']} mean={v['mean']}"
                             for g, v in list(result["groups"].items())[:3])
        if name == "distribution":
            return (f"{result['column']}: {len(result['groups'])} group(s), "
                    f"{len(result['bin_edges']) - 1} bins")
        if name == "trade_slice":
            return "; ".join(f"{g}: n_trades={v['n_trades']}"
                             for g, v in list(result["groups"].items())[:3])
        if name == "event_study":
            return f"{result['n_trades']} trades; after: " + ", ".join(
                f"{k}={v['mean']}" for k, v in list(result["after"].items())[:3])
        return f"{len(result.get('bar_columns', []))} usable bar columns"

    # -- loading --------------------------------------------------------------

    def _holdout(self) -> str:
        if self._holdout_start is None:
            try:
                import holdout_policy as hp
                self._holdout_start = hp.load_holdout_range()[0]
            except Exception as exc:  # noqa: BLE001 -- fail closed
                raise QueryRefused(f"the holdout start cannot be read ({type(exc).__name__}); "
                                   f"no data is read without it") from exc
        return self._holdout_start

    def _variant(self, variant) -> str:
        if not isinstance(variant, str) or not _SAFE_NAME.fullmatch(variant):
            raise QueryRefused(f"variant {variant!r} is not a variant id")
        try:
            graded, _ = ct.graded_variants(self.run_dir)
        except OSError as exc:
            raise QueryRefused(f"{self.run_dir.name}: no artifacts/variants to read "
                               f"({type(exc).__name__})") from exc
        if variant not in graded:
            raise QueryRefused(f"variant {variant!r} is not a graded variant of this run "
                               f"(graded: {graded})")
        return variant

    def _check_files(self, vid: str, with_trades: bool) -> None:
        """Every window file the loaders will open sits inside the run directory."""
        pr = self.run_dir / "artifacts" / "variants" / vid / "protocol_result.yaml"
        if not _inside(pr, self.run_dir):
            raise QueryRefused(f"{pr} resolves outside the run directory")
        doc = yaml.safe_load(pr.read_text(encoding="utf-8")) or {}
        for entry in doc.get("results") or []:
            rid = entry.get("run_id")
            if not rid:
                continue
            if not isinstance(rid, str) or not _SAFE_NAME.fullmatch(rid):
                raise QueryRefused(f"window run id {rid!r} is not a plain name: refused")
            names = ["bars.csv"] + (["trades.json"] if with_trades else [])
            for nm in names:
                p = self.run_dir / "variants" / vid / "results" / rid / nm
                if not _inside(p, self.run_dir):
                    raise QueryRefused(f"{nm} of window {rid} resolves outside the run directory")
        diag = self.run_dir / "variants" / vid / "trade_diagnostics.json"
        if with_trades and diag.exists() and not _inside(diag, self.run_dir):
            raise QueryRefused("trade_diagnostics.json resolves outside the run directory")

    def _bar_windows(self, variant) -> list:
        vid = self._variant(variant)
        if vid not in self._bars:
            self._check_files(vid, with_trades=False)
            try:
                windows = ct.load_variant_bars(self.run_dir, vid)    # no cache: no warm-up rows
                for w in windows:
                    ct._cadence(w.step)
            except (OSError, ValueError, KeyError) as exc:
                raise QueryRefused(f"the run's bars cannot be read ({type(exc).__name__}: "
                                   f"{exc})") from exc
            try:
                cmeas.check_before_holdout(windows, self._holdout())
            except cmeas.HoldoutOverlap as exc:
                raise QueryRefused(str(exc)) from exc
            for w in windows:
                if not _inside(Path(w.source), self.run_dir):
                    raise QueryRefused(f"{w.label}: bars file outside the run directory")
            self._bars[vid] = windows
        return self._bars[vid]

    def _trade_windows(self, variant) -> list:
        vid = self._variant(variant)
        if vid not in self._trades:
            self._check_files(vid, with_trades=True)
            try:
                tws = ct.load_variant_trade_windows(self.run_dir, vid)
                for tw in tws:
                    ct._cadence(tw.step)
            except (OSError, ValueError, KeyError) as exc:
                raise QueryRefused(f"the run's trades cannot be read ({type(exc).__name__}: "
                                   f"{exc})") from exc
            try:
                cmeas.check_before_holdout(tws, self._holdout())
            except cmeas.HoldoutOverlap as exc:
                raise QueryRefused(str(exc)) from exc
            self._trades[vid] = tws
        return self._trades[vid]

    def _dict(self) -> list:
        if self._dictionary is None:
            self._dictionary = load_bars_dictionary()
        return self._dictionary

    @staticmethod
    def _cadence(windows) -> str:
        return ct._cadence(windows[0].step)

    # -- columns --------------------------------------------------------------

    def _csv_header(self, w) -> list:
        with open(w.source, encoding="utf-8", newline="") as f:
            return f.readline().rstrip("\r\n").split(",")

    def _csv_column(self, w, column: str) -> np.ndarray:
        import csv
        with open(w.source, encoding="utf-8", newline="") as f:
            rd = csv.DictReader(f)
            return np.array([_to_float(r.get(column)) for r in rd])

    def _column_values(self, variant, column):
        """(list of per-window float arrays, role label) for an allowed column;
        refuses anything outside the vocabulary."""
        windows = self._bar_windows(variant)
        if not isinstance(column, str) or not column:
            raise QueryRefused("column must be a column name (see list_columns)")
        key = (variant, column)
        if key in self._cols:
            return self._cols[key]
        m = _DERIVED_RE.fullmatch(column)
        if m:
            n = int(m.group(2))
            lo = ct.MIN_FIELD_BARS[m.group(1)]
            if not lo <= n <= MAX_FIELD_BARS:
                raise QueryRefused(f"{column}: the length must be {lo}..{MAX_FIELD_BARS} bars")
            fn = ct._FIELD_FUNCS[m.group(1)]
            vals = [fn(w, n) for w in windows]
        else:
            header = self._csv_header(windows[0])
            if column not in header:
                raise QueryRefused(f"column {column!r} is not a column of this run's bars.csv "
                                   f"(see list_columns)")
            row = dictionary_row(self._dict(), column)
            if row is None:
                raise QueryRefused(f"column {column!r} is not in the data dictionary: not offered")
            if row["role"] == "never":
                raise QueryRefused(f"column {column!r} is never offered ({row['when']}: a value "
                                   f"known only at the end of the run or over a whole window)")
            if row["role"] == "outcome":
                raise QueryRefused(f"column {column!r} is outcome-only ({row['when']}): known "
                                   f"only after the bar, never a feature")
            if row["role"] == "label":
                raise QueryRefused(f"column {column!r} is a label ({row['when']}): use it as `by`")
            vals = [self._csv_column(w, column) for w in windows]
            if not any(np.isfinite(v).any() for v in vals):
                raise QueryRefused(f"column {column!r} has no numeric value in this run")
        self._cols[key] = vals
        return vals

    # -- grouping -------------------------------------------------------------

    @staticmethod
    def _bucket(hour: np.ndarray) -> np.ndarray:
        lo = (hour // 4) * 4
        return np.array([f"{int(a):02d}-{int(a) + 3:02d}" for a in lo], dtype=object)

    def _labels_bars(self, windows, by) -> list:
        out = []
        for w in windows:
            n = len(w.ts)
            if by == "window":
                lab = np.full(n, w.label, dtype=object)
            elif by == "coin":
                lab = np.full(n, w.symbol, dtype=object)
            elif by == "regime":
                lab = np.array([r if r else "(none)" for r in w.regime], dtype=object)
            elif by == "weekday":
                lab = np.array([_WEEKDAYS[int(d)] for d in (w.ts // DAY + 3) % 7], dtype=object)
            else:
                lab = self._bucket((w.ts % DAY) // 3600)
            out.append(lab)
        return out

    @staticmethod
    def _order(by, present) -> list:
        present = list(dict.fromkeys(present))
        if by == "weekday":
            return [d for d in _WEEKDAYS if d in present]
        if by == "window":
            return present                      # chronological as loaded
        return sorted(present)

    def _check_by(self, by, allowed, windows=None):
        if by is None:
            return
        if by not in allowed:
            raise QueryRefused(f"by={by!r} is not one of {[None, *allowed]}")
        if by == "hour" and windows is not None and ct._cadence(windows[0].step) != "hourly":
            raise QueryRefused("by=hour needs an hourly run")

    def _grouped(self, windows, by, arrays):
        """{label: concatenated finite+nan values}, ordered, <= MAX_GROUPS."""
        flat = np.concatenate(arrays) if arrays else np.zeros(0)
        if by is None:
            return {"all": flat}
        labels = np.concatenate(self._labels_bars(windows, by))
        groups = self._order(by, list(labels))
        if len(groups) > MAX_GROUPS:
            raise QueryRefused(f"by={by} makes {len(groups)} groups, over the cap of "
                               f"{MAX_GROUPS}")
        return {g: flat[labels == g] for g in groups}

    # -- list_columns -----------------------------------------------------------

    def _list_columns(self, variant):
        windows = self._bar_windows(variant)
        header = self._csv_header(windows[0])
        first = {}
        usable, not_offered = [], {"outcome_only": [], "label": [], "never": [],
                                   "not_in_dictionary": [], "not_numeric": []}
        import csv
        with open(windows[0].source, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        for col in header:
            row = dictionary_row(self._dict(), col)
            if row is None:
                not_offered["not_in_dictionary"].append(col)
                continue
            if row["role"] != "feature":
                key = {"outcome": "outcome_only"}.get(row["role"], row["role"])
                not_offered[key].append(col)
                continue
            vals = np.array([_to_float(r.get(col)) for r in rows])
            if not np.isfinite(vals).any():
                not_offered["not_numeric"].append(col)
                continue
            first[col] = row
            usable.append(col)

        def build(meaning_len: int) -> dict:
            cols = [f"{c} | {first[c]['unit']} | {first[c]['when']}"
                    + (f" | {first[c]['meaning'][:meaning_len]}" if meaning_len else "")
                    for c in usable]
            return {
                "variant": variant, "cadence": self._cadence(windows),
                "windows": [w.label for w in windows],
                "bar_columns": cols,
                "derived_columns": [f"{d}_<n> (n bars, {ct.MIN_FIELD_BARS[d]}..{MAX_FIELD_BARS})"
                                    for d in DERIVED_COLUMNS],
                "not_offered": {k: v for k, v in not_offered.items() if v},
                "by_bars": list(BY_BARS), "by_effect": list(BY_EFFECT),
                "by_trades": list(BY_TRADES),
                "trade_fields": {"entry_time": list(ct.TRADE_ENTRY_FIELDS),
                                 "exit_time": list(ct.TRADE_EXIT_FIELDS)},
                "trade_aggs": {"fields": list(AGG_FIELDS), "stats": list(AGG_STATS)},
                "condition_kinds": sorted(ct.SELECTORS) + [ct.TRADE_SELECTOR],
                "outcomes": sorted(ct.OUTCOMES) + list(ct.TRADE_OUTCOMES),
                "statistics": sorted(ct.STATISTICS),
                "caps": {"groups": MAX_GROUPS, "horizons": MAX_HORIZONS,
                         "result_chars": MAX_RESULT_CHARS, "comparisons": self.budget},
            }

        for ml in (60, 40, 24, 0):
            out = build(ml)
            if len(_canon_json(_py(out))) <= MAX_RESULT_CHARS:
                return out, 0
        return build(0), 0           # _run refuses it with the size reason

    # -- describe / distribution ---------------------------------------------

    def _describe(self, column, by, variant):
        windows = self._bar_windows(variant)
        self._check_by(by, BY_BARS, windows)
        vals = self._column_values(variant, column)
        groups = self._grouped(windows, by, vals)
        n = self._calendar_charge(column, by, groups)
        out = {}
        for g, v in groups.items():
            fin = v[np.isfinite(v)]
            cell = {"n": int(len(v)), "nan_share": r8(1 - len(fin) / len(v)) if len(v) else None}
            if len(fin):
                p10, p50, p90 = np.percentile(fin, [10, 50, 90])
                cell.update(mean=r8(fin.mean()), std=r8(fin.std(ddof=1)) if len(fin) > 1 else None,
                            p10=r8(p10), p50=r8(p50), p90=r8(p90))
            else:
                cell.update(mean=None, std=None, p10=None, p50=None, p90=None)
            out[g] = cell
        return {"column": column, "by": by, "groups": out}, n

    def _distribution(self, column, by, bins, variant):
        windows = self._bar_windows(variant)
        self._check_by(by, BY_BARS, windows)
        if (not isinstance(bins, int) or isinstance(bins, bool)
                or not BINS_RANGE[0] <= bins <= BINS_RANGE[1]):
            raise QueryRefused(f"bins must be an int in {BINS_RANGE[0]}..{BINS_RANGE[1]}")
        vals = self._column_values(variant, column)
        groups = self._grouped(windows, by, vals)
        n = self._calendar_charge(column, by, groups)
        pooled = np.concatenate([v[np.isfinite(v)] for v in groups.values()])
        if not len(pooled):
            raise QueryRefused(f"column {column!r} has no finite value")
        edges = np.histogram_bin_edges(pooled, bins=bins)
        counts = {g: np.histogram(v[np.isfinite(v)], bins=edges)[0].tolist()
                  for g, v in groups.items()}
        return {"column": column, "by": by, "bin_edges": [r8(e) for e in edges],
                "groups": counts}, n

    def _calendar_charge(self, column, by, groups) -> int:
        """Comparisons of a describe / distribution call: one per group with a finite value
        when grouped by hour, weekday or regime (a calendar or regime effect, whatever the
        column), else 0.
        Charged here, before any number is computed."""
        # a group with no finite value shows no number: not charged (review round 2)
        n = (sum(1 for v in groups.values() if np.isfinite(v).any())
             if by in _CALENDAR_BY else 0)
        self._charge(n)
        return n

    # -- conditional_effect ---------------------------------------------------

    @staticmethod
    def _spec_errors(spec) -> list:
        """check_spec with the gated trailing_vol field and the trade family on, and
        without the verdict-only refusal of regime selectors (an effect size needs no
        signal recompute: claim_measure / claim_card make the same exception)."""
        errs = ct.check_spec(spec, extra_fields=ct.GATED_BAR_T_FIELDS, trade_tests=True)
        return [e for e in errs if " cannot be graded under " not in e]

    def _conditional_effect(self, condition, horizons, outcome, baseline, statistic,
                            direction, by, variant, floor=None):
        if floor is None:
            floor = {"min_events": 1}
        elif not isinstance(floor, dict) or not floor:
            raise QueryRefused(f"floor must be a mapping of {list(ct.FLOOR_UNITS)} to whole "
                               f"numbers >= 1, e.g. {{min_events: 100, min_windows: 4}}")
        else:
            # spec_hash reads numbers as floats: an integer past float range would raise there
            for v in floor.values():
                if isinstance(v, int) and abs(v) > sys.float_info.max:
                    raise QueryRefused("floor: a value is too large")
        if not isinstance(condition, dict):
            raise QueryRefused("condition must be one selector mapping, e.g. "
                               "{kind: event, field: past_return, bars: 24, op: '<=', "
                               "value: -0.03}")
        is_trade = condition.get("kind") == ct.TRADE_SELECTOR
        self._check_by(by, BY_EFFECT)
        if is_trade:
            outcome = outcome or "trade_net_return"
            baseline = baseline if baseline is not None else {"kind": "other_trades"}
        else:
            outcome = outcome or "fwd_return"
            if baseline is None and statistic != "rank_ic":
                baseline = {"kind": "complement"}
        if horizons is not None:
            if not isinstance(horizons, list):
                raise QueryRefused("horizons must be a list of ints")
            if len(horizons) > MAX_HORIZONS:
                raise QueryRefused(f"{len(horizons)} horizons, over the cap of {MAX_HORIZONS}")
        if outcome == "trade_net_return":
            out_spec = {"kind": outcome}
            if horizons:
                raise QueryRefused("trade_net_return takes no horizons (the lot's own result)")
        else:
            out_spec = {"kind": outcome, "horizons": sorted(horizons) if isinstance(horizons, list)
                        and all(isinstance(h, int) and not isinstance(h, bool) for h in horizons)
                        else horizons}
        test = {"selector": condition, "outcome": out_spec, "baseline": baseline,
                "statistic": statistic, "direction": direction, "floor": floor}
        try:
            spec = ct.TestSpec.from_dict(test)
        except (TypeError, ValueError) as exc:
            raise QueryRefused(f"the slots are malformed: {exc}") from exc
        try:
            errors = self._spec_errors(spec)
        except (TypeError, ValueError, AttributeError, KeyError) as exc:
            raise QueryRefused(f"malformed test ({type(exc).__name__}: {exc})") from exc
        if errors:
            raise QueryRefused("; ".join(errors[:3]))
        windows = self._trade_windows(variant) if is_trade else self._bar_windows(variant)
        try:
            per, out_h, hz, _ = ct.effect_sizes(windows, spec)
        except (ct.MixedReturnBasis, ValueError) as exc:
            raise QueryRefused(f"the engine refused this test: {exc}") from exc
        unit = "trades" if is_trade else "bars"
        if by == "window":
            labels = [p["w"].label for p in per]
        elif by == "coin":
            labels = sorted({p["w"].symbol for p in per})
        else:
            labels = []
        if len(labels) > MAX_GROUPS:
            raise QueryRefused(f"by={by} makes {len(labels)} groups, over the cap of {MAX_GROUPS}")
        n = len(hz) * (len(labels) if by else 1)
        self._charge(n)

        def key(h):
            return "trade" if (is_trade and out_spec["kind"] == "trade_net_return") else str(h)

        horizons_out, groups_out = {}, {}
        for h in hz:
            r = out_h[h]
            k, nw = cmeas._claimed(r["per_window"].values())
            horizons_out[key(h)] = {
                "effect": r8(r["value"]), "oriented": r8(r["oriented"]),
                "n_events": r["n_events"], "n_windows_with_events": r["n_windows_with_events"],
                "n_blocks": r["n_blocks"], "windows_claimed_sign": k, "windows_with_value": nw}
            if by == "window":
                for p in per:
                    ev = p["mask"] & np.isfinite(p["ys"][h])
                    if statistic == "rank_ic":
                        ev = ev & np.isfinite(p["fc"])
                    c = r["per_window"][p["w"].label]
                    groups_out.setdefault(p["w"].label, {})[key(h)] = {
                        "effect": r8(c["value"]), "oriented": r8(c["oriented"]),
                        "n_events": int(ev.sum())}
            elif by == "coin":
                for sym, c in cmeas._per_coin(per, spec, h).items():
                    groups_out.setdefault(sym, {})[key(h)] = {
                        "effect": r8(c["value"]), "oriented": r8(c["oriented"]),
                        "n_events": c["n_events"]}
        name = "cond_" + ct.spec_hash(spec)[:10]
        block = {"name": name, **test}
        compiles, why = True, []
        try:
            import claim_card as cc
            errs, _h, _possible = cc._check_test(block, "test", True)
            compiles, why = not errs, [e[:160] for e in errs[:2]]
        except Exception as exc:  # noqa: BLE001 -- advisory only
            compiles, why = False, [f"{type(exc).__name__}: {exc}"[:160]]
        result = {"unit": unit, "outcome": out_spec["kind"], "statistic": statistic,
                  "direction": direction, "by": by, "horizons": horizons_out,
                  "test": block, "spec_hash": ct.spec_hash(spec),
                  "compiles_as_claim": compiles}
        if why:
            result["claim_check"] = why
        if by:
            result["groups"] = groups_out
        return result, n

    # -- trade-level helpers --------------------------------------------------

    @staticmethod
    def _check_filter(clauses, what: str) -> None:
        if not isinstance(clauses, list) or len(clauses) > MAX_TRADE_CLAUSES:
            raise QueryRefused(f"{what} must be a list of 0 to {MAX_TRADE_CLAUSES} clauses "
                               f"{{field, op, value}}")
        if clauses:
            errs = ct._check_trade_where({"kind": ct.TRADE_SELECTOR, "where": clauses})
            if errs:
                raise QueryRefused("; ".join(errs[:3]))

    @staticmethod
    def _selected(tw, clauses) -> np.ndarray:
        if not clauses:
            return np.ones(tw.n, dtype=bool)
        mask, valid = ct.sel_trade(tw, {"kind": ct.TRADE_SELECTOR, "where": clauses})
        return mask & valid

    def _trade_labels(self, tw, by) -> np.ndarray:
        if by == "window":
            return np.full(tw.n, tw.label, dtype=object)
        if by == "direction":
            return np.array(tw.side, dtype=object)
        if by == "regime_at_entry":
            return np.array([r if r else "(none)" for r in tw.regime_at_entry], dtype=object)
        if by == "weekday":
            return np.array([_WEEKDAYS[int(d)] for d in (tw.entry_ts // DAY + 3) % 7],
                            dtype=object)
        return self._bucket((tw.entry_ts % DAY) // 3600)

    # -- trade_slice ----------------------------------------------------------

    @staticmethod
    def _check_aggs(agg) -> list:
        if not isinstance(agg, list) or not 1 <= len(agg) <= MAX_AGGS:
            raise QueryRefused(f"agg must be a list of 1 to {MAX_AGGS} items {{field, stat[, h]}}")
        out = []
        for i, a in enumerate(agg):
            if not isinstance(a, dict) or not set(a) <= {"field", "stat", "h"} \
                    or not {"field", "stat"} <= set(a):
                raise QueryRefused(f"agg[{i}] is exactly {{field, stat}} (+ h for "
                                   f"post_exit_return)")
            f, s, h = a["field"], a["stat"], a.get("h")
            if f not in AGG_FIELDS:
                raise QueryRefused(f"agg[{i}].field {f!r} is not one of {list(AGG_FIELDS)}")
            if s not in AGG_STATS:
                raise QueryRefused(f"agg[{i}].stat {s!r} is not one of {list(AGG_STATS)}")
            if f == "post_exit_return":
                if not isinstance(h, int) or isinstance(h, bool) or not 1 <= h <= 500:
                    raise QueryRefused(f"agg[{i}]: post_exit_return needs h, an int 1..500 bars")
            elif h is not None:
                raise QueryRefused(f"agg[{i}]: h is only for post_exit_return")
            out.append((f, s, h))
        return out

    @staticmethod
    def _trade_values(tw, field_, h) -> np.ndarray:
        if field_ == "trade_net_return":
            return ct.trade_outcome(tw, "trade_net_return", 0)
        if field_ == "post_exit_return":
            return ct.trade_outcome(tw, "post_exit_return", int(h))
        if field_ == "holding_bars":
            return ((tw.exit_ts - tw.entry_ts) // tw.step).astype(float)
        return np.asarray(tw.entry_forecast, dtype=float)

    @staticmethod
    def _stat(v: np.ndarray, stat: str):
        fin = v[np.isfinite(v)]
        if stat == "count":
            return int(len(fin))
        if not len(fin):
            return None
        if stat == "mean":
            return r8(fin.mean())
        if stat == "median":
            return r8(np.median(fin))
        return r8((fin > 0).mean())

    def _trade_slice(self, flt, agg, by, variant):
        tws = self._trade_windows(variant)
        self._check_filter(flt, "filter")
        aggs = self._check_aggs(agg)
        self._check_by(by, BY_TRADES, tws)
        sel = [self._selected(tw, flt) for tw in tws]
        arrays = {(f, h): np.concatenate([self._trade_values(tw, f, h)[m]
                                          for tw, m in zip(tws, sel)])
                  for f, _s, h in aggs}
        if by is None:
            labels = np.full(int(sum(m.sum() for m in sel)), "all", dtype=object)
            groups = ["all"]
        else:
            labels = np.concatenate([self._trade_labels(tw, by)[m] for tw, m in zip(tws, sel)])
            groups = self._order(by, list(labels)) if len(labels) else []
            if len(groups) > MAX_GROUPS:
                raise QueryRefused(f"by={by} makes {len(groups)} groups, over the cap of "
                                   f"{MAX_GROUPS}")
        outcome_aggs = sum(1 for f, s, _h in aggs if f in _OUTCOME_AGG_FIELDS and s != "count")
        n = len(groups) * outcome_aggs
        self._charge(n)
        out = {}
        for g in groups:
            m = labels == g
            cell = {"n_trades": int(m.sum())}
            for f, s, h in aggs:
                nm = f"{f}_h{h}" if f == "post_exit_return" else f
                cell[f"{nm}_{s}"] = self._stat(arrays[(f, h)][m], s)
            out[g] = cell
        bases = sorted({tw.basis for tw in tws if tw.n})
        return {"by": by, "groups": out, "return_basis": bases}, n

    # -- event_study ----------------------------------------------------------

    def _event_study(self, trade_filter, bars_before, bars_after, variant):
        tws = self._trade_windows(variant)
        self._check_filter(trade_filter, "trade_filter")
        cad = self._cadence([tw.bars for tw in tws])
        pts = CHECKPOINTS[cad]
        top = pts[-1]
        for nm, v in (("bars_before", bars_before), ("bars_after", bars_after)):
            if not isinstance(v, int) or isinstance(v, bool) or not 1 <= v <= top:
                raise QueryRefused(f"{nm} must be an int in 1..{top} for a {cad} run")
        before_pts = [p for p in pts if p <= bars_before]
        after_pts = [p for p in pts if p <= bars_after]
        n = len(after_pts)
        self._charge(n)
        acc_b = {p: [] for p in before_pts}
        acc_a = {p: [] for p in after_pts}
        n_trades = 0
        for tw in tws:
            sel = self._selected(tw, trade_filter)
            b = tw.bars
            idx = {p: b.index_at(p) for p in after_pts}
            idxb = {p: b.index_at(-p) for p in before_pts}
            for i in np.nonzero(sel)[0]:
                e = int(tw.entry_idx[i])
                if e < 0:
                    continue
                n_trades += 1
                sign = 1.0 if tw.side[i] == "long" else -1.0
                for p in before_pts:
                    j = int(idxb[p][e])
                    if j >= 0:                       # the move INTO the entry bar's close
                        acc_b[p].append(sign * (b.close[e] / b.close[j] - 1.0))
                for p in after_pts:
                    j = int(idx[p][e])
                    if j >= 0:                       # an outcome: what the market did next
                        acc_a[p].append(sign * (b.close[j] / b.close[e] - 1.0))
        # a missing close gives no value: counted in neither n nor the mean (D-090)
        acc_b = {p: [x for x in v if math.isfinite(x)] for p, v in acc_b.items()}
        acc_a = {p: [x for x in v if math.isfinite(x)] for p, v in acc_a.items()}

        def cell(v):
            return {"n": len(v), "mean": r8(np.mean(v)) if v else None}
        return {"n_trades": n_trades, "cadence": cad,
                "note": ("returns are signed by the trade's side (positive = the trade's way) "
                         "from the entry bar's close; `before` is known at entry, `after` is an "
                         "OUTCOME"),
                "before": {str(p): cell(acc_b[p]) for p in before_pts},
                "after": {str(p): cell(acc_a[p]) for p in after_pts}}, n
