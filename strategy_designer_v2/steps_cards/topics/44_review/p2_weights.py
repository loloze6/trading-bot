"""Topic 44, P2: how much of each candidate (P1's 25 books, p1_returns.csv.gz), three weight rules compared out of fold.
The portfolio's daily return is the weighted sum of its books' daily returns (in parallel, P3); weights sum to 1 (the
same capital as one book), each at most 3 times the equal weight, recomputed every 7 days.
  equal capital:   1/n each.
  equal risk:      each book's weight in inverse proportion to its swing (standard deviation of its daily returns) over
                   all the days before, in calendar order.
  shared risk:     equal risk contribution with the correlations: each book adds the same share of the portfolio's swing,
                   from the covariance of the books' daily returns over all the days before, in calendar order.
Why this can't leak: a day's weights use only the returns of days before it in calendar time (the windows tile the
calendar; step 6's chain order puts 2022-23 first, so trailing in the chain would read later years); a book with
fewer than 60 days before it, or none of them in a position, takes the equal weight's place in the rule.
Out of fold: folds are the window blocks 1-6, 7-12, 13-18, 19-24 (step 4 numbers windows in the folds' order). For each
fold, the rule with the best Calmar on the other three (their windows chained in step 6's order) is chosen and judged on
that fold. Decision rule, written before the run: a rule replaces equal capital only if it is the one chosen in at least
3 of the 4 folds and beats equal capital on at least 3 of the 4 held-out folds; otherwise equal capital (the simplest).
  python3 topics/44_review/p2_weights.py [--earning]   (the candidates of P1's variant; outputs tagged _earning)"""
import pathlib, sys, warnings
import numpy as np, pandas as pd
from scipy.optimize import minimize

warnings.simplefilter("ignore")
HERE = pathlib.Path(__file__).resolve().parent
CAP, EVERY, MIN_DAYS = 3.0, 7, 60


def capped(w, cap):
    """Weights summing to 1, none above cap / n (excess spread over the others in proportion)."""
    w = np.asarray(w, float) / np.sum(w); top = cap / len(w)
    for _ in range(100):
        over = w > top + 1e-12
        if not over.any(): break
        extra = (w[over] - top).sum(); w[over] = top
        w[~over] += extra * w[~over] / w[~over].sum()
    return w


def inverse_swing(past):
    sd = past.std(axis=0, ddof=1)
    ok = (sd > 0) & (np.count_nonzero(past, axis=0) > 0)
    if not ok.any(): return np.full(past.shape[1], 1 / past.shape[1])
    w = np.where(ok, 1 / np.where(ok, sd, 1), 0.0)
    w[~ok] = np.mean(w[ok])                                  # a book with no swing yet: the others' mean weight
    return w / w.sum()


def risk_shared(past):
    """Equal risk contribution: minimise w'Cw/2 - mean(log w), then scale to sum 1 (Spinu's convex form)."""
    n = past.shape[1]; base = inverse_swing(past)
    ok = (past.std(axis=0, ddof=1) > 0) & (np.count_nonzero(past, axis=0) > 0)
    if ok.sum() < 2: return base
    C = np.cov(past[:, ok], rowvar=False) * 1e4; k = ok.sum()
    f = lambda x: 0.5 * x @ C @ x - np.log(x).sum() / k
    g = lambda x: C @ x - 1 / (k * x)
    x0 = base[ok] / base[ok].sum() / np.sqrt(base[ok] @ C @ base[ok] / base[ok].sum() ** 2 * k)
    r = minimize(f, x0, jac=g, bounds=[(1e-10, None)] * k, method="L-BFGS-B")
    w = np.zeros(n); w[ok] = r.x / r.x.sum() * ok.mean()
    w[~ok] = base[~ok] / base.sum() if (~ok).any() else 0
    return w / w.sum()


def weights(R, rule):
    """R: days x books in calendar order. Returns the weights each day, from the days before it only."""
    n_days, n = R.shape; W = np.full((n_days, n), 1 / n)
    if rule == "equal capital": return W
    fn = inverse_swing if rule == "equal risk" else risk_shared
    cur = np.full(n, 1 / n)
    for t in range(n_days):
        if t >= MIN_DAYS and t % EVERY == 0:
            cur = capped(fn(R[:t]), CAP)
        W[t] = cur
    return W


