import duckdb

con = duckdb.connect(database="data/exo_sql.duckdb", read_only=False)

test = con.execute("SELECT * FROM memory_state_df").df()
print(test)
