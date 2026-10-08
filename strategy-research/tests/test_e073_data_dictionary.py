"""
E-073 step 1 (P-CUL-81, D-081): the data dictionary, kept honest against the
code that writes each field, and given to the v3 readers behind the epic's one
flag, orchestrator.observable_backtest.enabled (off by default).

Sections:
  1. The dictionary parses: every row has a meaning, a unit, a code reference
     and a known "when known" value. Every reference is `KEY:symbol` (a
     function, method -- `Class.method`, a nested function -- `outer.inner` --
     or a module constant): the symbol must exist exactly once in that file,
     and a row's field key must appear inside one of the symbols it cites. No
     line numbers (they drifted silently).
  2. Field paths derived from the writers' code (no run artifact needed, CI
     has none): bars.csv's exact column patterns, and for every YAML/JSON file
     the FULL dotted paths its writers emit (`parent.child`, `<*>` for a
     dynamic key, `[]` for a list item), found by walking the writers' dict
     literals, subscript assignments, .update / .setdefault / .append calls,
     local variables and the same-repo functions they call. Both directions,
     on the prefix closure: every path the code writes is in the dictionary,
     every dictionary entry is still written. Writers the walk cannot reach
     (a callable passed as an argument, a parameter) are mounted explicitly
     (EXTRA_WRITERS); a `**spread` / .update() whose keys cannot be read is a
     listed exception with its reason (OPAQUE_ALLOWED).
  3. The flag: off by default, registered everywhere, a hard dependency on
     reader_findings, non-bool refused.
  4. The readers' subset (docs/DATA_DICTIONARY_READERS.md) is exactly
     tools/data_dictionary.reader_subset(full). Flag off: the v3 handoff and
     prompt are byte-identical. Flag on: the subset is an extra required input,
     with one line telling the reader to use it, and the prompt carries it.

No LLM, no backtest, no market data.
"""
import ast
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
REPO = SR_ROOT.parent
DICTIONARY = SR_ROOT / "docs" / "DATA_DICTIONARY.md"
READERS_DICTIONARY = SR_ROOT / "docs" / "DATA_DICTIONARY_READERS.md"
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import data_dictionary as dd  # noqa: E402
from build_reports import REPORT_CATEGORIES  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import RUN_ID, _set_orchestrator  # noqa: E402
from test_e068_5_readers_v3 import V3_ON, CLAIMS_ON, _run070_shaped  # noqa: E402

OB_ON = {**V3_ON, "observable_backtest": {"enabled": True}}
OB_OFF = {**V3_ON, "observable_backtest": {"enabled": False}}
WHEN = {"close", "fill", "exit", "after", "run", "end", "meta"}

TB = "trading-bot/core/trading_bot.py"
BT = "trading-bot/core/backtester.py"
PI = "trading-bot/execution/portfolio_info.py"
EH = "trading-bot/execution/execution_handler.py"
RM = "trading-bot/risk/risk_manager.py"
RG = "trading-bot/risk/portfolio_risk_gate.py"
SB = "trading-bot/strategies/strategy_base.py"
MS = "trading-bot/strategies/main_strategy.py"
SE = "trading-bot/strategies/strategy_engine.py"
DM = "trading-bot/data/data_manager.py"
FR = "trading-bot/data/feed_registry.py"
RA = "trading-bot/reporting/run_artifact.py"
SS = "trading-bot/performance/signal_statistics.py"
RP = "strategy-research/tools/run_protocol.py"
BR = "strategy-research/tools/build_reports.py"
VE = "strategy-research/tools/verdict_criteria_evaluator.py"
RF = "strategy-research/tools/reader_findings.py"
CF = "strategy-research/tools/claim_findings.py"
CM = "strategy-research/tools/claim_measure.py"
NB = "strategy-research/tools/nearest_build.py"
P1 = "strategy-research/workflow/run_phase1_research.py"

ITEM, DYN, SPREAD = "[]", "<*>", "**"  # a list item, a dynamic key, an unreadable spread


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# Parsing the dictionary
# ---------------------------------------------------------------------------

_SECTION_RE = re.compile(r"<!-- data-dictionary: (?P<name>\S+) -->\n(?P<body>.*?)"
                         r"<!-- /data-dictionary -->", re.S)
_SOURCES_RE = re.compile(r"<!-- data-dictionary-sources -->\n(?P<body>.*?)"
                         r"<!-- /data-dictionary-sources -->", re.S)
_ROW_RE = re.compile(r"^\| `(?P<field>[^`]+)` \|(?P<rest>.*)\|\s*$", re.M)
_REF_RE = re.compile(r"`(?P<key>[A-Z][A-Z0-9]):(?P<sym>[A-Za-z_][\w.]*)`")
_LINE_REF_RE = re.compile(r"`[A-Z][A-Z0-9]:\d")


def _text(path: Path = DICTIONARY) -> str:
    return path.read_text(encoding="utf-8")


def _sections(text: str) -> dict:
    """{section: [(field, [meaning, unit, code, when])]}; a section may be split
    over several tables (trade_diagnostics.json: the per-trade labels the
    readers' subset leaves out, then the rest)."""
    out: dict = defaultdict(list)
    for m in _SECTION_RE.finditer(text):
        for r in _ROW_RE.finditer(m.group("body")):
            cells = [c.strip() for c in r.group("rest").split(" | ")]
            out[m.group("name")].append((r.group("field"), cells))
    return dict(out)


def _sources(text: str) -> dict:
    body = _SOURCES_RE.search(text).group("body")
    return dict(re.findall(r"^\| `([A-Z][A-Z0-9])` \| `([^`]+)` \|", body, re.M))


def _split_report_field(field: str) -> tuple:
    """`profitability: slices.overall.source` -> ("profitability", path);
    a field without a category prefix belongs to every report ("*")."""
    cat, sep, path = field.partition(": ")
    return (cat, path) if sep else ("*", field)


def _parse_path(path: str) -> tuple:
    """`trades[].mae` -> ("trades", "[]", "mae"); a `<placeholder>` -> "<*>"."""
    out = []
    for seg in path.split("."):
        items = 0
        while seg.endswith("[]"):
            seg, items = seg[:-2], items + 1
        if seg:
            out.append(DYN if seg.startswith("<") else seg)
        out += [ITEM] * items
    return tuple(out)


def _render(p: tuple) -> str:
    s = ""
    for seg in p:
        s += seg if seg == ITEM else (f".{seg}" if s else seg)
    return s


