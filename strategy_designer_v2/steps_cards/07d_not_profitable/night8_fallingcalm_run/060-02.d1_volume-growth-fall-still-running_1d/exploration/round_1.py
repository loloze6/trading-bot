def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days = data["days"]; bars = data["bars"]
    # book daily: mean of coins per (window, day)
    rows = []
    for c in days:
        for w, d in days[c].items():
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
    B["idx"] = np.arange(len(B))
    out["max_dd"] = float(dd.min())
    # drawdown episodes: find top 4 troughs
    eps = []
    i = 0
    n = len(dd)
    inep = False
    for k in range(n):
        if dd[k] < 0 and not inep:
            inep = True; start = k
        if inep and (dd[k] == 0 or k == n - 1):
            seg = dd[start:k + 1]
            t = start + int(np.argmin(seg))
            eps.append((float(seg.min()), start, t, k))
            inep = False
    eps = sorted(eps)[:5]
    E = []
    for m, s, t, e in eps:
        sub = B.iloc[s:t + 1]
        E.append({"depth": m, "days_to_trough": t - s, "window": f"w{B.iloc[t]['wn']}",
                  "book_sum": sub.book_return.sum(), "coin_sum": sub.coin_return.sum()})
    out["worst_episodes"] = pd.DataFrame(E)
    # per bar position-level analysis
    R = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["gain"] = b["postRebalance_current_allocation"] * b["ret1"]
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["ret5p"] = b["close"] / b["close"].shift(5) - 1
            lr = np.log(b["close"]).diff()
            b["vol30"] = lr.rolling(30).std()
            b["volrank"] = b["vol30"].rolling(365, min_periods=100).rank(pct=True)
            b["fwd5"] = b["close"].shift(-5) / b["close"] - 1
            b["coin"] = c; b["w"] = w
            b["pos0"] = np.arange(len(b))
            R.append(b)
    A = pd.concat(R)
    A["side"] = np.sign(A["postRebalance_current_allocation"]).map({1: "long", -1: "short", 0: "flat"})
    g = A.dropna(subset=["gain"]).groupby("side")["gain"].agg(["count", "mean", "sum"])
    out["gain_by_side"] = g
    g2 = A.dropna(subset=["gain"]).groupby(["w", "side"])["gain"].sum().unstack()
    out["gain_by_window_side"] = g2
    out["gain_by_coin_side"] = A.dropna(subset=["gain"]).groupby(["coin", "side"])["gain"].sum().unstack()
    # position days by agitation
    P = A[A.side != "flat"].dropna(subset=["gain"]).copy()
    P["agit"] = np.where(P["volrank"] > 0.5, "agitated", "calm")
    out["gain_by_agit_side"] = P.groupby(["agit", "side"])["gain"].agg(["count", "mean", "sum"])
    P["r20q"] = pd.qcut(P["ret20"], 4, labels=["q1deep", "q2", "q3", "q4shallow"])
    out["gain_by_ret20q_side"] = P.groupby(["r20q", "side"])["gain"].agg(["count", "mean", "sum", "std"])
    P["fq"] = pd.qcut(P["forecast"].abs(), 3, labels=["weak", "mid", "strong"])
    out["gain_by_fstrength_side"] = P.groupby(["fq", "side"])["gain"].agg(["count", "mean", "sum", "std"])
    return out
