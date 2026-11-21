import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = 120
    rows = []
    drift = {}; usual = {}
    for coin, wins in bars.items():
        rr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rr += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rr); usual[coin] = np.std(rr)
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            f = df["forecast"].fillna(0).values.astype(float)
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            hi = pd.Series(c).rolling(720, min_periods=1).max().values
            dist = (hi - c) / c
            r720 = c / pd.Series(c).shift(720).bfill().values - 1
            r24 = c / pd.Series(c).shift(24).bfill().values - 1
            mn = f[0]; seen = set()
            for t in range(n):
                if f[t] - mn >= 2:
                    cell = t // H
                    if cell not in seen:
                        seen.add(cell)
                        rec = dict(coin=coin, win=w, year=ts.iloc[t].year, fc=f[t], dist=dist[t],
                                   r720=r720[t], r24=r24[t], hour=ts.iloc[t].hour)
                        for h in (1, 24, 48, 120, 240):
                            if t + h < n:
                                rec[f"u{h}"] = c[t + h] / c[t] - 1 - drift[coin] * h / H
                        if t >= 24:
                            rec["pre24"] = c[t] / c[t - 24] - 1
                        rec["usual"] = usual[coin]
                        rows.append(rec)
                    mn = f[t]
                mn = min(mn, f[t])
    d = pd.DataFrame(rows)
    d = d.dropna(subset=["u120"])
    def agg(g):
        x = g["u120"]
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "median": x.median()})
    out = {}
    out["all"] = agg(d).to_frame().T
    out["by_horizon"] = pd.DataFrame({h: [d[f"u{h}"].mean(), d[f"u{h}"].mean() / (d[f"u{h}"].std() / np.sqrt(d[f"u{h}"].notna().sum())), d[f"u{h}"].notna().sum()] for h in (1, 24, 48, 120, 240)}, index=["mean", "t", "n"]).T
    out["by_coin"] = d.groupby("coin").apply(agg)
    out["by_year"] = d.groupby("year").apply(agg)
    out["by_fc_q"] = d.groupby(pd.qcut(d["fc"].rank(method="first"), 5, labels=False)).apply(agg)
    out["fc_q_ranges"] = d.groupby(pd.qcut(d["fc"].rank(method="first"), 5, labels=False))["fc"].agg(["min", "max"])
    out["by_dist_q"] = d.groupby(pd.qcut(d["dist"].rank(method="first"), 5, labels=False)).apply(agg)
    out["dist_q_ranges"] = d.groupby(pd.qcut(d["dist"].rank(method="first"), 5, labels=False))["dist"].agg(["min", "max"])
    out["by_r720_q"] = d.groupby(pd.qcut(d["r720"].rank(method="first"), 5, labels=False)).apply(agg)
    out["r720_q_ranges"] = d.groupby(pd.qcut(d["r720"].rank(method="first"), 5, labels=False))["r720"].agg(["min", "max"])
    d["coingroup"] = np.where(d["coin"].isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]), "default", "other")
    out["by_coingroup"] = d.groupby("coingroup").apply(agg)
    out["strength"] = pd.Series({"strength": (d["u120"] / d["usual"]).mean(), "share_pos": (d["u120"] > 0).mean()})
    return out