def _render_report(p: tuple) -> str:
    return _render(p[1:]) if p[0] == "*" else f"{p[0]}: {_render(p[1:])}"


def _doc_paths(section: str, text: str | None = None) -> set:
    rows = _sections(_text() if text is None else text)[section]
    if section == "reports":
        return {(cat,) + _parse_path(path)
                for cat, path in (_split_report_field(f) for f, _ in rows)}
    return {_parse_path(f) for f, _ in rows}


def _field_key(field: str) -> str | None:
    """The literal key a row documents: its last segment that is not a
    placeholder (None for a pure placeholder such as `<reserved feed>`)."""
    path = _split_report_field(field)[1]
    lits = [s for s in _parse_path(path) if s not in (ITEM, DYN)]
    return lits[-1] if lits else None


# ---------------------------------------------------------------------------
# Reading the writers' code (AST, no import of the engine)
# ---------------------------------------------------------------------------

_TREES: dict = {}
_TEXTS: dict = {}


def _tree(rel: str) -> ast.Module:
    if rel not in _TREES:
        _TEXTS[rel] = (REPO / rel).read_text(encoding="utf-8")
        _TREES[rel] = ast.parse(_TEXTS[rel])
    return _TREES[rel]


_QUAL: dict = {}


def _qualnames(rel: str) -> dict:
    """{qualname: [nodes]}: functions, classes and methods (`Class.method`,
    `outer.inner` for a nested function) and module-level constants."""
    if rel in _QUAL:
        return _QUAL[rel]
    out: dict = defaultdict(list)

    def walk(node, prefix, top):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                out[prefix + ch.name].append(ch)
                walk(ch, prefix + ch.name + ".", False)
            elif top and isinstance(ch, (ast.Assign, ast.AnnAssign)):
                for t in (ch.targets if isinstance(ch, ast.Assign) else [ch.target]):
                    if isinstance(t, ast.Name):
                        out[t.id].append(ch)
            elif isinstance(ch, (ast.stmt, ast.excepthandler)):
                walk(ch, prefix, top)

    walk(_tree(rel), "", True)
    _QUAL[rel] = dict(out)
    return _QUAL[rel]


def _symbol(rel: str, name: str):
    found = _qualnames(rel).get(name, [])
    assert len(found) == 1, f"{rel}: expected one symbol {name!r}, found {len(found)}"
    return found[0]


def _qualname_of(rel: str, node) -> str | None:
    for q, nodes in _qualnames(rel).items():
        if any(n is node for n in nodes):
            return q
    return None


def _func(rel: str, name: str):
    node = _symbol(rel, name)
    assert isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)), f"{rel}: {name} is not a function"
    return node


def _const_str(node) -> str | None:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _dict_keys(node, nested: bool = True) -> set:
    """String keys of a dict literal (and of dict literals nested in it)."""
    out = set()
    nodes = ast.walk(node) if nested else [node]
    for n in nodes:
        if isinstance(n, ast.Dict):
            out |= {k for k in map(_const_str, n.keys) if k is not None}
    return out


def _subscript_assign_keys(node) -> set:
    """`x["key"] = ...` (also `x[a]["key"] = ...`) anywhere under node."""
    out = set()
    for n in ast.walk(node):
        if isinstance(n, (ast.Assign, ast.AugAssign)):
            for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                if isinstance(t, ast.Subscript) and _const_str(t.slice) is not None:
                    out.add(t.slice.value)
    return out


def _module_constant(rel: str, name: str):
    node = _symbol(rel, name)
    assert isinstance(node, (ast.Assign, ast.AnnAssign)), f"{rel}: {name} is not a constant"
    return node.value


def _assigned_dict(func, var: str):
    found = [n.value for n in ast.walk(func) if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == var for t in n.targets)
             and isinstance(n.value, ast.Dict)]
    assert found, f"{func.name}: no dict literal assigned to {var}"
    return found[0]


def _returned_dicts(func) -> list:
    """Dict literals returned by func: `return {...}` or inside `return (.., {...})`."""
    out = []
    for n in ast.walk(func):
        if isinstance(n, ast.Return) and n.value is not None:
            vals = n.value.elts if isinstance(n.value, ast.Tuple) else [n.value]
            out += [v for v in vals if isinstance(v, ast.Dict)]
    return out


# ---------------------------------------------------------------------------
# The path walker: the full dotted paths a writer emits
# ---------------------------------------------------------------------------

_SCOPE_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
_MUTATORS = {"append", "insert", "extend", "update", "setdefault"}


def _body(scope) -> list:
    """Every node of a function (or module) body, nested scopes left out."""
    out, stack = [], list(ast.iter_child_nodes(scope))
    while stack:
        n = stack.pop()
        if isinstance(n, _SCOPE_NODES):
            continue
        out.append(n)
        stack.extend(ast.iter_child_nodes(n))
    return out


