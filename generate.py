import pandas as pd
import requests

# Platinum
API_URL = (
    "https://api.pococha.com/v1/festivals/"
    "rank_segment_blocks/10012203700101/"
    "ranking?count=30&page=0"
)

# --------------------------
# Excel読込
# --------------------------

df = pd.read_excel(
    "data/burst.xlsx",
    sheet_name="まとめ"
)

# 必要列だけ取得
df = df[["名前", "ID", "合計"]].copy()

df = df.rename(
    columns={
        "名前": "name",
        "ID": "id",
        "合計": "burst"
    }
)

df["id"] = pd.to_numeric(
    df["id"],
    errors="coerce"
)

df["burst"] = pd.to_numeric(
    df["burst"],
    errors="coerce"
)

# --------------------------
# API取得
# --------------------------

r = requests.get(API_URL)
r.raise_for_status()

json_data = r.json()

event_rows = []

for item in json_data["ranking_ranks"]:

    event_rows.append({
        "id": item["user"]["id"],
        "event_rank": item["rank"],
        "event_point": item["score"],
        "api_name": item["user"]["name"],
    })

event_df = pd.DataFrame(event_rows)

# --------------------------
# IDで結合
# --------------------------

merged = event_df.merge(
    df,
    on="id",
    how="left"
)

# イベント順位順
merged = merged.sort_values(
    "event_rank"
)

# --------------------------
# HTML作成
# --------------------------

rows = ""

for _, row in merged.iterrows():

    burst = ""

    if pd.notna(row["burst"]):
        burst = f"{float(row['burst']) * 100:.2f}%"

    rows += f"""
    <tr>
        <td>{int(row['event_rank'])}位</td>
        <td>{row['api_name']}</td>
        <td>{burst}</td>
        <td>{int(row['event_point']):,}</td>
    </tr>
    """

html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>Pococha Ranking</title>

<style>
body {{
    font-family: sans-serif;
    margin: 20px;
}}

table {{
    border-collapse: collapse;
    width: 100%;
}}

th, td {{
    border: 1px solid #ccc;
    padding: 8px;
    text-align: left;
}}

th {{
    background: #f4f4f4;
}}

</style>
</head>

<body>

<h1>Pococha イベントランキング</h1>

<table>

<tr>
    <th>イベント順位</th>
    <th>名前</th>
    <th>合計バースト</th>
    <th>イベントpt</th>
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