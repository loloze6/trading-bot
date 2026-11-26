def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # --- book daily returns, mean across coins per day, per window
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    B = B.dropna()
    v = (1 + B["book_return"]).cumprod().values
    peak = np.maximum.accumulate(v)
    dd = v / peak - 1
    B["dd"] = dd
    out["max_dd"] = float(dd.min())
    # per window: book return, coin return, min dd inside chain
    out["per_window"] = B.groupby("wn").agg(book=("book_return", lambda x: (1 + x).prod() - 1),
                                            coin=("coin_return", lambda x: (1 + x).prod() - 1),
                                            min_dd=("dd", "min"), days=("dd", "size"))
    # worst book days: count and share of losses
    B["yr"] = pd.to_datetime(B["day"]).dt.year
    out["worst20_days_by_window"] = B.nsmallest(20, "book_return").groupby("wn").size()
    out["worst20_mean_book_coin"] = B.nsmallest(20, "book_return")[["book_return", "coin_return"]].mean()

    # --- cases and conditions per coin bar
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; hi = b["high"]
            prevhi = hi.shift(1).rolling(20).max()
            dist = cl / prevhi - 1
            brk = dist > 0
            fresh = brk & ~brk.shift(1, fill_value=False)
            r = cl.pct_change()
            fwd5 = cl.shift(-5) / cl - 1
            fwd1 = cl.shift(-1) / cl - 1
            ret5 = cl / cl.shift(5) - 1
            ret20 = cl / cl.shift(20) - 1
            ret60 = cl / cl.shift(60) - 1
            vol10 = r.rolling(10).std(); vol60 = r.rolling(60).std()
            dayret = r
            n = len(b)
            grid = (np.arange(n) % 5) == 0
            # per-bar position pnl
            pos = b["postRebalance_current_allocation"]
            pnl = pos * fwd1
            # streak of consecutive breakout days
            streak = brk.astype(int).groupby((~brk).cumsum()).cumsum()
            df = pd.DataFrame(dict(coin=c, w=w, dist=dist, brk=brk, fresh=fresh, fwd5=fwd5, ret5=ret5,
                                   ret20=ret20, ret60=ret60, vr=vol10 / vol60, dayret=dayret,
                                   grid=grid, pos=pos, pnl=pnl, fc=b["forecast"], streak=streak,
                                   rng=(hi - b["low"]) / cl))
            recs.append(df)
    X = pd.concat(recs, ignore_index=True)
    drift = X[X.grid]["fwd5"].mean()
    out["drift5"] = float(drift)
    X["u5"] = X["fwd5"] - drift
    C = X[X.fresh & X.fwd5.notna()].copy()
    out["n_fresh_cases"] = len(C)

    def g(df, col, q=3):
        k = pd.qcut(df[col], q, labels=False, duplicates="drop")
        r = df.groupby(k)["u5"].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r
    out["fresh_by_dist"] = g(C, "dist")
    out["fresh_by_ret20"] = g(C, "ret20")
    out["fresh_by_ret60"] = g(C.dropna(subset=["ret60"]), "ret60")
    out["fresh_by_volratio"] = g(C.dropna(subset=["vr"]), "vr")
    out["fresh_by_dayret"] = g(C, "dayret")
    out["fresh_by_window"] = C.groupby("w")["u5"].agg(["mean", "count"])
    # condition alone on non-breakout grid bars
    N = X[X.grid & ~X.brk & X.fwd5.notna()]
    out["nonbreak_by_ret60"] = g(N.dropna(subset=["ret60"]), "ret60")
    out["nonbreak_by_volratio"] = g(N.dropna(subset=["vr"]), "vr")
    # pnl of held bars by streak / by bars since entry
    H = X[X.pos.abs() > 0]
    out["pnl_by_streak"] = H.groupby(H.streak.clip(upper=6))["pnl"].agg(["mean", "count", "sum"])
    out["held_pnl_by_ret60"] = H.dropna(subset=["ret60"]).groupby(pd.qcut(H["ret60"].dropna(), 3, labels=False))["pnl"].agg(["mean", "count"])
    out["held_pnl_by_vr"] = H.dropna(subset=["vr"]).groupby(pd.qcut(H["vr"].dropna(), 3, labels=False))["pnl"].agg(["mean", "count"])
    out["held_share_bars"] = float((X.pos.abs() > 0).mean())
    out["mean_pos_when_held"] = float(H.pos.mean())
    return out
