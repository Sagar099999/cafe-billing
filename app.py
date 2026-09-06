import streamlit as st

st.set_page_config(page_title="South Indian Cafe Billing App", layout="centered")

st.title("🍽️ South Indian Cafe Billing")

# --- MENU DATA ---
menu = {
    "Idli Section": {
        "Idli": 70,
        "Idli Dip": 80,
        "Butter Idli": 90,
        "Podi Idli": 90,
        "Thatte Idli": 90,
        "Mini Idli": 100,
        "Mini Dip Idli": 120,
        "Mini Butter Idli": 120,
        "Mini Butter Podi Idli": 140,
        "Mini Mysore Idli": 160,
        "Mini Onion Tomato Masala Idli": 160,
        "Mini Tadka Idli": 160,
        "Mini Fry Idli": 140,
        "Mini Fry Podi Idli": 150
    },
    "Dosa Section (Butter & Cheese)": {
        "Sada Dosa": 110,
        "Podi Dosa": 140,
        "Masala Dosa": 150,
        "Mysore Masala Dosa": 150,
        "Mysore Sada Dosa": 120,
        "Mysore Paneer Masala Dosa": 180,
        "Paneer Cheese Dosa": 180,
        "Tomato Masala Dosa": 160,
        "Paneer Bhurji Dosa": 180,
        "GV Family Dosa": 400,
        "Onion Dosa": 150,
        "Onion Garlic Dosa": 160,
        "Onion Masala Dosa": 170,
        "Tomato Garlic Masala Dosa": 170,
        "Jain Mysore Masala Dosa": 160
    },
    "Rava Dosa Section": {
        "Rava Sada Dosa": 150,
        "Rava Masala Dosa": 170,
        "Rava Onion Dosa": 180,
        "Rava Onion Masala Dosa": 200,
        "Rava Mysore Masala Dosa": 190,
        "Rava Onion Mysore Masala Dosa": 210,
        "Rava Coconut Dosa": 180,
        "Rava Onion Coconut Dosa": 190,
        "Rava Onion Garlic Dosa": 180
    },
    "Uttapam Section": {
        "Sada Uttapam": 110,
        "Podi Uttapam": 140,
        "Onion Uttapam": 150,
        "Onion Tomato Uttapam": 150,
        "Onion Garlic Uttapam": 160,
        "Onion Tomato Garlic Uttapam": 160,
        "Tomato Uttapam": 150,
        "Tomato Capsicum Uttapam": 160,
        "Mix Veg Uttapam": 160
    },
    "Vada Section": {
        "Medu Vada": 80,
        "Dal Vada": 80
    },
    "Beverages Section": {
        "Filter Coffee": 50,
        "Ginger Lemon Tea": 50,
        "Tea": 40
    }
}

# Cart session state
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- ORDER SELECTION ---
section_name = st.selectbox("Select Menu Category", list(menu.keys()))
selected_item = st.selectbox("Select Item", list(menu[section_name].keys()))
base_price = menu[section_name][selected_item]

col1, col2 = st.columns(2)

with col1:
    # Beverages mein ghee/cheese ki zaroorat nahi hoti
    if section_name == "Beverages Section":
        variant = "Standard"
        st.write("Variant: Standard")
    else:
        # Dosa aur Rava Dosa mein agar GV Family Dosa hai toh cheese/ghee skip kar sakte hain
        if selected_item == "GV Family Dosa":
            variant = st.radio("Style", ["Butter (Default)", "Ghee (+₹20)"])
        else:
            variant = st.radio("Style / Add-on", ["Butter (Default)", "Ghee (+₹20)", "Cheese (+₹50)"])

with col2:
    quantity = st.number_input("Quantity", min_value=1, value=1)

# Price Calculation
final_price = base_price
if "Ghee" in variant:
    final_price += 20
elif "Cheese" in variant:
    final_price += 50

if st.button("Add to Bill 🛒", use_container_width=True):
    item_display_name = f"{selected_item} ({variant})" if variant != "Standard" else selected_item
    st.session_state.cart.append({"item": item_display_name, "price": final_price, "qty": quantity})
    st.success(f"Added: {quantity}x {item_display_name}")

st.divider()

# --- BILL SUMMARY SECTION ---
st.subheader("📋 Current Bill Summary")

if len(st.session_state.cart) > 0:
    total_amount = 0
    
    for idx, cart_item in enumerate(st.session_state.cart):
        item_total = cart_item['price'] * cart_item['qty']
        total_amount += item_total
        
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            st.write(f"**{idx+1}. {cart_item['item']}** (₹{cart_item['price']} x {cart_item['qty']})")
        with c2:
            st.write(f"₹{item_total}")
        with c3:
            if st.button("❌", key=f"del_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()

    st.markdown("---")
    st.markdown(f"### Grand Total: ₹{total_amount}")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Clear Bill 🗑️", use_container_width=True):
            st.session_state.cart = []
            st.rerun()
    with col_b:
        if st.button("Print / Finish Order ✅", use_container_width=True):
            st.success("Order completed successfully! Ready for next table.")
            st.session_state.cart = []
            st.rerun()
else:
    st.info("Bill is empty. Select items above to start billing.")
