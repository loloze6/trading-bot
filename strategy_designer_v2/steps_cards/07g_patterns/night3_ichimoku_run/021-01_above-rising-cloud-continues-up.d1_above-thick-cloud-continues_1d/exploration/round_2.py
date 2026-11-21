def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def tt(x):
        x = pd.Series(x).dropna()
        return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan
    rows = {10: [], 26: []}
    day = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            cs = b["close"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(cs)
            if n < 30:
                continue
            lr = np.log(cs).diff()
            vol20 = lr.rolling(20).std()
            p26 = cs / cs.shift(26) - 1
            p5 = cs / cs.shift(5) - 1
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            top = np.maximum(sa, sb)
            above = cs / top - 1
            widx = int(w[1:])
            for H in (10, 26):
                for i in range(0, n - H, H):
                    rows[H].append(dict(coin=coin, w=widx, fwd=cs[i + H] / cs[i] - 1,
                                        p26=p26[i], p5=p5[i], p26v=p26[i] / (vol20[i] * np.sqrt(26)) if vol20[i] > 0 else np.nan,
                                        above=above[i], reg=b["regime"].iloc[i], fc=b["forecast"].iloc[i]))
            r1 = cs.pct_change()
            for i in range(21, n - 1):
                day.append(dict(coin=coin, w=widx, zr=r1[i] / vol20[i], nxt=cs[i + 1] / cs[i] - 1,
                                pos=b["postRebalance_current_allocation"].iloc[i]))
    res = []
    for H in (10, 26):
        df = pd.DataFrame(rows[H])
        df["ex"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
        for f in ["p26", "p5", "p26v"]:
            d = df.dropna(subset=[f, "ex"]).copy()
            d["z"] = d.groupby("coin")[f].transform(lambda x: (x - x.mean()) / x.std())
            s = stats.linregress(d["z"], d["ex"])
            e = d[d.w <= 12]; l = d[d.w > 12]
            se = stats.linregress(e["z"], e["ex"]); sl = stats.linregress(l["z"], l["ex"])
            pc = [stats.linregress(g["z"], g["ex"]) for _, g in d.groupby("coin")]
            res.append(dict(H=H, f=f, n=len(d), slope=s.slope, t=s.slope / s.stderr,
                            t_early=se.slope / se.stderr, t_late=sl.slope / sl.stderr,
                            coins_pos=sum(p.slope > 0 for p in pc),
                            min_coin_t=min(p.slope / p.stderr for p in pc)))
        if H == 26:
            d = df.dropna(subset=["p26", "ex"]).copy()
            d["q"] = d.groupby("coin")["p26"].transform(lambda x: pd.qcut(x, 5, labels=False))
            out["fwd26_by_p26_quintile"] = d.groupby("q").agg(n=("ex", "size"), ex=("ex", "mean"), fwd=("fwd", "mean"))
            tr = df[(df.reg == "trending")].dropna(subset=["above", "p26"])
            res2 = []
            for f in ["above", "p26", "fc"]:
                s = stats.linregress(tr[f], tr["ex"]); res2.append(dict(f=f, n=len(tr), t=s.slope / s.stderr))
            out["in_regime_recomputed"] = pd.DataFrame(res2)
    out["momentum_tests"] = pd.DataFrame(res)
    dd = pd.DataFrame(day).dropna()
    dd["exn"] = dd["nxt"] - dd.groupby("coin")["nxt"].transform("mean")
    dd["sgn"] = -np.clip(dd["zr"], -3, 3)
    pc = []
    for coin, g in dd.groupby("coin"):
        s = stats.linregress(g["sgn"], g["exn"]); pc.append(dict(coin=coin, n=len(g), slope=s.slope, t=s.slope / s.stderr))
    for lab, g in [("early", dd[dd.w <= 12]), ("late", dd[dd.w > 12]), ("all", dd)]:
        s = stats.linregress(g["sgn"], g["exn"]); pc.append(dict(coin=lab, n=len(g), slope=s.slope, t=s.slope / s.stderr))
    out["next_day_reversal"] = pd.DataFrame(pc)
    dd["b"] = pd.cut(dd["zr"], [-99, -1, 1, 99])
    out["next_day_abs_move_by_bucket"] = dd.groupby("b")["exn"].agg(["count", "mean"])
    return out
