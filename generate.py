import pandas as pd

df = pd.read_excel("data/burst.xlsx")

rows = ""

for _, r in df.iterrows():
    rows += f"""
    <tr>
      <td>{r['ライバー']}</td>
      <td>{r['応援バースト']}%</td>
    </tr>
    """

html = f"""
<html>
<head>
<title>Pococha Burst</title>
</head>

<body>

<h1>応援バースト状況</h1>

<table border="1">
<tr>
<th>ライバー</th>
<th>バースト</th>
</tr>

{rows}

</table>

</body>
</html>
"""

open("html/index.html","w",encoding="utf8").write(html)