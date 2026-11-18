import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = [f"w{i}" for i in range(1, 25)]
    # book daily returns: mean across coins per day, per window
    rows = []
    for w in wins:
        dfs = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                dfs.append(d)
        d = pd.concat(dfs)
        g = d.groupby("day")[["book_return", "coin_return"]].mean().reset_index()
        g["w"] = w
        rows.append(g)
    B = pd.concat(rows).dropna().reset_index(drop=True)
    eq = (1 + B.book_return).cumprod()
    peak = eq.cummax()
    dd = eq / peak - 1
    B["dd"] = dd.values
    B["eq"] = eq.values
    out["deepest dd"] = float(dd.min())
    out["years"] = float(len(B) / 365)
    out["yearly ret"] = float(eq.iloc[-1] ** (365 / len(B)) - 1)
    # drawdown episodes
    ep = []
    i = 0
    n = len(B)
    in_dd = False
    for k in range(n):
        if dd.iloc[k] < 0 and not in_dd:
            start = k; in_dd = True
        if in_dd and (dd.iloc[k] == 0 or k == n - 1):
            seg = B.iloc[start:k + 1]
            tr = seg.dd.idxmin()
            ep.append({"start_w": B.w.iloc[start], "trough_w": B.w.loc[tr],
                       "depth": seg.dd.min(), "days_to_trough": tr - start + 1,
                       "len": k - start + 1,
                       "book_sum_to_trough": B.book_return.iloc[start:tr + 1].sum(),
                       "coin_sum_to_trough": B.coin_return.iloc[start:tr + 1].sum()})
            in_dd = False
    E = pd.DataFrame(ep).sort_values("depth").head(8)
    out["top dd episodes"] = E
    # per window book stats
    W = B.groupby("w").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
                           min_dd=("dd", "min"), n=("book_return", "size"))
    W["book_sum"] = B.groupby("w").book_return.sum()
    W["coin_sum"] = B.groupby("w").coin_return.sum()
    out["per window"] = W.reindex(wins)
    # bar-level: next-day return after falls, conditioned on 20d trend and vol
    R = []
    for c in coins:
        for w in wins:
            if w not in bars[c]: continue
            b = bars[c][w]
            cl = b.close
            r1 = cl.pct_change()
            fwd = cl.shift(-1) / cl - 1
            ret20 = cl / cl.shift(20) - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60, min_periods=20).std()
            f = b.forecast
            alloc = b.postRebalance_current_allocation
            R.append(pd.DataFrame({"coin": c, "w": w, "f": f, "fwd": fwd, "r1": r1,
                                   "ret20": ret20, "volratio": vol20 / vol60,
                                   "alloc": alloc, "gain": alloc * fwd}))
    R = pd.concat(R).dropna()
    cm = R.groupby("coin").fwd.mean()
    R["ex"] = R.fwd - R.coin.map(cm)
    A = R[R.f > 0].copy()
    A["trend_q"] = pd.qcut(A.ret20, 5, labels=False)
    A["vol_q"] = pd.qcut(A.volratio, 5, labels=False)
    A["f_q"] = pd.qcut(A.f, 4, labels=False)
    def summ(g):
        return pd.Series({"n": len(g), "ex_mean": g.ex.mean(),
                          "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))),
                          "gain_mean": g.gain.mean(), "gain_sd": g.gain.std(),
                          "worst5pct_gain": g.gain.quantile(0.05), "alloc": g.alloc.mean()})
    out["by 20d trend quintile"] = A.groupby("trend_q").apply(summ)
    out["by volratio quintile"] = A.groupby("vol_q").apply(summ)
    out["by forecast quartile"] = A.groupby("f_q").apply(summ)
    out["trend x f (ex mean)"] = A.groupby(["trend_q", "f_q"]).ex.mean().unstack()
    return out
