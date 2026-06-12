import streamlit as st

st.set_page_config(page_title="CA Teacher", page_icon="👨‍🏫", layout="wide")

# ---------- Simple CSS for clean look ----------
st.markdown("""
<style>
.teacher-header {
    background: #2c3e50;
    padding: 1rem;
    border-radius: 12px;
    color: white;
    text-align: center;
}
.step-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    border-left: 5px solid #28a745;
}
.link-btn {
    background: #007bff;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# ---------- Helper: Show step-by-step guide ----------
def show_gst_registration():
    st.markdown("### 📋 Step‑by‑Step: GST Registration (for E‑commerce Seller)")
    st.markdown("""
    <div class="step-card">
    ✅ <strong>Step 1:</strong> Get your PAN card (personal is enough).<br>
    ✅ <strong>Step 2:</strong> Keep address proof (electricity bill, rent agreement).<br>
    ✅ <strong>Step 3:</strong> Have a cancelled cheque or bank statement.<br>
    ✅ <strong>Step 4:</strong> Click the link below → New Registration → Fill Part A (PAN, mobile, email).<br>
    ✅ <strong>Step 5:</strong> Note down the TRN number.<br>
    ✅ <strong>Step 6:</strong> Login with TRN → Fill Part B (business details).<br>
    ✅ <strong>Step 7:</strong> Upload documents → Submit → Get ARN.<br>
    ✅ <strong>Step 8:</strong> Within 7 days you get GSTIN.
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<a href="https://www.gst.gov.in" target="_blank" class="link-btn">🔗 Open GST Portal →</a>', unsafe_allow_html=True)

def show_itr_guide():
    st.markdown("### 📋 Which ITR Form Should You Use?")
    opt = st.radio("Select your income type:", [
        "Salary + one house property + interest (no business)",
        "Capital gains / multiple houses / foreign assets",
        "Business or professional income (regular accounting)",
        "Business with presumptive tax (44AD/44ADA)"
    ])
    if "Salary" in opt:
        st.success("✅ You need *ITR-1 (Sahaj)* – easiest form.")
    elif "Capital gains" in opt:
        st.success("✅ You need *ITR-2*.")
    elif "Business or professional" in opt and "presumptive" not in opt:
        st.success("✅ You need *ITR-3*.")
    else:
        st.success("✅ You need *ITR-4 (Sugam)*.")
    st.markdown(f'<a href="https://www.incometax.gov.in" target="_blank" class="link-btn">🔗 File ITR Here →</a>', unsafe_allow_html=True)
    st.caption("Due dates: 31 July (no audit) | 31 October (audit required)")

def show_penalty_calculator():
    st.markdown("### ⚠️ Late Fee & Penalty Calculator")
    tax_due = st.number_input("Tax amount you forgot to pay (₹)", min_value=0, value=5000)
    days = st.number_input("How many days late?", min_value=0, value=15)
    late_fee = days * 50
    interest = tax_due * 0.18 * (days / 365)
    total = late_fee + interest
    st.metric("Late Fee (₹50/day)", f"₹{late_fee:,.0f}")
    st.metric("Interest (18% per year)", f"₹{interest:,.0f}")
    st.metric("Total Penalty", f"₹{total:,.0f}", delta="Pay now to stop more interest")
    st.info("💡 If you had zero sales (nil return), late fee is only ₹20/day.")

def show_tcs_guide():
    st.markdown("### 🏦 TCS on Amazon / Flipkart (for sellers)")
    st.markdown("""
    <div class="step-card">
    ✅ Amazon/Flipkart deducts <strong>1% TCS</strong> before paying you.<br>
    ✅ This TCS is <strong>your money</strong> – you can claim it back.<br>
    ✅ How to claim:<br>
    &nbsp;&nbsp;1. Download your GSTR-2B from GST portal on 14th of next month.<br>
    &nbsp;&nbsp;2. Check the "TCS Credit" section.<br>
    &nbsp;&nbsp;3. The credit will auto‑fill in your GSTR‑3B.<br>
    ✅ Always match marketplace report with GSTR‑2B before filing.
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<a href="https://services.gst.gov.in/services/login" target="_blank" class="link-btn">🔗 Check TCS Credit →</a>', unsafe_allow_html=True)

# ---------- Main App ----------
st.markdown('<div class="teacher-header"><h1>👨‍🏫 CA Teacher</h1><p>Your patient guide for GST, ITR & penalties</p></div>', unsafe_allow_html=True)

# Sidebar – Choose a topic
st.sidebar.title("📚 What do you want to do?")
task = st.sidebar.selectbox("Select a task:", [
    "📋 Register for GST",
    "📝 File Income Tax Return (ITR)",
    "💰 Calculate Late Fee / Penalty",
    "🏦 Understand TCS on Amazon/Flipkart"
])

# Main area – Show the guide
if task == "📋 Register for GST":
    show_gst_registration()
elif task == "📝 File Income Tax Return (ITR)":
    show_itr_guide()
elif task == "💰 Calculate Late Fee / Penalty":
    show_penalty_calculator()
else:
    show_tcs_guide()

# Footer – Quick tips
st.markdown("---")
st.caption("👨‍🏫 *Teacher’s Tip:* Always keep your PAN card and address proof ready before starting any registration. For any doubt, ask your local CA friend.")

# Optional: Chat for common questions
with st.expander("💬 Ask a quick question (like a teacher)"):
    q = st.text_input("Your question:", placeholder="e.g., What documents for GST?")
    if q:
        if "document" in q.lower():
            st.info("📄 Documents: PAN, Aadhaar, address proof, bank statement/cancelled cheque, photo.")
        elif "due date" in q.lower():
            st.info("📅 GSTR-3B due by 20th of next month. ITR due 31 July.")
        else:
            st.info("👨‍🏫 I'm a simple teacher. For complex questions, please select one of the tasks on the left.")
