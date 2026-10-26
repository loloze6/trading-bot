"""
D-198: the kept feed-registry readers, restored after test_e035_s2c_feed_requests.py went.

decide_next's feed gate is live (`dn.load_feed_set`, `dn.known_feeds`, `dn.load_feed_registry`,
`dn.component_consumed_feeds`, run_campaign's lazy feed set). From origin/master's section 4
(reading the registries and the components' consumes_feeds) and the lazy-feed-set test.

Dropped as tests of deleted code: the readers' `requires_feed` router (the stage's data_requests
rows), the readers' handoff and SKILL feed names, and the stage-level checks. No LLM, no backtest.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))
sys.path.insert(0, str(Path(__file__).parent))

import run_campaign as camp  # noqa: E402
import decide_next as dn  # noqa: E402

from test_e059_s2a_decide_next import CLS  # noqa: E402

_TBOT = _SR.parent / "trading-bot"


def _fake_registry(tmp_path, body: str) -> Path:
    mod = tmp_path / "data" / "feed_registry.py"
    mod.parent.mkdir(parents=True, exist_ok=True)
    mod.write_text(body, encoding="utf-8")
    return tmp_path


def _import_engine(module: str):
    pytest.importorskip("pandas")
    sys.path.insert(0, str(_TBOT))
    try:
        return __import__(module, fromlist=["_"])
    except ImportError as exc:  # the engine's fetchers need the trading-bot venv
        pytest.skip(f"trading-bot {module} not importable here: {exc}")


def test_known_feeds_reads_the_real_feed_registry_keys():
    feeds = dn.known_feeds(_TBOT)
    assert feeds == sorted(feeds) and {"funding_rate", "fear_greed"} <= set(feeds)
    assert not any(f.startswith("whale_") for f in feeds)


def test_load_feed_registry_matches_the_imported_registries():
    mod = _import_engine("data.feed_registry")
    assert dn.load_feed_registry(_TBOT) == {"wired": sorted(mod.FEED_REGISTRY),
                                            "reserved": sorted(mod.RESERVED_FEED_REGISTRY)}


def test_feed_status_is_the_gate_classification():
    """Review fix 3: the same order and sources as
    data_availability_gate.check_aux_feed_window (reserved first, then
    FEED_REGISTRY, else never built). Only the two branches that return
    before any data is read are called."""
    gate = _import_engine("data_availability_gate")
    reg = dn.load_feed_registry(_TBOT)
    for feed in reg["reserved"] + ["open_interest"]:
        res = gate.check_aux_feed_window(feed, "binance", ["BTCUSDT"], "2024-01-01", "2024-02-01")
        want = ("reserved" if "is a RESERVED feed" in res["reason"]
                else "unknown" if "is not a known feed" in res["reason"] else res["reason"])
        assert res["outcome"] == "decline" and dn.feed_status(feed, reg) == want, feed
    assert set(reg["reserved"]) == set(gate._RESERVED_FEED_NAMES)
    assert set(reg["wired"]) == set(gate.FEED_REGISTRY)
    assert all(dn.feed_status(f, reg) == "wired" for f in reg["wired"])
    assert dn.feed_status("open_interest", None) is None


def test_known_feeds_from_a_synthetic_registry(tmp_path):
    root = _fake_registry(tmp_path, "FEED_REGISTRY = {'b': 1, 'a': 2}\nOTHER = {'z': 0}\n")
    assert dn.known_feeds(root) == ["a", "b"]


def test_reserved_registry_as_a_comprehension_over_a_named_tuple(tmp_path):
    root = _fake_registry(tmp_path, "FEED_REGISTRY = {'a': 1}\nX = 'x_col'\nNAMES = ('y', X)\n"
                                    "RESERVED_FEED_REGISTRY = {n: 1 for n in NAMES}\n")
    assert dn.load_feed_registry(root) == {"wired": ["a"], "reserved": ["x_col", "y"]}


@pytest.mark.parametrize("body", ["X = 1\n", "FEED_REGISTRY = dict(a=1)\n", "FEED_REGISTRY = {}\n",
                                  "FEED_REGISTRY = {k: 1 for k in 'ab'}\n", "FEED_REGISTRY = {\n"])
def test_known_feeds_fails_loud_without_a_literal_registry(tmp_path, body):
    with pytest.raises(dn.DecideNextError, match="FEED_REGISTRY|cannot be read"):
        dn.known_feeds(_fake_registry(tmp_path, body))


def test_load_feed_registry_fails_loud_without_the_reserved_registry(tmp_path):
    with pytest.raises(dn.DecideNextError, match="RESERVED_FEED_REGISTRY"):
        dn.load_feed_registry(_fake_registry(tmp_path, "FEED_REGISTRY = {'a': 1}\n"))


def test_component_consumed_feeds_matches_the_imported_classes():
    mod = _import_engine("strategies.strategy_components")
    got = dn.component_consumed_feeds(_TBOT)
    want = {f"{dn.COMPONENT_MODULE}.{name}": sorted(set(cls.consumes_feeds))
            for name, cls in vars(mod).items()
            if isinstance(cls, type) and cls.__module__ == mod.__name__
            and getattr(cls, "consumes_feeds", ())}
    assert got == want and got[CLS] == ["funding_rate"]


def test_component_consumed_feeds_inherits_and_fails_loud(tmp_path):
    mod = tmp_path / "strategies" / "strategy_components.py"
    mod.parent.mkdir(parents=True)
    mod.write_text("from strategies.strategy_base import Base\nCOL = 'oi'\n"
                   "class A(Base):\n    consumes_feeds = (COL, 'x')\n"
                   "class B(A):\n    pass\nclass C(Base):\n    pass\n", encoding="utf-8")
    assert dn.component_consumed_feeds(tmp_path) == {
        f"{dn.COMPONENT_MODULE}.A": ["oi", "x"], f"{dn.COMPONENT_MODULE}.B": ["oi", "x"]}
    mod.write_text("class A:\n    consumes_feeds = tuple(['x'])\n", encoding="utf-8")
    with pytest.raises(dn.DecideNextError, match="consumes_feeds"):
        dn.component_consumed_feeds(tmp_path)



def test_run_campaign_passes_a_lazy_feed_set(monkeypatch):
    """_finish_lineage_with_decision hands load_inputs a callable over the
    public load_feed_set (no private helper, nothing read up front)."""
    seen = {}

    class _Stop(Exception):
        pass

    def _capture(root, queue, **kw):
        seen.update(kw)
        raise _Stop
    monkeypatch.setattr(dn, "load_inputs", _capture)
    entry = {"id": "E", "status": "done", "outcome": "refuted", "run_ids": ["run_1"]}
    with pytest.raises(_Stop):
        camp._finish_lineage_with_decision({"queue": [entry]}, entry, "run_1")
    assert callable(seen["feed_set"])
    assert seen["feed_set"]() == dn.load_feed_set(camp._TRADING_BOT_ROOT)

