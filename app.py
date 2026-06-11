import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="CarryMe Store",
    page_icon="🛍️",
    layout="wide"
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")
PROMOS_FILE = os.path.join(DATA_DIR, "promo_codes.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")

DEFAULT_PRODUCTS = [
    {
        "id": 1,
        "name": "PVC Waterproof Floral Table Cover",
        "category": "Table Covers",
        "price": 299,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/file_00000000f900720ba80eca2293d8bd22.png",
        "description": "A stylish waterproof table cover for daily use.",
    },
    {
        "id": 2,
        "name": "Luxury Quilted Sofa Cover",
        "category": "Sofa Covers",
        "price": 1299,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/Sofa%20cover.png",
        "description": "Elegant quilted cover designed to protect and beautify your sofa.",
    },
    {
        "id": 3,
        "name": "Terracotta Necklace Set",
        "category": "Terracotta Jewellery",
        "price": 599,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260605-WA0013.jpg",
        "description": "Handcrafted terracotta jewellery with a traditional finish.",
    },
    {
        "id": 4,
        "name": "Premium Cotton Towel Set",
        "category": "Towels",
        "price": 449,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260608-WA0001.jpg",
        "description": "Soft and absorbent towel set for everyday comfort.",
    },
    {
        "id": 5,
        "name": "Acrylic Mirror Wall Decor",
        "category": "Wall Decor",
        "price": 799,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/6c1592ecbddcb5ada6b491169c6c8bc7492ddbcf/images/file_0000000053c071faabfa8ed73bdf9dc5.png",
        "description": "Modern wall decor piece that adds a premium look to your room.",
    },
]

DEFAULT_PROMOS = [
    {"code": "WELCOME10", "type": "percent", "value": 10, "active": True},
    {"code": "SAVE100", "type": "flat", "value": 100, "active": True},
]


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def init_data():
    if not os.path.exists(PRODUCTS_FILE):
        save_json(PRODUCTS_FILE, DEFAULT_PRODUCTS)
    if not os.path.exists(PROMOS_FILE):
        save_json(PROMOS_FILE, DEFAULT_PROMOS)
    if not os.path.exists(REVIEWS_FILE):
        save_json(REVIEWS_FILE, [])
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, [])
    if not os.path.exists(ORDERS_FILE):
        save_json(ORDERS_FILE, [])


init_data()

products = load_json(PRODUCTS_FILE, DEFAULT_PRODUCTS)
promo_codes = load_json(PROMOS_FILE, DEFAULT_PROMOS)
reviews = load_json(REVIEWS_FILE, [])
users = load_json(USERS_FILE, [])
orders = load_json(ORDERS_FILE, [])

if "cart" not in st.session_state:
    st.session_state.cart = []
if "user" not in st.session_state:
    st.session_state.user = None
if "order_count" not in st.session_state:
    st.session_state.order_count = 0
if "admin" not in st.session_state:
    st.session_state.admin = False
if "applied_promo" not in st.session_state:
    st.session_state.applied_promo = ""


def get_product(pid):
    for p in products:
        if p["id"] == pid:
            return p
    return None


def product_reviews(pid):
    return [r for r in reviews if r["product_id"] == pid]


def avg_rating(pid):
    pr = product_reviews(pid)
    if not pr:
        return 0
    return round(sum(r["rating"] for r in pr) / len(pr), 1)


def ai_description(product_name, category):
    return f"{product_name} is a premium {category.lower()} option designed for everyday use, comfort, and a stylish home look."


def apply_discount(total, promo_code, order_count):
    discount = 0
    note = ""
    if order_count < 2:
        discount = total * 0.60
        note = "60% first 2 orders discount applied"
    else:
        for promo in promo_codes:
            if promo["active"] and promo["code"].upper() == promo_code.upper():
                if promo["type"] == "percent":
                    discount = total * promo["value"] / 100
                elif promo["type"] == "flat":
                    discount = promo["value"]
                note = f"Promo code {promo['code']} applied"
                break
    discount = min(discount, total)
    return total - discount, discount, note


st.sidebar.title("🛍️ CarryMe Store")

menu = st.sidebar.selectbox(
    "Menu",
    ["🏠 Home", "🛍️ Shop", "🛒 Cart", "⭐ Reviews", "👤 Login/Register", "📞 Contact", "🔐 Admin"]
)