def calmar(r):
    c = np.cumprod(1 + r); years = len(r) / 365
    ann = c[-1] ** (1 / years) - 1 if c[-1] > 0 else -1.0
    fall = float(np.max(1 - c / np.maximum.accumulate(np.r_[1.0, c])[1:]))
    return (ann / fall if fall > 0 else np.inf), ann, fall


def sharpe(r):
    return float(np.mean(r) / np.std(r, ddof=1) * np.sqrt(365))


RULES = ["equal capital", "equal risk", "shared risk"]

if __name__ == "__main__":
    TAG = "_earning" if "--earning" in sys.argv else ""
    R = pd.read_csv(HERE / f"p1_returns{TAG}.csv.gz", index_col=["w", "day"], parse_dates=["day"]).fillna(0.0)
    R["fold"] = (R.index.get_level_values("w") - 1) // 6 + 1
    cal = R.reset_index().sort_values("day")                  # calendar order, for the weights
    assert not cal.day.duplicated().any(), "a day in two windows"
    books = [c for c in R.columns if c != "fold"]
    X = cal[books].to_numpy(float)
    port = {}
    for rule in RULES:
        W = weights(X, rule)
        port[rule] = pd.Series((W * X).sum(1), index=pd.MultiIndex.from_frame(cal[["w", "day"]])).sort_index()   # back to the chain
        if rule != "equal capital":
            last = pd.Series(W[-1], index=[b.split("_")[0] for b in books])
            print(f"{rule}: last weights (x equal) min {last.min() * len(books):.2f}, max {last.max() * len(books):.2f}; "
                  f"largest: {(last * len(books)).sort_values().tail(3).round(2).to_dict()}")
    fold = R.fold
    rows = []
    for rule, p in port.items():
        for f in (1, 2, 3, 4, "all"):
            r = p.to_numpy() if f == "all" else p[fold.to_numpy() == f].to_numpy()
            c, a, fall = calmar(r)
            rows.append({"rule": rule, "fold": f, "calmar": c, "yearly_pct": 100 * a, "worst_fall_pct": 100 * fall, "sharpe": sharpe(r)})
    t = pd.DataFrame(rows)
    alone = []
    for b in books:
        for f in (1, 2, 3, 4, "all"):
            r = R[b].to_numpy() if f == "all" else R.loc[fold == f, b].to_numpy()
            alone.append({"book": b, "fold": f, "calmar": calmar(r)[0], "sharpe": sharpe(r) if r.std() > 0 else np.nan})
    a = pd.DataFrame(alone).groupby("fold").agg(calmar=("calmar", "median"), sharpe=("sharpe", "median"))
    pd.set_option("display.width", 200)
    print("\nEach rule, per fold (in sample: no choice made):")
    print(t.pivot(index="rule", columns="fold", values="calmar").round(2).to_string())
    print("Sharpe:"); print(t.pivot(index="rule", columns="fold", values="sharpe").round(2).to_string())
    print("The books alone, median per fold:"); print(a.T.round(2).to_string())
    print("\nOut of fold (rule chosen on the other three folds' chain, judged on this one):")
    oof = []
    for f in (1, 2, 3, 4):
        other = {rule: calmar(p[fold.to_numpy() != f].to_numpy())[0] for rule, p in port.items()}
        pick = max(other, key=other.get)
        held = t[(t.fold == f)].set_index("rule").calmar
        oof.append({"held_out_fold": f, "chosen": pick, "its_calmar_on_the_three": other[pick], "held_out_calmar": held[pick],
                    "equal_capital_held_out": held["equal capital"], "beats_equal": held[pick] > held["equal capital"]})
    o = pd.DataFrame(oof); print(o.round(2).to_string(index=False))
    top = o.chosen.value_counts()
    winner = top.index[0] if top.iloc[0] >= 3 and top.index[0] != "equal capital" and \
        (o[o.chosen == top.index[0]].beats_equal.sum() + 0) >= 3 else "equal capital"
    print(f"\nDecision by the rule written before the run: {winner}")
    t.to_csv(HERE / f"p2_weights{TAG}.csv", index=False, float_format="%.4g"); o.to_csv(HERE / f"p2_out_of_fold{TAG}.csv", index=False, float_format="%.4g")