def _params(scope) -> set:
    if not isinstance(scope, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return set()
    a = scope.args
    names = [x.arg for x in a.posonlyargs + a.args + a.kwonlyargs]
    names += [x.arg for x in (a.vararg, a.kwarg) if x is not None]
    return set(names)


def _seg(node) -> str:
    s = _const_str(node)
    if s is not None:
        return s
    if isinstance(node, ast.JoinedStr) and all(_const_str(v) is not None for v in node.values):
        return "".join(v.value for v in node.values)
    return DYN


def _chain(node, name: str):
    """The key path of `name[...][...]` / `name.setdefault(k, ..)[...]`, () for
    the bare name, None when node is not rooted at `name`."""
    if isinstance(node, ast.Name):
        return () if node.id == name else None
    if isinstance(node, ast.Subscript):
        base = _chain(node.value, name)
        return None if base is None else base + (_seg(node.slice),)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
            and node.func.attr == "setdefault" and node.args:
        base = _chain(node.func.value, name)
        return None if base is None else base + (_seg(node.args[0]),)
    return None


def _dict_shaped(node) -> bool:
    """A literal that may legitimately add no key (`{}`, `x if c else {}`)."""
    if isinstance(node, ast.Dict):
        return True
    if isinstance(node, ast.IfExp):
        return _dict_shaped(node.body) and _dict_shaped(node.orelse)
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
        and node.func.id == "dict" and not node.args


def _mount(segs: tuple, sub: set) -> set:
    return ({segs} if segs else set()) | {segs + p for p in sub}


def _items_call(node):
    """X for `X.items()`, else None."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
            and node.func.attr == "items" and not node.args:
        return node.func.value
    return None


class _Walk:
    """Statically reads the dict shapes a writer builds. Paths are tuples of
    keys, DYN for a key only known at run time, ITEM for a list item, and a
    trailing SPREAD where a `**x` / .update(x) adds keys the walk cannot read.
    Follows local variables, for-loop targets, tuple unpacking, mutations
    (subscript assignment, .append/.extend/.insert/.update/.setdefault,
    aliases such as `b = d.setdefault(k, {})`) and calls to functions of the
    same file or of another documented source file (by import)."""

    def __init__(self, sources: dict):
        self.stems = {Path(rel).stem: rel for rel in sources.values()}
        self.stack: set = set()
        self._imports: dict = {}

    # -- symbols ------------------------------------------------------------
    def imports(self, rel: str) -> dict:
        """{local name: (source file, attribute or None)} for imports of a
        documented source file (anywhere in the file, function-level too)."""
        if rel not in self._imports:
            out = {}
            for n in ast.walk(_tree(rel)):
                if isinstance(n, ast.Import):
                    for a in n.names:
                        stem = a.name.rsplit(".", 1)[-1]
                        if stem in self.stems:
                            out[a.asname or a.name] = (self.stems[stem], None)
                elif isinstance(n, ast.ImportFrom):
                    stem = (n.module or "").rsplit(".", 1)[-1]
                    if stem in self.stems:
                        for a in n.names:
                            out[a.asname or a.name] = (self.stems[stem], a.name)
            self._imports[rel] = out
        return self._imports[rel]

    def function(self, rel: str, scope, name: str):
        """(file, qualname) of the function `name` called from scope, or None."""
        quals = _qualnames(rel)
        sq = _qualname_of(rel, scope) if scope is not None else None
        for q in ([f"{sq}.{name}"] if sq else []) + [name]:
            nodes = quals.get(q, [])
            if len(nodes) == 1 and isinstance(nodes[0], (ast.FunctionDef, ast.AsyncFunctionDef)):
                return rel, q
        imp = self.imports(rel).get(name)
        if imp and imp[1] and len(_qualnames(imp[0]).get(imp[1], [])) == 1:
            return imp[0], imp[1]
        return None

    # -- expressions ----------------------------------------------------------
    def expr(self, rel: str, scope, node) -> set:
        E = lambda n: self.expr(rel, scope, n)  # noqa: E731
        if node is None:
            return set()
        if isinstance(node, ast.Dict):
            out = set()
            for k, v in zip(node.keys, node.values):
                if k is None:
                    sub = E(v)
                    out |= sub if (sub or _dict_shaped(v)) else {(SPREAD,)}
                else:
                    out |= _mount((_seg(k),), E(v))
            return out
        if isinstance(node, ast.IfExp):
            return E(node.body) | E(node.orelse)
        if isinstance(node, ast.BoolOp):
            return set().union(*(E(v) for v in node.values))
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            return {(ITEM,) + p for e in node.elts for p in E(e)}
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
            return {(ITEM,) + p for p in E(node.elt)}
        if isinstance(node, ast.DictComp):
            return self.dictcomp(rel, scope, node)
        if isinstance(node, ast.Name):
            return self.name(rel, scope, node.id)
        if isinstance(node, ast.Call):
            return self.call(rel, scope, node, None)
        return set()

    def literal_keys(self, rel: str, node):
        if isinstance(node, ast.Name) and len(_qualnames(rel).get(node.id, [])) == 1 \
                and isinstance(_qualnames(rel)[node.id][0], (ast.Assign, ast.AnnAssign)):
            node = _qualnames(rel)[node.id][0].value
        if isinstance(node, (ast.Tuple, ast.List)) and node.elts \
                and all(_const_str(e) is not None for e in node.elts):
            return [e.value for e in node.elts]
        return None

    def dictcomp(self, rel: str, scope, node) -> set:
        gen, key, val = node.generators[0], node.key, node.value
        tgt, it = gen.target, gen.iter
        if isinstance(key, ast.Name) and isinstance(tgt, ast.Name) and tgt.id == key.id:
            lits = self.literal_keys(rel, it)
            if lits is not None:  # {k: f(k) for k in ("a", "b")}
                sub = self.expr(rel, scope, val)
                return set().union(*(_mount((k,), sub) for k in lits))
        src = _items_call(it)
        if src is not None and isinstance(tgt, ast.Tuple) and len(tgt.elts) == 2 \
                and isinstance(key, ast.Name) and isinstance(val, ast.Name) \
                and all(isinstance(e, ast.Name) for e in tgt.elts) \
                and (key.id, val.id) == (tgt.elts[0].id, tgt.elts[1].id):
            return self.expr(rel, scope, src)  # {k: v for k, v in x.items() if ..}: a copy of x
        return _mount((DYN,), self.expr(rel, scope, val))

    def call(self, rel: str, scope, node, index) -> set:
        f = node.func
        target = None
        if isinstance(f, ast.Name):
            if f.id == "dict" and index is None:
                out = self.expr(rel, scope, node.args[0]) if node.args else set()
                for kw in node.keywords:
                    out |= _mount((kw.arg,), self.expr(rel, scope, kw.value)) if kw.arg \
                        else self.expr(rel, scope, kw.value)
                return out
            if f.id in ("list", "tuple") and index is None:
                return self.expr(rel, scope, node.args[0]) if node.args else set()
            target = self.function(rel, scope, f.id)
        elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
            imp = self.imports(rel).get(f.value.id)
            if imp and imp[1] is None and len(_qualnames(imp[0]).get(f.attr, [])) == 1:
                target = (imp[0], f.attr)
        return self.returns(*target, index) if target else set()

    def at_index(self, rel: str, scope, node, i: int) -> set:
        if isinstance(node, ast.Tuple):
            return self.expr(rel, scope, node.elts[i]) if i < len(node.elts) else set()
        if isinstance(node, ast.Call):
            return self.call(rel, scope, node, i)
        return set()

    def returns(self, rel: str, qual: str, index=None) -> set:
        """Paths of what a function returns (`index`: element i of a returned tuple)."""
        key = ("ret", rel, qual, index)
        if key in self.stack:
            return set()
        self.stack.add(key)
        try:
            fn = _func(rel, qual)
            out = set()
            for n in _body(fn):
                if isinstance(n, ast.Return) and n.value is not None:
                    if index is None:
                        if not isinstance(n.value, ast.Tuple):
                            out |= self.expr(rel, fn, n.value)
                    else:
                        out |= self.at_index(rel, fn, n.value, index)
            return out
        finally:
            self.stack.discard(key)

    # -- names ----------------------------------------------------------------
    def name(self, rel: str, scope, name: str) -> set:
        key = ("name", rel, id(scope), name)
        if key in self.stack:
            return set()
        self.stack.add(key)
        try:
            if isinstance(scope, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found, out = self.local(rel, scope, name)
                if found or name in _params(scope):
                    return out
            return self.local(rel, _tree(rel), name)[1]
        finally:
            self.stack.discard(key)

    def local(self, rel: str, scope, name: str, mutations_only: bool = False):
        """(found, paths) of `name` in one scope: its assignments (unless
        mutations_only), for-loop bindings and every mutation."""
        E = lambda n: self.expr(rel, scope, n)  # noqa: E731
        found, out = False, set()
        for n in _body(scope):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        if t.id == name and not mutations_only:
                            found, out = True, out | E(n.value)
                    elif isinstance(t, ast.Tuple):
                        for i, e in enumerate(t.elts):
                            if isinstance(e, ast.Name) and e.id == name and not mutations_only:
                                found, out = True, out | self.at_index(rel, scope, n.value, i)
                    else:
                        segs = _chain(t, name)
                        if segs:
                            found, out = True, out | _mount(segs, E(n.value))
                segs = _chain(n.value, name)  # alias: b = name[k] / name.setdefault(k, ..)
                if segs:
                    for t in n.targets:
                        if isinstance(t, ast.Name) and t.id != name:
                            out |= _mount(segs, self.local(rel, scope, t.id, True)[1])
            elif isinstance(n, (ast.AnnAssign, ast.AugAssign)) and n.value is not None:
                if isinstance(n.target, ast.Name) and n.target.id == name and not mutations_only:
                    found, out = True, out | E(n.value)
            elif isinstance(n, ast.For) and not mutations_only:
                t = n.target
                if isinstance(t, ast.Name) and t.id == name:  # for x in a_list
                    found = True
                    out |= {p[1:] for p in E(n.iter) if len(p) > 1 and p[0] == ITEM}
                elif isinstance(t, ast.Tuple) and len(t.elts) == 2 and _items_call(n.iter) \
                        and isinstance(t.elts[1], ast.Name) and t.elts[1].id == name:
                    found = True  # for k, x in a_dict.items()
                    out |= {p[1:] for p in E(_items_call(n.iter)) if len(p) > 1 and p[0] != ITEM}
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                    and n.func.attr in _MUTATORS:
                segs = _chain(n.func.value, name)
                if segs is not None:
                    found, out = True, out | self.mutation(rel, scope, segs, n)
        return found, out

    def mutation(self, rel: str, scope, segs: tuple, call) -> set:
        E = lambda n: self.expr(rel, scope, n)  # noqa: E731
        m, a = call.func.attr, call.args
        out = {segs} if segs else set()
        if m == "append" and a:
            out |= {segs + (ITEM,) + p for p in E(a[0])}
        elif m == "insert" and len(a) > 1:
            out |= {segs + (ITEM,) + p for p in E(a[1])}
        elif m == "extend" and a:
            out |= {segs + p for p in E(a[0])}
        elif m == "update":
            for x in a:
                sub = E(x)
                out |= {segs + p for p in sub} if (sub or _dict_shaped(x)) else {segs + (SPREAD,)}
            for kw in call.keywords:
                out |= _mount(segs + (kw.arg,), E(kw.value)) if kw.arg \
                    else {segs + p for p in E(kw.value)}
        elif m == "setdefault" and a:
            out |= _mount(segs + (_seg(a[0]),), E(a[1]) if len(a) > 1 else set())
        return out


_WALK: list = []


def _walker() -> _Walk:
    if not _WALK:
        _WALK.append(_Walk(_sources(_text())))
    return _WALK[0]


def _var(rel: str, scope: str, var: str) -> set:
    return _walker().name(rel, _func(rel, scope), var)


def _ret(rel: str, func: str, index=None) -> set:
    return _walker().returns(rel, func, index)


def _under(prefix: tuple, paths: set) -> set:
    return {p[len(prefix):] for p in paths if p[:len(prefix)] == prefix and len(p) > len(prefix)}


def _closure(paths) -> set:
    return {p[:i] for p in paths for i in range(1, len(p) + 1)}


# ---------------------------------------------------------------------------
# Where each file's fields come from
# ---------------------------------------------------------------------------

SLICES = ("overall", "per_window", "per_regime", "per_symbol")
BARS = ("grid", DYN, DYN, "bars")

# Writers the walk does not reach on its own: (section, mount point, how to
# read the writer, why it is not reached).
EXTRA_WRITERS = [
    ("core", (), lambda: _under(("core",), _var(RA, "write_metrics_json", "payload")),
     "write_metrics_json adds sharpe_annualization to build_core's dict (a parameter there)"),
    ("grid_evaluation.yaml", (),
     lambda: set().union(*(_walker().name(P1, f, "_grid_result") for f in _grid_stampers())),
     "run_phase1_research stamps evaluated_at on the grid it saves"),
    ("grid_evaluation.yaml", BARS + (ITEM,), lambda: _var(P1, "_grade_profit_bars._bar", "entry"),
     "evaluate_grid gets the profit-bars grader as a callable argument "
     "(run_phase1_research._profit_bars_grid_grader): the v1 bar rows"),
    ("grid_evaluation.yaml", BARS + (ITEM,), lambda: _var(P1, "_grade_profit_bars_v2", "entry"),
     "same grader, the v2 bar rows (orchestrator.profit_bars_v2)"),
    ("grid_evaluation.yaml", BARS, lambda: _ret(P1, "_hold_rows_not_evaluable", 0),
     "same grader, rows held NOT_EVALUABLE on partial coverage (v2)"),
    ("reports", (), lambda: _builder_paths(),
     "build_reports calls each builder through the BUILDERS dict; the builders' "
     "slices are the arguments of their _wrap(...) call"),
]

# A `**x` / .update(x) whose keys the walk cannot read: allowed only here,
# with the reason; the dictionary documents what x carries (by hand).
OPAQUE_ALLOWED = {
    "core": {"(root)": "build_core's dict (a parameter of write_metrics_json), walked from build_core"},
    "reports": {
        "forecast_power: (root)": "the forecast_power report itself, copied before statistic_labels is added",
        "variants.<*>": "_strip_legacy_verdict_fields (profitability) copies each variant block "
                        "(kind, symbol, status, coverage: walked in build_reports)",
        "profitability: slices.per_window[]": "_strip_legacy_verdict_slices copies each per_window row "
                                              "(walked in build_profitability_report)",
        "profitability: slices.per_regime.<*>[]": "the window's per_regime block (section 4)",
        "forecast_power: slices.per_regime.<*>[]": "the window's regime_validity block (section 4)",
        "trade_efficiency: slices.overall": "the trade_diagnostics summary (section 2), a parameter",
    },
    "grid_evaluation.yaml": {
        "grid.<*>.<*>.bars[]": "_hold_rows_not_evaluable copies the graded row "
                               "(_grade_profit_bars / _grade_profit_bars_v2, walked)",
    },
}

# Same shape at two places: paths under the first prefix are read as paths
# under the second (keep=True: the first prefix itself is a documented row).
ALIASES = {
    "grid_evaluation.yaml": [((("grid", DYN, DYN, "per_symbol", DYN)), ("grid", DYN, DYN), True)],
    "reports": (
        # a per-category slice under variants.<variant>.slices is the same slice
        [((c, "variants", DYN, "slices"), (c, "slices"), False) for c in REPORT_CATEGORIES]
        # a per-category copy of a variant block is the common variant block
        + [((c, "variants"), ("*", "variants"), False) for c in REPORT_CATEGORIES]
        # every report's {unavailable, reason} slice
        + [((c, "slices", s, leaf), ("*", "slices", DYN, leaf), False)
           for c in REPORT_CATEGORIES for s in SLICES for leaf in ("unavailable", "reason")]
        + [(("regime_power", "slices", "per_symbol", DYN, ITEM),
            ("regime_power", "slices", "per_window", ITEM), True)]),
}


def _grid_stampers() -> list:
    out = []
    for nodes in _qualnames(P1).values():
        fn = nodes[0]
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) and any(
                isinstance(n, ast.Assign) and any(_chain(t, "_grid_result") for t in n.targets)
                for n in _body(fn)):
            out.append(fn)
    assert out, "no function stamps _grid_result"
    return out


def _builder_paths() -> set:
    builders = _module_constant(BR, "BUILDERS")
    out = set()
    for k, v in zip(builders.keys, builders.values):
        fn = _func(BR, v.id)
        wraps = [n for n in _body(fn) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name) and n.func.id == "_wrap"]
        assert wraps, f"{v.id}: no _wrap(...) call"
        for c in wraps:
            assert _const_str(c.args[0]) == _const_str(k), (v.id, ast.dump(c.args[0]))
            for i, s in enumerate(SLICES):
                out |= {(k.value, "slices", s) + p
                        for p in _walker().expr(BR, fn, c.args[i + 1])}
    return out


def _report_paths() -> set:
    out = set()
    for p in _var(BR, "build_reports", "reports"):  # {category: report}
        out.add((("*",) if p[0] == DYN else p[:1]) + p[1:])
    out |= {("*",) + p for p in _ret(BR, "_wrap")}
    return out


def _auto_paths(section: str) -> set:
    if section == "trade_diagnostics.json":
        return _var(RP, "main", "td_payload")
    if section == "core":
        return _ret(RA, "build_core")
    if section == "per_regime":
        return _ret(RA, "build_per_regime")
    if section == "regime_validity":
        return _ret(RA, "build_regime_validity")
    if section == "diagnostics":
        return _ret(RP, "_build_diagnostics")
    if section == "reports":
        return _report_paths()
    if section == "grid_evaluation.yaml":
        return _ret(VE, "evaluate_grid")
    if section == "claim_result_digest.yaml":
        return _ret(RF, "claim_result_digest")
    if section == "claim_measurement.yaml":
        return _ret(CM, "run_doc") | _ret(CM, "error_doc")
    raise AssertionError(section)


def _apply_aliases(paths: set, section: str) -> set:
    out = set()
    for p in paths:
        for a, b, keep in ALIASES.get(section, []):
            if p[:len(a)] == a:
                if keep:
                    out |= _closure([a])
                p = b + p[len(a):]
                break
        out.add(p)
    return out


def code_paths(section: str) -> tuple:
    """(paths, opaque): the normalized paths the writers of `section` emit, and
    the containers into which a spread adds keys the walk cannot read."""
    raw = set(_auto_paths(section))
    for sec, mount, read, _why in EXTRA_WRITERS:
        if sec == section:
            raw |= {mount + p for p in read()}
    opaque = {p[:-1] for p in raw if p[-1] == SPREAD}
    paths = {p for p in raw if p[-1] != SPREAD} | {p for p in opaque if p}
    return _apply_aliases(paths, section), _apply_aliases(opaque, section)


def _render_for(section: str, p: tuple) -> str:
    if not p or (section == "reports" and len(p) == 1):
        return (f"{p[0]}: (root)" if p and p[0] != "*" else "(root)")
    return _render_report(p) if section == "reports" else _render(p)


SECTIONS = ("trade_diagnostics.json", "core", "per_regime", "regime_validity", "diagnostics",
            "reports", "grid_evaluation.yaml", "claim_result_digest.yaml", "claim_measurement.yaml")


# ---------------------------------------------------------------------------
# bars.csv: exact column patterns
# ---------------------------------------------------------------------------

def bars_csv_columns() -> set:
    """The exact column patterns bars.csv can carry, from the writers: the
    record_state keywords (core/trading_bot.py), the bar row (OHLCV + feeds),
    StrategyOutput, its debug_info and the nested debug dicts, each flattened
    the way portfolio_info.flatten_dict_columns does (a dict column becomes
    dotted columns; a dict column empty on every row stays as its own column)."""
    recorded = set()
    spreads = 0
    for n in ast.walk(_tree(TB)):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                and n.func.attr == "record_state":
            recorded |= {kw.arg for kw in n.keywords if kw.arg}
            spreads += sum(1 for kw in n.keywords if kw.arg is None)
    assert spreads == 1, "the per-bar record_state call spreads **risk_extras exactly once"
    recorded -= {"data", "signal", "replace_if_same_bar"}
    nested = {"balances", "postRebalance_balances", "debug_approve_allocation_change",
              "debug_execute_portfolio_rebalance"}
    assert nested <= recorded
    cols = recorded - nested

    # the bar row: OHLCV (CandleBuilder) + the aux feed columns
    cols |= _dict_keys(_func(DM, "CandleBuilder.get_candle_history"))
    cols |= _dict_keys(_module_constant(FR, "FEED_REGISTRY"), nested=False)
    assert _module_constant(FR, "WHALE_FOOTPRINT_FEEDS").elts, "reserved feeds exist"
    cols.add("<reserved feed>")
    # backtester's copy of total_portfolio_value
    assert "portfolio_value" in _subscript_assign_keys(_tree(BT))
    cols.add("portfolio_value")

    # StrategyOutput's fields; debug_info is always a non-empty dict (flattened)
    so = _symbol(SB, "StrategyOutput")
    fields = {n.target.id for n in so.body if isinstance(n, ast.AnnAssign)}
    assert "debug_info" in fields
    cols |= fields - {"debug_info"}
    gen = _func(MS, "AdvancedStrategy.generate_forecast")
    debug_keys = _dict_keys(_assigned_dict(gen, "debug_info"), nested=False)
    assert {"regime_scores", "components"} <= debug_keys
    cols |= {f"debug_info.{k}" for k in debug_keys - {"regime_scores", "components"}}
    for call in ast.walk(_func(SB, "MainStrategy.generate_signals")):  # NOT_READY / ERROR outputs
        if isinstance(call, ast.Call):
            for kw in call.keywords:
                if kw.arg == "debug_info" and isinstance(kw.value, ast.Dict):
                    cols |= {f"debug_info.{k}" for k in _dict_keys(kw.value)}
    cols |= {"debug_info.regime_scores", "debug_info.regime_scores.<regime>",
             "debug_info.components"}
    for name in ("ConfigDrivenStrategyEngine.forecast", "ConfigDrivenStrategyEngine._forecast_blocks"):
        f = _func(SE, name)
        for n in ast.walk(f):  # debug[cid] = {...}: one dict per component
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict) \
                    and isinstance(n.targets[0], ast.Subscript):
                cols |= {f"debug_info.components.<component>.{k}" for k in _dict_keys(n.value)}
        for d in _returned_dicts(f):  # (0.0, {"not_ready_...": id})
            cols |= {f"debug_info.components.{k}" for k in _dict_keys(d)}

    # balances: {asset: {free, locked}}
    bal = _dict_keys(_returned_dicts(_func(PI, "_default_balance"))[0])
    inner = bal - {"USDT"}
    assert inner == {"free", "locked"}, inner
    cols |= {f"{b}.<asset>.{k}" for b in ("balances", "postRebalance_balances") for k in inner}

    # the risk manager's debug dict and its controls
    approve = _func(RM, "RiskManager.approve_allocation_change")
    top = _dict_keys(_assigned_dict(approve, "debug"), nested=False)
    assert "controls" in top
    passed = set()
    for n in ast.walk(approve):
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict):
            passed |= _dict_keys(n.value) - top
    controls = {n.name[len("_ctrl_"):] for n in ast.walk(_tree(RM))
                if isinstance(n, ast.FunctionDef) and n.name.startswith("_ctrl_")}
    cols.add("debug_approve_allocation_change")
    cols |= {f"debug_approve_allocation_change.{k}" for k in top - {"controls"}}
    cols |= {f"debug_approve_allocation_change.controls.{c}.{p}" for c in controls for p in passed}

    # the (mock) execution handler's order dicts
    order = set()
    for name in ("MockExecutionHandler.open_long_position",
                 "MockExecutionHandler.open_short_position",
                 "MockExecutionHandler.close_position"):
        for d in _returned_dicts(_func(EH, name)):
            order |= _dict_keys(d)
    cols.add("debug_execute_portfolio_rebalance")
    cols |= {f"debug_execute_portfolio_rebalance.{k}" for k in order}

    # the portfolio risk gate's extras (**risk_extras)
    apply = _func(RG, "PortfolioRiskGate.apply")
    cols |= _dict_keys(_assigned_dict(apply, "extras")) | _subscript_assign_keys(apply)
    return cols


# ---------------------------------------------------------------------------
# 1. The dictionary parses; every reference resolves to a symbol holding the key
# ---------------------------------------------------------------------------

def test_every_section_is_present_and_every_row_is_complete():
    secs = _sections(_text())
    assert set(secs) == {"bars.csv", *SECTIONS}, sorted(set(secs) ^ {"bars.csv", *SECTIONS})
    for name, rows in secs.items():
        assert rows, f"{name}: no rows"
        fields = [f for f, _ in rows]
        dups = sorted({f for f in fields if fields.count(f) > 1})
        assert not dups, f"{name}: duplicate rows {dups}"
        for field, cells in rows:
            assert len(cells) == 4 and all(cells), f"{name} `{field}`: {cells}"
            meaning, unit, code, when = cells
            assert when in WHEN, f"{name} `{field}`: when known {when!r} not in {sorted(WHEN)}"
            assert _REF_RE.search(code), f"{name} `{field}`: no code reference in {code!r}"


def test_no_line_number_references():
    """References name a symbol; a line number drifts silently."""
    assert not _LINE_REF_RE.search(_text()), _LINE_REF_RE.findall(_text())[:5]


def test_every_code_reference_resolves_to_one_symbol():
    text = _text()
    sources = _sources(text)
    refs = list(_REF_RE.finditer(text))
    assert len(refs) > 300
    for m in refs:
        key, sym = m.group("key"), m.group("sym")
        assert key in sources, f"unknown source key {key} ({m.group(0)})"
        assert (REPO / sources[key]).exists(), f"{key}: {sources[key]} does not exist"
        _symbol(sources[key], sym)  # exactly one


def _symbol_strings(rel: str, sym: str) -> set:
    """The literal names inside a symbol: string constants (and their dotted
    parts), keyword-argument names and class-body field names."""
    out = set()
    for n in ast.walk(_symbol(rel, sym)):
        s = _const_str(n)
        if s is not None:
            out |= {s, *s.split(".")}
        elif isinstance(n, ast.keyword) and n.arg:
            out.add(n.arg)
        elif isinstance(n, ast.ClassDef):
            out |= {b.target.id for b in n.body
                    if isinstance(b, ast.AnnAssign) and isinstance(b.target, ast.Name)}
    return out


def test_every_row_cites_a_symbol_that_writes_its_key():
    """A row's key (its last literal segment) is a string literal, a keyword
    argument or a dataclass field inside one of the symbols the row cites."""
    text = _text()
    sources = _sources(text)
    bad = []
    for section, rows in _sections(text).items():
        for field, (_m, _u, code, _w) in rows:
            key = _field_key(field)
            if key is None:
                continue
            refs = [(sources[m.group("key")], m.group("sym")) for m in _REF_RE.finditer(code)]
            if not any(key in _symbol_strings(rel, sym) for rel, sym in refs):
                bad.append(f"{section} `{field}` ({key!r} not in {code})")
    assert not bad, "\n".join(bad)


def test_the_dictionary_has_no_holdout_dates():
    """The sealed holdout's dates never appear in a file a reader gets."""
    assert not re.search(r"2026-0[1-6]", _text())
    assert not re.search(r"2026-0[1-6]", _text(READERS_DICTIONARY))


# ---------------------------------------------------------------------------
# 2. Kept honest against the writers
# ---------------------------------------------------------------------------

def test_bars_csv_columns_match_the_code_exactly():
    doc = {f for f, _ in _sections(_text())["bars.csv"]}
    code = bars_csv_columns()
    assert not code - doc, f"bars.csv columns written by the code, missing here: {sorted(code - doc)}"
    assert not doc - code, f"bars.csv entries no longer written by the code: {sorted(doc - code)}"


def _compare(section: str, text: str | None = None) -> tuple:
    code, _opaque = code_paths(section)
    doc = _apply_aliases(_doc_paths(section, text), section)
    c, d = _closure(code), _closure(doc)
    return (sorted(_render_for(section, p) for p in c - d),
            sorted(_render_for(section, p) for p in d - c))


@pytest.mark.parametrize("section", SECTIONS)
def test_every_written_path_is_documented_and_no_entry_is_stale(section):
    code, _ = code_paths(section)
    assert code, f"{section}: the code-derived path list is empty"
    missing, stale = _compare(section)
    assert not missing, f"{section}: paths written by the code, missing here: {missing}"
    assert not stale, f"{section}: entries no longer written by the code: {stale}"


@pytest.mark.parametrize("section", SECTIONS)
def test_unreadable_spreads_are_exactly_the_allowed_ones(section):
    _, opaque = code_paths(section)
    found = {_render_for(section, p) for p in opaque}
    allowed = OPAQUE_ALLOWED.get(section, {})
    assert found == set(allowed), (
        f"{section}: a **spread / .update() the walk cannot read must be listed in "
        f"OPAQUE_ALLOWED with its reason: new {sorted(found - set(allowed))}, "
        f"gone {sorted(set(allowed) - found)}")
    assert all(allowed.values())


def test_the_derivation_is_not_vacuous():
    """The derived paths are the real ones (full paths, not bare names), and a
    dictionary with a row cut, a reused name under a new parent or a key moved
    to another parent is caught."""
    code = {s: code_paths(s)[0] for s in SECTIONS}
    assert {"forecast", "allocation_change", "debug_info.components.<component>.post_pipeline_value",
            "debug_approve_allocation_change.controls.min_allocation_change.passed",
            "succcess_execute_portfolio_rebalance", "fear_greed"} <= bars_csv_columns()
    assert {("trades", ITEM, "entry_efficiency"), ("trades", ITEM, "exit_reason"),
            ("summary", "per_trade_expectancy_bps", "n"),
            ("summary", "fee_reduction_metrics", "trade_less_often", "boundary_recross_rate"),
            ("summary", "cost_components_measured", "slippage")} <= code["trade_diagnostics.json"]
    assert {("forecast_return_corr",), ("sharpe_annualization",),
            ("post_backtest_cost_check_real", "basis"),
            ("post_backtest_cost_check", "edge_to_cost_ratio")} <= code["core"]
    assert {(DYN, "bar_count")} <= code["per_regime"]
    assert {("regime_power", "slices", "per_window", ITEM, "hindsight_lag", "median_lag_bars"),
            ("trade_efficiency", "slices", "per_window", DYN, DYN, "p90"),
            ("component_attribution", "slices", "per_regime", DYN, DYN, DYN, "mean"),
            ("forecast_power", "statistic_labels", "prescreen_pooled_ic"),
            ("*", "variants", DYN, "coverage"), ("*", "slices", DYN, "unavailable")} <= code["reports"]
    assert {("grid", DYN, DYN, "detail", "era_medians", DYN), ("evaluated_at",),
            ("grid", DYN, DYN, "fully_explained"), BARS + (ITEM, "actual"),
            BARS + (ITEM, "not_evaluable_reason")} <= code["grid_evaluation.yaml"]
    assert {("variants", DYN, "tests", DYN, "horizons", DYN, "per_coin", DYN, "effect"),
            ("tests", ITEM, "selector"), ("approximation", "deviations", ITEM, "clause"),
            ("variant_patches", "variants", ITEM, "patch", ITEM, "path")} \
        <= code["claim_result_digest.yaml"]
    assert ("n_tests_no_events",) in code["claim_measurement.yaml"]

    text = _text()
    row = "| `trades[].mae` |"
    assert text.count(row) == 1
    cut = "\n".join(ln for ln in text.splitlines() if not ln.startswith(row))
    assert _compare("trade_diagnostics.json", cut)[0] == ["trades[].mae"]
    # a reused name ("n" exists under per_trade_expectancy_bps) under a new parent
    anchor = "| `summary.per_trade_expectancy_bps.n` |"
    assert text.count(anchor) == 1
    reused = text.replace(anchor, "| `summary.pnl_concentration.n` | x. | count | `RP:_aggregate_trade_diagnostics` | run |\n"
                          + anchor)
    assert _compare("trade_diagnostics.json", reused)[1] == ["summary.pnl_concentration.n"]
    # a key moved to another parent
    moved = text.replace("| `summary.stop_loss_recovery_rate` |",
                         "| `summary.exit_reason_breakdown.stop_loss_recovery_rate` |")
    assert moved != text
    missing, stale = _compare("trade_diagnostics.json", moved)
    assert missing == ["summary.stop_loss_recovery_rate"]
    assert stale == ["summary.exit_reason_breakdown.stop_loss_recovery_rate"]


# ---------------------------------------------------------------------------
# 3. The flag
# ---------------------------------------------------------------------------

def test_flag_off_by_default_and_in_the_shipped_config():
    _set_orchestrator(V3_ON)
    assert rpr._observable_backtest_enabled() is False
    shipped = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(
        encoding="utf-8"))
    assert shipped["orchestrator"]["observable_backtest"]["enabled"] is False
    _set_orchestrator(OB_ON)
    assert rpr._observable_backtest_enabled() is True


