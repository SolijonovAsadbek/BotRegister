import pandas as pd
import numpy as np

# x = pd.DataFrame({'A': list(range(1, 10)), "B": list(range(1, 46, 5)), "C": list(range(1, 19, 2))})
# y = pd.Series([1.4, 4.5, np.nan, 3.5, 6])
# dates = pd.date_range('20250512', periods=7)
#
# print(x)
# print(y)
# print(dates)

dates = pd.date_range('20250506', periods=7)
df = pd.DataFrame(np.random.randn(7, 10), index=dates, columns=list('ABCDEFGHIJ'))
# print(df)

df2 = pd.DataFrame({
    "A": 1.0,
    "B": pd.Timestamp("20250512"),
    "C": pd.Series(list(range(1, 5)), index=list(range(4)), dtype="float32"),
})
print(df2)
