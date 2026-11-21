import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        wins = sorted(bars[coin].keys(), key=lambda s: int(s[1:]))
        for k, w in enumerate(wins):
            b = bars[coin][w].reset_index(drop=True)
            c = b["close"].values; n = len(c)
            hi = pd.Series(c).rolling(60, min_periods=60).max().values
            lo = pd.Series(c).rolling(60, min_periods=60).min().values
            for i in range(0, n - 10, 10):
                rows.append(dict(coin=coin, w=w, k=k, r=c[i+10]/c[i]-1,
                    p28=c[i]/c[i-28]-1 if i >= 28 else np.nan,
                    p10=c[i]/c[i-10]-1 if i >= 10 else np.nan,
                    pos60=(c[i]-lo[i])/(hi[i]-lo[i]) if i >= 59 and hi[i] > lo[i] else np.nan,
                    f=b["forecast"].iloc[i],
                    alloc=b["postRebalance_current_allocation"].iloc[i]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby("coin")["r"].transform("mean")
    df["ex"] = df["r"] - df["drift"]
    df["usual"] = df.groupby("coin")["r"].transform("std")
    out = {}
    def reg(d, x):
        d = d.dropna(subset=[x, "ex"])
        z = (d[x] - d[x].mean()) / d[x].std()
        s = stats.linregress(z, d["ex"])
        return pd.Series({"n": len(d), "slope_per_sd": s.slope, "t": s.slope / s.stderr})
    out["reg_all"] = pd.DataFrame({x: reg(df, x) for x in ["p28", "p10", "pos60"]}).T
    df["half"] = np.where(df.k < 12, "early", "late")
    out["reg_p28_by_half"] = pd.DataFrame({h: reg(df[df.half == h], "p28") for h in ["early", "late"]}).T
    out["reg_pos60_by_half"] = pd.DataFrame({h: reg(df[df.half == h], "pos60") for h in ["early", "late"]}).T
    out["reg_p28_by_coin"] = pd.DataFrame({c: reg(df[df.coin == c], "p28") for c in df.coin.unique()}).T
    d = df.dropna(subset=["p28"])
    up = d[d.p28 > 0]
    up = up.assign(q=pd.qcut(up.p28.rank(method="first"), 3, labels=False))
    g = up.groupby("q").agg(n=("ex", "size"), p28=("p28", "mean"), ex=("ex", "mean"), tot=("r", "mean"), usual=("usual", "mean"))
    g["strength"] = g.ex / g.usual
    out["rise_terciles"] = g
    D = pd.concat([dd.assign(coin=c, w=w) for c in days for w, dd in days[c].items()])
    D["k"] = D.w.str[1:].astype(int)
    D = D.sort_values(["k", "day"])
    daily = D.groupby(["k", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean")).dropna()
    eq = (1 + daily.book).cumprod(); dd = eq / eq.cummax() - 1
    ceq = (1 + daily.coin).cumprod(); cdd = ceq / ceq.cummax() - 1
    trough = dd.idxmin(); peak = eq.loc[:trough].idxmax()
    seg = daily.loc[peak:trough]
    out["book_dd"] = pd.Series({"book_maxdd": dd.min(), "coin_maxdd": cdd.min(), "dd_days": len(seg),
        "coin_ret_in_dd": (1 + seg.coin).prod() - 1, "book_ret_in_dd": (1 + seg.book).prod() - 1,
        "window_start": peak[0], "window_end": trough[0]})
    return out
