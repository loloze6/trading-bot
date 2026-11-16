def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean daily return over all windows
        rets = []
        for w, b in wins.items():
            r = b["close"].shift(-1) / b["close"] - 1
            rets.append(r)
        cmean = pd.concat(rets).mean()
        for w, b in wins.items():
            b = b.copy()
            b["fwd"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gross"] = b["pos"] * b["fwd"]
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["fee"] = fee
            b["mkt"] = b["pos"] * cmean
            b["timing"] = b["pos"] * (b["fwd"] - cmean)
            b["vsr"] = b["debug_info.components.vsr.last_history_value"]
            b["fc"] = b["forecast"]
            sma50 = b["close"].rolling(50, min_periods=20).mean()
            b["trend"] = np.where(b["close"] > sma50, "above50", "below50")
            r20 = b["close"] / b["close"].shift(20) - 1
            b["r20sign"] = np.where(r20 > 0, "up20", "down20")
            b["coin"] = coin; b["win"] = w
            b["absvsr_q"] = None
            rows.append(b[["coin", "win", "fwd", "pos", "gross", "fee", "mkt", "timing", "vsr", "fc", "trend", "r20sign", "close"]])
    d = pd.concat(rows).dropna(subset=["fwd", "pos"])
    d["side"] = np.where(d["pos"] > 0, "long", np.where(d["pos"] < 0, "short", "flat"))
    out = {}
    out["totals"] = pd.Series({"gross_mean": d.gross.mean(), "fee_mean": d.fee.mean(), "mkt_mean": d.mkt.mean(),
                               "timing_mean": d.timing.mean(), "mean_pos": d.pos.mean(), "mean_abs_pos": d.pos.abs().mean(),
                               "turnover_mean": d.groupby(["coin", "win"]).pos.diff().abs().mean()})
    g = d.groupby("side").agg(n=("gross", "size"), gross=("gross", "mean"), timing=("timing", "mean"), mkt=("mkt", "mean"), fwd=("fwd", "mean"), fee=("fee", "mean"))
    out["by_side"] = g
    d["vq"] = pd.qcut(d["vsr"], 10, labels=False, duplicates="drop")
    out["by_vsr_decile"] = d.groupby("vq").agg(n=("fwd", "size"), vsr=("vsr", "mean"), fwd=("fwd", "mean"), pos=("pos", "mean"), gross=("gross", "mean"), fee=("fee", "mean"))
    out["by_trend_side"] = d.groupby(["trend", "side"]).agg(n=("fwd", "size"), fwd=("fwd", "mean"), gross=("gross", "mean"), timing=("timing", "mean"))
    out["by_coin"] = d.groupby("coin").agg(gross=("gross", "mean"), fee=("fee", "mean"), timing=("timing", "mean"), mkt=("mkt", "mean"))
    # slope of fwd on vsr by trend
    res = {}
    for k, s in d.dropna(subset=["vsr"]).groupby("trend"):
        x = s["vsr"]; y = s["fwd"]
        sl, ic, rr, p, se = __import__("scipy").stats.linregress(x, y)
        res[k] = {"n": len(s), "slope": sl, "t": sl / se}
    out["vsr_slope_by_trend"] = pd.DataFrame(res).T
    return out
