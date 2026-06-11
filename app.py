import streamlit as st
import json
import os
from datetime import datetime
from urllib.parse import quote_plus

st.set_page_config(page_title="CarryMe Store", page_icon="🛍️", layout="wide")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "products": os.path.join(DATA_DIR, "products.json"),
    "reviews": os.path.join(DATA_DIR, "reviews.json"),
    "promos": os.path.join(DATA_DIR, "promo_codes.json"),
    "users": os.path.join(DATA_DIR, "users.json"),
    "orders": os.path.join(DATA_DIR, "orders.json"),
}

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


def init_file(path, default):
    if not os.path.exists(path):
        save_json(path, default)


for key, default in [
    ("products", DEFAULT_PRODUCTS),
    ("reviews", []),
    ("promos", DEFAULT_PROMOS),
    ("users", []),
    ("orders", []),
]:
    init_file(FILES[key], default)

products = load_json(FILES["products"], DEFAULT_PRODUCTS)
reviews = load_json(FILES["reviews"], [])
promo_codes = load_json(FILES["promos"], DEFAULT_PROMOS)
users = load_json(FILES["users"], [])
orders = load_json(FILES["orders"], [])

for key, default in [
    ("cart", []),
    ("user", None),
    ("order_count", 0),
    ("admin", False),
    ("applied_promo", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def avg_rating(pid):
    vals = [r["rating"] for r in reviews if r["product_id"] == pid]
    return round(sum(vals) / len(vals), 1) if vals else 0


def ai_description(product_name, category):
    return f"{product_name} is a premium {category.lower()} option designed for everyday use, comfort, and a stylish home look."


def apply_discount(total, promo_code, order_count):
    if order_count < 2:
        discount = total * 0.60
        return total - discount, discount, "60% first 2 orders discount applied"
    for promo in promo_codes:
        if promo.get("active") and promo["code"].upper() == promo_code.upper():
            if promo["type"] == "percent":
                discount = total * promo["value"] / 100
            else:
                discount = promo["value"]
            discount = min(discount, total)
            return total - discount, discount, f"Promo code {promo['code']} applied"
    return total, 0, ""


st.sidebar.title("🛍️ CarryMe Store")
page = st.sidebar.selectbox(
    "Menu",
    ["🏠 Home", "🛍️ Shop", "🛒 Cart", "⭐ Reviews", "👤 Login/Register", "📞 Contact", "🔐 Admin"]
)

if st.session_state.user:
    st.sidebar.success(f"Logged in as {st.session_state.user}")
    if st.sidebar.button("Logout", key="logout_btn"):
        st.session_state.user = None
        st.rerun()

if page == "🏠 Home":
    st.title("CarryMe Store")
    st.subheader("India's Premium Home Decor Store")
    cols = st.columns(3)
    for i, p in enumerate(products[:3]):
        with cols[i]:
            st.image(p["image"])
            st.write(p["name"])
            st.write(f"₹{p['price']}")
            st.caption(p.get("description", ""))

elif page == "🛍️ Shop":
    st.title("🛍️ Shop")
    search = st.text_input("🔍 Search Products", key="shop_search")
    categories = ["All"] + sorted({p["category"] for p in products})
    category = st.selectbox("Category", categories, key="shop_category")
    filtered = []
    for p in products:
        if category != "All" and p["category"] != category:
            continue
        if search.lower() not in p["name"].lower():
            continue
        filtered.append(p)

    if not filtered:
        st.info("No products found.")
    else:
        cols = st.columns(3)
        for i, p in enumerate(filtered):
            with cols[i % 3]:
                st.image(p["image"])
                st.subheader(p["name"])
                st.write(f"₹{p['price']}")
                st.caption(p.get("description", ""))
                st.write(f"⭐ {avg_rating(p['id'])} / 5")
                if st.button("Add To Cart", key=f"add_{p['id']}"):
                    st.session_state.cart.append(p)
                    st.success("Added")
                with st.expander("AI Description"):
                    st.write(ai_description(p["name"], p["category"]))

elif page == "🛒 Cart":
    st.title("🛒 Cart")
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        total = sum(item["price"] for item in st.session_state.cart)
        for idx, item in enumerate(st.session_state.cart):
            st.write(f"{item['name']} - ₹{item['price']}")
        promo_code = st.text_input("Promo Code", value=st.session_state.applied_promo, key="cart_promo")
        final_total, discount, note = apply_discount(total, promo_code, st.session_state.order_count)
        st.subheader(f"Total: ₹{round(final_total, 2)}")
        if discount:
            st.success(f"Discount: ₹{round(discount, 2)}")
        if note:
            st.info(note)
        st.session_state.applied_promo = promo_code

        whatsapp_message = "Hello CarryMe Store, I want to order:" + "".join(
            f"
- {item['name']}" for item in st.session_state.cart
        )
        st.link_button(
            "Checkout on WhatsApp",
            f"https://wa.me/919250036334?text={quote_plus(whatsapp_message)}",
        )

        if st.button("Place Order", key="place_order_btn"):
            st.session_state.order_count += 1
            orders.append(
                {
                    "user": st.session_state.user or "Guest",
                    "items": [x["name"] for x in st.session_state.cart],
                    "total": final_total,
                    "time": datetime.now().isoformat(),
                }
            )
            save_json(FILES["orders"], orders)
            st.success("Order saved")

        if st.button("Clear Cart", key="clear_cart_btn"):
            st.session_state.cart = []
            st.rerun()

elif page == "⭐ Reviews":
    st.title("⭐ Product Reviews")
    mapping = {p["name"]: p["id"] for p in products}
    selected_name = st.selectbox("Select Product", list(mapping.keys()), key="review_product")
    selected_id = mapping[selected_name]
    st.write(f"Average Rating: ⭐ {avg_rating(selected_id)} / 5")
    rating = st.slider("Rating", 1, 5, 5, key="review_rating")
    review_text = st.text_area("Your Review", key="review_text")
    if st.button("Submit Review", key="submit_review_btn"):
        reviews.append(
            {
                "product_id": selected_id,
                "user": st.session_state.user or "Guest",
                "rating": rating,
                "review": review_text,
                "time": datetime.now().isoformat(),
            }
        )
        save_json(FILES["reviews"], reviews)
        st.success("Review submitted")
    st.markdown("### Recent Reviews")
    selected_reviews = [r for r in reviews if r["product_id"] == selected_id]
    for r in selected_reviews[-10:][::-1]:
        st.write(f"⭐ {r['rating']} by {r['user']}")
        st.write(r["review"])
        st.caption(r["time"])

elif page == "👤 Login/Register":
    st.title("👤 Login / Register")
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        email = st.text_input("Login Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_btn"):
            found = next((u for u in users if u["email"] == email and u["password"] == password), None)
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
        if st.button("Register", key="register_btn"):
            users.append({"name": name, "email": email, "password": password})
            save_json(FILES["users"], users)
            st.success("Registered successfully")

elif page == "📞 Contact":
    st.title("Contact Us")
    st.link_button("WhatsApp", "https://wa.me/919250036334")
    st.link_button("Instagram", "https://www.instagram.com/carryme_stores")

elif page == "🔐 Admin":
    st.title("🔐 Admin Panel")
    admin_pass = st.text_input("Admin Password", type="password", key="admin_pass")
    if st.button("Enter Admin", key="admin_enter_btn"):
        st.session_state.admin = admin_pass == "carrymeadmin"
        if st.session_state.admin:
            st.success("Admin Access Granted")
        else:
            st.error("Wrong password")

    if st.session_state.admin:
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
                products.append(
                    {
                        "id": new_id,
                        "name": name,
                        "category": category,
                        "price": price,
                        "image": image,
                        "description": description,
                    }
                )
                save_json(FILES["products"], products)
                st.success("Product added")

st.divider()
st.markdown("© 2026 CarryMe Store")
