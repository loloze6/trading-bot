def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coin = list(data["bars"].keys())[0]
    wins = sorted(data["bars"][coin].keys(), key=lambda w: int(w[1:]))
    rows = []
    for w in wins:
        b = data["bars"][coin][w].copy().reset_index(drop=True)
        b["w"] = w
        b["year"] = pd.to_datetime(b["timestamp"]).dt.year
        b["r"] = b["close"].pct_change()
        b["rnext"] = b["close"].shift(-1) / b["close"] - 1
        b["vol30"] = b["r"].rolling(30, min_periods=20).std()
        b["z"] = b["r"] / b["vol30"]
        b["ret20"] = b["close"] / b["close"].shift(20) - 1
        b["ret60"] = b["close"] / b["close"].shift(60) - 1
        b["pos"] = b["postRebalance_current_allocation"]
        b["gain"] = b["pos"] * b["rnext"]
        b["turn"] = (b["pos"] - b["previous_allocation"]).abs()
        b["bookret"] = b["postRebalance_total_value"].pct_change()
        rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    mu = B["rnext"].mean()
    out["mean coin daily ret"] = mu
    out["mean turnover per bar"] = B["turn"].mean()
    out["fee drag per bar est (turn*0.31%/2)"] = B["turn"].mean() * 0.0031 / 2
    out["mean gross gain per bar"] = B["gain"].mean()
    # drawdown on chained book
    eq = (1 + B["bookret"].fillna(0)).cumprod()
    dd = eq / eq.cummax() - 1
    B["dd"] = dd
    out["max dd"] = dd.min()
    # find top episodes
    peak = eq.cummax()
    B["peakid"] = (eq == peak).cumsum()
    ep = B.groupby("peakid").agg(depth=("dd", "min"), n=("dd", "size"), w0=("w", "first"), w1=("w", "last"), year=("year", "first"))
    ep = ep.sort_values("depth").head(6)
    out["deepest episodes"] = ep
    # stats inside the 3 deepest episodes
    rs = []
    for pid in ep.index[:4]:
        e = B[B["peakid"] == pid]
        trough = e["dd"].idxmin()
        e2 = e.loc[:trough]
        rs.append({"pid": pid, "depth": e["dd"].min(), "days_to_trough": len(e2),
                   "coin_ret_to_trough": (1 + e2["r"].fillna(0)).prod() - 1,
                   "mean_pos": e2["pos"].mean(), "share_long": (e2["pos"] > 0).mean(),
                   "mean_absz": e2["z"].abs().mean(), "mean_vol30": e2["vol30"].mean(),
                   "ret60_at_start": e2["ret60"].iloc[0], "gain_long": e2.loc[e2.pos > 0, "gain"].sum(),
                   "gain_short": e2.loc[e2.pos < 0, "gain"].sum()})
    out["episodes detail"] = pd.DataFrame(rs)
    out["overall vol30 mean"] = B["vol30"].mean()
    # gain by side
    B["side"] = np.sign(B["pos"])
    out["by side"] = B.groupby("side").agg(n=("gain", "size"), gain=("gain", "mean"), sd=("gain", "std"), ex=("rnext", "mean"))
    # by trend state and side
    B["trend60"] = pd.cut(B["ret60"], [-10, -0.2, 0, 0.2, 10])
    g = B.groupby(["trend60", "side"]).agg(n=("gain", "size"), gain=("gain", "mean"), sd=("gain", "std"))
    g["t"] = g["gain"] / (g["sd"] / np.sqrt(g["n"]))
    out["by ret60 x side"] = g
    B["volq"] = pd.qcut(B["vol30"], 3, labels=["lo", "mid", "hi"])
    g = B.groupby(["volq", "side"]).agg(n=("gain", "size"), gain=("gain", "mean"), sd=("gain", "std"))
    g["t"] = g["gain"] / (g["sd"] / np.sqrt(g["n"]))
    out["by vol x side"] = g
    B["zb"] = pd.cut(B["z"], [-20, -2, -1, -0.5, 0, 0.5, 1, 2, 20])
    g = B.groupby("zb").agg(n=("gain", "size"), gain=("gain", "mean"), rnext=("rnext", "mean"), pos=("pos", "mean"), sd=("gain", "std"))
    g["t"] = g["gain"] / (g["sd"] / np.sqrt(g["n"]))
    out["by z"] = g
    g = B.groupby("year").agg(gain=("gain", "mean"), sd=("gain", "std"), n=("gain", "size"), dd=("dd", "min"))
    out["by year"] = g
    return out
