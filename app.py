"""
NovaTech Electronics — Dynamic Retail Dashboard & Quick-Commerce App
=====================================================================
Run with:  streamlit run app.py

A split-screen dynamic dashboard:
  LEFT  half  -> Live inventory dashboard (table + Plotly analytics), scrollable
  RIGHT half  -> 15 product showcase boxes (zoomable images, marketing videos),
                 scrollable, syncs with table selection

Also includes: cart, checkout, payment-gateway simulation, quick-commerce style
order tracking (Blinkit/Zepto-like), a spin-the-wheel discount game, rotating
marketing banner/ads, background music, and TextBlob-powered review sentiment.
"""
import copy
import random
import time
import uuid

import pandas as pd
import plotly.express as px
import streamlit as st

from data.products import PRODUCTS, DISCOUNT_CODES, MARKETING_BANNERS
from utils.styles import CUSTOM_CSS
from utils.sentiment import analyze_reviews, aggregate_sentiment
from utils.spin_wheel import build_wheel_html, pick_winner

MUSIC_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

# ----------------------------------------------------------------------------
# PAGE CONFIG + CSS
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="NovaTech Electronics | Live Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SESSION STATE INIT
# ----------------------------------------------------------------------------
def init_state():
    if "products" not in st.session_state:
        st.session_state.products = copy.deepcopy(PRODUCTS)
    if "cart" not in st.session_state:
        st.session_state.cart = {}          # {product_id: qty}
    if "selected_product" not in st.session_state:
        st.session_state.selected_product = None
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    if "discount_code" not in st.session_state:
        st.session_state.discount_code = None   # (code, percent)
    if "order" not in st.session_state:
        st.session_state.order = None
    if "music_on" not in st.session_state:
        st.session_state.music_on = False
    if "last_spin" not in st.session_state:
        st.session_state.last_spin = None


init_state()


def get_product(pid):
    for p in st.session_state.products:
        if p["id"] == pid:
            return p
    return None


def add_to_cart(pid, qty=1):
    prod = get_product(pid)
    if not prod:
        return
    if prod["quantity"] < qty:
        st.toast(f"⚠️ Only {prod['quantity']} units of {prod['name']} left in stock!")
        return
    prod["quantity"] -= qty
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + qty
    st.toast(f"🛒 Added {prod['name']} to cart")


def remove_from_cart(pid, qty=1):
    if pid not in st.session_state.cart:
        return
    prod = get_product(pid)
    current = st.session_state.cart[pid]
    new_qty = current - qty
    if new_qty <= 0:
        del st.session_state.cart[pid]
        if prod:
            prod["quantity"] += current
    else:
        st.session_state.cart[pid] = new_qty
        if prod:
            prod["quantity"] += qty


def cart_line_items():
    items = []
    for pid, qty in st.session_state.cart.items():
        prod = get_product(pid)
        if not prod:
            continue
        unit_price = prod["price"] * (1 - prod["discount"] / 100)
        items.append({
            "id": pid, "name": prod["name"], "qty": qty,
            "unit_price": unit_price, "line_total": unit_price * qty,
            "image": prod["image"],
        })
    return items


def cart_totals():
    items = cart_line_items()
    subtotal = sum(i["line_total"] for i in items)
    discount_pct = st.session_state.discount_code[1] if st.session_state.discount_code else 0
    promo_discount = subtotal * discount_pct / 100
    delivery_fee = 0 if subtotal >= 999 or subtotal == 0 else 49
    total = subtotal - promo_discount + delivery_fee
    return subtotal, promo_discount, delivery_fee, total


