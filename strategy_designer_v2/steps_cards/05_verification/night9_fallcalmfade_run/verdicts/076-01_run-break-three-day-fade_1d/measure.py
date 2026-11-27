import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    LHV = "debug_info.components.run_len.last_history_value"

    def run_counts(close):
        """Count of down closes in the run ending at the prior bar, for each bar (NaN when unknown)."""
        n = len(close)
        up = np.full(n, np.nan)
        cnt = np.full(n, np.nan)
        for i in range(1, n):
            up[i] = 1.0 if close[i] > close[i - 1] else 0.0
        for i in range(2, n):
            c = 0
            j = i - 1
            while j >= 1 and close[j] < close[j - 1] and c < 30:
                c += 1
                j -= 1
            cnt[i] = c
        return up, cnt

    # ---- per coin: situation, cases, drift ----
    active_total = 0
    active_agree = 0
    case_rows = []  # (coin, day, raw_ret, run_len)
    drift = {}

    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(close)
            up, cnt = run_counts(close)
            lhv = df[LHV].astype(float).values if LHV in df.columns else np.full(n, np.nan)

            sit = np.zeros(n, dtype=bool)
            runlen = np.full(n, np.nan)
            for i in range(n):
                if not np.isnan(up[i]) and not np.isnan(cnt[i]):
                    sit[i] = (up[i] == 1.0) and (cnt[i] >= 1)
                    if sit[i]:
                        runlen[i] = lhv[i] if not np.isnan(lhv[i]) else cnt[i]
                elif not np.isnan(lhv[i]):
                    sit[i] = lhv[i] >= 1
                    if sit[i]:
                        runlen[i] = lhv[i]

            fc = df["forecast"].astype(float).values
            act = np.isfinite(fc) & (fc != 0)
            active_total += int(act.sum())
            active_agree += int((act & sit & (fc < 0)).sum())

            # drift grid: non-overlapping 3-bar returns from positions 0, 3, 6, ...
            for k in range(0, n - H, H):
                grid_rets.append(close[k + H] / close[k] - 1.0)

            days = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").values
            # cases: first run-breaking up day in each 3-bar grid cell, with a full horizon inside the window
            for k in range(0, n, H):
                for i in range(k, min(k + H, n)):
                    if sit[i]:
                        if i + H < n:
                            coin_cases.append((coin, days[i], close[i + H] / close[i] - 1.0, runlen[i]))
                        break
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        case_rows.extend(coin_cases)

    agreement = (active_agree / active_total) if active_total > 0 else 0.0
    passed_sit = active_total > 0 and agreement >= 0.9
    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": "fewer than 90% of the bars with a non-zero forecast are run-breaking up days (close above prior close after one or more down closes) with a short forecast, as the plan's situation and side require",
            "reading": "none",
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "ret", "run"])
    cases["drift"] = cases["coin"].map(drift)
    cases = cases.dropna(subset=["ret", "drift"])
    cases["x"] = -(cases["ret"] - cases["drift"])

    n_cases = int(len(cases))
    long_c = cases[cases["run"] >= 3]
    one_c = cases[cases["run"] == 1]
    n_long = int(len(long_c))
    n_one = int(len(one_c))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    main_val = float(cases["x"].mean()) if n_cases else None
    main_t = None
    if n_cases > 0 and n_days > 1:
        dev = cases["x"] - main_val
        s = dev.groupby(cases["day"]).sum().values
        var = (n_days / (n_days - 1.0)) * np.sum(s ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        main_t = float(main_val / se) if se > 0 else None

    diff = None
    welch = None
    if n_long >= 2 and n_one >= 2:
        diff = float(long_c["x"].mean() - one_c["x"].mean())
        tt = stats.ttest_ind(long_c["x"].values, one_c["x"].values, equal_var=False)
        welch = float(tt.statistic) if np.isfinite(tt.statistic) else None

    check_pass = None
    if diff is not None and welch is not None:
        check_pass = bool(diff > 0 and welch >= 2)

    counts = {
        "cases": n_cases,
        "cases after runs of 3 or more down days": n_long,
        "cases after runs of exactly 1 down day": n_one,
        "days": n_days,
    }

    if n_cases < 100:
        status = "not observable"
        decided = f"the plan's minimum of 100 cases is not reached ({n_cases})"
    elif n_long < 30:
        status = "not observable"
        decided = f"the plan's minimum of 30 cases after runs of 3 or more down days is not reached ({n_long})"
    else:
        rej_main = main_t is not None and main_val < 0 and main_t <= -2
        rej_chk = welch is not None and diff is not None and diff < 0 and welch <= -2
        conf_main = main_t is not None and main_val > 0 and main_t >= 2
        if rej_main or rej_chk:
            status = "rejected"
            decided = ("reject: the main unusual move is negative with t <= -2" if rej_main
                       else "reject: the check difference (3+ run minus 1-day run) is negative with Welch t <= -2")
        elif conf_main and check_pass:
            status = "confirmed"
            decided = "confirm: the main unusual move is positive with t >= 2 and the check difference is positive with Welch t >= 2"
        elif conf_main:
            status = "inconclusive"
            decided = "inconclusive: the main unusual move meets the confirm rule but the supporting check (difference positive with t >= 2) fails"
        else:
            status = "inconclusive"
            decided = "inconclusive: t between -2 and 2 on the main measure and no reject rule met"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "short-signed 3-day return minus normal 3-day drift on run-breaking up days",
            "value": main_val,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": main_t}
                          if main_t is not None else None),
            "threshold": "positive with t >= 2 to confirm; negative with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "unusual move after 3+ down-day runs minus after 1-day runs (Welch t)",
            "value": diff,
            "passed": check_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are run-breaking up days recomputed from closes (close above prior close after >=1 strict down closes, the recorded run_len raw value used for run length where present), "
                    "taking the first such day in each 3-bar grid cell from each window's first row with its 3-bar return inside the window, "
                    "the normal drift being the coin's mean non-overlapping 3-bar return over all its windows, and the t using day-clustered standard errors."),
    }
