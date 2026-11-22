def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted(set(w for c in coins for w in bars[c].keys()), key=lambda s: int(s[1:]))
    # book daily returns, chained in window order
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy(); d["coin"] = c
                frames.append(d)
        if not frames: continue
        d = pd.concat(frames).groupby("day")[["book_return", "coin_return"]].mean().reset_index()
        d["win"] = w
        rows.append(d.dropna())
    bk = pd.concat(rows, ignore_index=True)
    v = (1 + bk["book_return"]).cumprod()
    peak = v.cummax(); dd = v / peak - 1
    bk["dd"] = dd.values
    # drawdown episodes
    eps = []; inep = False
    for i in range(len(bk)):
        if dd.iloc[i] < 0 and not inep:
            inep = True; st = i
        if inep and (dd.iloc[i] == 0 or i == len(bk) - 1):
            seg = bk.iloc[st:i + 1]
            j = seg["dd"].idxmin()
            eps.append({"start_win": bk.loc[st, "win"], "trough_win": bk.loc[j, "win"], "days_to_trough": j - st + 1,
                        "depth": seg["dd"].min(),
                        "coin_ret_to_trough": (1 + bk.loc[st:j, "coin_return"]).prod() - 1,
                        "book_ret_to_trough": (1 + bk.loc[st:j, "book_return"]).prod() - 1})
            inep = False
    e = pd.DataFrame(eps).sort_values("depth").head(6)
    out["deepest_falls"] = e
    yrs = len(bk) / 365
    out["calmar_parts"] = pd.Series({"yearly": v.iloc[-1] ** (1 / yrs) - 1, "maxdd": dd.min(), "days": len(bk)})
    # cases and bar-level gain with context
    cs = []; bg = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; n = len(b)
            r1 = cl.pct_change()
            fwd18 = cl.shift(-18) / cl - 1
            ret30d = cl / cl.shift(180) - 1
            ret5d = cl / cl.shift(30) - 1
            vol5 = r1.rolling(30).std(); vol30 = r1.rolling(180).std()
            vr = vol5 / vol30
            ma = cl.rolling(180).mean()
            dist = cl / ma - 1
            f = b["forecast"].fillna(0)
            rise = f - f.shift(1).fillna(0)
            sig = (rise >= 2) & (f > 0)
            cell = np.arange(n) // 18
            df = pd.DataFrame({"sig": sig, "cell": cell, "fwd": fwd18, "ret30d": ret30d, "ret5d": ret5d, "vr": vr,
                               "dist": dist, "f": f, "year": pd.to_datetime(b["timestamp"]).dt.year})
            s = df[df.sig & df.fwd.notna()].groupby("cell").head(1).copy()
            s["coin"] = c; s["win"] = w
            cs.append(s)
            pos = b["postRebalance_current_allocation"].fillna(0)
            g = pos * (cl.shift(-1) / cl - 1)
            bg.append(pd.DataFrame({"g": g, "pos": pos, "ret30d": ret30d, "vr": vr, "dist": dist, "coin": c,
                                    "r1n": cl.shift(-1) / cl - 1}).dropna())
    cs = pd.concat(cs); bg = pd.concat(bg)
    # drift per coin: mean 18-bar return non-overlapping
    drift = {}
    for c in coins:
        rr = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 18, 18)
            rr.extend(cl[idx + 18] / cl[idx] - 1)
        drift[c] = np.mean(rr)
    cs["ex"] = cs["fwd"] - cs["coin"].map(drift)
    def grp(df, col, q=5):
        df = df.dropna(subset=[col]).copy()
        df["q"] = pd.qcut(df[col], q, labels=False, duplicates="drop")
        a = df.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"), mean_ex=("ex", "mean"),
                               std=("ex", "std"), mean_fwd=("fwd", "mean"))
        a["t"] = a["mean_ex"] / (a["std"] / np.sqrt(a["n"]))
        return a.drop(columns="std")
    out["cases_by_ret30d"] = grp(cs, "ret30d")
    out["cases_by_dist_ma30d"] = grp(cs, "dist")
    out["cases_by_ret5d"] = grp(cs, "ret5d")
    out["cases_by_volratio"] = grp(cs, "vr")
    out["cases_by_forecast"] = grp(cs, "f")
    out["cases_by_year"] = cs.groupby("year")["ex"].agg(["size", "mean"])
    out["cases_by_coin"] = cs.groupby("coin")["ex"].agg(["size", "mean"])
    # bar gain by trend state when held
    h = bg[bg.pos > 0].copy()
    h["q"] = pd.qcut(h["ret30d"], 5, labels=False)
    out["held_bars_by_ret30d"] = h.groupby("q").agg(lo=("ret30d", "min"), hi=("ret30d", "max"), n=("g", "size"),
                                                   mean_gain=("g", "mean"), sum_gain=("g", "sum"), mean_pos=("pos", "mean"),
                                                   std_gain=("g", "std"))
    h["qv"] = pd.qcut(h["vr"], 5, labels=False)
    out["held_bars_by_vr"] = h.groupby("qv").agg(lo=("vr", "min"), hi=("vr", "max"), n=("g", "size"),
                                                 mean_gain=("g", "mean"), std_gain=("g", "std"), mean_pos=("pos", "mean"))
    out["share_time_held"] = float((bg.pos > 0).mean())
    return out
