import numpy as np
import pandas as pd

from core.indicators.Indicator import Indicator


class FVGIndicator(Indicator):

    def __init__(self, data, merge_consecutive_fvg_start=False, merge_consecutive_fvg_end=False):
        self.data = data

        assert not (merge_consecutive_fvg_start and merge_consecutive_fvg_end)
        self.merge_consecutive_fvg_start = merge_consecutive_fvg_start
        self.merge_consecutive_fvg_end = merge_consecutive_fvg_end

    def calculate(self):
        fvg = np.where(
            (
                    (self.data["high"].shift(1) < self.data["low"].shift(-1))
                    & (self.data["close"] > self.data["open"])
            )
            | (
                    (self.data["low"].shift(1) > self.data["high"].shift(-1))
                    & (self.data["close"] < self.data["open"])
            ),
            np.where(self.data["close"] > self.data["open"], 1, -1),
            np.nan,
        )

        top = np.where(
            ~np.isnan(fvg),
            np.where(
                self.data["close"] > self.data["open"],
                self.data["low"].shift(-1),
                self.data["low"].shift(1),
            ),
            np.nan,
        )

        bottom = np.where(
            ~np.isnan(fvg),
            np.where(
                self.data["close"] > self.data["open"],
                self.data["high"].shift(1),
                self.data["high"].shift(-1),
            ),
            np.nan,
        )

        # if there are multiple consecutive fvg then join them together using the highest top and
        # lowest bottom and the last index
        if self.merge_consecutive_fvg_end:
            for i in range(len(fvg) - 1):
                if fvg[i] == fvg[i + 1]:
                    top[i + 1] = max(top[i], top[i + 1])
                    bottom[i + 1] = min(bottom[i], bottom[i + 1])
                    fvg[i] = top[i] = bottom[i] = np.nan

        elif self.merge_consecutive_fvg_start:
            for i in reversed(range(len(fvg) - 1)):
                if fvg[i] == fvg[i + 1]:
                    top[i] = max(top[i], top[i + 1])
                    bottom[i] = min(bottom[i], bottom[i + 1])
                    fvg[i + 1] = top[i + 1] = bottom[i + 1] = np.nan

        mitigated_index = np.zeros(len(self.data), dtype=np.int32)
        for i in np.where(~np.isnan(fvg))[0]:
            mask = np.zeros(len(self.data), dtype=np.bool_)
            if fvg[i] == 1:
                mask = self.data["low"][i + 2:] <= top[i]
            elif fvg[i] == -1:
                mask = self.data["high"][i + 2:] >= bottom[i]
            if np.any(mask):
                j = np.argmax(mask) + i + 2
                mitigated_index[i] = j

        mitigated_index = np.where(np.isnan(fvg), np.nan, mitigated_index)

        new_df = pd.DataFrame(index=self.data.index)
        new_df = new_df.assign(FVG=fvg,
                               Top=top,
                               Bottom=bottom,
                               MitigatedIndex=mitigated_index)

        return new_df
