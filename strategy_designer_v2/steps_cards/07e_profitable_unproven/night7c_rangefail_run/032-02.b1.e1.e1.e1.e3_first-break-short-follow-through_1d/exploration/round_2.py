def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    PC = "debug_info.components.margin_prox.last_history_value"
    # 1) book: drift part vs timing
    rows = []
    for c in days:
        mu = pd.concat([days[c][w]["coin_return"] for w in days[c]]).mean()
        for w in days[c]:
            d = days[c][w].copy()
            b = bars[c][w].copy()
            b["dk"] = pd.to_datetime(b["timestamp"], utc=True).dt.floor("D").dt.tz_localize(None)
            alloc = b.groupby("dk")["postRebalance_current_allocation"].last().shift(1)
            d["dk"] = pd.to_datetime(d["day"], utc=True).dt.floor("D").dt.tz_localize(None)
            d["alloc"] = d["dk"].map(alloc).fillna(0)
            d["drift"] = d["alloc"] * mu
            d["coin"] = c; d["win"] = w
            d["year"] = d["dk"].dt.year
            rows.append(d)
    D = pd.concat(rows)
    bk = D.groupby(["win", "dk"]).agg(br=("book_return", "mean"), dr=("drift", "mean"), cr=("coin_return", "mean")).dropna()
    out["book mean, drift part, timing"] = pd.Series({"book_mean": bk.br.mean(), "drift_part": bk.dr.mean(),
        "timing": bk.br.mean() - bk.dr.mean(), "t_book": bk.br.mean() / bk.br.std() * np.sqrt(len(bk)),
        "sharpe": bk.br.mean() / bk.br.std() * np.sqrt(365), "ndays": len(bk)})
    out["book by window"] = bk.groupby(level=0).br.agg(["mean", "count", "sum"])
    out["book sum by coin /6"] = D.groupby("coin")["book_return"].sum() / 6
    out["book by year"] = D.groupby("year")["book_return"].agg(["mean", "sum"])
    # 2) trades concentration
    T = pd.concat([trades[c][w].assign(coin=c, win=w) for c in trades for w in trades[c] if len(trades[c][w])])
    r = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(r), "mean": r.mean(), "median": r.median(), "share_pos": (r > 0).mean(),
        "sum": r.sum(), "top5_sum": r.head(5).sum(), "top10_sum": r.head(10).sum(),
        "sum_without_top10": r.iloc[10:].sum(), "mean_days": T["duration_minutes"].mean() / 1440})
    # 3) break cases
    H = [1, 3, 5, 10, 20]
    allret = {h: [] for h in H}
    cases = []
    for c in bars:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"].values.astype(float); n = len(cl)
            for h in H:
                idx = np.arange(0, n - h, h)
                allret[h].append(pd.Series(cl[idx + h] / cl[idx] - 1))
            prox = b[PC].values if PC in b.columns else np.full(n, np.nan)
            brk = (b["regime"] == "trending").values
            s = pd.Series(cl)
            ret20 = s.pct_change(20).values
            ret60 = s.pct_change(60).values
            hi = s.shift(1).rolling(60).max().values
            lo = s.shift(1).rolling(60).min().values
            last = -999; run = 0
            for i in range(n):
                run = run + 1 if brk[i] else 0
                if brk[i] and i - last > 3:
                    last = i
                    p = prox[i]
                    m = (1 / p - 1) if pd.notna(p) and p > 0 else (cl[i] / hi[i] - 1) * 100 if pd.notna(hi[i]) else np.nan
                    rec = {"coin": c, "win": w, "margin": m, "ret20": ret20[i], "ret60": ret60[i],
                           "width": (hi[i] / lo[i] - 1) if pd.notna(hi[i]) else np.nan,
                           "fresh": int(run == 1),
                           "year": pd.to_datetime(b["timestamp"].iloc[i]).year}
                    for h in H:
                        rec[f"f{h}"] = cl[i + h] / cl[i] - 1 if i + h < n else np.nan
                    cases.append(rec)
    C = pd.DataFrame(cases)
    mu = {h: pd.concat(allret[h]).mean() for h in H}
    sd = {h: pd.concat(allret[h]).std() for h in H}
    for h in H:
        C[f"x{h}"] = C[f"f{h}"] - mu[h]
    res = {}
    for h in H:
        x = C[f"x{h}"].dropna()
        res[h] = {"n": len(x), "mean_excess": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)),
                  "drift": mu[h], "usual": sd[h], "strength": x.mean() / sd[h]}
    out["break excess by horizon"] = pd.DataFrame(res).T
    out["margin missing share"] = C["margin"].isna().mean()
    def agg(g):
        return g.agg(n=("x3", "count"), x1=("x1", "mean"), x3=("x3", "mean"), x5=("x5", "mean"),
                     x10=("x10", "mean"), x20=("x20", "mean"))
    C["mq"] = pd.qcut(C["margin"], 4, labels=False, duplicates="drop")
    out["by margin quartile"] = agg(C.groupby("mq")).join(C.groupby("mq")["margin"].median())
    C["r20q"] = pd.qcut(C["ret20"], 4, labels=False, duplicates="drop")
    out["by prior 20d return quartile"] = agg(C.groupby("r20q")).join(C.groupby("r20q")["ret20"].median())
    C["r60q"] = pd.qcut(C["ret60"], 4, labels=False, duplicates="drop")
    out["by prior 60d return quartile"] = agg(C.groupby("r60q")).join(C.groupby("r60q")["ret60"].median())
    C["wq"] = pd.qcut(C["width"], 4, labels=False, duplicates="drop")
    out["by prior 60d range width quartile"] = agg(C.groupby("wq")).join(C.groupby("wq")["width"].median())
    out["by fresh (first day of break run)"] = agg(C.groupby("fresh"))
    out["by coin"] = agg(C.groupby("coin"))
    out["by window"] = agg(C.groupby("win"))
    out["by year"] = agg(C.groupby("year"))
    # t of x10 within r60 quartiles
    out["t x10 by r60q"] = C.groupby("r60q")["x10"].apply(lambda x: x.mean() / x.std() * np.sqrt(x.count()))
    out["t x10 by width q"] = C.groupby("wq")["x10"].apply(lambda x: x.mean() / x.std() * np.sqrt(x.count()))
    return out
