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
            s = pd.Series(c)
            hi = s.rolling(720, min_periods=1).max().values
            dist = (hi - c) / c
            r720 = (s / s.shift(720) - 1).values
            r2160 = (s / s.shift(2160) - 1).values
            ma2160 = s.rolling(2160, min_periods=2160).mean().values
            mn = f[0]; seen = set()
            for t in range(n):
                if f[t] - mn >= 2:
                    cell = t // H
                    if cell not in seen:
                        seen.add(cell)
                        rec = dict(coin=coin, win=w, year=ts.iloc[t].year, fc=f[t], dist=dist[t],
                                   r720=r720[t], r2160=r2160[t], abovema=(c[t] > ma2160[t]) if not np.isnan(ma2160[t]) else np.nan)
                        for h in (120, 240):
                            if t + h < n:
                                rec[f"u{h}"] = c[t + h] / c[t] - 1 - drift[coin] * h / H
                        rec["usual"] = usual[coin]
                        rows.append(rec)
                    mn = f[t]
                mn = min(mn, f[t])
    d = pd.DataFrame(rows).dropna(subset=["u120"])
    def agg(g, col="u120"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "share_pos": (x > 0).mean()})
    out = {}
    d["r720_pos"] = d["r720"] > 0
    out["year_x_r720pos"] = d.dropna(subset=["r720"]).groupby(["year", "r720_pos"]).apply(agg)
    out["r720pos"] = d.dropna(subset=["r720"]).groupby("r720_pos").apply(agg)
    out["r720pos_240"] = d.dropna(subset=["r720"]).groupby("r720_pos").apply(lambda g: agg(g, "u240"))
    dd = d.dropna(subset=["r720"])
    dd["r720_q"] = pd.qcut(dd["r720"].rank(method="first"), 10, labels=False)
    out["r720_dec"] = dd.groupby("r720_q").apply(agg)
    out["r720_dec_rng"] = dd.groupby("r720_q")["r720"].agg(["min", "max"])
    pos = dd[dd["r720"] > 0].copy()
    pos["fc_hi"] = pos["fc"] >= pos["fc"].median()
    out["pos_by_fc_half"] = pos.groupby("fc_hi").apply(agg)
    pos["r_q"] = pd.qcut(pos["r720"].rank(method="first"), 4, labels=False)
    out["pos_by_r720_q"] = pos.groupby("r_q").apply(agg)
    out["pos_by_year"] = pos.groupby("year").apply(agg)
    out["pos_by_coin_sign"] = pd.Series({"coins_pos": (pos.groupby("coin")["u120"].mean() > 0).sum(), "coins": pos["coin"].nunique()})
    out["pos_strength"] = pd.Series({"strength": (pos["u120"] / pos["usual"]).mean(), "mean": pos["u120"].mean()})
    e = d.dropna(subset=["r2160"])
    e["r2160_pos"] = e["r2160"] > 0
    out["r2160pos"] = e.groupby("r2160_pos").apply(agg)
    out["abovema"] = d.dropna(subset=["abovema"]).groupby("abovema").apply(agg)
    return out
