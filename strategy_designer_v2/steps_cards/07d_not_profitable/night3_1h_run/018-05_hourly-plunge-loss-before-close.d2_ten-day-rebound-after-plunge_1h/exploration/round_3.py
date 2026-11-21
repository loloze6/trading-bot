import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; trades = data["trades"]
    coins = list(bars.keys())
    H = 240
    cases = []
    G = []
    for c in coins:
        # coin drift over 240 bars, non-overlapping, all windows
        rs = []
        for w, b in bars[c].items():
            s = b["close"].astype(float).values
            idx = np.arange(0, len(s) - H, H)
            rs += list(s[idx + H] / s[idx] - 1)
        drift = np.mean(rs); usual = np.std(rs)
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            s = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            ma1440 = s.rolling(1440, min_periods=720).mean()
            ma720 = s.rolling(720, min_periods=480).mean()
            r1440 = s.pct_change(1440)
            above60 = s / ma1440 - 1
            above30 = s / ma720 - 1
            a = b["postRebalance_current_allocation"].astype(float)
            r1 = s.pct_change().shift(-1)
            # entry-state of current position: state at entry bar carried forward
            ent = (a > 0) & (a.shift(1).fillna(0) <= 0)
            st60 = above60.where(ent).ffill()
            st30 = above30.where(ent).ffill()
            G.append(pd.DataFrame(dict(coin=c, window=w, ts=ts, gain=a * r1,
                                       st60=st60.where(a > 0), st30=st30.where(a > 0))))
            if w in trades[c] and len(trades[c][w]):
                seen = set()
                for et in pd.to_datetime(trades[c][w]["entry_time"]):
                    i = ts.searchsorted(et, side="right") - 1
                    if i < 0 or i + H >= len(s): continue
                    cell = i // H
                    if cell in seen: continue
                    seen.add(cell)
                    u = s[i + H] / s[i] - 1 - drift
                    cases.append(dict(coin=c, u=u, st=u / usual, a60=above60[i], a30=above30[i], r1440=r1440[i]))
    C = pd.DataFrame(cases)
    def summ(x):
        return pd.Series({"n": len(x), "unusual_mean": x["u"].mean(), "t": x["u"].mean() / x["u"].std() * np.sqrt(len(x)),
                          "strength": x["st"].mean(), "p10": x["u"].quantile(.1)})
    out["cases_all"] = summ(C)
    for col in ["a60", "a30", "r1440"]:
        x = C.dropna(subset=[col])
        out["cases_by_sign_" + col] = x.groupby(x[col] > 0).apply(summ)
    x = C.dropna(subset=["a60"]).copy()
    x["q"] = pd.qcut(x["a60"], 5, labels=False)
    out["cases_by_a60_q"] = x.groupby("q").apply(lambda g: pd.concat([pd.Series({"lo": g["a60"].min(), "hi": g["a60"].max()}), summ(g)]))
    # book-like chain of hourly mean gains, masked by entry state
    P = pd.concat(G, ignore_index=True).dropna(subset=["gain"])
    res = {}
    for name, keep in [("all", np.ones(len(P), bool)),
                       ("drop_entry_below_ma60", ~(P["st60"] < 0)),
                       ("drop_entry_below_ma30", ~(P["st30"] < 0))]:
        g = P["gain"].where(keep, 0.0)
        Q = P.assign(g=g)
        Q["day"] = Q["ts"].dt.floor("D")
        d = Q.groupby(["window", "coin", "day"])["g"].apply(lambda v: (1 + v).prod() - 1).reset_index()
        dd = d.groupby(["window", "day"])["g"].mean().reset_index()
        dd["wn"] = dd["window"].str[1:].astype(int)
        dd = dd.sort_values(["wn", "day"])
        eq = (1 + dd["g"]).cumprod()
        mdd = (eq / eq.cummax() - 1).min()
        yrs = len(dd) / 365
        cagr = eq.iloc[-1] ** (1 / yrs) - 1
        res[name] = {"cagr_gross": cagr, "maxdd": mdd, "calmar_gross": cagr / -mdd,
                     "sharpe_gross": dd["g"].mean() / dd["g"].std() * np.sqrt(365),
                     "share_bars_long": (Q["g"] != 0).mean()}
    out["mask_tests"] = pd.DataFrame(res).T
    return out
