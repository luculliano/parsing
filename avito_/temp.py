import pandas as pd
from string import digits, ascii_letters

a = dict(zip(digits, ascii_letters))

df = pd.Series(a)

with pd.ExcelWriter('my_data.xlsx', mode='a') as writer:
    df.to_excel(writer, index=False, header=False)
