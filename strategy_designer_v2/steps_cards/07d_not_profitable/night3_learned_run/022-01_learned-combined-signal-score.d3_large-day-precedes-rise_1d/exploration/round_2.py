def explore(data):
    import numpy as np, pandas as pd
    out = {}
    B = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            alloc = b["postRebalance_current_allocation"]
            prev = b["previous_allocation"]
            # side of the day that opened/raised the current position: last bar where allocation increased
            inc = (alloc - prev) > 1e-6
            side_at_inc = pd.Series(np.where(inc, np.where(r1 > 0, "up", "down"), None)).ffill()
            df = pd.DataFrame({"coin": c, "window": w, "r1": r1, "alloc": alloc,
                "next1": cl.shift(-1)/cl-1, "tr20": cl/cl.shift(20)-1, "tr60": cl/cl.shift(60)-1,
                "entry_side": side_at_inc})
            df["gain"] = df["alloc"]*df["next1"]
            df["winnum"] = int(w[1:])
            B.append(df)
    B = pd.concat(B, ignore_index=True).dropna(subset=["gain","tr20"])
    B["trend"] = np.where(B.tr20 > 0, "tr20+", "tr20-")
    B["fall"] = np.where(B.winnum.between(12,14), "w12-14", "other")
    out["gain_by_fall_entryside_trend"] = B.groupby(["fall","entry_side","trend"]).agg(
        n=("gain","size"), mean_alloc=("alloc","mean"), mean_gain=("gain","mean"), sum_gain=("gain","sum"))
    # per-window sum of gain, split by entry side
    pw = B.groupby(["winnum","entry_side"])["gain"].sum().unstack()
    out["window_gain_by_entryside"] = pw
    # 60-day trend split
    B["trend60"] = np.where(B.tr60 > 0, "tr60+", "tr60-")
    H = B.dropna(subset=["tr60"])
    out["gain_by_trend60_side"] = H.groupby(["trend60","entry_side"]).agg(n=("gain","size"),
        mean_gain=("gain","mean"), sum_gain=("gain","sum"), sd=("gain","std"))
    # worst-window drawdown proxy: chained gain per entry side
    def mdd(g):
        eq = (1+g).cumprod(); return (eq/eq.cummax()-1).min()
    res = {}
    for s in ["up","down"]:
        g = B.assign(g2=np.where(B.entry_side==s, B.gain, 0.0)).groupby(["winnum"]).apply(
            lambda x: x.groupby(x.index)["g2"].sum()) if False else None
    out["share_alloc_down_entry"] = pd.Series({
        "share_bars_down_entry": (B.entry_side=="down").mean(),
        "gain_down_entry_tr20-": B[(B.entry_side=="down")&(B.trend=="tr20-")].gain.sum(),
        "gain_up_entry_tr20+": B[(B.entry_side=="up")&(B.trend=="tr20+")].gain.sum()})
    return out
