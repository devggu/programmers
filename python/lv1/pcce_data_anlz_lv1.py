columns = ["code", "date", "maximum", "remain"]
data = [
    [1, 20300104, 100, 80],
    [2, 20300804, 847, 37],
    [3, 20300401, 10, 8],
]
ext = "date" #기준 칼럼명
val_ext = 20300501 #이보다 작은값
sort_by = "remain" #정령 칼럼명
result = [
    [3, 20300401, 10, 8],
    [1, 20300104, 100, 80],
]

import pandas as pd

df = pd.DataFrame(data, columns=columns)
df = df[df[ext] < val_ext]
df.sort_values(by=sort_by, inplace=True)

print(df.values.tolist())