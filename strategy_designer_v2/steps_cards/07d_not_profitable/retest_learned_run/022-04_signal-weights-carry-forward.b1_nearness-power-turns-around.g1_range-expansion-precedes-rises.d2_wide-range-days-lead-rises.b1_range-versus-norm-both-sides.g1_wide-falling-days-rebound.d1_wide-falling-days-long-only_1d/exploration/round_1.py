def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    wins = sorted(data["days"][coins[0]].keys(), key=lambda w: int(w[1:]))
    # book daily
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            d = data["days"][c].get(w)
            if d is None: continue
            frames.append(d.set_index("day")[["book_return","coin_return"]].add_suffix("_"+c))
        df = pd.concat(frames, axis=1)
        br = df[[x for x in df if x.startswith("book_return")]].mean(axis=1)
        cr = df[[x for x in df if x.startswith("coin_return")]].mean(axis=1)
        t = pd.DataFrame({"b": br, "c": cr}).dropna()
        t["w"] = w
        rows.append(t.reset_index(drop=True))
    B = pd.concat(rows, ignore_index=True)
    v = (1 + B["b"]).cumprod()
    dd = v / v.cummax() - 1
    B["dd"] = dd
    out["maxdd"] = float(dd.min())
    # drawdown episodes
    peak_i = None; eps = []
    curmax = -1; start = 0
    vv = v.values
    runmax = np.maximum.accumulate(vv)
    i = 0; n = len(vv)
    while i < n:
        if vv[i] < runmax[i]:
            s = i - 1
            j = i
            while j < n and vv[j] < runmax[s]: j += 1
            trough = s + np.argmin(vv[s:j]) if j > s else s
            eps.append((s, trough, j, vv[trough]/vv[s]-1))
            i = j
        else:
            i += 1
    eps = sorted(eps, key=lambda e: e[3])[:6]
    er = []
    for s, tr, j, depth in eps:
        seg = B.iloc[s+1:tr+1]
        cv = (1 + seg["c"]).prod() - 1
        er.append({"window": B["w"].iloc[tr], "depth": depth, "days_to_trough": tr - s,
                   "coins_hold_ret_same": cv, "recovery_days": j - tr})
    out["worst_dd_episodes"] = pd.DataFrame(er)
    # per-window book vs coin
    g = B.groupby("w").agg(book=("b", lambda x: (1+x).prod()-1), coin=("c", lambda x: (1+x).prod()-1), mindd=("dd","min"))
    out["per_window"] = g.loc[wins]
    # case-level analysis with conditions
    H = 3
    allret = {}
    for c in coins:
        rs = []
        for w in wins:
            b = data["bars"][c].get(w)
            if b is None: continue
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            rs.append(cl[idx + H] / cl[idx] - 1)
        allret[c] = np.concatenate(rs)
    cases = []
    for c in coins:
        drift = allret[c].mean(); usual = allret[c].std()
        for w in wins:
            b = data["bars"][c].get(w)
            if b is None: continue
            b = b.reset_index(drop=True)
            cl = b["close"]; f = b["forecast"].fillna(0).values
            rng = (b["high"] - b["low"]) / cl
            r30 = cl / cl.shift(30) - 1
            r7 = cl / cl.shift(7) - 1
            r1 = cl.pct_change()
            ma50 = cl / cl.rolling(50, min_periods=20).mean() - 1
            vol30 = r1.rolling(30, min_periods=15).std()
            vol_rel = vol30 / r1.rolling(30, min_periods=15).std().rolling(120, min_periods=30).mean()
            hi30 = cl / cl.rolling(30, min_periods=10).max() - 1
            fwd = cl.shift(-H) / cl - 1
            n = len(b)
            last_low = f[0]; 
            for cell in range(0, n - H, H):
                for t in range(cell, min(cell + H, n)):
                    pass
            # simple case definition: first bar in each grid cell where forecast rises >=2 from min since previous bet
            lo = 0.0
            taken_cell = -1
            for t in range(n):
                if t > 0:
                    pass
                lo = min(lo, f[t])
                if f[t] - lo >= 2:
                    cellid = t // H
                    if cellid != taken_cell and t + H < n:
                        taken_cell = cellid
                        cases.append({"coin": c, "w": w, "fc": f[t], "fwd": fwd[t], "u": fwd[t] - drift,
                                      "s": (fwd[t]-drift)/usual, "r30": r30[t], "r7": r7[t], "r1": r1[t],
                                      "ma50": ma50[t], "vol_rel": vol_rel[t], "hi30": hi30[t], "rng": rng[t]})
                    lo = f[t]
    C = pd.DataFrame(cases)
    out["n_cases"] = len(C)
    out["case_mean_u"] = float(C["u"].mean())
    def split(col, q=3):
        d = C.dropna(subset=[col]).copy()
        d["bin"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        return d.groupby("bin").agg(lo=(col, "min"), hi=(col, "max"), n=("u", "size"), mean_u=("u", "mean"),
                                    std_u=("u", "std"), p10=("fwd", lambda x: x.quantile(0.1)),
                                    t=("u", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    for col in ["r30", "r7", "r1", "ma50", "vol_rel", "hi30", "fc"]:
        out["by_" + col] = split(col)
    # by coin
    out["by_coin"] = C.groupby("coin").agg(n=("u","size"), mean_u=("u","mean"), p10=("fwd", lambda x: x.quantile(0.1)))
    return out
