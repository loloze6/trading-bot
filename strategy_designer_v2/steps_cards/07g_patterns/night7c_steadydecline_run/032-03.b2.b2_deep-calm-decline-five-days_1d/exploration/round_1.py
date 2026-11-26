import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["fwd"] = c.shift(-H) / c - 1
            b["r1"] = c.pct_change()
            b["r5p"] = c / c.shift(5) - 1
            b["r28"] = c / c.shift(28) - 1
            b["vol20"] = b["r1"].rolling(20).std()
            b["rng"] = (b["high"] - b["low"]) / c
            b["rngratio"] = b["rng"].rolling(28).mean() / b["rng"].rolling(90).mean()
            b["vratio28"] = b["volume"].rolling(28).mean() / b["volume"].rolling(90).mean()
            b["vspike"] = b["volume"] / b["volume"].rolling(20).mean()
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * (c.shift(-1) / c - 1)
            b["coin"] = coin; b["w"] = w
            g = b.iloc[::H]
            rows.append(g)
    d = pd.concat(rows, ignore_index=True)
    d = d.dropna(subset=["fwd"])
    drift = d.groupby("coin")["fwd"].mean()
    usual = d.groupby("coin")["fwd"].std()
    d["un"] = d["fwd"] - d["coin"].map(drift)
    d["z"] = d["un"] / d["coin"].map(usual)
    out = {}
    def summ(gcol, df):
        s = df.groupby(gcol, observed=True)["z"].agg(["mean", "count", "std"])
        s["t"] = s["mean"] / (s["std"] / np.sqrt(s["count"]))
        s["un_mean%"] = df.groupby(gcol, observed=True)["un"].mean() * 100
        return s.round(3)
    d["trend"] = d["regime"] == "trending"
    d["q28"] = d.groupby("coin")["r28"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["z by r28 quintile x lowvol regime"] = summ(["trend", "q28"], d.dropna(subset=["q28"]))
    d["q5p"] = d.groupby("coin")["r5p"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["z by past 5d return quintile"] = summ("q5p", d.dropna(subset=["q5p"]))
    d["qvol"] = d.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["z by vol20 quintile"] = summ("qvol", d.dropna(subset=["qvol"]))
    d["qvs"] = d.groupby("coin")["vspike"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["z by volume spike quintile"] = summ("qvs", d.dropna(subset=["qvs"]))
    d["qvr"] = d.groupby("coin")["vratio28"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["z by vratio28 quintile"] = summ("qvr", d.dropna(subset=["qvr"]))
    d["qr1"] = d.groupby("coin")["r1"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["z by last day return quintile"] = summ("qr1", d.dropna(subset=["qr1"]))
    out["z by weekday"] = summ("wd", d)
    out["z by coin"] = summ("coin", d)
    out["z by window"] = summ("w", d)
    # correlations
    cr = {}
    for col in ["r28", "r5p", "r1", "vol20", "vspike", "vratio28", "rngratio"]:
        x = d[[col, "z"]].dropna()
        r, p = stats.pearsonr(x[col], x["z"])
        cr[col] = (round(r, 4), round(r * np.sqrt((len(x) - 2) / (1 - r * r)), 2), len(x))
    out["corr with fwd z (r, t, n)"] = pd.DataFrame(cr, index=["r", "t", "n"]).T
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)], ignore_index=True)
    if len(tr):
        tr["fq"] = pd.qcut(tr["entry_forecast"].abs(), 4, labels=False, duplicates="drop")
        out["trades by |entry forecast| quartile"] = tr.groupby("fq")["net_profit_loss_percent"].agg(["mean", "median", "count"]).round(3)
        out["trades by side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
