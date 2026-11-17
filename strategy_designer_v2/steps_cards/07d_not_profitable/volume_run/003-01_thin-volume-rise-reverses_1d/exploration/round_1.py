import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    # book daily returns, coin daily returns
    br = []; cr = []
    for c in days:
        for w in days[c]:
            d = days[c][w]
            br.append(d["book_return"].dropna()); cr.append(d["coin_return"].dropna())
    br = pd.concat(br); cr = pd.concat(cr)
    out["book_daily"] = pd.Series({"mean": br.mean(), "sd": br.std(), "n": len(br), "coin_mean": cr.mean()})
    rows = []
    for c in bars:
        allr = []
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            allr.append(b["close"].pct_change())
        cm = pd.concat(allr).mean()
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True).copy()
            b["r1"] = b["close"].pct_change()
            b["nxt1"] = b["close"].shift(-1) / b["close"] - 1
            b["nxt5"] = b["close"].shift(-5) / b["close"] - 1
            b["vr"] = b["volume"] / b["volume"].rolling(30, min_periods=10).mean()
            b["sd20"] = b["r1"].rolling(20).std()
            b["z"] = b["r1"] / b["sd20"]
            b["ret10"] = b["close"] / b["close"].shift(10) - 1
            b["ret30"] = b["close"] / b["close"].shift(30) - 1
            b["fee"] = b["total_portfolio_value"] - b["postRebalance_total_value"]
            b["fee_frac"] = b["fee"] / b["total_portfolio_value"]
            b["gain"] = b["postRebalance_current_allocation"] * b["nxt1"]
            b["coin"] = c; b["win"] = w; b["cm"] = cm
            b["pos"] = np.arange(len(b))
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    act = B[B["postRebalance_current_allocation"].abs() > 1e-9]
    out["gain_vs_fee"] = pd.Series({"gross_gain_sum_per_bar_all": B["gain"].sum() / len(B),
                                    "fee_per_bar": B["fee_frac"].sum() / len(B),
                                    "active_bars": len(act),
                                    "mean_gain_active": act["gain"].mean(),
                                    "t_gain_active": stats.ttest_1samp(act["gain"].dropna(), 0).statistic,
                                    "mean_alloc_active": act["postRebalance_current_allocation"].mean()})
    out["by_regime_active"] = act.groupby("regime").agg(n=("gain", "size"), gain=("gain", "mean"),
                                                         nxt1=("nxt1", "mean"))
    out["by_coin"] = act.groupby("coin").agg(n=("gain", "size"), gain=("gain", "mean"), nxt1=("nxt1", "mean"))
    out["by_year"] = act.groupby("year").agg(n=("gain", "size"), gain=("gain", "mean"), nxt1=("nxt1", "mean"))
    # non-overlapping 5-day grid: up days by z-bucket and vr bucket
    G = B[(B["pos"] % 5 == 0)].dropna(subset=["nxt5", "z", "vr"]).copy()
    G["ex5"] = G["nxt5"] - G.groupby("coin")["nxt5"].transform("mean")
    up = G[G["z"] > 0].copy()
    up["zb"] = pd.cut(up["z"], [0, 0.5, 1, 1.5, 2, 99])
    up["vb"] = pd.cut(up["vr"], [0, 0.5, 0.75, 1.25, 99])
    t = up.groupby(["vb", "zb"])["ex5"].agg(["mean", "count", lambda s: s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan])
    t.columns = ["mean", "n", "t"]
    out["up_ex5_by_vol_z"] = t
    # trend state for thin rises
    th = up[(up["vr"] <= 0.75) & (up["z"] > 1)].copy()
    th["trend"] = pd.cut(th["ret30"], [-9, -0.1, 0, 0.1, 9])
    out["thin_rise_by_ret30"] = th.groupby("trend")["ex5"].agg(["mean", "count"])
    th["t10"] = pd.cut(th["ret10"], [-9, -0.05, 0, 0.05, 9])
    out["thin_rise_by_ret10"] = th.groupby("t10")["ex5"].agg(["mean", "count"])
    dn = G[G["z"] < -1].copy()
    dn["vb"] = pd.cut(dn["vr"], [0, 0.75, 1.25, 99])
    out["down_ex5_by_vol"] = dn.groupby("vb")["ex5"].agg(["mean", "count"])
    return out