# ----------------------------------------------------------------------------
# SIDEBAR — Navigation / journey map / music / cart summary
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ NovaTech Electronics")
    st.caption("Dynamic retail dashboard & quick-commerce demo")

    journey = ["Dashboard", "Cart", "Checkout", "Track Order", "Spin & Win"]
    icons = {"Dashboard": "🏠", "Cart": "🛒", "Checkout": "💳",
             "Track Order": "📦", "Spin & Win": "🎡"}
    choice = st.radio(
        "Navigate",
        journey,
        format_func=lambda x: f"{icons[x]}  {x}",
        index=journey.index(st.session_state.page),
    )
    st.session_state.page = choice

    st.divider()
    cart_count = sum(st.session_state.cart.values())
    subtotal, promo_discount, delivery_fee, total = cart_totals()
    st.markdown(
        f'<span class="metric-pill">🛒 {cart_count} items</span>'
        f'<span class="metric-pill">₹{total:,.0f} total</span>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("#### 🎵 Store Music")
    st.session_state.music_on = st.toggle("Play background music", value=st.session_state.music_on)
    if st.session_state.music_on:
        st.audio(MUSIC_URL, format="audio/mp3", autoplay=True, loop=True)

    st.divider()
    if st.session_state.discount_code and st.session_state.discount_code[1] > 0:
        st.success(f"Promo applied: {st.session_state.discount_code[0]} "
                   f"(-{st.session_state.discount_code[1]}%)")

# ----------------------------------------------------------------------------
# TOP MARKETING MARQUEE (ads)
# ----------------------------------------------------------------------------
banner_text = "     •     ".join(MARKETING_BANNERS * 2)
st.markdown(
    f'<div class="marquee-wrap"><div class="marquee-text">{banner_text}</div></div>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# PAGE: DASHBOARD  (split-screen: left = table/analytics, right = product boxes)
# ----------------------------------------------------------------------------
def render_dashboard():
    left, right = st.columns(2, gap="medium")

    # ---------------- LEFT HALF: Dynamic dashboard ----------------
    with left:
        st.markdown('<div class="panel-header">📊 Live Inventory Dashboard</div>',
                     unsafe_allow_html=True)
        with st.container(height=780, border=True):
            df = pd.DataFrame(st.session_state.products)[
                ["id", "name", "category", "price", "quantity", "discount", "rating"]
            ].rename(columns={
                "id": "ID", "name": "Product", "category": "Category",
                "price": "Price (₹)", "quantity": "Stock Qty",
                "discount": "Discount %", "rating": "Rating",
            })

            st.markdown("##### 🔎 Click a row to preview it on the right panel")
            event = st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                key="dash_table",
                on_select="rerun",
                selection_mode="single-row",
                column_config={
                    "Price (₹)": st.column_config.NumberColumn(format="₹%d"),
                    "Discount %": st.column_config.ProgressColumn(
                        min_value=0, max_value=30, format="%d%%"),
                    "Rating": st.column_config.NumberColumn(format="⭐ %.1f"),
                },
            )
            if event.selection.rows:
                row_idx = event.selection.rows[0]
                st.session_state.selected_product = int(df.iloc[row_idx]["ID"])

            st.divider()
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total SKUs", len(st.session_state.products))
            m2.metric("Units in Stock", int(df["Stock Qty"].sum()))
            m3.metric("Avg. Discount", f"{df['Discount %'].mean():.1f}%")
            m4.metric("Avg. Rating", f"{df['Rating'].mean():.2f} ⭐")

            st.markdown("##### 📈 Stock levels by product")
            fig_bar = px.bar(
                df.sort_values("Stock Qty"), x="Stock Qty", y="Product",
                orientation="h", color="Discount %",
                color_continuous_scale="Sunsetdark",
                height=420,
            )
            fig_bar.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="white", margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("##### 💰 Price vs. Rating by category")
            fig_scatter = px.scatter(
                df, x="Price (₹)", y="Rating", size="Stock Qty", color="Category",
                hover_name="Product", height=380,
            )
            fig_scatter.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="white", margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

            st.markdown("##### 🎯 Sponsored / Promo tiles")
            p1, p2, p3 = st.columns(3)
            for col, title, sub in zip(
                [p1, p2, p3],
                ["Refer & Earn", "Combo Deals", "New Launch"],
                ["Get ₹200 per friend", "Buy 2 accessories, save 10%", "ImmerseVR One is live"],
            ):
                col.markdown(
                    f'<div class="product-card"><div class="product-badge">AD</div>'
                    f'<div class="product-title">{title}</div>'
                    f'<div style="color:#bbb;font-size:12px;">{sub}</div></div>',
                    unsafe_allow_html=True,
                )

    # ---------------- RIGHT HALF: Product showcase boxes ----------------
    with right:
        st.markdown('<div class="panel-header">🛍️ Product Showcase (15 items)</div>',
                     unsafe_allow_html=True)
        with st.container(height=780, border=True):
            products = st.session_state.products
            cols_per_row = 3
            for row_start in range(0, len(products), cols_per_row):
                row_products = products[row_start:row_start + cols_per_row]
                cols = st.columns(cols_per_row)
                for col, prod in zip(cols, row_products):
                    render_product_box(col, prod)


def render_product_box(col, prod):
    is_selected = st.session_state.selected_product == prod["id"]
    with col:
        with st.container(border=True):
            card_class = "product-card selected" if is_selected else "product-card"
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)

            st.markdown(
                f'<div class="zoom-wrap"><img src="{prod["image"]}" /></div>',
                unsafe_allow_html=True,
            )
            st.markdown(f'<div class="product-title">{prod["name"]}</div>',
                        unsafe_allow_html=True)

            discounted = prod["price"] * (1 - prod["discount"] / 100)
            st.markdown(
                f'<span class="product-price">₹{discounted:,.0f}</span>'
                f'<span class="product-strike">₹{prod["price"]:,.0f}</span> '
                f'<span class="product-badge">{prod["discount"]}% OFF</span>',
                unsafe_allow_html=True,
            )
            stock_cls = "stock-low" if prod["quantity"] < 10 else "stock-ok"
            stock_txt = "Only a few left!" if prod["quantity"] < 10 else "In stock"
            st.markdown(
                f'<div class="{stock_cls}">{stock_txt} · Qty: {prod["quantity"]}</div>',
                unsafe_allow_html=True,
            )

            b1, b2 = st.columns(2)
            if b1.button("👁 View", key=f"view_{prod['id']}", use_container_width=True):
                st.session_state.selected_product = (
                    None if is_selected else prod["id"]
                )
                st.rerun()
            if b2.button("➕ Add", key=f"add_{prod['id']}", use_container_width=True):
                add_to_cart(prod["id"])
                st.rerun()

            if is_selected:
                st.video(prod["video"])
                st.markdown(f"<div style='color:#ccc;font-size:13px;'>{prod['description']}</div>",
                            unsafe_allow_html=True)

                avg_sent = aggregate_sentiment(prod["reviews"])
                sent_label = "🟢 Mostly Positive" if avg_sent > 0.15 else (
                    "🔴 Mostly Negative" if avg_sent < -0.15 else "🟡 Mixed / Neutral")
                st.caption(f"Customer sentiment: {sent_label}  (score {avg_sent:+.2f})")

                with st.expander("💬 Customer Reviews (TextBlob sentiment)"):
                    for r in analyze_reviews(prod["reviews"]):
                        css = {"Positive": "sent-pos", "Neutral": "sent-neu",
                               "Negative": "sent-neg"}[r["label"]]
                        st.markdown(
                            f'{r["emoji"]} <span class="{css}">{r["label"]}</span> — {r["text"]}',
                            unsafe_allow_html=True,
                        )

            st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# PAGE: CART