if st.session_state.user:
    st.sidebar.success(f"Logged in as {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

if menu == "🏠 Home":
    st.title("CarryMe Store")
    st.subheader("India's Premium Home Decor Store")
    st.markdown("### Featured Products")
    cols = st.columns(3)
    for i, product in enumerate(products[:3]):
        with cols[i]:
            st.image(product["image"])
            st.write(product["name"])
            st.write(f"₹{product['price']}")
            st.caption(product.get("description", ""))

elif menu == "🛍️ Shop":
    st.title("🛍️ Shop")
    search = st.text_input("🔍 Search Products")
    categories = ["All"] + sorted(list(set([p["category"] for p in products])))
    category = st.selectbox("Category", categories)
    filtered = []
    for product in products:
        if category != "All" and product["category"] != category:
            continue
        if search.lower() not in product["name"].lower():
            continue
        filtered.append(product)
    cols = st.columns(3)
    for i, product in enumerate(filtered):
        with cols[i % 3]:
            st.image(product["image"])
            st.subheader(product["name"])
            st.write(f"₹{product['price']}")
            st.caption(product.get("description", ""))
            st.write(f"⭐ {avg_rating(product['id'])} / 5")
            if st.button("Add To Cart", key=f"add_{product['id']}"):
                st.session_state.cart.append(product)
                st.success("Added")
            with st.expander("AI Description"):
                st.write(ai_description(product["name"], product["category"]))

elif menu == "🛒 Cart":
    st.title("🛒 Cart")
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        total = 0
        for item in st.session_state.cart:
            st.write(f"{item['name']} - ₹{item['price']}")
            total += item["price"]
        promo_code = st.text_input("Promo Code", value=st.session_state.applied_promo)
        final_total, discount, note = apply_discount(total, promo_code, st.session_state.order_count)
        st.subheader(f"Total: ₹{final_total}")
        if discount > 0:
            st.success(f"Discount: ₹{round(discount, 2)}")
        if note:
            st.info(note)
        st.session_state.applied_promo = promo_code
        whatsapp_message = "Hello CarryMe Store, I want to order:"
        for item in st.session_state.cart:
            whatsapp_message += f"
- {item['name']}"
        if st.button("Place Order"):
            st.session_state.order_count += 1
            orders.append({
                "user": st.session_state.user or "Guest",
                "items": [x["name"] for x in st.session_state.cart],
                "total": final_total,
                "time": datetime.now().isoformat()
            })
            save_json(ORDERS_FILE, orders)
            st.success("Order saved")
        st.link_button(
            "Checkout on WhatsApp",
            f"https://wa.me/919250036334?text={whatsapp_message}"
        )
        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.rerun()

elif menu == "⭐ Reviews":
    st.title("⭐ Product Reviews")
    product_names = {p["name"]: p["id"] for p in products}
    selected_name = st.selectbox("Select Product", list(product_names.keys()))
    selected_id = product_names[selected_name]
    st.write(f"Average Rating: ⭐ {avg_rating(selected_id)} / 5")
    st.markdown("### Add Review")
    rating = st.slider("Rating", 1, 5, 5)
    review_text = st.text_area("Your Review")
    if st.button("Submit Review"):
        reviews.append({
            "product_id": selected_id,
            "user": st.session_state.user or "Guest",
            "rating": rating,
            "review": review_text,
            "time": datetime.now().isoformat()
        })
        save_json(REVIEWS_FILE, reviews)
        st.success("Review submitted")
    st.markdown("### Recent Reviews")
    for r in reversed(product_reviews(selected_id))[-10:]:
        st.write(f"⭐ {r['rating']} by {r['user']}")
        st.write(r["review"])
        st.caption(r["time"])

elif menu == "👤 Login/Register":
    st.title("👤 Login / Register")
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        email = st.text_input("Login Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            found = None
            for u in users:
                if u["email"] == email and u["password"] == password:
                    found = u
                    break
            if found:
                st.session_state.user = found["name"]
                st.success("Logged in")
                st.rerun()
            else:
                st.error("Invalid credentials")
    with tab2:
        name = st.text_input("Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Register"):
            users.append({"name": name, "email": email, "password": password})
            save_json(USERS_FILE, users)
            st.success("Registered successfully")

elif menu == "📞 Contact":
    st.title("Contact Us")
    st.link_button("WhatsApp", "https://wa.me/919250036334")
    st.link_button("Instagram", "https://www.instagram.com/carryme_stores")

elif menu == "🔐 Admin":
    st.title("🔐 Admin Panel")
    admin_pass = st.text_input("Admin Password", type="password")
    if st.button("Enter Admin"):
        if admin_pass == "carrymeadmin":
            st.session_state.admin = True
        else:
            st.error("Wrong password")
    if st.session_state.admin:
        st.success("Admin Access Granted")
        st.markdown("### Products")
        for p in products:
            st.write(f"{p['id']}. {p['name']} - ₹{p['price']}")
        st.markdown("### Promo Codes")
        for promo in promo_codes:
            st.write(promo)
        st.markdown("### Orders")
        for o in orders[-10:]:
            st.write(o)
        st.markdown("### Add Product")
        with st.form("add_product"):
            name = st.text_input("Product Name")
            category = st.text_input("Category")
            price = st.number_input("Price", min_value=1, step=1)
            image = st.text_input("Image URL")
            description = st.text_area("Description")
            submitted = st.form_submit_button("Save Product")
            if submitted:
                new_id = max([p["id"] for p in products]) + 1 if products else 1
                products.append({"id": new_id, "name": name, "category": category, "price": price, "image": image, "description": description})
                save_json(PRODUCTS_FILE, products)
                st.success("Product added")

st.divider()
st.markdown("© 2026 CarryMe Store")
