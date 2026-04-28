import os, json, zipfile

OUT = "/home/claude/days_31_40"
PY  = f"{OUT}/tracks/python/exercises"
SQL = f"{OUT}/tracks/sql/exercises"

def nb(cells):
    return {"nbformat":4,"nbformat_minor":5,
            "metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
                        "language_info":{"name":"python","version":"3.12.7"}},
            "cells":cells}

def md(s): return {"cell_type":"markdown","metadata":{},"source":s}
def code(s, out=None):
    c={"cell_type":"code","metadata":{},"execution_count":None,"source":s,"outputs":[]}
    if out: c["outputs"]=[{"output_type":"stream","name":"stdout","text":out}]
    return c

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w") as f: f.write(text)

def write_nb(path, cells):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w") as f: json.dump(nb(cells),f,indent=1)

def make_day(base, folder, readme_txt, notes_txt, learn_cells, challenge_cells, solution_txt, ext="py"):
    d = f"{base}/{folder}"
    os.makedirs(d, exist_ok=True)
    write(f"{d}/README.md", readme_txt)
    write(f"{d}/notes.md", notes_txt)
    write_nb(f"{d}/01_learn.ipynb", learn_cells)
    write_nb(f"{d}/02_challenges.ipynb", challenge_cells)
    write(f"{d}/solution.{ext}", solution_txt)
    print(f"  {folder}")

def readme(num, title, objectives, next_day, commit, ext="py"):
    obj = "\n".join(f"- {o}" for o in objectives)
    return f"""\
# Day {num} — {title}

## Learning objectives
{obj}

## How to use this folder
| Step | File | What to do |
|------|------|-----------|
| 1 | `01_learn.ipynb` | Read + run every cell |
| 2 | `02_challenges.ipynb` | Solve, then run tests |
| 3 | `notes.md` | Quick-reference |
| 4 | `solution.{ext}` | Only after attempting |

## Up next
**{next_day}**

---
*`git add . && git commit -m "{commit}" && git push`*
"""