def test_flag_on_without_reader_findings_raises():
    _set_orchestrator({**CLAIMS_ON, "observable_backtest": {"enabled": True}})
    with pytest.raises(ValueError, match="reader_findings.enabled=true"):
        rpr._observable_backtest_enabled()


@pytest.mark.parametrize("bad", ["true", 1, None])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**V3_ON, "observable_backtest": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._observable_backtest_enabled()


def test_flag_is_registered_everywhere():
    reg = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml").read_text(
        encoding="utf-8"))
    [entry] = [f for f in reg["flags"] if f["name"] == "observable_backtest"]
    assert entry["config_key"] == "orchestrator.observable_backtest.enabled"
    assert entry["reader"] == "run_phase1_research._observable_backtest_enabled"
    assert entry["state"] == "off_incomplete" and entry["blocked_on"]
    assert camp._flag_readers()["observable_backtest"] is rpr._observable_backtest_enabled
    import test_e061_end_to_end_wiring as wiring
    assert wiring.TARGET_FLAGS["observable_backtest"] is False


# ---------------------------------------------------------------------------
# 4. The readers' subset, the handoff and the prompt
# ---------------------------------------------------------------------------

def test_the_readers_subset_is_generated_from_the_full_file():
    full = _text()
    assert _text(READERS_DICTIONARY) == dd.reader_subset(full), (
        "docs/DATA_DICTIONARY_READERS.md is stale: run `python tools/data_dictionary.py` "
        "from strategy-research/")
    assert rpr.DATA_DICTIONARY_DOC == "../../docs/" + READERS_DICTIONARY.name


