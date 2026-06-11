import streamlit as st

st.set_page_config(
    page_title="CarryMe Store",
    page_icon="🛍️",
    layout="wide"
)

# Session State
if "cart" not in st.session_state:
    st.session_state.cart = []

# Products
products = [
    {
        "id": 1,
        "name": "PVC Waterproof Floral Table Cover",
        "category": "Table Covers",
        "price": 299,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/file_00000000f900720ba80eca2293d8bd22.png"
    },
    {
        "id": 2,
        "name": "Luxury Quilted Sofa Cover",
        "category": "Sofa Covers",
        "price": 1299,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/Sofa%20cover.png"
    },
    {
        "id": 3,
        "name": "Terracotta Necklace Set",
        "category": "Terracotta Jewellery",
        "price": 599,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260605-WA0013.jpg"
    },
    {
        "id": 4,
        "name": "Premium Cotton Towel Set",
        "category": "Towels",
        "price": 449,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260608-WA0001.jpg"
    },
    {
        "id": 5,
        "name": "Acrylic Mirror Wall Decor",
        "category": "Wall Decor",
        "price": 799,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/6c1592ecbddcb5ada6b491169c6c8bc7492ddbcf/images/file_0000000053c071faabfa8ed73bdf9dc5.png"
    }
]

# Sidebar
st.sidebar.title("🛍️ CarryMe Store")

page = st.sidebar.selectbox(
    "Menu",
    ["🏠 Home", "🛍️ Shop", "🛒 Cart", "📞 Contact"]
)

# Home
if page == "🏠 Home":
    st.title("CarryMe Store")
    st.subheader("India's Premium Home Decor Store")

    st.markdown("### Featured Products")

    cols = st.columns(3)

    for i, product in enumerate(products[:3]):
        with cols[i]:
            st.image(product["image"])
            st.write(product["name"])
            st.write(f"₹{product['price']}")

# Shop
elif page == "🛍️ Shop":
    st.title("🛍️ Shop")

    search = st.text_input("🔍 Search Products")

    categories = ["All"] + sorted(
        list(set([p["category"] for p in products]))
    )

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

            if st.button(
                "Add To Cart",
                key=f"add_{product['id']}"
            ):
                st.session_state.cart.append(product)
                st.success("Added")

# Cart
elif page == "🛒 Cart":
    st.title("🛒 Cart")

    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        total = 0

        for item in st.session_state.cart:
            st.write(
                f"{item['name']} - ₹{item['price']}"
            )
            total += item["price"]

        st.subheader(f"Total: ₹{total}")

        whatsapp_message = (
            "Hello CarryMe Store, I want to order:"
        )

        for item in st.session_state.cart:
            whatsapp_message += f"\n- {item['name']}"

        st.link_button(
            "Checkout on WhatsApp",
            f"https://wa.me/919250036334?text={whatsapp_message}"
        )

# Contact
elif page == "📞 Contact":
    st.title("Contact Us")

    st.link_button(
        "WhatsApp",
        "https://wa.me/919250036334"
    )

    st.link_button(
        "Instagram",
        "https://www.instagram.com/carryme_stores"
    )

st.divider()
st.markdown("© 2026 CarryMe Store")
