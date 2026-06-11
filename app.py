if page == "🏠 Home":

    st.title("🛍️ CarryMe Store")
    st.subheader("India's Premium Home Decor & Lifestyle Store")

    st.image(
        "https://raw.githubusercontent.com/iefuture108-afk/carryme/cea602302447a05a2acad6b60994b469c2ba444b/images/IMG-20260608-WA0009.jpg",
        use_container_width=True
    )

    st.markdown("### 🏷️ Shop By Category")

    category_cols = st.columns(5)

    category_list = [
        "Table Covers",
        "Sofa Covers",
        "Terracotta Jewellery",
        "Towels",
        "Wall Decor"
    ]

    for i, cat in enumerate(category_list):
        with category_cols[i]:
            st.info(cat)

    st.markdown("### ⭐ Featured Products")

    featured_cols = st.columns(3)

    for i, product in enumerate(products[:6]):
        with featured_cols[i % 3]:
            st.image(product["image"], use_container_width=True)
            st.write(f"**{product['name']}**")
            st.write(f"₹{product['price']}")