def test_the_readers_subset_holds_what_the_readers_receive():
    sub = _text(READERS_DICTIONARY)
    secs = _sections(sub)
    assert set(secs) == set(SECTIONS), sorted(set(secs) ^ set(SECTIONS))  # no bars.csv
    assert "## 1. bars.csv" not in sub and dd.OMIT_OPEN not in sub and dd.OMIT_CLOSE not in sub
    for heading in ("## How to read it", "## Not recorded today", "## Audit findings",
                    "<!-- data-dictionary-sources -->"):
        assert heading in sub
    full = _sections(_text())
    for s in SECTIONS:
        if s != "trade_diagnostics.json":
            assert secs[s] == full[s], s
    # trade_diagnostics.json: the summary and the numeric per-trade fields the
    # trade_efficiency report aggregates; the per-trade labels (no report carries
    # them) are left out
    kept = {f for f, _ in secs["trade_diagnostics.json"]}
    left = {f for f, _ in full["trade_diagnostics.json"]} - kept
    assert {f for f in kept if f.startswith("summary")} \
        == {f for f, _ in full["trade_diagnostics.json"] if f.startswith("summary")}
    assert left == {f"trades[].{k}" for k in (
        "trade_id", "symbol", "window", "regime_at_entry", "direction", "entry_time",
        "exit_time", "profitable_net", "exit_reason", "entered_earlier_better",
        "held_longer_better")}
    units = {f: c[1] for f, c in full["trade_diagnostics.json"]}
    assert all(units[f] in ("id", "label", "time", "bool") for f in left)
    assert all(units[f] not in ("id", "label", "time", "bool")
               for f in kept if f.startswith("trades[]."))
    assert len(sub.encode("utf-8")) < len(_text().encode("utf-8"))