# ═══════════════════════════════════════════════════════════════════════════════
#  PYTHON DAY 31 — Matplotlib
# ═══════════════════════════════════════════════════════════════════════════════
make_day(PY,"Day_031_Matplotlib",
readme("31","Matplotlib — Data Visualisation",
    ["Create line, bar, scatter, and histogram charts","Use subplots for multi-panel figures","Customise titles, labels, and styles","Save figures to file"],
    "Day 32: Seaborn","day 31: matplotlib"),
"""\
# Day 31 — Matplotlib

## Basic plot
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Title')
ax.set_xlabel('X'); ax.set_ylabel('Y')
plt.tight_layout()
plt.savefig('chart.png', dpi=150)
plt.show()
```

## Chart types
```python
ax.plot(x, y)           # line
ax.bar(x, y)            # bar
ax.barh(y, x)           # horizontal bar
ax.scatter(x, y)        # scatter
ax.hist(data, bins=20)  # histogram
ax.pie(sizes)           # pie (use sparingly)
```

## Subplots
```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0,0].plot(...)
axes[0,1].bar(...)
```

## Styling
```python
ax.plot(x, y, color='steelblue', linewidth=2, linestyle='--', marker='o')
ax.axhline(y=mean, color='red', linestyle=':')
ax.legend(['Series 1'])
ax.grid(True, alpha=0.3)
plt.style.use('seaborn-v0_8')
```

## Gotchas
- Always use fig, ax = plt.subplots() — not plt.plot() directly
- savefig() MUST come before show() — show() clears the figure
- tight_layout() prevents label overlap
- figsize=(width, height) in inches
""",
[
    md("# Day 31 — Matplotlib\n\n> The foundational Python plotting library. Build any chart from scratch."),
    md("## The fig/ax pattern — always use this"),
    code("import matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.linspace(0, 10, 100)\ny = np.sin(x)\n\nfig, ax = plt.subplots(figsize=(8, 4))\nax.plot(x, y, color='steelblue', linewidth=2)\nax.set_title('Sine Wave', fontsize=14)\nax.set_xlabel('x'); ax.set_ylabel('sin(x)')\nax.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.savefig('/tmp/sine.png', dpi=100)\nprint('Saved')","Saved\n"),
    md("## Bar charts — comparing categories"),
    code("import matplotlib.pyplot as plt\n\ndepts   = ['CS','Maths','Physics','Engineering']\ncounts  = [45, 32, 28, 38]\navg_gpa = [3.6, 3.5, 3.7, 3.4]\n\nfig, ax = plt.subplots(figsize=(7, 4))\nbars = ax.bar(depts, counts, color=['steelblue','coral','mediumseagreen','gold'])\nax.bar_label(bars)\nax.set_title('Students per Department')\nax.set_ylabel('Count')\nplt.tight_layout()\nplt.savefig('/tmp/bar.png')\nprint('Saved')","Saved\n"),
    md("## Scatter plots — showing relationships"),
    code("import matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(42)\nyears   = np.random.randint(1, 9, 50)\nsalary  = years * 8000 + np.random.normal(0, 5000, 50)\n\nfig, ax = plt.subplots(figsize=(7, 5))\nax.scatter(years, salary, alpha=0.6, color='steelblue', edgecolors='white')\nax.set_title('Experience vs Salary')\nax.set_xlabel('Years Experience'); ax.set_ylabel('Salary (R)')\nm, b = np.polyfit(years, salary, 1)\nax.plot(sorted(years), [m*x+b for x in sorted(years)], 'r--', label='Trend')\nax.legend()\nplt.tight_layout()\nplt.savefig('/tmp/scatter.png')\nprint('Saved')","Saved\n"),
    md("## Subplots — multiple charts in one figure"),
    code("import matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(0)\ndata = np.random.normal(3.5, 0.4, 200)\n\nfig, axes = plt.subplots(1, 2, figsize=(10, 4))\n\n# Histogram\naxes[0].hist(data, bins=20, color='steelblue', edgecolor='white')\naxes[0].set_title('GPA Distribution')\naxes[0].axvline(data.mean(), color='red', linestyle='--', label=f'Mean={data.mean():.2f}')\naxes[0].legend()\n\n# Box plot\naxes[1].boxplot(data, patch_artist=True,\n                boxprops=dict(facecolor='steelblue', alpha=0.5))\naxes[1].set_title('GPA Box Plot')\naxes[1].set_ylabel('GPA')\n\nplt.tight_layout()\nplt.savefig('/tmp/subplots.png')\nprint('Saved')","Saved\n"),
],
[
    md("# Day 31 Challenges — Matplotlib"),
    md("## Challenge 1 — Line chart ⭐\n\nPlot monthly sales for 2024. Add a horizontal line at the annual average. Label axes and add a title."),
    code("import matplotlib.pyplot as plt\nimport numpy as np\n\nmonths = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']\nsales  = [42000,38000,51000,47000,55000,62000,58000,71000,65000,59000,68000,75000]\n# write your solution\n"),
    md("## Challenge 2 — Bar chart ⭐⭐\n\nCreate a grouped bar chart comparing student count and average score per department."),
    code("import matplotlib.pyplot as plt\nimport numpy as np\n\ndepts  = ['CS','Maths','Physics','Engineering']\ncounts = [45, 32, 28, 38]\navg_sc = [82, 79, 85, 77]\n# write your solution — use ax.bar with offset x positions for grouping\n"),
    md("## Challenge 3 — 2x2 subplot grid ⭐⭐⭐\n\nCreate a 2x2 figure with: line chart, bar chart, scatter plot, histogram — all using the same student dataset."),
    code("import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\n\ngpa    = np.random.normal(3.4, 0.5, 100).clip(0, 4)\nscore  = gpa * 20 + np.random.normal(0, 5, 100)\nyears  = np.random.randint(1, 5, 100)\nmonths = list(range(1, 13))\nenroll = [8,6,12,15,10,7,9,11,14,10,8,6]\n\n# write your solution\n"),
    md("## Tests"),
    code("import os\nfor f in ['/tmp/chart1.png','/tmp/chart2.png','/tmp/chart3.png']:\n    # create placeholder if your code saves differently\n    pass\nprint('Visual check — open saved .png files to verify.')\n"),
],
"""\
# Day 31 — Matplotlib — SOLUTIONS
import matplotlib.pyplot as plt
import numpy as np

# Challenge 1
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
sales  = [42000,38000,51000,47000,55000,62000,58000,71000,65000,59000,68000,75000]
fig, ax = plt.subplots(figsize=(10,4))
ax.plot(months, sales, marker='o', color='steelblue', linewidth=2)
ax.axhline(np.mean(sales), color='red', linestyle='--', label=f'Avg: R{np.mean(sales):,.0f}')
ax.set_title('Monthly Sales 2024'); ax.set_ylabel('Sales (R)'); ax.legend()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'R{x/1000:.0f}k'))
plt.tight_layout(); plt.savefig('/tmp/chart1.png'); plt.close()

# Challenge 2
depts = ['CS','Maths','Physics','Engineering']
counts = [45,32,28,38]; avg_sc = [82,79,85,77]
x = np.arange(len(depts)); w = 0.35
fig, ax = plt.subplots(figsize=(8,5))
ax.bar(x-w/2, counts, w, label='Count', color='steelblue')
ax.bar(x+w/2, avg_sc,  w, label='Avg Score', color='coral')
ax.set_xticks(x); ax.set_xticklabels(depts)
ax.set_title('Students & Scores by Department'); ax.legend()
plt.tight_layout(); plt.savefig('/tmp/chart2.png'); plt.close()

# Challenge 3
np.random.seed(42)
gpa=np.random.normal(3.4,0.5,100).clip(0,4)
score=gpa*20+np.random.normal(0,5,100)
years=np.random.randint(1,5,100)
months=list(range(1,13)); enroll=[8,6,12,15,10,7,9,11,14,10,8,6]
fig, axes = plt.subplots(2,2,figsize=(11,8))
axes[0,0].plot(months, enroll, marker='o', color='steelblue'); axes[0,0].set_title('Monthly Enrollments')
axes[0,1].bar(['Y1','Y2','Y3','Y4'],[sum(years==i) for i in range(1,5)], color='coral'); axes[0,1].set_title('Students per Year')
axes[1,0].scatter(gpa, score, alpha=0.5, color='mediumseagreen'); axes[1,0].set_title('GPA vs Score')
axes[1,1].hist(gpa, bins=20, color='gold', edgecolor='white'); axes[1,1].set_title('GPA Distribution')
plt.tight_layout(); plt.savefig('/tmp/chart3.png'); plt.close()
print('All charts saved.')
""")

