import io
import duckdb
import pandas as pd

con = duckdb.connect(database="data/exo_sql.duckdb", read_only=False)

# *********************************************************************
# CROSS JOIN EXERCICES
# *********************************************************************

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""

food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

size = '''
size
XS
M
L
XL
'''

size= pd.read_csv(io.StringIO(size))
con.execute("CREATE TABLE IF NOT EXISTS size AS SELECT * FROM size")

trademark = '''
trademark
Nike
Asphalte
Abercrombie
Lewis
'''

trademark=pd.read_csv(io.StringIO(trademark))
con.execute("CREATE TABLE IF NOT EXISTS trademark AS SELECT * FROM trademark")

data = {
    "theme": ["cross_join", "cross_join"],
    "exercice_name": ["beverages_and_food", "size_and_trademark"],
    "tables": [["beverages", "food_items"], ["size","trademark"]],
    "last_reviewed": ["2000-01-01", "1994-04-05"],
}


memory_state_df = pd.DataFrame(data)
con.execute(
    "CREATE TABLE IF NOT EXISTS memory_state_df AS SELECT * from memory_state_df"
)
