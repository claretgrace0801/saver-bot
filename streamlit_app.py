import streamlit as st
import json
import os
from datetime import datetime

users = ["Sahiti", "Shreyas"]
options = ["Sahiti owes Shreyas", "Shreyas owes Sahiti"]

file_path = 'savers.json'

def save_data(data):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        savers = {}
        for user in users:
            savers[user] = 0
        savers["transactions"] = []
        return savers

st.session_state.savers = load_data()

st.title("Saver Bot")
st.markdown("""
This app tracks your savers.
* **Saver**: A custom currency made with love.
""")

def record_transaction(selected_option, integer_value):
    if selected_option == options[0]:
        user = "Shreyas"
    else:
        user = "Sahiti"
    st.session_state.savers[user] += integer_value
    current_datetime = datetime.now()
    st.session_state.savers["transactions"].append({"owed to": user, "savers": integer_value, "date": current_datetime.strftime('%I:%M%p on %B %d, %Y')})
    save_data(st.session_state.savers)

def delete_transaction(index):
    n = len(st.session_state.savers["transactions"])
    tr = st.session_state.savers["transactions"].pop(n-index-1)
    st.session_state.savers[tr["owed to"]] -= tr["savers"]
    save_data(st.session_state.savers)
    st.rerun()


col1, col2 = st.columns(2)

with col1:
# Create a dropdown menu in Streamlit
    selected_option = st.selectbox('Who owes who?', options)

with col2:
    integer_value = st.number_input('How many savers?', min_value=1, step=1)

col21, col22 = st.columns(2)

with col21:
    # Display the selected value
    st.write(f'Current Transaction: {selected_option} {integer_value} saver')

with col22:
    if st.button('Submit'):
        record_transaction(selected_option, integer_value)


st.header("Current Balance")
balances = st.session_state.savers.copy()
balances.pop("transactions")
st.write(balances)
ower = users[0] if st.session_state.savers[users[0]] < st.session_state.savers[users[1]] else users[1]
owed_to = users[0] if users[0] != ower else users[1]
st.subheader(f"{ower} owes {owed_to} {abs(st.session_state.savers[users[0]] - st.session_state.savers[users[1]])} savers")

st.header("Transactions")

for ind, tr in enumerate(st.session_state.savers["transactions"][::-1]):
    tr_col1, tr_col2 = st.columns(2)
    with tr_col1:
        st.write(tr)
    with tr_col2:
        if st.button("🗑", key=ind):
            delete_transaction(ind)