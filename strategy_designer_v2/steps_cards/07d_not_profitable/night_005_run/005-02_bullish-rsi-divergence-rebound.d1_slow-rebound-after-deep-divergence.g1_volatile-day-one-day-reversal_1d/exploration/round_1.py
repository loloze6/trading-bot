def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    drows = []
    for coin, wins in data["bars"].items():
        # coin mean daily return over all windows
        cr = pd.concat([data["days"][coin][w]["coin_return"] for w in wins], ignore_index=True)
        mu = cr.mean()
        for w, b in wins.items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["ret1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            r = b["close"].pct_change()
            sd20 = r.rolling(20).std()
            b["z"] = r / sd20
            b["vr"] = sd20 / sd20.rolling(60).mean()
            b["r20"] = b["close"] / b["close"].shift(20) - 1
            b["coin"] = coin; b["w"] = w; b["mu"] = mu
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
            d = data["days"][coin][w].copy(); d["coin"] = coin; d["w"] = w
            d["year"] = pd.to_datetime(d["day"]).dt.year
            drows.append(d)
    B = pd.concat(rows, ignore_index=True)
    D = pd.concat(drows, ignore_index=True)
    act = B[B["pos"].abs() > 1e-9].dropna(subset=["ret1"])
    out["share_active"] = float((B["pos"].abs() > 1e-9).mean())
    act = act.assign(side=np.where(act["pos"] > 0, "long", "short"))
    out["by_side"] = act.groupby(["coin", "side"]).agg(n=("gain", "size"), mean_gain=("gain", "mean"),
        mean_pos=("pos", "mean"), drift_part=("mu", "mean"), mean_ret1=("ret1", "mean"))
    act["drift"] = act["pos"] * act["mu"]
    out["drift_vs_timing"] = pd.Series({"mean_gain_all_bars": B["gain"].mean(),
        "drift_all_bars": (B["pos"] * B["mu"]).mean(), "fee_per_bar": B["fee"].mean()})
    act["zb"] = pd.qcut(act["z"].abs(), 5, labels=False, duplicates="drop")
    out["by_absz_q"] = act.groupby(["zb", "side"]).agg(n=("gain", "size"), gain=("gain", "mean"),
        absz=("z", lambda s: s.abs().mean()))
    act["vrb"] = pd.qcut(act["vr"], 4, labels=False, duplicates="drop")
    out["by_volratio_q"] = act.groupby(["vrb", "side"]).agg(n=("gain", "size"), gain=("gain", "mean"))
    act["tr"] = pd.qcut(act["r20"], 4, labels=False, duplicates="drop")
    out["by_r20_q"] = act.groupby(["tr", "side"]).agg(n=("gain", "size"), gain=("gain", "mean"),
        r20=("r20", "mean"))
    out["book_by_year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
        sd=("book_return", "std"))
    # equity drawdown per coin chained windows
    dd = {}
    for coin in D["coin"].unique():
        x = D[D["coin"] == coin]["book_return"].fillna(0)
        eq = (1 + x).cumprod().values
        peak = np.maximum.accumulate(eq)
        ddv = eq / peak - 1
        dd[coin] = ddv.min()
    out["coin_maxdd"] = pd.Series(dd)
    # worst 5% book days: what side and z
    m = B.merge(D[["coin", "w", "book_return"]].assign(k=1), how="left", left_index=False, right_index=False, on=["coin", "w"]) if False else None
    worst = act.nsmallest(int(len(act) * 0.05), "gain")
    out["worst5pct_bars"] = pd.Series({"n": len(worst), "share_long": (worst["pos"] > 0).mean(),
        "mean_absz": worst["z"].abs().mean(), "mean_vr": worst["vr"].mean(), "mean_r20": worst["r20"].mean(),
        "all_share_long": (act["pos"] > 0).mean(), "all_absz": act["z"].abs().mean(), "all_r20": act["r20"].mean()})
    return out
