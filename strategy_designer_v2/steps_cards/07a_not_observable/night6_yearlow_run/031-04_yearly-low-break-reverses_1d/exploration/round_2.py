import numpy as np
import pandas as pd

def explore(data):
    bars = data["bars"]
    cases = []
    cy = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            fc = df["forecast"].fillna(0).values
            reg = (df["regime"] == "mean_reversion").values
            n = len(df)
            cy.append(dict(coin=coin, window=w, year=int(ts.iloc[0].year), days=n))
            low = 0.0
            taken = set()
            for i in range(n):
                if fc[i] <= 0:
                    low = 0.0
                    continue
                if reg[i] and fc[i] - low >= 2:
                    cell = i // 10
                    if cell not in taken and i + 10 < n:
                        taken.add(cell)
                        cases.append(dict(coin=coin, window=w, year=int(ts.iloc[i].year),
                                          day=ts.iloc[i].normalize(), fc=fc[i],
                                          r10=c[i+10]/c[i]-1))
                    low = fc[i]
                else:
                    low = min(low, fc[i])
    cs = pd.DataFrame(cases)
    cyt = pd.DataFrame(cy)
    coin_years = cyt.groupby("coin")["days"].sum() / 365.0
    out = {}
    out["n_cases"] = len(cs)
    out["n_distinct_days"] = cs["day"].nunique() if len(cs) else 0
    out["cases_by_coin"] = cs.groupby("coin").size() if len(cs) else "none"
    out["cases_by_year"] = cs.groupby("year").size() if len(cs) else "none"
    out["coin_years"] = coin_years
    out["cases_per_coin_year"] = float(len(cs) / coin_years.sum())
    out["regime_bars_per_coin_year"] = float(227 / coin_years.sum())
    if len(cs):
        out["r10_stats"] = cs["r10"].describe()
        out["fc_stats"] = cs["fc"].describe()
    # coin-year days per year (to see fold years)
    out["days_by_year"] = cyt.groupby("year")["days"].sum()
    return out