# ----------------------------------------------------------------------------
def render_cart():
    st.markdown('<div class="panel-header">🛒 Your Cart</div>', unsafe_allow_html=True)
    items = cart_line_items()
    if not items:
        st.info("Your cart is empty. Head to the Dashboard and add some products!")
        return

    for item in items:
        c1, c2, c3, c4, c5 = st.columns([1, 3, 2, 2, 1])
        c1.image(item["image"], width=70)
        c2.markdown(f"**{item['name']}**")
        with c3:
            cc1, cc2, cc3 = st.columns(3)
            if cc1.button("➖", key=f"minus_{item['id']}"):
                remove_from_cart(item["id"], 1)
                st.rerun()
            cc2.markdown(f"<div style='text-align:center;padding-top:6px;'>{item['qty']}</div>",
                         unsafe_allow_html=True)
            if cc3.button("➕", key=f"plus_{item['id']}"):
                add_to_cart(item["id"], 1)
                st.rerun()
        c4.markdown(f"₹{item['line_total']:,.0f}")
        if c5.button("🗑️", key=f"del_{item['id']}"):
            remove_from_cart(item["id"], item["qty"])
            st.rerun()

    st.divider()
    subtotal, promo_discount, delivery_fee, total = cart_totals()

    with st.container():
        st.markdown('<div class="cart-box">', unsafe_allow_html=True)
        code_input = st.text_input("Promo code", placeholder="e.g. SAVE10")
        cc1, cc2 = st.columns([1, 3])
        if cc1.button("Apply"):
            match = next((c for c in DISCOUNT_CODES if c[0] == code_input.strip().upper()), None)
            if match:
                st.session_state.discount_code = match
                st.success(f"Applied {match[0]} (-{match[1]}%)")
            else:
                st.error("Invalid promo code")

        st.markdown(f"Subtotal: **₹{subtotal:,.0f}**")
        st.markdown(f"Promo discount: **-₹{promo_discount:,.0f}**")
        st.markdown(f"Delivery fee: **₹{delivery_fee:,.0f}**" +
                    (" (Free above ₹999)" if delivery_fee == 0 else ""))
        st.markdown(f"### Total: ₹{total:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Proceed to Checkout →", type="primary", use_container_width=True):
            st.session_state.page = "Checkout"
            st.rerun()


