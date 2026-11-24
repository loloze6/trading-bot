def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    total_days = 0
    for coin, wins in bars.items():
        r3 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 3, 3)
            r3 += list(c[idx + 3] / c[idx] - 1)
        drift[coin] = (np.mean(r3), np.std(r3, ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            total_days += len(df)
            o, h, l, c = df["open"], df["high"], df["low"], df["close"]
            rng = (h - l).replace(0, np.nan)
            rr = rng.rolling(20).mean() / rng
            flat = 1 - (c - o).abs() / rng
            rise6 = c / c.shift(6) - 1
            rise5b = c.shift(1) / c.shift(6) - 1
            fwd = c.shift(-3) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)), "rr": rr, "flat": flat,
                              "rise6": rise6, "rise5b": rise5b, "fwd": fwd, "day": ts.dt.floor("D"),
                              "year": ts.dt.year, "fc": df["forecast"]})
            d["unus"] = d["fwd"] - drift[coin][0]
            d["str"] = d["unus"] / drift[coin][1]
            d["cell"] = d["pos"] // 3
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A = A[A["fwd"].notna() & A["rr"].notna() & A["rise6"].notna()]

    def summarise(mask, name):
        s = A[mask].sort_values(["coin", "win", "pos"]).groupby(["coin", "win", "cell"]).head(1)
        n = len(s)
        if n < 5:
            return dict(name=name, n=n)
        dev = s["unus"] - s["unus"].mean()
        g = dev.groupby(s["day"]).sum()
        D = len(g)
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / n
        return dict(name=name, n=n, days=D, per_coinday=n / total_days, mean_unus=s["unus"].mean(),
                    t=s["unus"].mean() / se, strength=s["str"].mean(), total=s["fwd"].mean())

    out = []
    up = A["rise6"] > 0
    for rrth in [0.6667, 0.75, 0.85, 1.0, 9]:
        for fl in [0.9, 0.8, 0.7, 0.6, 0.0]:
            out.append(summarise(up & (A["rr"] <= rrth) & (A["flat"] >= fl), f"up rr<={rrth} flat>={fl}"))
    out.append(summarise(up & (A["rr"] <= 0.6667) & (A["flat"] < 0.6), "up wide notflat<0.6"))
    out.append(summarise(up & (A["rr"] > 1.0) & (A["flat"] >= 0.9), "up narrow flat"))
    out.append(summarise(~up & (A["rr"] <= 0.6667) & (A["flat"] >= 0.9), "down wide flat"))
    out.append(summarise(up & (A["rr"] <= 0.85) & (A["flat"] >= 0.7) & (A["rise5b"] > 0), "up5b rr<=.85 flat>=.7"))
    T = pd.DataFrame(out)
    # gradient by flatness in wide-range uprun
    W = A[up & (A["rr"] <= 0.85)]
    W = W.sort_values(["coin", "win", "pos"]).groupby(["coin", "win", "cell"]).head(1)
    gflat = W.groupby(pd.cut(W["flat"], [0, 0.5, 0.7, 0.8, 0.9, 1.0]))["unus"].agg(["count", "mean"])
    W2 = A[up & (A["flat"] >= 0.7)]
    W2 = W2.sort_values(["coin", "win", "pos"]).groupby(["coin", "win", "cell"]).head(1)
    grr = W2.groupby(pd.cut(W2["rr"], [0, 0.5, 0.6667, 0.85, 1.0, 1.5, 10]))["unus"].agg(["count", "mean"])
    # actual trades per day
    ntr = sum(len(t) for wins in data["trades"].values() for t in wins.values())
    sig = A[up & (A["rr"] <= 0.6667) & (A["flat"] >= 0.9)]
    return {"grid": T, "by_flat_wide_up": gflat, "by_rangeratio_flat07_up": grr,
            "trades": ntr, "coin_days": total_days,
            "signal_bars_strict": len(sig), "strict_with_fc_pos": int((sig["fc"] > 0).sum())}
