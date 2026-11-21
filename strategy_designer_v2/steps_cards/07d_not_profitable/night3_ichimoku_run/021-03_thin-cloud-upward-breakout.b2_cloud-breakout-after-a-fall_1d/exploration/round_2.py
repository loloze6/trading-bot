import numpy as np, pandas as pd

def explore(data):
    H = 26
    out = {}
    rows = []
    days_in = []
    for coin, wins in data["bars"].items():
        fr = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                fr.append(c[i + H] / c[i] - 1)
        drift = np.mean(fr); usual = np.std(fr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            hi = pd.Series(b["high"].values); lo = pd.Series(b["low"].values)
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            top = np.maximum(sa, sb).values; bot = np.minimum(sa, sb).values
            thick = (top - bot) / c
            tr = (b["regime"] == "trending").values
            seen = set()
            for i in np.where(tr)[0]:
                cell = i // H
                if cell in seen or i + H >= n:
                    continue
                seen.add(cell)
                prior = c[i] / c[i - H] - 1 if i >= H else np.nan
                rows.append(dict(coin=coin, win=w, prior=prior, thick=thick[i],
                                 dist=(c[i] - top[i]) / c[i] if not np.isnan(top[i]) else np.nan,
                                 fwd=c[i + H] / c[i] - 1 - drift,
                                 strength=(c[i + H] / c[i] - 1 - drift) / usual,
                                 rising=(sa.values[i] > sb.values[i]) if not np.isnan(top[i]) else np.nan))
        d = data["days"][coin]
        for w, dd in d.items():
            b = data["bars"][coin][w]
            days_in.append(dict(coin=coin, n=len(dd), trades=len(data["trades"][coin][w])))
    X = pd.DataFrame(rows)
    def summ(g):
        f = g["fwd"].dropna()
        return pd.Series(dict(n=len(f), mean_unusual=f.mean(),
                              t=f.mean() / (f.std(ddof=1) / np.sqrt(len(f))) if len(f) > 2 else np.nan,
                              strength=g["strength"].mean(), share_pos=(f > 0).mean()))
    out["all crosses, one per grid cell"] = summ(X)
    Xt = X.dropna(subset=["thick"]).copy()
    out["n with cloud known"] = len(Xt)
    if len(Xt) >= 6:
        Xt["q"] = pd.qcut(Xt["thick"], 3, labels=["thin", "mid", "thick"])
        out["by cloud thickness tercile"] = Xt.groupby("q").apply(summ)
        out["mean thickness by tercile"] = Xt.groupby("q")["thick"].mean()
        out["by cloud colour (senkouA>B)"] = Xt.groupby("rising").apply(summ)
    Xp = X.dropna(subset=["prior"]).copy()
    Xp["q"] = pd.qcut(Xp["prior"], 3, labels=["fall/flat", "mid", "big rise"])
    out["by prior26 tercile"] = Xp.groupby("q").apply(summ)
    out["by coin"] = X.groupby("coin").apply(summ)
    D = pd.DataFrame(days_in)
    out["trades total and days"] = pd.Series(dict(trades=D["trades"].sum(), days=D["n"].sum()))
    return out
