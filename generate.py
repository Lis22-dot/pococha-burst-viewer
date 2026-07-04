import pandas as pd

# まとめシートを読む
df = pd.read_excel(
    "data/burst.xlsx",
    sheet_name="まとめ"
)

# ランキング作成
rows = ""

for i, row in df.iterrows():

    if pd.isna(row["名前"]):
        continue

    rank = i + 1
    name = row["名前"]
    total = float(row["合計"]) * 100

    rows += f"""
    <tr>
        <td>{rank}位</td>
        <td>{name}</td>
        <td>{total:.2f}%</td>
    </tr>
    """

html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>

<meta charset="UTF-8">

<title>Pococha バーストランキング</title>

<style>

body {{
    font-family: sans-serif;
    background: #f5f5f5;
    padding: 20px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    background: white;
}}

th {{
    background: #ff5d7a;
    color: white;
    padding: 10px;
}}

td {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
}}

tr:hover {{
    background: #f7f7f7;
}}

</style>

</head>

<body>

<h1>応援バーストランキング</h1>

<table>

<tr>
<th>順位</th>
<th>ライバー</th>
<th>合計バースト</th>
</tr>

{rows}

</table>

</body>
</html>
"""

with open(
    "html/index.html",
    "w",
    encoding="utf-8"
) as f:
    f.write(html)

print("HTML生成完了")