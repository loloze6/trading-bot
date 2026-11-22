import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted({w for c in coins for w in days[c].keys()}, key=lambda s: int(s[1:]))
    # book daily returns
    rows = []
    for w in wins:
        br = []; cr = []
        for c in coins:
            if w in days[c]:
                d = days[c][w].set_index("day")
                br.append(d["book_return"].rename(c)); cr.append(d["coin_return"].rename(c))
        B = pd.concat(br, axis=1).mean(axis=1); C = pd.concat(cr, axis=1).mean(axis=1)
        df = pd.DataFrame({"b": B, "h": C}).dropna(); df["w"] = w
        rows.append(df.reset_index(drop=True))
    D = pd.concat(rows, ignore_index=True)
    eq = (1 + D["b"]).cumprod(); dd = eq / eq.cummax() - 1
    D["dd"] = dd
    heq = (1 + D["h"]).cumprod(); hdd = heq / heq.cummax() - 1
    yrs = len(D) / 365
    out["summary"] = pd.Series({"book_yearly": eq.iloc[-1] ** (1 / yrs) - 1, "book_maxdd": dd.min(),
                                "hold_yearly": heq.iloc[-1] ** (1 / yrs) - 1, "hold_maxdd": hdd.min(),
                                "days": len(D)})
    # per window
    g = D.groupby("w", sort=False)
    pw = pd.DataFrame({"book_sum": g["b"].sum(), "hold_sum": g["h"].sum(),
                       "book_min_dd_in_chain": g["dd"].min()})
    out["per_window"] = pw
    # bar level: position gain, conditions
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r1 = cl.shift(-1) / cl - 1
            a = b["postRebalance_current_allocation"]
            r30 = cl / cl.shift(180) - 1
            r7 = cl / cl.shift(42) - 1
            r1d = cl / cl.shift(6) - 1
            lr = np.log(cl).diff()
            vol = lr.rolling(42).std() / lr.rolling(360, min_periods=180).std()
            fwd = cl.shift(-84) / cl - 1
            recs.append(pd.DataFrame({"c": c, "w": w, "a": a, "g": a * r1, "r1": r1, "r30": r30, "r7": r7,
                                      "r1d": r1d, "vol": vol, "f": b["forecast"], "fwd": fwd, "i": np.arange(len(b))}))
    R = pd.concat(recs, ignore_index=True)
    out["alloc_stats"] = pd.Series({"share_bars_long": (R["a"] > 0).mean(), "mean_alloc_when_long": R.loc[R.a > 0, "a"].mean(),
                                    "share_bars_forecast_pos": (R["f"] > 0).mean()})
    L = R[R.a > 0].dropna(subset=["r30", "g"]).copy()
    L["r30q"] = pd.qcut(L["r30"], 5, labels=False)
    out["gain_by_prior30d_quintile"] = L.groupby("r30q").agg(r30_mean=("r30", "mean"), bars=("g", "size"),
                                                             gain_mean_bp=("g", lambda x: x.mean() * 1e4),
                                                             gain_sum=("g", "sum"), r1_mean_bp=("r1", lambda x: x.mean()*1e4))
    L2 = L.dropna(subset=["vol"]).copy(); L2["vq"] = pd.qcut(L2["vol"], 5, labels=False)
    out["gain_by_vol_ratio_quintile"] = L2.groupby("vq").agg(vol_mean=("vol", "mean"), bars=("g", "size"),
                                                             gain_mean_bp=("g", lambda x: x.mean()*1e4), gain_sum=("g", "sum"))
    # signal cases on grid: fwd excess by prior 30d trend
    G = R[(R.i % 84 == 0)].dropna(subset=["fwd", "r30"]).copy()
    drift = G.groupby("c")["fwd"].mean(); G["ex"] = G["fwd"] - G["c"].map(drift)
    S = G[G.f > 0].copy(); S["r30q"] = pd.qcut(S["r30"], 4, labels=False)
    out["cases_excess_by_prior30d"] = S.groupby("r30q").agg(r30=("r30", "mean"), n=("ex", "size"), ex_mean=("ex", "mean"),
                                                            ex_t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))),
                                                            fwd_min=("fwd", "min"))
    S2 = S.dropna(subset=["vol"]).copy(); S2["vq"] = pd.qcut(S2["vol"], 4, labels=False)
    out["cases_excess_by_volratio"] = S2.groupby("vq").agg(vol=("vol", "mean"), n=("ex", "size"), ex_mean=("ex", "mean"),
                                                           ex_t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    # worst drawdown windows: what was held
    worst = pw.sort_values("book_sum").head(5).index.tolist()
    W = R[R.w.isin(worst)]
    out["worst5_windows_held"] = W.groupby("w").agg(share_long=("a", lambda x: (x > 0).mean()), mean_alloc=("a", "mean"),
                                                   gain_sum_per_coin=("g", lambda x: x.sum()/6),
                                                   mean_r30_when_long=("r30", lambda x: x[W.loc[x.index, "a"] > 0].mean()))
    return out