@pytest.mark.parametrize("bad", [
    "# T\n<!-- readers: omit -->\nx\n",
    "# T\n<!-- /readers: omit -->\nx\n<!-- readers: omit -->\n",
    "# T\n<!-- readers: omit -->\n<!-- readers: omit -->\nx\n<!-- /readers: omit -->\n"
    "<!-- /readers: omit -->\n",
    "# T\nno markers at all\n"])
def test_the_subset_refuses_broken_markers(bad):
    with pytest.raises(ValueError):
        dd.reader_subset(bad)


def _seed_dictionary() -> None:
    for src in (DICTIONARY, READERS_DICTIONARY):
        dst = rpr.ROOT / "docs" / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)


def _prompt(cat: str, handoff: dict, run_dir: Path) -> str:
    return rpr._build_stage_prompt("specialist_readers", handoff, run_dir,
                                   skill_file_name=rpr._reader_skill_dir(cat))


@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_flag_off_handoff_and_prompt_are_byte_identical(cat, monkeypatch):
    run_dir = _run070_shaped(monkeypatch)  # reader_findings on, the key absent
    _seed_dictionary()
    absent = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    assert absent == rpr._reader_handoff_v3(cat, RUN_ID, 0, run_dir)
    prompt_absent = _prompt(cat, absent, run_dir)
    _set_orchestrator(OB_OFF)  # the key present, false
    off = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    assert off == absent
    assert _prompt(cat, off, run_dir) == prompt_absent
    assert "DATA_DICTIONARY" not in prompt_absent


