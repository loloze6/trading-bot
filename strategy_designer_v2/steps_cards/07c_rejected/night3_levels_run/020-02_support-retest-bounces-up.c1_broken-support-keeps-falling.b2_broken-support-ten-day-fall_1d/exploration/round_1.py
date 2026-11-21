import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.support_above.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            r10back = np.full(n, np.nan)
            r10back[10:] = c[10:] / c[:-10] - 1
            for h in [1, 3, 5, 10, 20]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, yr=yr[i], h=h, f=f[i], raw=raw[i],
                                     ret=c[i + h] / c[i] - 1, past10=r10back[i]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["drift"]
    out = {}
    act = R[R.f < 0]
    inact = R[R.f >= 0]

    def summ(g):
        return pd.Series({"n": len(g), "mean_ex_pct": 100 * g.ex.mean(),
                          "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "mean_ret_pct": 100 * g.ret.mean()})

    out["by_h_active"] = act.groupby("h").apply(summ)
    out["by_h_inactive"] = inact.groupby("h").apply(summ)
    a10 = act[act.h == 10].copy()
    out["coin_h10"] = a10.groupby("coin").apply(summ)
    out["year_h10"] = a10.groupby("yr").apply(summ)
    a10["fq"] = pd.qcut(a10.f.abs().rank(method="first"), 4, labels=["q1small", "q2", "q3", "q4large"])
    out["fsize_h10"] = a10.groupby("fq").apply(summ)
    a10["pq"] = pd.qcut(a10.past10.rank(method="first"), 4, labels=["p1fell", "p2", "p3", "p4rose"])
    out["past10_h10_active"] = a10.groupby("pq").apply(summ)
    i10 = inact[inact.h == 10].copy().dropna(subset=["past10"])
    i10["pq"] = pd.qcut(i10.past10.rank(method="first"), 4, labels=["p1fell", "p2", "p3", "p4rose"])
    out["past10_h10_inactive"] = i10.groupby("pq").apply(summ)
    a5 = act[act.h == 5].copy()
    a5["fq"] = pd.qcut(a5.f.abs().rank(method="first"), 4, labels=["q1small", "q2", "q3", "q4large"])
    out["fsize_h5"] = a5.groupby("fq").apply(summ)
    a20 = act[act.h == 20].copy()
    a20["fq"] = pd.qcut(a20.f.abs().rank(method="first"), 4, labels=["q1small", "q2", "q3", "q4large"])
    out["fsize_h20"] = a20.groupby("fq").apply(summ)
    out["share_active_h10"] = len(a10) / len(R[R.h == 10])
    return out
