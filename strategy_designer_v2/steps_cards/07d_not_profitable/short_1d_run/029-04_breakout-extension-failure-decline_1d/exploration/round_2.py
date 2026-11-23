import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 5
    col = "debug_info.components.fail_exc.last_history_value"
    rows = []; allrows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c); v = df["volume"].values
            fwd = np.full(n, np.nan); fwd[:n-H] = c[H:]/c[:n-H]-1
            hi20 = pd.Series(c).rolling(20).max().shift(1).values
            r20 = np.full(n, np.nan); r20[20:] = c[20:]/c[:-20]-1
            r5 = np.full(n, np.nan); r5[5:] = c[5:]/c[:-5]-1
            vr = v/pd.Series(v).rolling(20, min_periods=10).mean().shift(1).values
            lr = np.r_[np.nan, np.log(c[1:]/c[:-1])]
            vol20 = pd.Series(lr).rolling(20).std().values
            vol60 = pd.Series(lr).rolling(60, min_periods=30).std().values
            fc = df["forecast"].values
            for g in range(0, n-H, H):
                allrows.append((coin, fwd[g]))
            prev = 0.0; seen = set()
            for t in range(n):
                f = fc[t]
                if f <= prev-2 and f < 0:
                    cell = t//H
                    if cell not in seen and not np.isnan(fwd[t]):
                        seen.add(cell)
                        # bars since breakout & depth below old high
                        k = None
                        for j in range(1, 5):
                            if t-j >= 0 and not np.isnan(hi20[t-j]) and c[t-j] > hi20[t-j]:
                                k = j; break
                        oldhi = hi20[t-k] if k else np.nan
                        bvr = vr[t-k] if k else np.nan
                        rows.append(dict(coin=coin, fwd=fwd[t], k=k, depth=c[t]/oldhi-1 if k else np.nan,
                                         bvr=bvr, r20=r20[t], r5=r5[t], vratio=vol20[t]/vol60[t] if vol60[t] else np.nan,
                                         dayret=lr[t]))
                prev = f if f != 0 else 0.0
    A = pd.DataFrame(allrows, columns=["coin","fwd"])
    drift = A.groupby("coin")["fwd"].mean()
    C = pd.DataFrame(rows)
    C["u"] = C["fwd"] - C["coin"].map(drift)
    def agg(g):
        x = g["u"].dropna(); return pd.Series({"n":len(x),"mean_unus_long":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    out["by_k"] = C.groupby("k").apply(agg)
    for var in ["depth","bvr","r20","r5","vratio","dayret"]:
        s = C.dropna(subset=[var]).copy()
        s["q"] = pd.qcut(s[var].rank(method="first"),4,labels=False)
        out["by_"+var] = s.groupby("q").apply(agg).join(s.groupby("q")[var].median())
        lr_ = stats.linregress(s[var], s["u"])
        out["slope_"+var] = f"slope {lr_.slope:.5f} t {lr_.slope/lr_.stderr:.2f} n {len(s)}"
    return out
