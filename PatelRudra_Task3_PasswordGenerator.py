import streamlit as st
import random
import string

st.set_page_config(page_title="Password Generator | OIBSIP", page_icon="🔐", layout="centered")

st.markdown("""
<style>
    .pwd-box {
        background: #0f3460;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-family: monospace;
        font-size: 24px;
        font-weight: 700;
        color: #e2b96f;
        letter-spacing: 2px;
        word-break: break-all;
        margin: 16px 0;
    }
    .strength-label { font-size: 16px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS    = string.digits
SYMBOLS   = "!@#$%^&*()_+-=[]{}|;:,.<>?"
AMBIGUOUS = "0O1lI"

def build_pool(low, up, dig, sym, no_amb):
    pool = ""
    if low: pool += LOWERCASE
    if up:  pool += UPPERCASE
    if dig: pool += DIGITS
    if sym: pool += SYMBOLS
    if no_amb:
        pool = "".join(c for c in pool if c not in AMBIGUOUS)
    return pool

def generate(length, pool, low, up, dig, sym):
    must = []
    if low: must.append(random.choice([c for c in LOWERCASE if c in pool]))
    if up:  must.append(random.choice([c for c in UPPERCASE if c in pool]))
    if dig: must.append(random.choice([c for c in DIGITS    if c in pool]))
    if sym: must.append(random.choice([c for c in SYMBOLS   if c in pool]))
    rest = [random.choice(pool) for _ in range(length - len(must))]
    combo = must + rest
    random.shuffle(combo)
    return "".join(combo)

def get_strength(pwd):
    score = 0
    if len(pwd) >= 8:  score += 1
    if len(pwd) >= 12: score += 1
    if len(pwd) >= 16: score += 1
    if any(c in LOWERCASE for c in pwd): score += 1
    if any(c in UPPERCASE for c in pwd): score += 1
    if any(c in DIGITS    for c in pwd): score += 1
    if any(c in SYMBOLS   for c in pwd): score += 1
    if score <= 2:   return "Weak",   "#e74c3c", score/7
    elif score <= 4: return "Fair",   "#f39c12", score/7
    elif score <= 5: return "Good",   "#2ecc71", score/7
    else:            return "Strong", "#27ae60", score/7

# ── Header ──────────────────────────────────
st.markdown("## 🔐 Password Generator")
st.markdown("*Oasis Infobyte Internship | OIBSIP*")
st.divider()

# ── Settings ────────────────────────────────
st.markdown("#### ⚙️ Settings")

length = st.slider("Password Length", min_value=6, max_value=32, value=12)

col1, col2 = st.columns(2)
with col1:
    low = st.checkbox("Lowercase (a-z)", value=True)
    up  = st.checkbox("Uppercase (A-Z)", value=True)
with col2:
    dig = st.checkbox("Digits (0-9)",    value=True)
    sym = st.checkbox("Symbols (!@#$)", value=False)

no_amb = st.checkbox("Exclude ambiguous characters  (0, O, 1, l, I)")
count  = st.number_input("Number of passwords", min_value=1, max_value=20, value=1)

# ── Generate ────────────────────────────────
if st.button("⚡ Generate Password(s)", type="primary", use_container_width=True):
    pool = build_pool(low, up, dig, sym, no_amb)

    if not pool:
        st.error("Please select at least one character type.")
    else:
        passwords = [generate(length, pool, low, up, dig, sym) for _ in range(count)]

        st.markdown("#### 🔑 Generated Password(s)")

        all_pwds = "\n".join(passwords)

        for i, pwd in enumerate(passwords, 1):
            label, color, pct = get_strength(pwd)
            st.markdown(f'<div class="pwd-box">{pwd}</div>', unsafe_allow_html=True)

            c1, c2 = st.columns([3, 1])
            with c1:
                st.progress(pct)
            with c2:
                st.markdown(f'<span class="strength-label" style="color:{color}">{label}</span>',
                            unsafe_allow_html=True)

            if count > 1 and i < count:
                st.markdown("---")

        # Copy & download
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.code(all_pwds, language=None)
        with c2:
            st.download_button(
                label="💾 Download Passwords",
                data=all_pwds,
                file_name="generated_passwords.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.info("💡 Copy from the code box on the left")

# ── Tips ────────────────────────────────────
with st.expander("💡 Password Safety Tips"):
    st.markdown("""
- Use a **different password** for every account
- Aim for **16+ characters** for strong security
- Enable **two-factor authentication** wherever possible
- Use a **password manager** to store your passwords safely
- Never share your password with anyone
    """)

st.markdown("---")
st.caption("Patel Rudra | AICTE OIB-SIP May 2026 | Python Programming Internship")