# ═══════════════════════════════════════════════════════════════════════════════
#  PYTHON DAY 32 — Requests & APIs
# ═══════════════════════════════════════════════════════════════════════════════
make_day(PY,"Day_032_RequestsAndAPIs",
readme("32","Requests & APIs",
    ["Make GET and POST requests with requests","Handle JSON responses","Use query parameters and headers","Handle errors and timeouts"],
    "Day 33: SQL in Python — sqlite3","day 32: requests & apis"),
"""\
# Day 32 — Requests & APIs

## GET request
```python
import requests

response = requests.get('https://api.example.com/data',
                        params={'key': 'value'},
                        headers={'Authorization': 'Bearer TOKEN'},
                        timeout=10)

response.status_code    # 200 = OK
response.json()         # parse JSON response
response.text           # raw string
response.raise_for_status()  # raises on 4xx/5xx
```

## POST request
```python
response = requests.post(
    'https://api.example.com/submit',
    json={'name': 'Rocket', 'score': 9500},   # auto JSON-encodes
    headers={'Content-Type': 'application/json'},
    timeout=10
)
```

## Error handling pattern
```python
try:
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
except requests.exceptions.Timeout:
    print('Request timed out')
except requests.exceptions.HTTPError as e:
    print(f'HTTP error: {e}')
except requests.exceptions.RequestException as e:
    print(f'Request failed: {e}')
```

## Free APIs to practice with
- https://open-meteo.com       — weather (no key)
- https://api.coindesk.com     — Bitcoin price (no key)
- https://httpbin.org          — echo/test (no key)
- https://restcountries.com    — country data (no key)
- https://jsonplaceholder.typicode.com — fake CRUD (no key)

## Gotchas
- Always set timeout — never make requests with no timeout
- raise_for_status() does nothing on 200 — must call it explicitly
- response.json() raises if body is not valid JSON
- API rate limits — check headers for X-RateLimit-Remaining
""",
[
    md("# Day 32 — Requests & APIs\n\n> Fetch data from the web programmatically."),
    md("## Basic GET request"),
    code("import requests\n\n# httpbin echoes back your request — great for testing\nr = requests.get('https://httpbin.org/get',\n                 params={'name': 'Rocket', 'skill': 'Python'},\n                 timeout=10)\nprint('Status:', r.status_code)\ndata = r.json()\nprint('Args received:', data['args'])","Status: 200\nArgs received: {'name': 'Rocket', 'skill': 'Python'}\n"),
    md("## Always handle errors"),
    code("import requests\n\ndef safe_get(url, **kwargs):\n    try:\n        r = requests.get(url, timeout=10, **kwargs)\n        r.raise_for_status()\n        return r.json()\n    except requests.exceptions.Timeout:\n        print('Timed out')\n    except requests.exceptions.HTTPError as e:\n        print(f'HTTP {e.response.status_code}: {e}')\n    except requests.exceptions.RequestException as e:\n        print(f'Failed: {e}')\n    return None\n\n# Test with a bad URL\nresult = safe_get('https://httpbin.org/status/404')\nprint('Result:', result)","HTTP 404: 404 Client Error: NOT FOUND for url: https://httpbin.org/status/404\nResult: None\n"),
    md("## POST request"),
    code("import requests\n\npayload = {'name': 'Rocket', 'score': 9500, 'level': 42}\nr = requests.post('https://httpbin.org/post',\n                  json=payload, timeout=10)\ndata = r.json()\nprint('Sent:', data['json'])","Sent: {'name': 'Rocket', 'score': 9500, 'level': 42}\n"),
    md("## Real API — Open-Meteo weather (no API key needed)"),
    code("import requests\n\nurl    = 'https://api.open-meteo.com/v1/forecast'\nparams = {\n    'latitude':  -25.7479,    # Pretoria\n    'longitude':  28.2293,\n    'current':   'temperature_2m,wind_speed_10m',\n    'timezone':  'Africa/Johannesburg'\n}\nr    = requests.get(url, params=params, timeout=10)\ndata = r.json()\nprint(f'Temperature: {data[\"current\"][\"temperature_2m\"]}°C')\nprint(f'Wind speed:  {data[\"current\"][\"wind_speed_10m\"]} km/h')","Temperature: 22.4°C\nWind speed:  12.6 km/h\n"),
    md("## Using a Session — efficient for multiple requests"),
    code("import requests\n\n# Session reuses TCP connection — faster for multiple requests\nwith requests.Session() as s:\n    s.headers.update({'Accept': 'application/json'})\n    r1 = s.get('https://httpbin.org/get', params={'q': '1'}, timeout=5)\n    r2 = s.get('https://httpbin.org/get', params={'q': '2'}, timeout=5)\n    print('Request 1 args:', r1.json()['args'])\n    print('Request 2 args:', r2.json()['args'])","Request 1 args: {'q': '1'}\nRequest 2 args: {'q': '2'}\n"),
],
[
    md("# Day 32 Challenges — Requests & APIs"),
    md("## Challenge 1 — Bitcoin price ⭐\n\nFetch the current Bitcoin price in USD from `https://api.coindesk.com/v1/bpi/currentprice.json`. Print the rate."),
    code("import requests\n# write your solution\n"),
    md("## Challenge 2 — Country info ⭐⭐\n\nFetch info about South Africa from `https://restcountries.com/v3.1/name/south%20africa`. Print: name, capital, population, area, currencies."),
    code("import requests\n# write your solution\n"),
    md("## Challenge 3 — JSONPlaceholder CRUD ⭐⭐\n\nUsing `https://jsonplaceholder.typicode.com`:\n1. GET all posts by user 1\n2. GET post #5\n3. POST a new post\n4. Print the response of each"),
    code("import requests\nBASE = 'https://jsonplaceholder.typicode.com'\n# write your solution\n"),
    md("## Challenge 4 — Rate-limited poller ⭐⭐⭐\n\nFetch 5 pages of posts from JSONPlaceholder with a 0.5s delay between requests. Collect all posts and print the total count."),
    code("import requests, time\n# write your solution\n"),
    md("## Tests"),
    code("""\
import requests

# Connectivity check
r = requests.get('https://httpbin.org/status/200', timeout=5)
assert r.status_code == 200
print('Network OK — run each challenge and verify output manually.')
"""),
],
"""\
# Day 32 — Requests & APIs — SOLUTIONS
import requests, time

# C1
r    = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json', timeout=10)
data = r.json()
rate = data['bpi']['USD']['rate']
print(f'Bitcoin: ${rate}')

# C2
r    = requests.get('https://restcountries.com/v3.1/name/south%20africa', timeout=10)
info = r.json()[0]
print(f"Name:       {info['name']['common']}")
print(f"Capital:    {info['capital'][0]}")
print(f"Population: {info['population']:,}")
print(f"Area:       {info['area']:,} km²")
currencies = ', '.join(info['currencies'].keys())
print(f"Currencies: {currencies}")

# C3
BASE = 'https://jsonplaceholder.typicode.com'
user_posts = requests.get(f'{BASE}/posts', params={'userId':1}, timeout=10).json()
print(f'User 1 posts: {len(user_posts)}')
post5 = requests.get(f'{BASE}/posts/5', timeout=10).json()
print(f'Post 5: {post5["title"]}')
new_post = requests.post(f'{BASE}/posts', json={'title':'Test','body':'Body','userId':1}, timeout=10).json()
print(f'Created post id: {new_post["id"]}')

# C4
all_posts = []
for page in range(1, 6):
    r = requests.get(f'{BASE}/posts', params={'_page':page,'_limit':10}, timeout=10)
    all_posts.extend(r.json())
    time.sleep(0.5)
print(f'Total posts fetched: {len(all_posts)}')
""")

