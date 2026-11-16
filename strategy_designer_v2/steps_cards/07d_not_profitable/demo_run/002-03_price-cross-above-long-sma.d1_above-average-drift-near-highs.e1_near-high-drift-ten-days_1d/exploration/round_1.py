def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            r1 = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"]
            g = pos * r1
            fc = b["forecast"]
            # 20-day range position and 10-day past return
            hi = b["close"].rolling(20, min_periods=20).max()
            lo = b["close"].rolling(20, min_periods=20).min()
            rp = (b["close"] - lo) / (hi - lo)
            ret10p = b["close"] / b["close"].shift(10) - 1
            sma200dist = np.nan
            df = pd.DataFrame({"coin": coin, "w": w, "pos": pos, "g": g, "r1": r1, "fc": fc,
                               "regime": b["regime"], "rp": rp, "ret10p": ret10p})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["g"])
    A["side"] = np.sign(A["pos"]).map({1: "long", -1: "short", 0: "flat"})
    out["gain by side"] = A.groupby("side").agg(n=("g", "size"), mean_g=("g", "mean"), sum_g=("g", "sum"),
                                                 mean_pos=("pos", "mean"), mean_r1=("r1", "mean"))
    A["fcb"] = pd.cut(A["fc"], [-20.01, -10, -0.001, 0.001, 10, 20.01])
    out["gain by forecast bucket"] = A.groupby("fcb").agg(n=("g", "size"), mean_g=("g", "mean"),
                                                           sum_g=("g", "sum"), mean_r1=("r1", "mean"))
    act = A[A["regime"] == "trending"].copy()
    act["rpb"] = pd.cut(act["rp"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.0])
    out["trending r1 by range pos"] = act.groupby("rpb").agg(n=("r1", "size"), mean_r1=("r1", "mean"),
                                                              mean_g=("g", "mean"), mean_pos=("pos", "mean"))
    # book daily
    d = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["day", "book_return", "coin_return"]].copy()
            x["w"] = w
            d.append(x)
    D = pd.concat(d)
    B = D.groupby(["w", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean")).reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna()
    eq = (1 + B["book"]).cumprod()
    dd_ = eq / eq.cummax() - 1
    out["book per window"] = B.groupby("wn").agg(n=("book", "size"), book_mean=("book", "mean"),
                                                 coin_mean=("coin", "mean"),
                                                 book_sum=("book", "sum"), coin_sum=("coin", "sum"))
    out["max dd"] = float(dd_.min())
    B["dd"] = dd_.values
    out["dd depth by window"] = B.groupby("wn")["dd"].min()
    return out
