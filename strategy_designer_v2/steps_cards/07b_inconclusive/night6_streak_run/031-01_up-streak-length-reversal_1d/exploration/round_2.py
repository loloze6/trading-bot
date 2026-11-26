def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = [1, 3, 5, 10, 20]
    drift = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            fc = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            up = np.zeros(n); dn = np.zeros(n)
            for i in range(1, n):
                up[i] = up[i-1] + 1 if ret1[i] > 0 else 0
                dn[i] = dn[i-1] + 1 if ret1[i] < 0 else 0
            # step-5 bet logic
            low = None; bets = np.zeros(n, bool)
            for i in range(n):
                a = -fc[i] if fc[i] < 0 else 0.0
                if a <= 0:
                    low = None; continue
                if low is None: low = 0.0
                if a - low >= 2:
                    bets[i] = True; low = a
                else:
                    low = min(low, a)
            seen = set()
            for i in range(n):
                cell = i // 5
                isc = False
                if bets[i] and cell not in seen:
                    seen.add(cell); isc = True
                r = {"coin": coin, "win": w, "i": i, "day": ts[i].normalize(), "year": ts[i].year,
                     "case": isc, "fc": fc[i], "up": up[i], "dn": dn[i]}
                for h in H:
                    r[f"s{h}"] = -(c[i+h]/c[i]-1-drift[(coin, h)]) if i+h < n else np.nan
                rows.append(r)
    D = pd.DataFrame(rows)

    def clt(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 5: return (len(s), np.nan, np.nan)
        m = s[col].mean(); g = (s[col]-m).groupby(s["day"]).sum(); G = len(g)
        se = np.sqrt((g**2).sum()*G/(G-1))/len(s)
        return (len(s), m, m/se)

    C = D[D.case].copy()
    out["cases count"] = len(C)
    r = []
    for h in H:
        n, m, t = clt(C, f"s{h}"); r.append({"h": h, "n": n, "short_unusual": m, "t": t})
    out["cases: short unusual by horizon"] = pd.DataFrame(r)
    C["q"] = pd.qcut(C.fc.abs().rank(method="first"), 3, labels=False)
    r = []
    for q, s in C.groupby("q"):
        for h in [5, 10]:
            n, m, t = clt(s, f"s{h}"); r.append({"absfc_third": q, "h": h, "n": n, "mean": m, "t": t,
                                                  "mean_absfc": s.fc.abs().mean(), "mean_up": s.up.mean()})
    out["cases by |fc| third"] = pd.DataFrame(r)
    r = []
    for k, s in C.groupby(C.up.clip(upper=5)):
        n, m, t = clt(s, "s5"); r.append({"up_len(5=5+)": k, "n": n, "mean": m, "t": t})
    out["cases by streak length h5"] = pd.DataFrame(r)
    r = []
    for k, s in C.groupby("coin"):
        n, m, t = clt(s, "s5"); r.append({"coin": k, "n": n, "mean": m, "t": t})
    out["cases by coin h5"] = pd.DataFrame(r)
    r = []
    for k, s in C.groupby("year"):
        n, m, t = clt(s, "s5"); r.append({"year": k, "n": n, "mean": m, "t": t})
    out["cases by year h5"] = pd.DataFrame(r)
    # down streaks: grid, by length, long-sign at h5/h10 (= minus short)
    r = []
    for h in [5, 10]:
        G = D[D.i % h == 0]
        for k, s in G[G.dn >= 1].groupby(G.dn.clip(upper=5)):
            n, m, t = clt(s, f"s{h}"); r.append({"h": h, "dn_len": k, "n": n, "short_unusual": m, "t": t})
    out["down streaks grid short-sign"] = pd.DataFrame(r)
    return out
