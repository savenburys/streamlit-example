# streamlit_app.py

import streamlit as st
import snowflake.connector

# Initialize connection.
# Uses st.cache to only run once.
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

# Perform query.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from ADW_PROD.ADW_SUPPLY_CHAIN_PL.FACT_DEPOT_STOCK limit 10;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")



