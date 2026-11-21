def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 72
    rows = []
    hr = []
    bookrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            if n < 2 * H + 2:
                continue
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            ts = pd.to_datetime(b["timestamp"])
            # hourly returns next bar by hour/weekday
            nxt = np.r_[c[1:] / c[:-1] - 1, np.nan]
            hr.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values, "nxt": nxt}))
            vol = b["volume"].values.astype(float)
            for t in range(0, n - H, H):
                if t < H:
                    continue
                past = c[t] / c[t - H] - 1
                rr = r1[t - H + 1:t + 1]
                pos = np.sort(rr[rr > 0])[::-1]
                lr = np.log1p(rr)
                top3 = pos[:3].sum()
                share = top3 / past if past > 0 else np.nan
                rv = np.nanstd(rr)
                eff = abs(np.log(c[t] / c[t - H])) / np.nansum(np.abs(lr))
                vv = vol[t - H + 1:t + 1]
                vconc = np.sort(vv)[::-1][:3].sum() / vv.sum() if vv.sum() > 0 else np.nan
                fwd = c[t + H] / c[t] - 1
                rows.append(dict(coin=coin, w=w, past=past, share=share, rv=rv, eff=eff,
                                 vconc=vconc, fwd=fwd, alloc=b["postRebalance_current_allocation"].iloc[t],
                                 fc=b["forecast"].iloc[t], year=ts.iloc[t].year))
    df = pd.DataFrame(rows)
    out = {}
    df["fwd_dm"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    def tq(g, col, q=5):
        g = g.copy()
        g["q"] = g.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        s = g.groupby("q")["fwd_dm"].agg(["mean", "count", "std"])
        s["t"] = s["mean"] / (s["std"] / np.sqrt(s["count"]))
        return s
    out["by_past_quintile"] = tq(df, "past")
    out["by_rv_quintile"] = tq(df, "rv")
    out["by_eff_quintile"] = tq(df, "eff")
    out["by_vconc_quintile"] = tq(df, "vconc")
    up = df[df.past > 0]
    out["up_by_share_q"] = tq(up, "share")
    dn = df[df.past < 0]
    out["down_by_eff_q"] = tq(dn, "eff")
    out["up_by_eff_q"] = tq(up, "eff")
    # signed efficiency: eff * sign(past)
    df["seff"] = df["eff"] * np.sign(df["past"])
    out["by_signed_eff_q"] = tq(df, "seff")
    out["fwd_by_coin"] = df.groupby("coin")["fwd"].agg(["mean", "count"])
    h = pd.concat(hr).dropna()
    h["nxt_dm"] = h["nxt"] - h.groupby("coin")["nxt"].transform("mean")
    hh = h.groupby("hour")["nxt_dm"].agg(["mean", "count", "std"]); hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    out["by_hour"] = hh
    ww = h.groupby("wd")["nxt_dm"].agg(["mean", "count", "std"]); ww["t"] = ww["mean"] / (ww["std"] / np.sqrt(ww["count"]))
    out["by_weekday"] = ww
    # book attribution
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bookrows.append(pd.DataFrame({"coin": coin, "w": w, "br": d["book_return"].values, "cr": d["coin_return"].values}))
    bk = pd.concat(bookrows).dropna()
    daily = bk.groupby(["w"]).size()
    out["book_vs_coin_by_coin"] = bk.groupby("coin")[["br", "cr"]].mean()
    out["book_by_window"] = bk.groupby("w")[["br", "cr"]].mean()
    out["active_share_by_coin"] = df.assign(act=df.alloc.abs() > 0).groupby("coin")["act"].mean()
    return out