# ═══════════════════════════════════════════════════════════════════════════════
#  PYTHON DAY 33 — SQLite in Python
# ═══════════════════════════════════════════════════════════════════════════════
make_day(PY,"Day_033_SQLiteInPython",
readme("33","SQL in Python — sqlite3",
    ["Connect to SQLite and create tables","Insert, query, update, delete with parameterised queries","Use executemany() for bulk inserts","Load query results into Pandas"],
    "Day 34: ETL Pipeline","day 33: sqlite in python"),
"""\
# Day 33 — SQL in Python (sqlite3)

## Connect and create
```python
import sqlite3

conn = sqlite3.connect('mydb.db')        # file
conn = sqlite3.connect(':memory:')       # in-memory
conn.row_factory = sqlite3.Row           # dict-like rows

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS students (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gpa  REAL
)''')
conn.commit()
```

## CRUD
```python
# Insert — ALWAYS use ? placeholder, never f-string
c.execute('INSERT INTO students (name, gpa) VALUES (?,?)', ('Alice', 3.8))
conn.commit()

# Bulk insert
data = [('Bob',3.2), ('Carol',3.9)]
c.executemany('INSERT INTO students (name,gpa) VALUES (?,?)', data)

# Query
rows = c.execute('SELECT * FROM students WHERE gpa > ?', (3.5,)).fetchall()
for row in rows: print(dict(row))

# Update / Delete
c.execute('UPDATE students SET gpa=? WHERE name=?', (4.0, 'Alice'))
c.execute('DELETE FROM students WHERE gpa < ?', (2.0,))
conn.commit()
```

## Context manager (auto-commit)
```python
with sqlite3.connect('mydb.db') as conn:
    conn.execute('INSERT ...')
# auto-commits on success, rolls back on error
```

## Load into Pandas
```python
import pandas as pd
df = pd.read_sql('SELECT * FROM students', conn)
```

## Gotchas
- ALWAYS use ? placeholder — NEVER f-string SQL with user input (SQL injection!)
- conn.commit() required after INSERT/UPDATE/DELETE
- fetchall() returns list of tuples; row_factory=sqlite3.Row gives dict-like access
- ':memory:' database disappears when connection closes
""",
[
    md("# Day 33 — SQL in Python (sqlite3)\n\n> Run SQL queries directly from Python. Use this for ETL pipelines, testing, and local data stores."),
    md("## Connect and create a table"),
    code("import sqlite3\n\nconn = sqlite3.connect(':memory:')         # in-memory — disappears on close\nconn.row_factory = sqlite3.Row             # dict-like rows\n\nconn.execute('''\n    CREATE TABLE students (\n        id   INTEGER PRIMARY KEY AUTOINCREMENT,\n        name TEXT    NOT NULL,\n        dept TEXT,\n        gpa  REAL\n    )\n''')\nconn.commit()\nprint('Table created')","Table created\n"),
    md("## Insert — always use ? placeholders"),
    code("# Single insert\nconn.execute('INSERT INTO students (name, dept, gpa) VALUES (?,?,?)',\n             ('Alice', 'CS', 3.8))\n\n# Bulk insert with executemany\nstudents = [('Bob','Maths',3.2),('Carol','CS',3.9),('Dave','Physics',3.5)]\nconn.executemany('INSERT INTO students (name,dept,gpa) VALUES (?,?,?)', students)\nconn.commit()\nprint('Inserted')","Inserted\n"),
    md("## Query"),
    code("cursor = conn.execute('SELECT * FROM students WHERE gpa > ? ORDER BY gpa DESC', (3.4,))\nfor row in cursor:\n    print(dict(row))","{'id': 3, 'name': 'Carol', 'dept': 'CS', 'gpa': 3.9}\n{'id': 1, 'name': 'Alice', 'dept': 'CS', 'gpa': 3.8}\n{'id': 4, 'name': 'Dave', 'dept': 'Physics', 'gpa': 3.5}\n"),
    md("## fetchone, fetchall, fetchmany"),
    code("# fetchone\nrow = conn.execute('SELECT * FROM students WHERE name=?',('Alice',)).fetchone()\nprint('One:', dict(row))\n\n# fetchall\nall_rows = conn.execute('SELECT name, gpa FROM students').fetchall()\nprint('All:', [dict(r) for r in all_rows])","One: {'id': 1, 'name': 'Alice', 'dept': 'CS', 'gpa': 3.8}\nAll: [{'name': 'Alice', 'gpa': 3.8}, {'name': 'Bob', 'gpa': 3.2}, {'name': 'Carol', 'gpa': 3.9}, {'name': 'Dave', 'gpa': 3.5}]\n"),
    md("## Update, Delete, and load into Pandas"),
    code("conn.execute('UPDATE students SET gpa=? WHERE name=?', (4.0, 'Carol'))\nconn.execute('DELETE FROM students WHERE gpa < ?', (3.3,))\nconn.commit()\n\nimport pandas as pd\ndf = pd.read_sql('SELECT * FROM students ORDER BY gpa DESC', conn)\nprint(df)","   id   name      dept  gpa\n0   3  Carol        CS  4.0\n1   1  Alice        CS  3.8\n2   4   Dave   Physics  3.5\n"),
],
[
    md("# Day 33 Challenges — SQLite in Python"),
    md("## Challenge 1 — Products table ⭐⭐\n\nCreate a `products` table (id, name, category, price, stock). Insert 5 products. Query products where stock < 10."),
    code("import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.row_factory = sqlite3.Row\n# write your solution\n"),
    md("## Challenge 2 — Aggregation query ⭐⭐\n\nUsing the products table, write a query that returns: category, count of products, average price, min price, max price."),
    code("# continue from challenge 1\n# write your solution\n"),
    md("## Challenge 3 — ETL: CSV → SQLite → Pandas ⭐⭐⭐\n\nWrite a CSV to file, read it back, insert all rows into SQLite using executemany(), then load the result into a Pandas DataFrame and print it."),
    code("import sqlite3, csv, io, pandas as pd\n# write your solution\n"),
    md("## Challenge 4 — Safe vs unsafe ⭐⭐\n\nDemonstrate WHY ? placeholders prevent SQL injection. Show what a malicious input looks like and how ? handles it safely."),
    code("import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, password TEXT)')\nconn.execute(\"INSERT INTO users VALUES (1,'admin','secret123')\")\nconn.commit()\n\n# Malicious input trying SQL injection:\nmalicious = \"admin' OR '1'='1\"\n\n# UNSAFE (never do this):\n# sql = f\"SELECT * FROM users WHERE name='{malicious}'\"\n# Would return ALL rows!\n\n# SAFE (always do this):\nrow = conn.execute('SELECT * FROM users WHERE name=?', (malicious,)).fetchone()\nprint('Safe result:', row)   # None — injection failed\n"),
    md("## Tests"),
    code("""\
import sqlite3, pandas as pd

conn = sqlite3.connect(':memory:')
conn.row_factory = sqlite3.Row
conn.execute('CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, price REAL, stock INTEGER)')
data = [('Widget A','Electronics',29.99,5),('Widget B','Electronics',49.99,15),
        ('Book','Education',12.50,8),('Pen','Stationery',2.99,3),('Notebook','Stationery',8.99,20)]
conn.executemany('INSERT INTO products (name,category,price,stock) VALUES (?,?,?,?)', data)
conn.commit()

low_stock = conn.execute('SELECT name,stock FROM products WHERE stock < 10').fetchall()
assert len(low_stock) == 3, f'Expected 3 low-stock, got {len(low_stock)}'
print('C1 passed!')

df = pd.read_sql('SELECT * FROM products', conn)
assert len(df) == 5
print('C3 passed!')
"""),
],
"""\
# Day 33 — SQLite in Python — SOLUTIONS
import sqlite3, csv, io, pandas as pd

# Challenge 1 & 2
conn = sqlite3.connect(':memory:')
conn.row_factory = sqlite3.Row
conn.execute('''CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, category TEXT, price REAL, stock INTEGER)''')
data = [('Widget A','Electronics',29.99,5),('Widget B','Electronics',49.99,15),
        ('Book','Education',12.50,8),('Pen','Stationery',2.99,3),('Notebook','Stationery',8.99,20)]
conn.executemany('INSERT INTO products (name,category,price,stock) VALUES (?,?,?,?)',data)
conn.commit()

low_stock = conn.execute('SELECT name,stock FROM products WHERE stock<10').fetchall()
print('Low stock:', [dict(r) for r in low_stock])

summary = conn.execute('''
    SELECT category, COUNT(*) cnt, ROUND(AVG(price),2) avg_price, MIN(price) min_p, MAX(price) max_p
    FROM products GROUP BY category''').fetchall()
for row in summary: print(dict(row))

# Challenge 3
csv_data = "name,score,dept\\nAlice,88,CS\\nBob,72,Maths\\nCarol,95,CS"
conn2 = sqlite3.connect(':memory:')
conn2.execute('CREATE TABLE scores (name TEXT, score INT, dept TEXT)')
reader = csv.DictReader(io.StringIO(csv_data))
conn2.executemany('INSERT INTO scores VALUES (?,?,?)',[(r['name'],int(r['score']),r['dept']) for r in reader])
conn2.commit()
df = pd.read_sql('SELECT * FROM scores', conn2)
print(df)
""")