@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_flag_on_adds_the_readers_subset_and_one_line(cat, monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    _seed_dictionary()
    off = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    _set_orchestrator(OB_ON)
    on = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    assert on["required_inputs"][:-1] == off["required_inputs"]
    assert on["required_inputs"][-1]["path"] == rpr.DATA_DICTIONARY_DOC
    assert on["optional_inputs"] == off["optional_inputs"]
    assert on["objective"] == off["objective"] + " " + rpr.DATA_DICTIONARY_LINE
    assert on["injected_context"] == {**off["injected_context"],
                                      "data_dictionary": rpr.DATA_DICTIONARY_LINE}
    assert {k: v for k, v in on.items() if k not in ("required_inputs", "objective",
                                                     "injected_context")} \
        == {k: v for k, v in off.items() if k not in ("required_inputs", "objective",
                                                      "injected_context")}
    prompt = _prompt(cat, on, run_dir)
    assert f"--- CONTENT OF {rpr.DATA_DICTIONARY_DOC} ---\n{_text(READERS_DICTIONARY)}" in prompt
    assert "## 1. bars.csv" not in prompt  # the readers' subset, not the full file
    assert yaml.dump(on, sort_keys=False) in prompt  # the handoff, line included


def test_flag_on_does_not_touch_the_v2_readers(monkeypatch):
    """Without reader_findings the v2 handoff is built and the flag is never
    read there (the launch pre-flight refuses that combination)."""
    _set_orchestrator({**CLAIMS_ON})
    monkeypatch.chdir(SR_ROOT)
    from test_e046a_slice5b_ii_b_readers_stage import _seed_run
    run_dir = _seed_run()
    v2 = rpr._reader_handoff("profitability", RUN_ID, 0, run_dir)
    _set_orchestrator({**CLAIMS_ON, "observable_backtest": {"enabled": True}})
    assert rpr._reader_handoff("profitability", RUN_ID, 0, run_dir) == v2