# ----------------------------------------------------------------------------
# PAGE: CHECKOUT (payment gateway simulation)
# ----------------------------------------------------------------------------
def render_checkout():
    st.markdown('<div class="panel-header">💳 Checkout</div>', unsafe_allow_html=True)
    items = cart_line_items()
    if not items:
        st.info("Your cart is empty — nothing to check out.")
        return

    subtotal, promo_discount, delivery_fee, total = cart_totals()
    col1, col2 = st.columns([2, 1])

    with col1:
        with st.form("checkout_form"):
            st.markdown("##### 📍 Delivery details")
            name = st.text_input("Full name", value="Guest User")
            phone = st.text_input("Phone number", placeholder="+91 9XXXXXXXXX")
            address = st.text_area("Delivery address", placeholder="House no, street, area")
            pincode = st.text_input("Pincode", placeholder="302001")

            st.markdown("##### 💳 Payment method")
            payment_method = st.radio(
                "Choose payment method",
                ["UPI", "Credit / Debit Card", "Cash on Delivery"],
                horizontal=True,
            )
            if payment_method == "Credit / Debit Card":
                cc1, cc2 = st.columns(2)
                cc1.text_input("Card number", placeholder="XXXX XXXX XXXX XXXX")
                cc2.text_input("Expiry (MM/YY)", placeholder="12/28")
                st.text_input("CVV", placeholder="•••", type="password")
            elif payment_method == "UPI":
                st.text_input("UPI ID", placeholder="yourname@upi")

            submitted = st.form_submit_button(f"Pay ₹{total:,.0f} Now", type="primary",
                                               use_container_width=True)

        if submitted:
            if not name or not phone or not address or not pincode:
                st.error("Please fill in all delivery details before paying.")
            else:
                order_id = "NT-" + str(uuid.uuid4())[:8].upper()
                st.session_state.order = {
                    "id": order_id, "items": items, "total": total,
                    "name": name, "address": address, "phone": phone,
                    "payment_method": payment_method, "placed_at": time.time(),
                    "eta_minutes": random.randint(10, 25),
                }
                st.session_state.cart = {}
                st.session_state.discount_code = None
                st.session_state.page = "Track Order"
                st.balloons()
                st.rerun()

    with col2:
        st.markdown('<div class="cart-box">', unsafe_allow_html=True)
        st.markdown("##### 🧾 Order Summary")
        for item in items:
            st.markdown(f"{item['name']} × {item['qty']} — ₹{item['line_total']:,.0f}")
        st.divider()
        st.markdown(f"Subtotal: ₹{subtotal:,.0f}")
        st.markdown(f"Discount: -₹{promo_discount:,.0f}")
        st.markdown(f"Delivery: ₹{delivery_fee:,.0f}")
        st.markdown(f"### Total: ₹{total:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# PAGE: TRACK ORDER (quick-commerce style, Blinkit/Zepto-like)
# ----------------------------------------------------------------------------
def render_track_order():
    st.markdown('<div class="panel-header">📦 Track Your Order</div>', unsafe_allow_html=True)
    order = st.session_state.order
    if not order:
        st.info("No active order yet. Place an order from Checkout to see live tracking here.")
        return

    st.success(f"Order **{order['id']}** confirmed! Estimated delivery in "
               f"**{order['eta_minutes']} minutes**.")
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("##### 🧾 Items")
        for item in order["items"]:
            st.markdown(f"- {item['name']} × {item['qty']} — ₹{item['line_total']:,.0f}")
        st.markdown(f"**Total paid:** ₹{order['total']:,.0f}  •  **Payment:** {order['payment_method']}")
        st.markdown(f"**Deliver to:** {order['address']}")

        st.divider()
        steps = [
            ("🧾", "Order Confirmed"),
            ("📦", "Packing your items"),
            ("🛵", "Out for delivery"),
            ("📍", "Arriving at your location"),
            ("✅", "Delivered"),
        ]
        if st.button("▶️ Simulate live tracking", type="primary"):
            progress = st.progress(0, text="Starting...")
            status = st.empty()
            for i, (icon, label) in enumerate(steps):
                status.markdown(f"### {icon} {label}")
                progress.progress(int((i + 1) / len(steps) * 100), text=label)
                time.sleep(1.1)
            st.balloons()
            st.success("🎉 Delivered! Enjoy your new gear.")

    with c2:
        st.markdown('<div class="cart-box">', unsafe_allow_html=True)
        st.markdown("##### 🛵 Delivery Partner")
        st.markdown("**Rahul S.** — ⭐ 4.9")
        st.markdown("Vehicle: E-Scooter · 🟢 En route")
        st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# PAGE: SPIN & WIN (marketing gamification)
# ----------------------------------------------------------------------------
def render_spin_wheel():
    st.markdown('<div class="panel-header">🎡 Spin & Win — Marketing Game</div>',
                 unsafe_allow_html=True)
    st.write("Spin the wheel for a chance to win up to **30% OFF** your order!")

    if st.button("🎯 Spin Now", type="primary"):
        idx, code, percent = pick_winner(DISCOUNT_CODES)
        st.session_state.last_spin = (idx, code, percent)

    if st.session_state.last_spin:
        idx, code, percent = st.session_state.last_spin
        spin_id = str(uuid.uuid4())[:6]
        html = build_wheel_html(DISCOUNT_CODES, idx, spin_id)
        st.components.v1.html(html, height=380)

        if percent > 0:
            st.success(f"🎉 You won **{code}** — {percent}% off!")
            if st.button("Apply this code to my cart"):
                st.session_state.discount_code = (code, percent)
                st.success("Promo code applied to your cart!")
        else:
            st.warning("Better luck next time! Spin again 🎡")
    else:
        st.info("Click **Spin Now** to play.")


# ----------------------------------------------------------------------------
# ROUTER
# ----------------------------------------------------------------------------
PAGES = {
    "Dashboard": render_dashboard,
    "Cart": render_cart,
    "Checkout": render_checkout,
    "Track Order": render_track_order,
    "Spin & Win": render_spin_wheel,
}
PAGES[st.session_state.page]()
