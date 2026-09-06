import streamlit as st

# Page Configuration
st.set_page_config(page_title="Cafe Billing App", page_icon="☕", layout="centered")

st.markdown(
    """
    <h1 style='text-align: center; color: #FF4B4B;'>☕ South Indian Cafe Billing</h1>
    """,
    unsafe_allow_html=True,
)

# Menu Data with Categories and Base Prices
menu = {
    "Idli Section": {"Idli": 40, "Rava Idli": 50, "Thattu Idli": 60},
    "Dosa Section": {
        "Plain Dosa": 60,
        "Masala Dosa": 80,
        "Rava Dosa": 90,
        "GV Family Dosa": 180,
    },
    "Uttapam Section": {
        "Plain Uttapam": 70,
        "Onion Uttapam": 85,
        "Tomato Uttapam": 85,
    },
    "Vada Section": {"Medu Vada": 45, "Sambar Vada": 55},
    "Beverages Section": {
        "South Indian Filter Coffee": 30,
        "Masala Tea": 25,
        "Buttermilk": 35,
    },
}

# --- CUSTOMER & TABLE DETAILS SECTION ---
st.markdown("### 📋 Order & Customer Details")
col_c1, col_c2, col_c3 = st.columns(3)
with col_c1:
    customer_name = st.text_input("Customer Name", placeholder="Enter name")
with col_c2:
    customer_phone = st.text_input("Contact Number", placeholder="10-digit mobile")
with col_c3:
    table_number = st.selectbox(
        "Table Number", ["Table 1", "Table 2", "Table 3", "Table 4", "Parcel / Takeaway"]
    )

st.markdown("---")

# Initialize Session State for Cart
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- MENU SELECTION SECTION ---
st.markdown("### 🍽️ Menu Selection")
section_name = st.selectbox("Select Menu Category", list(menu.keys()))
selected_item = st.selectbox(
    "Select Item", list(menu[section_name].keys())
)
base_price = menu[section_name][selected_item]

# Add-on logic using Checkboxes (Multiple selection allowed)
final_price = base_price
selected_addons = []

if section_name != "Beverages Section":
    st.markdown("#### Extra Add-ons")
    add_butter = st.checkbox("Butter (Default)")
    add_ghee = st.checkbox("Extra Ghee (+₹20)")
    add_cheese = st.checkbox("Extra Cheese (+₹50)")

    if add_butter:
        selected_addons.append("Butter")
    if add_ghee:
        final_price += 20
        selected_addons.append("Ghee")
    if add_cheese:
        final_price += 50
        selected_addons.append("Cheese")
    
    variant_text = ", ".join(selected_addons) if selected_addons else "Standard"
else:
    variant_text = "Standard"
    st.info("ℹ️ Beverages do not require add-ons.")

quantity = st.number_input("Quantity", min_value=1, max_value=50, value=1)

# Add to Bill Button
if st.button("Add to Bill 🛒", use_container_width=True):
    item_entry = {
        "item": selected_item,
        "variant": variant_text,
        "price": final_price,
        "qty": quantity,
    }
    st.session_state.cart.append(item_entry)
    st.success(f"Added {quantity}x {selected_item} ({variant_text}) to the bill!")

st.markdown("---")

# --- CURRENT BILL SUMMARY SECTION ---
st.markdown("### 🧾 Current Bill Summary")

if len(st.session_state.cart) > 0:
    st.markdown(
        f"**Customer:** {customer_name if customer_name else 'Walk-in'} | "
        f"**Phone:** {customer_phone if customer_phone else 'N/A'} | "
        f"**Table:** {table_number}"
    )
    st.markdown("")

    total_amount = 0

    for idx, cart_item in enumerate(st.session_state.cart):
        item_total = cart_item["price"] * cart_item["qty"]
        total_amount += item_total

        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            st.write(
                f"**{idx+1}. {cart_item['item']}** ({cart_item['variant']}) x {cart_item['qty']} @ ₹{cart_item['price']}"
            )
        with c2:
            st.write(f"**₹{item_total}**")
        with c3:
            if st.button("❌", key=f"del_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()

    st.markdown("---")
    st.markdown(f"### Grand Total: ₹{total_amount}")

    # Clear Cart Button
    if st.button("Clear Bill 🗑️", use_container_width=True):
        st.session_state.cart = []
        st.rerun()

    # --- PRINT / RECEIPT VIEW SECTION ---
    st.markdown("---")
    if st.button("🖨️ Generate Printable Bill", use_container_width=True):
        st.markdown(
            """
        <style>
        .printable-receipt {
            background-color: white;
            color: black;
            padding: 20px;
            border-radius: 10px;
            border: 2px dashed #333;
            font-family: monospace;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        receipt_html = f"""
        <div class="printable-receipt">
            <h2 style="text-align: center; margin: 0;">☕ SOUTH INDIAN CAFE ☕</h2>
            <p style="text-align: center; margin: 5px 0;">Authentic Taste & Tradition</p>
            <hr style="border: 1px dashed black;">
            <p><b>Customer Name:</b> {customer_name if customer_name else 'Walk-in'}</p>
            <p><b>Contact No:</b> {customer_phone if customer_phone else 'N/A'}</p>
            <p><b>Table Number:</b> {table_number}</p>
            <hr style="border: 1px dashed black;">
            <table style="width:100%; text-align: left;">
                <tr><th>Item</th><th>Qty</th><th>Price</th><th>Total</th></tr>
        """
        for item in st.session_state.cart:
            t = item["price"] * item["qty"]
            receipt_html += f"<tr><td>{item['item']} ({item['variant']})</td><td>{item['qty']}</td><td>₹{item['price']}</td><td>₹{t}</td></tr>"

        receipt_html += f"""
            </table>
            <hr style="border: 1px dashed black;">
            <h3 style="text-align: right;">Grand Total: ₹{total_amount}</h3>
            <p style="text-align: center; margin-top: 15px;">🙏 Thank You! Visit Again 🙏</p>
        </div>
        """
        st.markdown(receipt_html, unsafe_allow_html=True)
        st.info("💡 Tip: You can take a screenshot or print this receipt!")

else:
    st.info("Bill is empty. Select items and customer details above to start billing.")
