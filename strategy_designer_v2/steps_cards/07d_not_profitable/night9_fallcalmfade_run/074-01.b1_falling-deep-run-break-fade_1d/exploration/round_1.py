def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            dd["wn"] = int(w[1:])
            dd["i"] = np.arange(len(dd))
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    B = B.dropna(subset=["br"])
    v = (1 + B["br"]).cumprod()
    B["dd"] = v / v.cummax() - 1
    out["book by window"] = B.groupby("wn").agg(n=("br", "size"), mean=("br", "mean"), sd=("br", "std"), sum=("br", "sum"), worst_dd=("dd", "min"), coin_mean=("cr", "mean"))
    # worst days
    out["worst 15 book days"] = B.nsmallest(15, "br")[["wn", "br", "cr"]].reset_index(drop=True)
    # cases
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            r = b["close"].pct_change()
            b["r"] = r
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["vol30"] = r.rolling(30).std()
            b["vol_rank"] = b["vol30"].rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            b["tr20"] = b["close"] / b["close"].shift(20) - 1
            b["tr60"] = b["close"] / b["close"].shift(60) - 1
            # run length before
            down = (r < 0).astype(int)
            run = []; k = 0
            for x in down:
                k = k + 1 if x else 0
                run.append(k)
            b["runprev"] = pd.Series(run).shift(1)
            b["alloc"] = b["postRebalance_current_allocation"]
            b["coin"] = c; b["wn"] = int(w[1:])
            cs.append(b)
    A = pd.concat(cs)
    mu = A["r"].mean()
    out["coin mean daily"] = mu
    C = A[A["forecast"] < 0].dropna(subset=["nxt"]).copy()
    C["gain"] = -(C["nxt"] - mu)
    C["pnl"] = C["alloc"] * C["nxt"]
    out["n cases"] = len(C)
    def g(col, q=4):
        x = C.dropna(subset=[col])
        x["bin"] = pd.qcut(x[col], q, duplicates="drop")
        return x.groupby("bin").agg(n=("gain", "size"), gain=("gain", "mean"), t=("gain", lambda s: s.mean() / s.std() * np.sqrt(len(s))), pnl=("pnl", "sum"), alloc=("alloc", "mean"))
    out["by bounce-day return r"] = g("r")
    out["by vol_rank"] = g("vol_rank")
    out["by tr20"] = g("tr20")
    out["by tr60"] = g("tr60")
    out["by runprev"] = g("runprev")
    out["by forecast"] = g("forecast")
    out["by window"] = C.groupby("wn").agg(n=("gain", "size"), gain=("gain", "mean"), pnl=("pnl", "sum"))
    out["by coin"] = C.groupby("coin").agg(n=("gain", "size"), gain=("gain", "mean"), pnl=("pnl", "sum"))
    # gains distribution tail
    out["case gain quantiles"] = C["gain"].quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    # non-case falling market days, by r bins (condition alone)
    F = A[(A["tr60"] < -0.10) & ~(A["forecast"] < 0)].dropna(subset=["nxt"]).copy()
    F["gain"] = -(F["nxt"] - mu)
    F["volbin"] = pd.cut(F["vol_rank"], [0, 0.5, 1.0])
    out["noncase falling days by agitation"] = F.groupby("volbin").agg(n=("gain", "size"), gain=("gain", "mean"))
    return out
