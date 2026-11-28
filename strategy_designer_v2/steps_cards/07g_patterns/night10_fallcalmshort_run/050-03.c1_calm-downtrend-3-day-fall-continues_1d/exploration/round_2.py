import pandas as pd, numpy as np
from scipy import stats

def tstat(x):
    x = pd.Series(x).dropna()
    return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            b["s3"] = (c / c.shift(3) - 1) / sd30
            b["s5"] = (c / c.shift(5) - 1) / sd30
            b["s3z"] = (b["s3"] - b["s3"].rolling(60, min_periods=20).mean()) / b["s3"].rolling(60, min_periods=20).std()
            b["r60"] = c / c.shift(60) - 1
            for h in (3, 5):
                b[f"f{h}"] = c.shift(-h) / c - 1
                b[f"fs{h}"] = b[f"f{h}"] / (sd30 * np.sqrt(h))
            b["pos"] = np.arange(len(b))
            b["inprof"] = (b["regime"] == "unknown")
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["coin"] = coin; b["win"] = w
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    out = {}
    for h in (3, 5):
        drift = B[B.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        G = B[(B.pos % h == 0) & B.inprof].copy()
        G["u"] = G[f"f{h}"] - G["coin"].map(drift)
        G = G.dropna(subset=["u", "s3", "s3z"])
        # short direction unusual move for falls, graded
        F = G[G.s3 < 0].copy()
        F["us"] = -F["u"]
        d = F.groupby("day")["us"].sum()
        out[f"h{h}_falls_short_u"] = pd.Series({"n": len(F), "days": len(d), "mean": F.us.mean(),
            "t_day": d.mean() / (d.std() / np.sqrt(len(d))) * 1.0})
        F["half"] = np.where(F.s3 <= F.s3.median(), "large_fall", "small_fall")
        out[f"h{h}_falls_by_half"] = F.groupby("half")["us"].agg(["size", "mean", tstat])
        rho = stats.spearmanr(-F.s3, F.us)
        out[f"h{h}_falls_spearman_size_vs_us"] = pd.Series({"rho": rho.correlation, "p": rho.pvalue})
        # standardised version (like the forecast) vs raw
        for col in ["s3", "s3z"]:
            rho = stats.spearmanr(G[col], G["u"])
            out[f"h{h}_all_spearman_{col}"] = pd.Series({"n": len(G), "rho": rho.correlation, "p": rho.pvalue})
        F["szq"] = pd.qcut(F.s3z, 3, labels=["z_low", "z_mid", "z_high"])
        out[f"h{h}_falls_by_s3z_tercile"] = F.groupby("szq")["us"].agg(["size", "mean", tstat])
        out[f"h{h}_falls_by_coin"] = F.groupby("coin")["us"].agg(["size", "mean", tstat])
        out[f"h{h}_falls_by_year"] = F.groupby("year")["us"].agg(["size", "mean"])
        # depth of 60-day trend
        F["r60q"] = pd.qcut(F.r60, 3, labels=["deep", "mid", "shallow"])
        out[f"h{h}_falls_by_trend_depth"] = F.groupby("r60q")["us"].agg(["size", "mean", tstat])
        # rises in profile (for comparison)
        R = G[G.s3 > 0]
        out[f"h{h}_rises_long_u"] = pd.Series({"n": len(R), "mean": R.u.mean(), "t": tstat(R.u)})
    # book days: largest gain/loss days context
    D = pd.concat([d.assign(coin=c) for c, ws in data["days"].items() for d in ws.values()], ignore_index=True)
    out["book_ret_days_nonzero"] = D[D.book_return.abs() > 1e-9]["book_return"].describe()
    return out
