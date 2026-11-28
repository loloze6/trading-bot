import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]; trades = data["trades"]
    H = [3, 5]
    rows = []; drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            f = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)),
                "ts": pd.to_datetime(df["timestamp"]),
                "inprof": (df["regime"] == "unknown").astype(int),
                "s7": (c / c.shift(7) - 1) / (vol30 * np.sqrt(7)),
                "dd20": (c / c.rolling(20, min_periods=10).max() - 1) / vol30,
                "up20": (c / c.rolling(20, min_periods=10).min() - 1) / vol30,
                "alloc": df["postRebalance_current_allocation"],
                "nxt": c.shift(-1) / c - 1})
            for h in H:
                f[f"fx{h}"] = c.shift(-h) / c - 1 - drift[(coin, h)]
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    P = A[A["inprof"] == 1]
    out = {}
    def ct(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 5: return (np.nan, np.nan, len(s))
        m = s[col].mean(); d = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((d ** 2).sum()) / len(s)
        return (m, m / se, len(s))
    # robustness of s7 ordering across grid offsets
    tab = []
    for h in H:
        for off in range(h):
            s = P[((P["pos"] - off) % h == 0)].dropna(subset=["s7", f"fx{h}"])
            rho = s[["s7", f"fx{h}"]].corr(method="spearman").iloc[0, 1]
            top = s[s["s7"] > 0]; bot = s[s["s7"] <= 0]
            mt, tt, nt = ct(top, f"fx{h}"); mb, tb, nb = ct(bot, f"fx{h}")
            sl = np.polyfit(top["s7"], top[f"fx{h}"], 1)[0] if len(top) > 5 else np.nan
            tab.append([h, off, rho, rho * np.sqrt(len(s)), mt, tt, nt, sl, mb, tb, nb])
    out["s7 by grid offset"] = pd.DataFrame(tab, columns=["h","off","rho","t_rho","m_pos","t_pos","n_pos","slope_pos","m_neg","t_neg","n_neg"])
    # positive s7 terciles at h3, by coin and year
    s = P[(P["pos"] % 3 == 0) & (P["s7"] > 0)].dropna(subset=["fx3"])
    s = s.assign(q=pd.qcut(s["s7"], 3, labels=False))
    out["pos s7 terciles h3"] = pd.DataFrame([[q, g["s7"].mean(), *ct(g, "fx3")] for q, g in s.groupby("q")], columns=["q","s7","mean","t","n"])
    out["pos s7 h3 by coin"] = pd.DataFrame([[k, *ct(g, "fx3")] for k, g in s.groupby("coin")], columns=["coin","mean","t","n"])
    out["pos s7 h3 by year"] = pd.DataFrame([[k, *ct(g, "fx3")] for k, g in s.groupby(s["ts"].dt.year)], columns=["yr","mean","t","n"])
    # rise off 20-day low (up20) quintiles, h3 h5
    tab = []
    for h in H:
        s = P[P["pos"] % h == 0].dropna(subset=["up20", f"fx{h}"]).copy()
        s["q"] = pd.qcut(s["up20"], 5, labels=False, duplicates="drop")
        for q, g in s.groupby("q"):
            tab.append([h, q, g["up20"].mean(), *ct(g, f"fx{h}")])
        rho = s[["up20", f"fx{h}"]].corr(method="spearman").iloc[0, 1]
        tab.append([h, "rho", np.nan, rho, rho*np.sqrt(len(s)), len(s)])
    out["up20 quintiles"] = pd.DataFrame(tab, columns=["h","q","feat","mean","t","n"])
    # book: daily returns of the coin-book, in-position vs not, by weekday
    d = A.copy(); d["held"] = d["alloc"].abs() > 1e-9
    d["g"] = d["alloc"] * d["nxt"]
    hb = d[d["held"]]
    out["held bars gain by weekday"] = pd.DataFrame([[k, g["g"].mean(), g["g"].mean()/(g["g"].std()/np.sqrt(len(g))), len(g)] for k, g in hb.groupby(hb["ts"].dt.weekday)], columns=["wd","mean","t","n"])
    out["held bars gain by coin"] = pd.DataFrame([[k, g["g"].mean(), g["g"].mean()/(g["g"].std()/np.sqrt(len(g))), len(g)] for k, g in hb.groupby("coin")], columns=["coin","mean","t","n"])
    T = pd.concat([t.assign(coin=c) for c, ws in trades.items() for t in ws.values() if len(t)], ignore_index=True)
    T["dur"] = T["duration_minutes"] / 1440
    T["fq"] = pd.qcut(T["entry_forecast"], 3, labels=False, duplicates="drop")
    out["trades by entry forecast tercile"] = T.groupby("fq").agg(n=("net_profit_loss_percent","size"), mean=("net_profit_loss_percent","mean"), med=("net_profit_loss_percent","median"), win=("net_profit_loss_percent", lambda x: (x>0).mean()), dur=("dur","mean"), fc=("entry_forecast","mean"))
    return out
