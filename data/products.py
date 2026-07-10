"""
Product catalog for the Electronics Retail Dashboard.
15 products with pricing, stock, discounts, media, and reviews.

NOTE ON MEDIA: Images use picsum.photos (deterministic via seed) and videos use
public Google sample-video CDN links so the app works out of the box with no
API keys. Swap these URLs for your own CDN / S3 links in production.
"""

SAMPLE_VIDEOS = [
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
]

PRODUCTS = [
    {
        "id": 1, "name": "Nova X12 Smartphone", "category": "Smartphones",
        "price": 59999, "quantity": 24, "discount": 12, "rating": 4.5,
        "image": "https://picsum.photos/seed/novax12/500/400",
        "video": SAMPLE_VIDEOS[0],
        "description": "Flagship smartphone with 120Hz AMOLED display, triple camera "
                        "system, and all-day battery life.",
        "reviews": [
            "Absolutely love this phone, camera quality is stunning!",
            "Battery drains a bit fast but overall great performance.",
            "Best phone I've owned, super smooth and fast.",
        ],
    },
    {
        "id": 2, "name": "AeroBook Pro 14 Laptop", "category": "Laptops",
        "price": 89999, "quantity": 15, "discount": 8, "rating": 4.7,
        "image": "https://picsum.photos/seed/aerobookpro/500/400",
        "video": SAMPLE_VIDEOS[1],
        "description": "Ultra-slim laptop with 12-core CPU, 16GB RAM, and a stunning "
                        "2.8K display for creators and professionals.",
        "reviews": [
            "Incredibly fast and the display is gorgeous.",
            "A bit expensive but worth every rupee.",
            "Fan noise is noticeable under heavy load.",
        ],
    },
    {
        "id": 3, "name": "PulseFit Smartwatch", "category": "Wearables",
        "price": 8999, "quantity": 40, "discount": 20, "rating": 4.2,
        "image": "https://picsum.photos/seed/pulsefit/500/400",
        "video": SAMPLE_VIDEOS[2],
        "description": "AMOLED smartwatch with SpO2, heart-rate tracking, and 10-day "
                        "battery backup.",
        "reviews": [
            "Great value for money, tracks workouts accurately.",
            "App is a bit buggy but the hardware is solid.",
            "Disappointed with the strap quality.",
        ],
    },
    {
        "id": 4, "name": "SonicBuds Air Earbuds", "category": "Audio",
        "price": 3499, "quantity": 60, "discount": 25, "rating": 4.4,
        "image": "https://picsum.photos/seed/sonicbuds/500/400",
        "video": SAMPLE_VIDEOS[3],
        "description": "True wireless earbuds with active noise cancellation and "
                        "immersive spatial audio.",
        "reviews": [
            "ANC is fantastic for the price!",
            "Comfortable fit, great for long calls.",
            "Bass could be a little punchier.",
        ],
    },
    {
        "id": 5, "name": "BoomBox 360 Speaker", "category": "Audio",
        "price": 5999, "quantity": 30, "discount": 15, "rating": 4.3,
        "image": "https://picsum.photos/seed/boombox360/500/400",
        "video": SAMPLE_VIDEOS[4],
        "description": "360-degree portable Bluetooth speaker, waterproof, with "
                        "18-hour playtime.",
        "reviews": [
            "Loud, clear, and the bass is amazing outdoors.",
            "Great for parties, highly recommend.",
            "Pairing takes a few tries sometimes.",
        ],
    },
    {
        "id": 6, "name": "GameSphere X Console", "category": "Gaming",
        "price": 49999, "quantity": 10, "discount": 5, "rating": 4.8,
        "image": "https://picsum.photos/seed/gamesphere/500/400",
        "video": SAMPLE_VIDEOS[0],
        "description": "Next-gen gaming console with 4K/120fps support and "
                        "ultra-fast SSD load times.",
        "reviews": [
            "Graphics are next level, loading times are near instant.",
            "Worth the wait, best console this generation.",
            "Wish more games were bundled at launch.",
        ],
    },
    {
        "id": 7, "name": "TabMax 11 Tablet", "category": "Tablets",
        "price": 27999, "quantity": 18, "discount": 10, "rating": 4.1,
        "image": "https://picsum.photos/seed/tabmax11/500/400",
        "video": SAMPLE_VIDEOS[1],
        "description": "11-inch tablet with stylus support, perfect for note-taking "
                        "and digital art.",
        "reviews": [
            "Stylus lag is minimal, great for sketching.",
            "Battery life could be better.",
            "Excellent screen quality for the price.",
        ],
    },
    {
        "id": 8, "name": "VisionMax 55 Smart TV", "category": "Television",
        "price": 45999, "quantity": 12, "discount": 18, "rating": 4.6,
        "image": "https://picsum.photos/seed/visionmax55/500/400",
        "video": SAMPLE_VIDEOS[2],
        "description": "55-inch 4K QLED Smart TV with Dolby Vision and built-in "
                        "voice assistant.",
        "reviews": [
            "Picture quality is cinema-level, love the colors.",
            "Smart features are intuitive and fast.",
            "Remote could feel more premium.",
        ],
    },
    {
        "id": 9, "name": "ClickShot Pro Camera", "category": "Cameras",
        "price": 64999, "quantity": 8, "discount": 7, "rating": 4.5,
        "image": "https://picsum.photos/seed/clickshotpro/500/400",
        "video": SAMPLE_VIDEOS[3],
        "description": "Mirrorless camera with 4K video, 33MP sensor, and "
                        "in-body stabilization.",
        "reviews": [
            "Sharp images even in low light, very impressed.",
            "Menu system takes time to learn.",
            "Perfect upgrade from my old DSLR.",
        ],
    },
    {
        "id": 10, "name": "SkyHover 4K Drone", "category": "Drones",
        "price": 38999, "quantity": 9, "discount": 14, "rating": 4.3,
        "image": "https://picsum.photos/seed/skyhover/500/400",
        "video": SAMPLE_VIDEOS[4],
        "description": "Foldable 4K drone with obstacle avoidance and 34-minute "
                        "flight time.",
        "reviews": [
            "Stable flight even in light wind, footage is crisp.",
            "App crashed once but overall a solid drone.",
            "Great for beginners and hobbyists alike.",
        ],
    },
    {
        "id": 11, "name": "ChargeMate 20K Power Bank", "category": "Accessories",
        "price": 1999, "quantity": 75, "discount": 30, "rating": 4.0,
        "image": "https://picsum.photos/seed/chargemate/500/400",
        "video": SAMPLE_VIDEOS[0],
        "description": "20,000mAh fast-charging power bank with dual USB-C "
                        "PD output.",
        "reviews": [
            "Charges my laptop and phone together, super handy.",
            "A bit heavy to carry daily.",
            "Fast charging works exactly as advertised.",
        ],
    },
    {
        "id": 12, "name": "NetLink AX6000 Router", "category": "Networking",
        "price": 12999, "quantity": 22, "discount": 11, "rating": 4.4,
        "image": "https://picsum.photos/seed/netlinkax6000/500/400",
        "video": SAMPLE_VIDEOS[1],
        "description": "WiFi 6 router with mesh support, covering up to 3000 "
                        "sq. ft. with zero dead zones.",
        "reviews": [
            "Killed all my dead zones, rock solid connection.",
            "Setup app could be more beginner friendly.",
            "Great range and speed for the price.",
        ],
    },
    {
        "id": 13, "name": "TypeCraft RGB Keyboard", "category": "Accessories",
        "price": 4499, "quantity": 35, "discount": 22, "rating": 4.6,
        "image": "https://picsum.photos/seed/typecraft/500/400",
        "video": SAMPLE_VIDEOS[2],
        "description": "Hot-swappable mechanical keyboard with per-key RGB and "
                        "PBT keycaps.",
        "reviews": [
            "Typing feel is amazing, switches are buttery smooth.",
            "RGB software is a little clunky.",
            "Best keyboard purchase I've made.",
        ],
    },
    {
        "id": 14, "name": "GlidePoint Pro Mouse", "category": "Accessories",
        "price": 2499, "quantity": 50, "discount": 18, "rating": 4.3,
        "image": "https://picsum.photos/seed/glidepoint/500/400",
        "video": SAMPLE_VIDEOS[3],
        "description": "Ergonomic wireless mouse with 26K DPI sensor and "
                        "silent clicks.",
        "reviews": [
            "Super comfortable for long work sessions.",
            "Sensor is precise, no lag at all.",
            "Battery lasts weeks, very happy with it.",
        ],
    },
    {
        "id": 15, "name": "ImmerseVR One Headset", "category": "VR/AR",
        "price": 32999, "quantity": 14, "discount": 9, "rating": 4.2,
        "image": "https://picsum.photos/seed/immersevr/500/400",
        "video": SAMPLE_VIDEOS[4],
        "description": "Standalone VR headset with 4K per-eye resolution and "
                        "hand tracking, no PC required.",
        "reviews": [
            "Visual clarity blew me away, minimal screen door effect.",
            "Comfortable for about an hour, then a bit heavy.",
            "Great library of games already available.",
        ],
    },
]

DISCOUNT_CODES = [
    ("SAVE5", 5), ("SAVE10", 10), ("SAVE15", 15), ("SAVE20", 20),
    ("BETTER_LUCK", 0), ("FREESHIP", 0), ("SAVE25", 25), ("JACKPOT30", 30),
]

MARKETING_BANNERS = [
    "⚡ Flash Sale: Up to 30% OFF on Audio gear — today only!",
    "🚚 Free 10-minute delivery on all orders above ₹999",
    "🎁 Spin the wheel and win up to 30% extra discount!",
    "💳 Get 5% instant cashback with UPI payments",
    "🔥 New Arrivals: ImmerseVR One is here — grab yours now!",
]
