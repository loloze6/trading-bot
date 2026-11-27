"""Compare the files run_idea wrote with the joined code (out_new) and with the code before the join (out_old).
Prints: files in each, identical bytes, differing; for each differing file, whether it is identical once the volatile
fields are masked (times, durations, git shas, engine run ids, temporary paths), and the first lines that still differ."""
import gzip, re, sys, collections
from pathlib import Path

P = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent     # the PROOF_DIR of run_one.sh
A, B = P / "out_new", P / "out_old"
MASKS = [
    (re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?"), "<time>"),
    (re.compile(r"\b[0-9a-f]{7,40}(-dirty)?\b"), "<sha>"),
    (re.compile(r"/tmp/[^\s\"',)]+"), "<tmp>"),
    (re.compile(r"\"(seconds|elapsed[a-z_]*|duration[a-z_]*|wall[a-z_]*|minutes)\":\s*[-0-9.eE]+"), r'"\1": <n>'),
    (re.compile(r"\b(run|bt|backtest)[_-]?id[\"']?[:=]\s*[\"']?[\w.-]+"), "<runid>"),
    (re.compile(r"\b\d+(\.\d+)? ?(s|min|seconds|minutes)\b"), "<dur>"),
    (re.compile(r"\b\d{8}T\d{6}Z_[0-9a-f]+\b"), "<protocol_run_id>"),
]


def read(p):
    b = p.read_bytes()
    if p.suffix == ".gz":
        b = gzip.decompress(b)
    return b.decode("utf-8", "replace")


def mask(t):
    for rx, rep in MASKS:
        t = rx.sub(rep, t)
    return t


fa = {p.relative_to(A) for p in A.rglob("*") if p.is_file()}
fb = {p.relative_to(B) for p in B.rglob("*") if p.is_file()}
print(f"new: {len(fa)} files; old: {len(fb)}; only new: {len(fa - fb)}; only old: {len(fb - fa)}")
for x in sorted(fa - fb)[:20]: print("  only new:", x)
for x in sorted(fb - fa)[:20]: print("  only old:", x)
same = differ_masked_same = 0
kinds = collections.Counter(); rest = []
for f in sorted(fa & fb):
    if (A / f).read_bytes() == (B / f).read_bytes():
        same += 1; continue
    ta, tb = read(A / f), read(B / f)
    if mask(ta) == mask(tb):
        differ_masked_same += 1; kinds[f.name] += 1; continue
    la, lb = mask(ta).splitlines(), mask(tb).splitlines()
    d = [(i, x, y) for i, (x, y) in enumerate(zip(la, lb)) if x != y]
    rest.append((f, len(la), len(lb), d[:3]))
print(f"identical bytes: {same}; identical once times, shas, ids, paths and durations are masked: {differ_masked_same}; "
      f"still different: {len(rest)}")
print("  masked-identical by file name:", dict(kinds.most_common(12)))
for f, na, nb, d in rest:
    print(f"\n== {f} (lines new {na}, old {nb})")
    for i, x, y in d:
        print(f"  line {i}:\n    new: {x[:220]}\n    old: {y[:220]}")
