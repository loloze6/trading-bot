def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coins = list(data["bars"].keys())
    H = 120
    # ---- book daily chain, drawdown
    wins = sorted(data["days"][coins[0]].keys(), key=lambda w: int(w[1:]))
    book_rows = []
    for w in wins:
        frames = []
        for c in coins:
            d = data["days"][c].get(w)
            if d is None: continue
            frames.append(d.set_index("day")[["book_return","coin_return"]].add_prefix(c+"_"))
        df = pd.concat(frames, axis=1)
        br = df[[k for k in df.columns if k.endswith("book_return")]].mean(axis=1)
        cr = df[[k for k in df.columns if k.endswith("coin_return")]].mean(axis=1)
        t = pd.DataFrame({"b": br, "c": cr}).dropna()
        t["w"] = w
        book_rows.append(t)
    B = pd.concat(book_rows, ignore_index=True)
    eq = (1 + B["b"]).cumprod()
    dd = eq / eq.cummax() - 1
    B["dd"] = dd.values
    out["book_by_window"] = B.groupby("w", sort=False).agg(book_sum=("b","sum"), coin_sum=("c","sum"), min_dd=("dd","min"), n=("b","size"))
    out["deepest_dd"] = float(dd.min())
    yr = (eq.iloc[-1]) ** (365 / len(B)) - 1
    out["yearly"] = float(yr)
    # ---- grid cases with features
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r24 = cl / cl.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            mult = r24 / mabs
            r720 = cl / cl.shift(720) - 1
            r168 = cl.shift(24) / cl.shift(192) - 1
            vol24 = np.log(cl).diff().rolling(24).std()
            vol720 = np.log(cl).diff().rolling(720).std()
            hi720 = cl.rolling(720).max()
            nearhi = cl / hi720
            fwd = cl.shift(-H) / cl - 1
            f = b["forecast"].astype(float)
            alloc = b["postRebalance_current_allocation"].astype(float)
            n = len(b)
            # grid stretches for drift
            g = np.arange(0, n - H, H)
            for i in g:
                # case: first bar in cell [i, i+H) where forecast rises >=2 from its low since last rise
                pass
            # simpler: first bar in each grid cell with forecast>=2 and prev forecast<2
            up = (f >= 2) & (f.shift(1).fillna(0) < 2)
            for i in range(0, n, H):
                idx = np.where(up.values[i:i+H])[0]
                rec = {"coin": c, "w": w, "grid": True, "fwd_grid": (cl.iloc[i+H]/cl.iloc[i]-1) if i+H < n else np.nan}
                rows.append(rec)
                if len(idx):
                    j = i + idx[0]
                    if j + H < n:
                        rows.append({"coin": c, "w": w, "grid": False, "fwd": fwd.iloc[j], "mult": mult.iloc[j],
                                     "r30": r720.iloc[j], "r7prior": r168.iloc[j], "volr": vol24.iloc[j]/vol720.iloc[j],
                                     "nearhi": nearhi.iloc[j], "fc": f.iloc[j], "alloc": alloc.iloc[j]})
    R = pd.DataFrame(rows)
    G = R[R.grid]
    drift = G.groupby("coin")["fwd_grid"].mean()
    C = R[~R.grid].copy()
    C["unus"] = C["fwd"] - C["coin"].map(drift)
    out["n_cases"] = len(C)
    def grp(col, q=5):
        x = C.dropna(subset=[col, "unus"])
        x = x.assign(b=pd.qcut(x[col], q, duplicates="drop"))
        a = x.groupby("b", observed=True)["unus"].agg(["mean","count","std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["fwd_total"] = x.groupby("b", observed=True)["fwd"].mean()
        a["lo_q10"] = x.groupby("b", observed=True)["unus"].quantile(0.1)
        return a.drop(columns="std")
    for col in ["mult", "r30", "r7prior", "volr", "nearhi"]:
        out["by_" + col] = grp(col)
    out["by_coin"] = C.groupby("coin")["unus"].agg(["mean","count"])
    return out
