import streamlit as st
from urllib.parse import quote

st.set_page_config(
    page_title="CarryMe Store",
    page_icon="🛍️",
    layout="wide"
)

WA_NUMBER = "919250036334"
INSTAGRAM = "https://www.instagram.com/carryme_stores"

if "cart" not in st.session_state:
    st.session_state.cart = []

products = [
    {
        "id": 1,
        "name": "PVC Waterproof Floral Table Cover",
        "category": "Table Covers",
        "price": 299,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/file_00000000f900720ba80eca2293d8bd22.png",
        "description": "Waterproof PVC floral table cover."
    },
    {
        "id": 2,
        "name": "Premium Rose Print Table Cover",
        "category": "Table Covers",
        "price": 349,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/file_00000000f3887207953b80b42ae8aa39.png",
        "description": "Elegant rose print waterproof table cover."
    },
    {
        "id": 3,
        "name": "PVC Basket Weave Table Cover",
        "category": "Table Covers",
        "price": 399,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/file_000000009eb0720bbc5b9d608913af84.png",
        "description": "Premium basket weave table cover."
    },
    {
        "id": 4,
        "name": "Luxury Dining Table Cover",
        "category": "Table Covers",
        "price": 449,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/file_0000000015687207b3385629671f534b.png",
        "description": "Luxury waterproof dining table cover."
    },
    {
        "id": 5,
        "name": "Designer Floral Table Cover",
        "category": "Table Covers",
        "price": 399,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/file_000000003c1872088551187258035193.png",
        "description": "Designer floral PVC table cover."
    },
    {
        "id": 6,
        "name": "Premium Waterproof Table Cover",
        "category": "Table Covers",
        "price": 349,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260609-WA0002.jpg",
        "description": "Premium waterproof dining table cover."
    },
    {
        "id": 7,
        "name": "Modern PVC Table Cover",
        "category": "Table Covers",
        "price": 329,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260609-WA0003.jpg",
        "description": "Modern printed PVC table cover."
    },
    {
        "id": 8,
        "name": "Elegant Dining Table Cover",
        "category": "Table Covers",
        "price": 449,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260609-WA0006.jpg",
        "description": "Elegant dining table cover."
    },
    {
        "id": 9,
        "name": "Luxury Quilted Sofa Cover",
        "category": "Sofa Covers",
        "price": 1299,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/Sofa%20cover.png",
        "description": "Premium sofa cover."
    },
    {
        "id": 10,
        "name": "Handcrafted Terracotta Necklace",
        "category": "Terracotta Jewellery",
        "price": 599,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260605-WA0013.jpg",
        "description": "Handcrafted terracotta jewellery."
    },
    {
        "id": 11,
        "name": "Terracotta Designer Jewellery Set",
        "category": "Terracotta Jewellery",
        "price": 699,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260608-WA0000.jpg",
        "description": "Designer terracotta jewellery."
    },
    {
        "id": 12,
        "name": "Premium Terracotta Necklace Set",
        "category": "Terracotta Jewellery",
        "price": 749,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260608-WA0010.jpg",
        "description": "Premium terracotta necklace."
    },
    {
        "id": 13,
        "name": "Ethnic Terracotta Beaded Necklace",
        "category": "Terracotta Jewellery",
        "price": 799,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260608-WA0011.jpg",
        "description": "Ethnic terracotta beaded jewellery."
    },
    {
        "id": 14,
        "name": "Premium Cotton Hand & Face Towel Set",
        "category": "Towels",
        "price": 449,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260608-WA0001.jpg",
        "description": "Soft absorbent cotton towels."
    },
    {
        "id": 15,
        "name": "Acrylic Mirror Wall Decor",
        "category": "Wall Decor",
        "price": 799,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/6c1592ecbddcb5ada6b491169c6c8bc7492ddbcf/images/file_0000000053c071faabfa8ed73bdf9dc5.png",
        "description": "Modern acrylic wall decor."
    },
    {
        "id": 16,
        "name": "MDF Wall Decor",
        "category": "Wall Decor",
        "price": 999,
        "image": "https://raw.githubusercontent.com/iefuture108-afk/carryme/6c1592ecbddcb5ada6b491169c6c8bc7492ddbcf/images/file_000000001788720693c13f5f09d171bd.png",
        "description": "Premium MDF wall decor."
    }
]

