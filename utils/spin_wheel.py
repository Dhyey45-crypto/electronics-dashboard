"""
Generates a self-contained HTML/CSS/JS 'Spin the Wheel' widget.
The WINNING segment is decided in Python (server-side, using `random`)
BEFORE the HTML is built, so the wheel animation is simply told which
angle to stop at -- this keeps the game fair and reproducible.
"""
import random

SEGMENT_COLORS = [
    "#f107a3", "#7b2ff7", "#00c6ff", "#7CFC00",
    "#ffd43b", "#ff6161", "#00e5a0", "#ff9f1c",
]


def pick_winner(discount_codes):
    """Pick a random (code, percent) pair and its index."""
    idx = random.randrange(len(discount_codes))
    code, percent = discount_codes[idx]
    return idx, code, percent


def build_wheel_html(discount_codes, winner_index: int, spin_id: str) -> str:
    n = len(discount_codes)
    slice_angle = 360 / n
    labels = [f"{c[1]}%" if c[1] > 0 else "TRY AGAIN" for c in discount_codes]

    # Build conic-gradient stops for the wheel background
    stops = []
    for i in range(n):
        color = SEGMENT_COLORS[i % len(SEGMENT_COLORS)]
        stops.append(f"{color} {i*slice_angle}deg {(i+1)*slice_angle}deg")
    gradient = ", ".join(stops)

    # Target rotation: winner slice's mid-angle must align with top pointer (0deg)
    mid = winner_index * slice_angle + slice_angle / 2
    spins = 6  # extra full rotations for drama
    target_rotation = spins * 360 + (360 - mid)

    # Label positioning (rotate each label to its slice's mid-angle)
    label_divs = ""
    for i, lab in enumerate(labels):
        ang = i * slice_angle + slice_angle / 2
        label_divs += f"""
        <div class="wheel-label" style="transform: rotate({ang}deg) translate(0,-108px) rotate(-{ang}deg);">
            {lab}
        </div>"""

    html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; font-family:'Segoe UI',sans-serif;">
      <style>
        .wheel-outer {{
            position: relative;
            width: 260px; height: 260px;
            margin-top: 10px;
        }}
        .pointer {{
            position: absolute; top: -14px; left: 50%;
            transform: translateX(-50%);
            width: 0; height: 0;
            border-left: 14px solid transparent;
            border-right: 14px solid transparent;
            border-top: 24px solid #fff;
            z-index: 5;
            filter: drop-shadow(0 0 4px rgba(0,0,0,0.5));
        }}
        .wheel {{
            width: 260px; height: 260px;
            border-radius: 50%;
            background: conic-gradient({gradient});
            border: 6px solid #fff;
            box-shadow: 0 0 30px rgba(241,7,163,0.5);
            position: relative;
            transition: transform 4.5s cubic-bezier(0.17, 0.67, 0.16, 0.99);
            transform: rotate(0deg);
        }}
        .wheel-label {{
            position: absolute;
            top: 50%; left: 50%;
            width: 60px; margin-left: -30px; margin-top: -8px;
            text-align: center;
            color: #05060d;
            font-weight: 800;
            font-size: 13px;
            text-shadow: 0 1px 2px rgba(255,255,255,0.4);
        }}
        .hub {{
            position: absolute; top: 50%; left: 50%;
            width: 34px; height: 34px;
            margin-left: -17px; margin-top: -17px;
            background: #fff; border-radius: 50%;
            box-shadow: 0 0 10px rgba(0,0,0,0.4);
            z-index: 6;
        }}
      </style>
      <div class="wheel-outer">
        <div class="pointer"></div>
        <div class="wheel" id="wheel_{spin_id}">
          {label_divs}
        </div>
        <div class="hub"></div>
      </div>
      <script>
        setTimeout(function() {{
            var w = document.getElementById("wheel_{spin_id}");
            if (w) {{ w.style.transform = "rotate({target_rotation}deg)"; }}
        }}, 300);
      </script>
    </div>
    """
    return html
