# Install required packages
import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import qrcode
except ImportError:
    install("qrcode")
    import qrcode  # Try importing again after installation

import streamlit as st
from PIL import Image
from io import BytesIO
from datetime import datetime

# --- Configurations ---
VAT_RATE = 0.075
currencies = {"Naira": "₦", "Dollar": "$", "Euro": "€"}
languages = ["English", "French"]  # Fixed typo here

# --- Functions ---
def generate_qr_code(purchase_address, date):
    qr_text = f"Purchase Location: {purchase_address}\nDate: {date}"
    qr = qrcode.make(qr_text)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")   
    return buffer.getvalue()

def calculate_vat_and_total(amount):
    vat = amount * VAT_RATE
    total_amount = amount + vat
    return vat, total_amount


# --- Streamlit UI ---
st.set_page_config(page_title="sales invoice App", layout= "centered")
st.title("Sales Invoice Generator")

# --- Sidebar Details ---
st.sidebar.header("Business Details")
business_name = st.sidebar.text_input("Business Name", "Your Business Name")
business_address = st.sidebar.text_input("Address", "Your Business Address")
phone = st.sidebar.text_input("Phone Number", "Your Phone Number")
email = st.sidebar.text_input("Email", "Your Email Address")    
logo = st.sidebar.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])

# --- Language and Currency Selection ---
languages = st.selectbox("Select Language", languages)
currency_lable = st.selectbox("Select Currency", list(currencies.keys()))
currency_symbol = currencies[currency_lable]

# --- Customer & Sales Entry ---
st.subheader("Customer Details")
customer_name = st.text_input("Customer Name")
purchase_address = st.text_input("purchase Address")
date_of_purchase = st.date_input("Date of Purchase", value=datetime.today())
st.subheader("Item Entry")
item_name = st.text_input("Item Name")
item_quantity = st.number_input("Item Quantity", min_value=1, value=1)
unit_price = st.number_input("Unit Price", min_value=0.0, value=0.0, step=0.01)

# --- Financial Calculations ---
subtotal = item_quantity * unit_price
vat, total = calculate_vat_and_total(subtotal)
amount_paid = st.number_input("Amount Paid", min_value=0.0, value=0.0, step=0.01)
balance = total - amount_paid

# --- QR Code Generation ---
qr_code_data = generate_qr_code(purchase_address, date_of_purchase.strftime('%Y-%m-%d'))

# --- Display Invoice ---
if st.button("Generate Invoice"):
    st.subheader("invoice preview")
    if logo:
        logo_image = Image.open(logo)
        st.image(logo_image, width=150)
    st.markdown(f"**Business Name:** {business_name}")
    st.markdown(f"**Business Address:** {business_address}")
    st.markdown(f"**Phone:** {phone}")
    st.markdown(f"**Email:** {email}")
    st.divider()
    st.markdown(f"**Customer Name:** {customer_name}")
    st.markdown(f"**Item Name:** {item_name}")
    st.markdown(f"**Item Quantity:** {item_quantity}")
    st.markdown(f"**Unit Price:** {currency_symbol}{unit_price:.2f}")
    st.markdown(f"**Subtotal:** {currency_symbol}{subtotal:.2f}")
    st.markdown(f"**VAT (7.5%):** {currency_symbol}{vat:.2f}")
    st.markdown(f"**Total:** {currency_symbol}{total:.2f}")
    st.markdown(f"**Amount Paid:** {currency_symbol}{amount_paid:.2f}")
    st.markdown(f"**Balance:** {currency_symbol}{balance:.2f}") 
    st.divider()
    st.image(qr_code_data, caption="Scan QR code to verify location and date of purchase", width=200)
    st.markdown(f"**Purchase Location:** {purchase_address}")
    st.markdown(f"**Date of Purchase:** {date_of_purchase.strftime('%Y-%m-%d')}")
    st.success("Invoice generated successfully!")