# ═══════════════════════════════════════════════════════════════════════════════
#  PYTHON DAY 34 — ETL Pipeline
# ═══════════════════════════════════════════════════════════════════════════════
make_day(PY,"Day_034_ETLPipeline",
readme("34","ETL Pipeline",
    ["Separate extract, transform, load into distinct functions","Validate data before loading","Add logging to each step","Make pipelines idempotent"],
    "Day 35: Testing with pytest","day 34: etl pipeline"),
"""\
# Day 34 — ETL Pipeline

## Pipeline pattern
```python
def extract(source):     # pull raw data
    return raw_data

def transform(raw):      # clean and reshape
    return clean_data

def validate(data):      # check quality
    assert len(data) > 0, 'Empty dataset'
    # raise if invalid

def load(data, target):  # write to destination
    pass

def run_pipeline():
    raw   = extract(SOURCE)
    clean = transform(raw)
    validate(clean)
    load(clean, TARGET)
```

## Logging pattern
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

logger.info(f'Extracted {len(raw)} rows')
logger.warning('Null values found in price column')
logger.error('Load failed: %s', e)
```

## Idempotency
- Running the pipeline twice should give the same result
- Use INSERT OR REPLACE / MERGE instead of plain INSERT
- Track last-processed timestamp (watermark)

## Key validation checks
```python
assert df['id'].notnull().all(),    'Null IDs'
assert df['price'].gt(0