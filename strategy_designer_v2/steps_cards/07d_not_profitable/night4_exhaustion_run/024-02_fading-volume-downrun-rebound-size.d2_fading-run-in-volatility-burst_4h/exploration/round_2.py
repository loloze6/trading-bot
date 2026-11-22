def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted(set(w for c in coins for w in bars[c].keys()), key=lambda s: int(s[1:]))
    # per-bar state, daily-level book context per window
    cs = []; bg = []
    drift = {}
    for c in coins:
        rr = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 18, 18)
            rr.extend(cl[idx + 18] / cl[idx] - 1)
        drift[c] = np.mean(rr)
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; n = len(b)
            fwd18 = cl.shift(-18) / cl - 1
            r30 = cl / cl.shift(180) - 1
            r90 = cl / cl.shift(540) - 1
            r1 = cl.pct_change()
            vr = r1.rolling(30).std() / r1.rolling(180).std()
            f = b["forecast"].fillna(0)
            sig = ((f - f.shift(1).fillna(0)) >= 2) & (f > 0)
            df = pd.DataFrame({"sig": sig, "cell": np.arange(n) // 18, "fwd": fwd18, "r30": r30, "r90": r90, "vr": vr, "f": f})
            s = df[df.sig & df.fwd.notna()].groupby("cell").head(1).copy()
            s["coin"] = c; s["win"] = w
            cs.append(s)
            pos = b["postRebalance_current_allocation"].fillna(0)
            g = pos * (cl.shift(-1) / cl - 1)
            bg.append(pd.DataFrame({"g": g, "pos": pos, "r30": r30, "r90": r90, "vr": vr, "win": w, "coin": c}).dropna(subset=["g"]))
    cs = pd.concat(cs); bg = pd.concat(bg)
    cs["ex"] = cs["fwd"] - cs["coin"].map(drift)
    def tab(df, col, q=5):
        df = df.dropna(subset=[col]).copy()
        df["q"] = pd.qcut(df[col], q, labels=False, duplicates="drop")
        a = df.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"))
        a["t"] = a.mean_ex / (a.sd / np.sqrt(a.n))
        return a.drop(columns="sd")
    out["cases_by_r90"] = tab(cs, "r90")
    c2 = cs.dropna(subset=["r30", "vr"]).copy()
    c2["trend_up"] = c2.r30 > 0
    c2["vr_hi"] = c2.vr > c2.vr.median()
    a = c2.groupby(["trend_up", "vr_hi"]).agg(n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"))
    a["t"] = a.mean_ex / (a.sd / np.sqrt(a.n)); out["cases_trend_x_vr"] = a.drop(columns="sd")
    # fall windows: what was held
    fallw = ["w1", "w2", "w3", "w12", "w13", "w14", "w21", "w22"]
    bg["in_fall"] = bg.win.isin(fallw)
    out["held_in_fall_vs_rest"] = bg.groupby("in_fall").agg(mean_pos=("pos", "mean"), share_held=("pos", lambda x: (x > 0).mean()),
                                                            mean_gain=("g", "mean"), share_r30_neg=("r30", lambda x: (x < 0).mean()),
                                                            share_r90_neg=("r90", lambda x: (x < 0).mean()))
    h = bg[bg.pos > 0].dropna(subset=["r90"]).copy()
    h["q"] = pd.qcut(h.r90, 5, labels=False)
    out["held_bars_by_r90"] = h.groupby("q").agg(lo=("r90", "min"), hi=("r90", "max"), n=("g", "size"), mean_gain=("g", "mean"), sum_gain=("g", "sum"))
    # book daily: market rise vs timing
    rows = []
    for w in wins:
        fr = [days[c][w][["day", "book_return", "coin_return"]] for c in coins if w in days[c]]
        d = pd.concat(fr).groupby("day").mean().dropna(); d["win"] = w; rows.append(d)
    bk = pd.concat(rows)
    out["book_by_window"] = bk.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean")).reindex(wins)
    return out
