import streamlit as st
import json
import os

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
        return savers

savers = load_data()

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
    savers[user] += integer_value
    save_data(savers)

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
st.write(savers)
st.subheader(f"{users[0] if savers[users[0]] < savers[users[1]] else users[1]} owes {users[0] if savers[users[0]] > savers[users[1]] else users[1]} {abs(savers[users[0]] - savers[users[1]])} savers")