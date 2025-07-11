import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="📊 Invoice Generator", layout="centered")
st.title("📦 Invoice Generator (Accounting + Tech)")

# --- Business Info ---
with st.sidebar:
    st.header("🏢 Business Details")
    business_name = st.text_input("Business Name", "Campus Eats")
    business_email = st.text_input("Email", "campuseats@email.com")
    invoice_date = st.date_input("Invoice Date", datetime.today())

# --- Client Info ---
st.subheader("👤 Client Info")
client_name = st.text_input("Client Name")
client_email = st.text_input("Client Email")

# --- Items ---
st.subheader("🧾 Items")
item_data = {
    "Item Description": [],
    "Quantity": [],
    "Unit Price (ZAR)": [],
    "Total (ZAR)": []
}

item_count = st.number_input("Number of Items", min_value=1, max_value=10, value=1)

for i in range(item_count):
    st.markdown(f"**Item {i+1}**")
    desc = st.text_input(f"Description {i+1}", key=f"desc{i}")
    qty = st.number_input(f"Quantity {i+1}", min_value=1, value=1, key=f"qty{i}")
    price = st.number_input(f"Unit Price {i+1} (ZAR)", min_value=0.0, step=1.0, key=f"price{i}")
    total = qty * price

    item_data["Item Description"].append(desc)
    item_data["Quantity"].append(qty)
    item_data["Unit Price (ZAR)"].append(price)
    item_data["Total (ZAR)"].append(total)

# --- Calculate ---
df = pd.DataFrame(item_data)
subtotal = df["Total (ZAR)"].sum()
tax = subtotal * 0.15  # 15% VAT
grand_total = subtotal + tax

st.subheader("📄 Invoice Summary")
st.dataframe(df, use_container_width=True)
st.write(f"**Subtotal:** R{subtotal:.2f}")
st.write(f"**VAT (15%):** R{tax:.2f}")
st.write(f"**Total Due:** R{grand_total:.2f}")

# --- Download Excel ---
if st.button("📥 Download Excel Invoice"):
    invoice_df = df.copy()
    invoice_df.loc[len(df.index)] = ["", "", "Total (incl. VAT)", grand_total]

    filename = f"{client_name}_invoice.xlsx"
    invoice_df.to_excel(filename, index=False)

    with open(filename, "rb") as f:
        st.download_button(
            label="📥 Click to Download Invoice",
            data=f,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
