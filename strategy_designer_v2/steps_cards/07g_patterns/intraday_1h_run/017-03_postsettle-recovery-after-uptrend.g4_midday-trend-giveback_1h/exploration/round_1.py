import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    gross = []; fee = []; daily = []
    for coin, wins in data["bars"].items():
        # coin mean 3-bar return on grid, pooled windows
        g3 = []; h1 = []
        for w, b in wins.items():
            c = b["close"].values
            g3.append(c[3::3][:len(c[0::3])-1] / c[0::3][:len(c[3::3])] - 1)
            h1.append(c[1:]/c[:-1]-1)
        m3 = np.nanmean(np.concatenate(g3)); m1 = np.nanmean(np.concatenate(h1))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r72 = c / c.shift(72) - 1
            sc = r72.abs().rolling(72, min_periods=20).mean().shift(1)
            sig = (-r72 / sc).clip(-2, 2)
            f3 = c.shift(-3) / c - 1 - m3
            f1 = c.shift(-1) / c - 1
            r1 = c / c.shift(1) - 1
            vol = b["volume"]
            relv = vol / vol.rolling(168, min_periods=48).median()
            rv = r1.abs().rolling(24).mean()
            d = pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                              "year": ts.dt.year, "sig": sig, "f3": f3, "f1": f1 - m1, "r1": r1,
                              "relv": relv, "r24": c / c.shift(24) - 1, "rvq": rv})
            rows.append(d)
            a = b["postRebalance_current_allocation"]
            gross.append((a * f1).sum())
            fee.append((b["total_portfolio_value"] - b["postRebalance_total_value"]).clip(lower=0).sum() / b["total_portfolio_value"].mean())
    D = pd.concat(rows, ignore_index=True)
    out["book gross sum alloc*ret vs fee share"] = pd.Series({"gross_sum": np.nansum(gross), "fee_sum": np.nansum(fee)})
    # per-hour slope t of 3h excess fwd on sig (one case per day per hour)
    res = []
    for h, g in D.dropna(subset=["sig", "f3"]).groupby("hour"):
        s = stats.linregress(g["sig"], g["f3"])
        res.append({"hour": h, "n": len(g), "slope_bp": s.slope * 1e4, "t": s.slope / s.stderr,
                    "mean_f1_bp": g["f1"].mean() * 1e4, "t_f1": g["f1"].mean() / g["f1"].std() * np.sqrt(len(g)),
                    "relv": g["relv"].median()})
    out["by hour: 3h reversal slope, 1h mean excess, rel volume"] = pd.DataFrame(res).round(3)
    # 1h reversal after large moves: f1 on r1 by hour (one per day per hour)
    res = []
    for h, g in D.dropna(subset=["r1", "f1"]).groupby("hour"):
        s = stats.linregress(g["r1"], g["f1"])
        res.append({"hour": h, "slope": s.slope, "t": s.slope / s.stderr})
    out["by hour: next-1h on last-1h slope"] = pd.DataFrame(res).round(3)
    res = []
    for wd, g in D.dropna(subset=["f1"]).groupby("wd"):
        res.append({"wd": wd, "n": len(g), "mean_bp": g["f1"].mean() * 1e4, "t": g["f1"].mean() / g["f1"].std() * np.sqrt(len(g))})
    out["weekday mean 1h excess"] = pd.DataFrame(res).round(3)
    # 3h reversal slope by coin and by year for hours 10-12
    G = D[D.hour.isin([10])].dropna(subset=["sig", "f3"])
    res = []
    for k, g in G.groupby("coin"):
        s = stats.linregress(g["sig"], g["f3"]); res.append({"coin": k, "n": len(g), "t": s.slope / s.stderr})
    for k, g in G.groupby("year"):
        s = stats.linregress(g["sig"], g["f3"]); res.append({"coin": str(k), "n": len(g), "t": s.slope / s.stderr})
    out["10h reversal t by coin/year"] = pd.DataFrame(res).round(3)
    return out
