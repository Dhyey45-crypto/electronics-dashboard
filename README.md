# ⚡ NovaTech Electronics — Dynamic Retail Dashboard & Quick-Commerce App
### 🔗 [Launch the Live App](https://electronics-dashboard-atd4rcauupdy9pzsgwmois.streamlit.app/)

A single-page, split-screen **Streamlit** web application for an electronics
retail company. Built to demo a fully dynamic dashboard + a Blinkit/Zepto-style
quick-commerce shopping journey — table selection, media showcase, cart,
checkout, payment simulation, live order tracking, and a spin-the-wheel
marketing game.

---

## ✨ Features

| Area | Details |
|---|---|
| **Split-screen layout** | Page is divided into exactly 2 halves, each an independently scrollable panel (`st.container(height=...)` acts as the "slider"/scrollbar). |
| **Left panel — Dashboard** | Live table of 15 products (name, stock qty, price, discount, rating) with **row-click selection**, KPI metrics, and 2 Plotly charts (stock levels, price vs. rating). |
| **Right panel — Product showcase** | 15 product boxes with **zoomable images** (CSS hover-zoom), marketing videos, descriptions, and **TextBlob-powered review sentiment**. Clicking a table row auto-expands the matching box. |
| **Cart** | Add/remove per product, live quantity, promo code box, dynamic totals. |
| **Checkout** | Delivery form + simulated **payment gateway** (UPI / Card / COD). |
| **Order Tracking** | Quick-commerce style live tracking simulation (Confirmed → Packing → Out for delivery → Arriving → Delivered) with ETA, similar to Blinkit/Zepto. |
| **Spin & Win** | Animated canvas/CSS spin-the-wheel discount game; winning code can be auto-applied to the cart. |
| **Marketing** | Rotating marquee ad banner + sponsored promo tiles on the dashboard. |
| **Music** | Optional looping background store music (toggle in sidebar). |
| **Dynamic on both sides** | Stock quantities update live as items are added/removed from cart; every widget re-renders through Streamlit's reactive session state. |

---

## 🗂️ Project Structure

```
electronics_dashboard/
├── app.py                     # Main Streamlit app (routes, layout, logic)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .streamlit/
│   └── config.toml            # Dark theme + server config
├── data/
│   └── products.py            # 15-product catalog, discount codes, ad banners
└── utils/
    ├── styles.py               # Injected custom CSS (cards, zoom, marquee, etc.)
    ├── sentiment.py             # TextBlob review sentiment helpers
    └── spin_wheel.py            # Spin-the-wheel HTML/CSS/JS component builder
```

---

## 🚀 Setup & Run in VS Code (step by step)

### 1. Prerequisites
- Python 3.10+ installed
- VS Code with the **Python extension** installed

### 2. Get the project
Unzip the downloaded project and open the `electronics_dashboard` folder in VS Code
(`File → Open Folder…`).

### 3. Create & activate a virtual environment
Open the VS Code integrated terminal (`` Ctrl+` ``) and run:

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Download the TextBlob text corpora (one-time, needed for sentiment analysis)
```bash
python -m textblob.download_corpora
```

### 6. Run the app
```bash
streamlit run app.py
```

### 7. View it
Streamlit will print a local URL in the terminal, typically:
```
Local URL: http://localhost:8501
```
It should also open automatically in your default browser. If not, open that
URL manually.

---

## 🧭 How to use the app

1. **Dashboard page** — click any row in the left inventory table; the matching
   product box on the right auto-expands with its video, description, and
   review sentiment. Hover any product image to zoom in. Use **Add** to add a
   product straight to the cart from either panel.
2. **Cart** — adjust quantities, apply a promo code (try `SAVE10`, `SAVE20`,
   `JACKPOT30`), then **Proceed to Checkout**.
3. **Checkout** — fill delivery details, pick a payment method, and pay.
4. **Track Order** — click **Simulate live tracking** to watch the order move
   through quick-commerce style delivery stages.
5. **Spin & Win** — spin the wheel for a bonus discount code and apply it to
   your cart.

---

## 🛠️ Customizing

- **Swap product images/videos**: edit `data/products.py` — replace the
  `image` / `video` URLs with your own CDN/S3 links.
- **Change branding/colors**: edit `utils/styles.py` (CSS variables) and
  `.streamlit/config.toml` (Streamlit theme).
- **Add more products**: append new dicts to `PRODUCTS` in
  `data/products.py` (keep unique `id` values); the dashboard and showcase
  grid both resize automatically.
- **Wire up a real payment gateway**: replace the simulated `st.form` logic in
  `render_checkout()` inside `app.py` with your provider's SDK/API (e.g.
  Razorpay, Stripe) — keep the same order object shape so tracking still works.

---

## 📦 Tech Stack

- **Streamlit** — reactive web app framework & UI
- **Pandas** — tabular data handling for the dashboard
- **Plotly Express** — interactive charts
- **TextBlob** — NLP sentiment analysis on customer reviews
- **Vanilla CSS/JS** (embedded via `st.components.v1.html`) — zoom effects,
  marquee banner, and the spin-the-wheel game