st.sidebar.title("🛍️ CarryMe Store")
st.sidebar.markdown("### Premium Home Decor")

page = st.sidebar.selectbox(
    "Menu",
    [
        "🏠 Home",
        "🛍️ Shop",
        "✨ AI Marketing Studio",
        "🛒 Cart",
        "📞 Contact"
    ]
)

if page == "🏠 Home":
    st.title("CarryMe Store")
    st.subheader("India's Premium Home Decor Store")

    st.markdown("### Shop By Category")

    cols = st.columns(5)

    categories = [
        "Table Covers",
        "Sofa Covers",
        "Terracotta Jewellery",
        "Towels",
        "Wall Decor"
    ]
for i, product in enumerate(products[:6])
        with cols[i]:
            st.info(cat)

    st.markdown("### Featured Products")

    cols = st.columns(3)

    for i, product in enumerate(products[:6]):
        with cols[i]:
            st.image(product["image"], use_container_width=True)
            st.write(product["name"])
            st.write(f"₹{product['price']}")

elif page == "🛍️ Shop":

    st.title("🛍️ Shop")

    search = st.text_input("🔍 Search Products")

    categories = ["All"] + sorted(
        list({p["category"] for p in products})
    )

    category = st.selectbox("Category", categories)

    filtered = []

    for p in products:

        if category != "All" and p["category"] != category:
            continue

        if search.lower() not in p["name"].lower():
            continue

        filtered.append(p)

    cols = st.columns(3)

    for idx, p in enumerate(filtered):

        with cols[idx % 3]:

            st.image(p["image"], use_container_width=True)
            st.subheader(p["name"])
            st.caption(p["description"])
            st.write(f"₹{p['price']}")

            if st.button("🛒 Add To Cart", key=f"add_{p['id']}"):
                st.session_state.cart.append(p)
                st.success("Added to cart")

elif page == "✨ AI Marketing Studio":

    st.title("✨ AI Marketing Studio")

    product_name = st.text_input("Product Name")

    features = st.text_area(
        "Product Features",
        height=150
    )

    if st.button("Generate Marketing Kit"):

        if product_name and features:

            st.subheader("📝 Product Description")

            st.code(
                f"{product_name} features {features}. "
                f"Designed for quality, durability and style."
            )

            st.subheader("📸 Instagram Caption")

            st.code(
                f"Upgrade your home with {product_name}. "
                f"✨ {features} ✨ #CarryMeStore"
            )

            st.subheader("📱 WhatsApp Message")

            st.code(
                f"Hello 👋\n\n"
                f"Check out our {product_name}.\n"
                f"{features}\n\n"
                f"Available at CarryMe Store."
            )

            st.subheader("🔍 SEO Title")

            st.code(
                f"Buy {product_name} Online | CarryMe Store"
            )

        else:
            st.error("Enter product name and features.")

elif page == "🛒 Cart":

    st.title("🛒 Cart")

    if not st.session_state.cart:
        st.info("Cart is empty")

    else:

        total = 0
        message = "Hello CarryMe Store,%0A%0AI want to order:%0A"

        for item in st.session_state.cart:

            st.write(
                f"{item['name']} - ₹{item['price']}"
            )

            total += item["price"]

            message += (
                f"- {item['name']} "
                f"(₹{item['price']})%0A"
            )

        st.subheader(f"Total: ₹{total}")

        whatsapp_url = (
            f"https://wa.me/{WA_NUMBER}?text={message}"
        )

        st.link_button(
            "💬 Checkout on WhatsApp",
            whatsapp_url
        )

elif page == "📞 Contact":

    st.title("📞 Contact Us")

    st.link_button(
        "WhatsApp",
        f"https://wa.me/{WA_NUMBER}"
    )

    st.link_button(
        "Instagram",
        INSTAGRAM
    )

st.divider()
st.markdown("© 2026 CarryMe Store")
