def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        # m_h: mean non-overlapping h-bar return over all windows
        mh = {}
        for h in (1, 2, 3, 5):
            vals = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals.extend(c[idx + h] / c[idx] - 1)
            mh[h] = np.nanmean(vals)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            ret1 = pd.Series(c).pct_change().values
            sd20 = pd.Series(ret1).rolling(20).std().values
            vol = df["volume"].values
            volrel = vol / pd.Series(vol).rolling(28).mean().values
            for i in range(len(df)):
                if ts.iloc[i].dayofweek != 6 or df["forecast"].iloc[i] == 0:
                    continue
                r = {"coin": coin, "win": w, "year": ts.iloc[i].year,
                     "f": df["forecast"].iloc[i], "wk": ret1[i] / sd20[i] if sd20[i] else np.nan,
                     "volrel": volrel[i]}
                for h in (1, 2, 3, 5):
                    r[f"x{h}"] = (c[i + h] / c[i] - 1 - mh[h]) if i + h < len(c) else np.nan
                r["tue"] = (c[i + 2] / c[i + 1] - 1 - mh[1]) if i + 2 < len(c) else np.nan
                rows.append(r)
    d = pd.DataFrame(rows).dropna(subset=["x2"])
    d["s"] = -np.sign(d["wk"])
    out = {}
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x))})
    d["main"] = d["f"] / 10 * d["x2"]
    out["main_check"] = tt(d["main"])
    for h in ("x1", "tue", "x2", "x3", "x5"):
        d["sx_" + h] = d["s"] * d[h]
    out["signed_by_horizon"] = pd.DataFrame({h: tt(d["sx_" + h]) for h in ("x1", "tue", "x2", "x3", "x5")}).T
    out["by_side_x2"] = d.groupby(np.where(d["wk"] > 0, "after_rise", "after_fall"))["x2"].apply(lambda x: tt(x)).unstack()
    d["q"] = pd.qcut(d["wk"], 5, labels=False)
    out["x2_by_wk_quintile"] = d.groupby("q").agg(n=("x2", "size"), wk=("wk", "mean"), f=("f", "mean"), x1=("x1", "mean"), x2=("x2", "mean"), x3=("x3", "mean"))
    d["aq"] = pd.qcut(d["f"].abs(), 4, labels=False)
    out["signed_x2_by_absf_quartile"] = d.groupby("aq").agg(absf=("f", lambda x: x.abs().mean()), sx2=("sx_x2", "mean"), main=("main", "mean"), n=("x2", "size"))
    out["by_coin"] = d.groupby("coin")["main"].apply(tt).unstack()
    out["by_year"] = d.groupby("year")["main"].apply(tt).unstack()
    d["vq"] = pd.qcut(d["volrel"], 3, labels=False)
    out["by_volrel_tercile"] = d.groupby("vq").agg(n=("x2", "size"), sx2=("sx_x2", "mean"), main=("main", "mean"))
    out["corr_wk_f"] = d[["wk", "f"]].corr().iloc[0, 1]
    return out
