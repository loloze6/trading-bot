# Component wish list

One block per idea that needs components the catalogue does not have.

## 017-01_presettle-drop-after-uptrend_1h
- Component: settlement clock: from `timestamp`, the hours from the coming bar's start to the next funding settlement (00:00, 08:00, 16:00 UTC), that is 8 minus (coming bar's UTC hour mod 8), from 1 to 8; it grows the further the coming bar is from settlement, so a rule `between` 1 and 2 selects the bars stamped 22:00, 23:00, 06:00, 07:00, 14:00 and 15:00 | measures: situation

## 017-02_presettle-rise-after-downtrend_1h
- Component: HourOfDayComponent: the UTC hour of the coming bar (the current bar's `timestamp` plus one bar's spacing), 0 to 23, rising by one each hour; it would let a regime rule pick hours 22-23, 6-7 and 14-15, like `WeekdayComponent` does for days. | measures: situation

## 017-03_postsettle-recovery-after-uptrend_1h
- Component: HourOfDayComponent: the UTC hour of the coming bar (the current bar's timestamp plus one bar's spacing), 0 to 23, read from `timestamp`, rising by one each hour and wrapping at 24; a regime measure for rules such as "between 0 and 1, 8 and 9, 16 and 17" | measures: situation

## 017-04_postsettle-decline-after-downtrend_1h
- Component: HourOfDayComponent: the UTC hour (0 to 23) of the coming bar, taken from the current bar's `timestamp` plus one bar's spacing, like `WeekdayComponent`; it rises by one each hour and returns to 0 at midnight. A regime rule with `any_of` on hours 0–1, 8–9 and 16–17 then selects the post-settlement bars | measures: situation

## 017-05_settlement-move-reverses-after_1h
- Component: HourOfDayComponent: the UTC hour (0 to 23) of the coming bar, read from `timestamp` plus one bar's spacing; it rises by one each hour and wraps at 24, for regime rules that select the bars around 00, 08 and 16 UTC. | measures: situation
