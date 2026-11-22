import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); v = b["volume"].astype(float)
            ret1 = c.pct_change()
            ph = hi.shift(1).rolling(20).max()
            brk = c > ph
            vr = v / v.rolling(20).mean()
            # most recent breakout within last 4 bars (not today) and today back below its high
            fail = pd.Series(False, index=b.index); fvr = pd.Series(np.nan, index=b.index)
            fdepth = pd.Series(np.nan, index=b.index); ext = pd.Series(np.nan, index=b.index)
            for k in range(1, 5):
                bk = brk.shift(k).fillna(False).astype(bool)
                lvl = ph.shift(k)
                cond = bk & (c < lvl) & ~fail
                fail |= cond
                fvr[cond] = vr.shift(k)[cond]
                fdepth[cond] = (lvl[cond] - c[cond]) / lvl[cond]
                ext[cond] = (hi.rolling(k).max().shift(0)[cond] / lvl[cond] - 1)
            fwd = c.shift(-H) / c - 1
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            vol20 = ret1.rolling(20).std()
            dist = c / hi.rolling(20).max() - 1
            idx = np.arange(0, len(b), H)
            g = pd.DataFrame({"coin": coin, "w": w, "fwd": fwd.iloc[idx].values,
                              "fail": fail.iloc[idx].values, "fvr": fvr.iloc[idx].values,
                              "fdepth": fdepth.iloc[idx].values, "ext": ext.iloc[idx].values,
                              "brk": brk.iloc[idx].values, "r5": r5.iloc[idx].values,
                              "r20": r20.iloc[idx].values, "vol20": vol20.iloc[idx].values,
                              "dist": dist.iloc[idx].values, "vr": vr.iloc[idx].values,
                              "dow": pd.to_datetime(b["timestamp"]).dt.dayofweek.iloc[idx].values})
            rows.append(g)
            d = pd.DataFrame({"coin": coin, "r": ret1, "dow": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                              "prev": ret1.shift(1), "alloc": b["postRebalance_current_allocation"]})
            daily.append(d)
    G = pd.concat(rows).dropna(subset=["fwd"])
    drift = G.groupby("coin")["fwd"].mean()
    sd = G.groupby("coin")["fwd"].std()
    G["u"] = G["fwd"] - G["coin"].map(drift)
    G["z"] = G["u"] / G["coin"].map(sd)
    def summ(df, by):
        x = df.groupby(by, observed=True)["u"].agg(["count", "mean", "std"])
        x["t"] = x["mean"] / (x["std"] / np.sqrt(x["count"]))
        x["z_mean"] = df.groupby(by, observed=True)["z"].mean()
        return x.drop(columns="std")
    out = {}
    out["all_fail_vs_not"] = summ(G, "fail")
    F = G[G.fail].copy()
    F["vr_q"] = pd.qcut(F["fvr"], 3, labels=["thin", "mid", "heavy"])
    out["fail_by_breakout_volume"] = summ(F, "vr_q")
    F["depth_q"] = pd.qcut(F["fdepth"], 3, labels=["shallow", "mid", "deep"])
    out["fail_by_depth"] = summ(F, "depth_q")
    F["ext_q"] = pd.qcut(F["ext"], 3, labels=["small", "mid", "large"], duplicates="drop")
    out["fail_by_extension"] = summ(F, "ext_q")
    out["breakout_today"] = summ(G, "brk")
    for col in ["r5", "r20", "vol20", "dist", "vr"]:
        Gc = G.dropna(subset=[col]).copy()
        Gc["q"] = Gc.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out[f"by_{col}_quintile"] = summ(Gc, "q")
    out["by_coin_fail"] = summ(F, "coin")
    D = pd.concat(daily).dropna(subset=["r"])
    out["daily_by_dow"] = D.groupby("dow")["r"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    D["pq"] = pd.qcut(D["prev"], 5, labels=False)
    out["daily_after_prev_quintile"] = D.groupby("pq")["r"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    out["share_bars_short"] = float((D["alloc"] < 0).mean())
    return out
