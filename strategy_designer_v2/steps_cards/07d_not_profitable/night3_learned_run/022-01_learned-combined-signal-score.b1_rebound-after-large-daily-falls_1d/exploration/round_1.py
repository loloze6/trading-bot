def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily returns, mean across coins per day within window
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    B = B.dropna(subset=["br"])
    eq = (1 + B["br"]).cumprod().values
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1
    B["dd"] = dd
    B["idx"] = np.arange(len(B))
    out["deepest_fall"] = float(dd.min())
    out["yearly"] = float(eq[-1] ** (365 / len(B)) - 1)
    # drawdown episodes
    eps = []
    i = 0; n = len(dd)
    while i < n:
        if dd[i] < 0:
            j = i
            while j < n and dd[j] < 0: j += 1
            seg = slice(i, j)
            k = i + int(np.argmin(dd[i:j]))
            eps.append((i, k, j, dd[k]))
            i = j
        else:
            i += 1
    eps = sorted(eps, key=lambda e: e[3])[:6]
    E = []
    for (s, k, e, m) in eps:
        sub = B.iloc[s - 1 if s > 0 else s:k + 1]
        E.append({"depth": m, "days_to_trough": k - s + 1, "windows": f"w{B.iloc[s]['wn']}-w{B.iloc[k]['wn']}",
                  "coin_mean_chain": float((1 + B.iloc[s:k + 1]["cr"]).prod() - 1),
                  "book_chain": float((1 + B.iloc[s:k + 1]["br"]).prod() - 1)})
    out["episodes"] = pd.DataFrame(E)
    # bar level states
    R = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            cl = b["close"]
            r1 = cl.pct_change()
            vol = r1.rolling(30).std()
            b["z"] = r1 / vol
            b["r30"] = cl / cl.shift(30) - 1
            b["r7"] = cl / cl.shift(7) - 1
            b["volrank"] = vol.rolling(180, min_periods=60).rank(pct=True)
            b["volratio"] = r1.rolling(7).std() / vol
            b["nxt"] = cl.shift(-1) / cl - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["nxt"]
            b["coin"] = c; b["wn"] = int(w[1:])
            R.append(b[["coin", "wn", "z", "r30", "r7", "volrank", "volratio", "nxt", "pos", "gain", "forecast"]])
    A = pd.concat(R).dropna(subset=["nxt", "r30"])
    mu = A.groupby("coin")["nxt"].transform("mean")
    A["ex"] = A["nxt"] - mu
    act = A[A["forecast"] > 0].copy()
    def grp(col, q=4):
        act["g"] = pd.qcut(act[col], q, labels=False, duplicates="drop")
        t = act.groupby("g").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"), ex=("ex", "mean"),
                                 nxt=("nxt", "mean"), sd=("nxt", "std"), gain_sum=("gain", "sum"),
                                 worst=("gain", "min"), pos=("pos", "mean"))
        t["t"] = t["ex"] / (t["sd"] / np.sqrt(t["n"]))
        return t
    out["by_r30"] = grp("r30")
    out["by_r7"] = grp("r7")
    out["by_volrank"] = grp("volrank")
    out["by_volratio"] = grp("volratio")
    out["by_z"] = grp("z")
    # worst gain bars state
    worst = act.nsmallest(60, "gain")
    out["worst60_state"] = worst[["z", "r30", "r7", "volrank", "volratio", "pos", "nxt"]].mean()
    out["all_active_state"] = act[["z", "r30", "r7", "volrank", "volratio", "pos", "nxt"]].mean()
    out["by_coin"] = act.groupby("coin").agg(n=("ex", "size"), ex=("ex", "mean"), gain=("gain", "sum"), pos=("pos", "mean"))
    return out
