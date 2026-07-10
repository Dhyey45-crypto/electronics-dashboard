"""Custom CSS injected into the Streamlit app for a sophisticated, dynamic look."""

CUSTOM_CSS = """
<style>
/* ---------- Global ---------- */
html, body, [class*="css"]  {
    font-family: 'Segoe UI', 'Inter', sans-serif;
}
.main {
    background: radial-gradient(circle at top left, #0f1225 0%, #05060d 60%);
}
h1, h2, h3, h4 { color: #f5f5ff; }

/* ---------- Marketing marquee banner ---------- */
.marquee-wrap {
    background: linear-gradient(90deg, #7b2ff7, #f107a3);
    border-radius: 10px;
    padding: 10px 0;
    margin-bottom: 14px;
    overflow: hidden;
    white-space: nowrap;
    box-shadow: 0 0 18px rgba(241, 7, 163, 0.45);
}
.marquee-text {
    display: inline-block;
    padding-left: 100%;
    color: white;
    font-weight: 600;
    font-size: 16px;
    animation: marquee 16s linear infinite;
}
@keyframes marquee {
    0%   { transform: translate(0, 0); }
    100% { transform: translate(-100%, 0); }
}

/* ---------- Panel headers ---------- */
.panel-header {
    background: linear-gradient(90deg, #1f2340, #2c1550);
    padding: 10px 16px;
    border-radius: 10px;
    color: #fff;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
    border-left: 5px solid #f107a3;
}

/* ---------- Product card (right panel) ---------- */
.product-card {
    background: linear-gradient(160deg, #161a30 0%, #0d0f1c 100%);
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 14px;
    border: 1px solid #292d4a;
    transition: 0.25s ease;
}
.product-card:hover {
    border: 1px solid #f107a3;
    box-shadow: 0 0 16px rgba(241, 7, 163, 0.35);
    transform: translateY(-2px);
}
.product-card.selected {
    border: 2px solid #7CFC00;
    box-shadow: 0 0 22px rgba(124, 252, 0, 0.45);
}
.product-title { color: #fff; font-weight: 700; font-size: 16px; margin: 6px 0 2px 0; }
.product-price { color: #7CFC00; font-weight: 700; font-size: 15px; }
.product-strike { color: #888; text-decoration: line-through; font-size: 13px; margin-left: 6px;}
.product-badge {
    display: inline-block;
    background: #f107a3;
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 20px;
    margin-bottom: 4px;
}
.stock-low { color: #ff6161; font-size: 12px; font-weight: 600; }
.stock-ok { color: #7CFC00; font-size: 12px; font-weight: 600; }

/* ---------- Zoomable image ---------- */
.zoom-wrap {
    overflow: hidden;
    border-radius: 10px;
    width: 100%;
    height: 180px;
}
.zoom-wrap img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    transition: transform 0.4s ease;
    cursor: zoom-in;
}
.zoom-wrap:hover img {
    transform: scale(1.65);
}

/* ---------- Sentiment badges ---------- */
.sent-pos { color: #7CFC00; font-weight: 600; }
.sent-neu { color: #ffd43b; font-weight: 600; }
.sent-neg { color: #ff6161; font-weight: 600; }

/* ---------- Cart summary ---------- */
.cart-box {
    background: linear-gradient(160deg, #161a30 0%, #0d0f1c 100%);
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #292d4a;
}

/* ---------- Metric pills ---------- */
.metric-pill {
    display: inline-block;
    background: #1f2340;
    color: #fff;
    padding: 8px 14px;
    border-radius: 20px;
    margin-right: 8px;
    font-size: 13px;
    font-weight: 600;
    border: 1px solid #35396a;
}
</style>
"""
