# Component wish list

One block per idea that needs components the catalogue does not have.

## 020-01_resistance-retest-turns-down_1d
- Component: TurnDownLevelProximity: from high and close over the last 90 bars, find each swing high, a bar whose high is the highest of the 2 bars on each side. Take the nearest swing-high price at or above the current close. Output how near the close sits below it, for example (1 / (1 + percent gap))^power. Its value grows from 0 toward 1 as the close rises to that level from below. | measures: situation
- Component: TurnDownLevelTouchCount: from high and close over the last 90 bars, count the swing highs whose prices lie within a band (for example 1 ATR or 2 percent) of the level the close is approaching. The output is that count, optionally times the proximity above. It grows by one with each prior turn-down at the level and is 0 when no turn lies near the close. | measures: comparison

## 020-02_support-retest-bounces-up_1d
- Component: SupportTouchCountComponent: from high, low and close over the last 90 bars, it finds the swing lows (a bar whose low is below the lows of the k bars on each side, confirmed only k bars later so there is no lookahead). It counts those whose low lies within a band (for example 1.5 percent) of the current close, only while the close has come down to that band from above (close below its own value n bars ago). Each touch is weighted by how near the close sits to it, so the value is 0 with no nearby turns and grows continuously with the number of past turns at the level and with nearness | measures: situation
