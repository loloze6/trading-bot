def explore(data):
    import numpy as np, pandas as pd
    rows = []
    fc_vals = []
    outs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            n = len(b)
            act = (b["regime"] == "trending")
            fc = b["forecast"].fillna(0)
            raw = b.get("debug_info.components.prior_fall.last_history_value")
            bets = (fc >= 2)
            # grid cases
            cases = 0
            for start in range(0, n, 26):
                cell = b.iloc[start:start+26]
                idx = cell.index[(fc.iloc[start:start+26] >= 2).values]
                idx = [i for i in idx if i + 26 < n]
                if len(idx):
                    cases += 1
                    i = idx[0]
                    outs.append((coin, w, fc.iloc[i], b["close"].iloc[i+26]/b["close"].iloc[i]-1))
            # crosses recomputed simply: up-cross count from active
            rows.append(dict(coin=coin, window=w, bars=n, active=int(act.sum()),
                             bets=int(bets.sum()), pos_fc_any=int((fc > 0).sum()),
                             active_fc0=int((act & (fc <= 0)).sum()),
                             active_fc_0_2=int((act & (fc > 0) & (fc < 2)).sum()),
                             active_late=int((act & (b.index + 26 >= n)).sum()),
                             cases=cases))
            fc_vals += list(fc[act].values)
    df = pd.DataFrame(rows)
    per_coin = df.groupby("coin")[["bars","active","bets","active_fc0","active_fc_0_2","active_late","cases"]].sum()
    per_coin["windows"] = df.groupby("coin").size()
    df["wnum"] = df["window"].str[1:].astype(int)
    per_win = df.groupby("wnum")[["bars","active","bets","cases"]].sum()
    fcs = pd.Series(fc_vals)
    o = pd.DataFrame(outs, columns=["coin","w","fc","ret"])
    return {"per_coin": per_coin, "per_window": per_win,
            "active_forecast_dist": fcs.describe(),
            "share_active_fc_ge2": float((fcs >= 2).mean()),
            "case_returns": o[["fc","ret"]].describe(),
            "bars_per_window": df["bars"].describe()}
