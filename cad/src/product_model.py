"""VatReel product appearance model (build123d), TRL 3, constructable design (VTR-DDR-002).

For photoreal renders only. Every component of cad/src/model.py components() is used as it is, at the
modelled mid-depth arm angle (20 degrees below level, lowest carrier 658 mm below the rim). Only the look
is added: snap hooks on the carrier bar eyes, two goat skins and a yarn hank hanging from three carrier
bars, the pit cut into a concrete floor with the liquor 150 mm below the rim, and a 1.75 m mannequin at the
crank for scale. APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: X along the pit, Y across it from the near rim (the operator stands at -Y), Z up from the
rim. Groups: "shell" (stands, tubes, shield, lift screw), "internal" (arm frame, reel, chains, loads) and
"context" (floor and pit, liquor, mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos, Rot, Torus  # noqa: E402
import model as m  # noqa: E402
from model import BOM_NAMES, PARAMS as P, box, cyl_y  # noqa: E402

TITLE = "VatReel: hand-cranked reel frame that moves hides and yarn through a pit"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 28, "az": 50,
     "note": "Product render from across the pit and to the right, about 28 deg elevation; reel at mid depth with two "
             "goat skins and a yarn hank on its carrier bars, liquor 150 mm below the rim; 1.75 m person at the crank "
             "behind the splash shield for scale"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 26, "az": 55,
     "note": "Exploded view from across the pit, about 26 deg elevation: near stand, tower and drive, splash shield, "
             "lift screw, pivot and extension tubes, far stand, arm frame, chain guard, reel and carrier bars"},
    {"name": "detail", "groups": ["shell", "internal", "context"], "explode": False, "el": 22, "az": -125,
     "note": "Operator side from behind and to the left, about 22 deg elevation: crank, ratchet cover, lift screw "
             "handwheel and the splash shield between the person and the reel"},
]

C_STEEL = "#B9BEC4"      # 304 frame, brushed
C_316 = "#C8CDD2"        # 316L wetted parts
C_DARK = "#5B636B"
C_ACCENT = "#0F766E"
C_PLASTIC = "#F2F2EE"
C_PP = "#E3EEF5"
C_RUBBER = "#26292E"
C_CHAIN = "#4B5056"
C_BRONZE = "#B08D57"
C_RED = "#B91C1C"
C_SKIN = "#A87C52"
C_YARN = "#2F5D8A"
C_CONCRETE = "#BDB7AD"
C_LIQUOR = "#5B4A2E"
C_CLAY = "#B9B4AC"

# component key -> (display name, colour, material, group)
LOOK = {
    "base": ("Near stand base frame", C_STEEL, "metal", "shell"),
    "pads": ("Rubber pads", C_RUBBER, "rubber", "shell"),
    "tower": ("Bearing tower (stainless)", C_STEEL, "metal", "shell"),
    "braces": ("Tower braces (stainless)", C_STEEL, "metal", "shell"),
    "tower_bushes": ("Tower bushes", C_PLASTIC, "plastic", "shell"),
    "jackshaft": ("Jackshaft (stainless shaft)", C_316, "metal", "shell"),
    "sprocket_j1": ("Chain 1 sprocket, large", C_DARK, "metal", "shell"),
    "sprocket_j2": ("Chain 2 sprocket, small (stainless)", C_316, "metal", "internal"),
    "crankshaft": ("Crank shaft (stainless)", C_316, "metal", "shell"),
    "sprocket_c": ("Chain 1 sprocket, small", C_DARK, "metal", "shell"),
    "crank": ("Crank arm", C_ACCENT, "painted", "shell"),
    "grip": ("Crank grip", C_RUBBER, "rubber", "shell"),
    "ratchet": ("Ratchet wheel (stainless)", C_316, "metal", "shell"),
    "pawl": ("Pawl and release lever", C_RED, "painted", "shell"),
    "ratchet_cover": ("Ratchet cover (stainless)", C_STEEL, "metal", "shell"),
    "chain1": ("Chain 1", C_CHAIN, "metal", "shell"),
    "shield_frame": ("Splash shield frame (stainless)", C_STEEL, "metal", "shell"),
    "shield_sheet": ("Splash shield sheet", C_PP, "clear", "shell"),
    "bracket": ("Lift screw bracket (stainless)", C_STEEL, "metal", "shell"),
    "screw": ("Lift screw (stainless rod)", C_316, "metal", "shell"),
    "trunnion_up": ("Upper trunnion (stainless)", C_316, "metal", "shell"),
    "trunnion_nut": ("Nut trunnion, bronze nut", C_BRONZE, "metal", "shell"),
    "handwheel": ("Handwheel", C_RUBBER, "painted", "shell"),
    "tube_a": ("Pivot tube (stainless)", C_STEEL, "metal", "shell"),
    "plug": ("Pivot tube plug", C_PLASTIC, "plastic", "shell"),
    "tube_b": ("Extension tube (stainless)", C_STEEL, "metal", "shell"),
    "collars": ("Shaft collars", C_DARK, "metal", "shell"),
    "far_stand": ("Far stand (stainless)", C_STEEL, "metal", "shell"),
    "sleeve": ("Split sleeve", C_STEEL, "metal", "shell"),
    "far_pads": ("Rubber pads, far stand", C_RUBBER, "rubber", "shell"),
    "torque_tube": ("Torque tube (stainless)", C_316, "metal", "internal"),
    "near_arm": ("Near arm (stainless)", C_316, "metal", "internal"),
    "far_arm": ("Far arm (stainless)", C_316, "metal", "internal"),
    "near_arm_bush": ("Torque tube bush, near", C_PLASTIC, "plastic", "internal"),
    "far_arm_bush": ("Torque tube bush, far", C_PLASTIC, "plastic", "internal"),
    "axle_bushes": ("Axle bushes", C_PLASTIC, "plastic", "internal"),
    "keeper": ("Saddle keeper", C_RED, "painted", "internal"),
    "guard2": ("Chain 2 guard case (stainless)", C_316, "metal", "internal"),
    "axle": ("Reel axle (stainless)", C_316, "metal", "internal"),
    "spider_near": ("Reel spider, near (stainless)", C_316, "metal", "internal"),
    "spider_far": ("Reel spider, far (stainless)", C_316, "metal", "internal"),
    "bars": ("Carrier bars (stainless)", C_316, "metal", "internal"),
    "sprocket_a": ("Axle sprocket (stainless)", C_316, "metal", "internal"),
    "chain2": ("Chain 2 (stainless)", C_CHAIN, "metal", "internal"),
    "hooks": ("Loading hooks", C_RED, "painted", "shell"),
}


def _explode(bom):
    return BOM_NAMES[bom][2] if bom in BOM_NAMES else (0, 0, 0)


def product_parts():
    comps = m.components()
    out = []

    def add(name, shape, color, material, bom, group, explode=None):
        out.append({"name": name, "shape": shape, "color": color, "material": material, "bom": bom, "group": group,
                    "explode": tuple(float(v) for v in (explode if explode is not None else _explode(bom)))})

    for c in comps:
        if c.key in LOOK:
            name, col, mat, grp = LOOK[c.key]
            add(name, c.shape, col, mat, c.bom, grp)

    # snap hooks (rings) on the eye tabs, and loads on three carrier bars
    T = m.arm_frame()
    L = P["ARM_L"]
    th = P["THETA"]
    angles = [90.0 + th + 60.0 * k for k in range(P["N_BARS"])]
    rings, hides, yarn = [], [], []
    for k, a in enumerate(angles):
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
        r = P["RC"] + P["BAR_OD"] / 2 + 22
        for ye in P["EYE_Y"]:
            rings.append(Pos(L + r * c, ye, r * s_) * Rot(90, 0, 0) * Torus(9.0, 2.5))
    # world positions of the bars; hang loads from the two bars on the rising side and one yarn hank
    for k in (1, 2):
        a = math.radians(angles[k] - th)          # world angle of bar k
        ax, az = m.axle_xz()
        bx, bz = ax + P["RC"] * math.cos(a), az + P["RC"] * math.sin(a)
        hides.append(box(bx - 2, bx + 2, 300, 780, bz - 520, bz - 18))
    a = math.radians(angles[0] - th)
    ax, az = m.axle_xz()
    bx, bz = ax + P["RC"] * math.cos(a), az + P["RC"] * math.sin(a)
    for dy in range(0, 240, 12):
        yarn.append(Pos(bx, 420 + dy, bz - 160) * Rot(90, 0, 0) * Torus(150.0, 5.0))
    from build123d import Compound
    add("Snap hooks (stainless)", Compound(rings), C_316, "metal", 19, "internal")
    add("Goat skins on the carrier bars", Compound(hides), C_SKIN, "fabric", None, "internal", (0, 0, 0))
    add("Yarn hank on a carrier bar", Compound(yarn), C_YARN, "fabric", None, "internal", (0, 0, 0))

    # context: concrete floor with the pit cut in, the liquor, a 1.75 m mannequin at the crank
    W, x0 = P["PIT_W"], P["PIT_END"]
    x1 = x0 + P["PIT_LEN"]
    D = P["PIT_DEPTH"]
    floor = box(x0 - 1300, x1 + 700, -2000, W + 900, -D - 150, 0) - box(x0, x1, 0, W, -D, 1)
    add("Concrete floor and pit", floor, C_CONCRETE, "painted", None, "context")
    add("Pit liquor", box(x0 + 1, x1 - 1, 1, W - 1, -D + 1, P["LIQUOR"]), C_LIQUOR, "clear", None, "context")
    try:
        from context_parts import mannequin
        man = Pos(-109.0, -1130.0, 0) * Rot(0, 0, 180) * mannequin(1750.0, "push")
        add("Person, 1.75 m (scale)", man, C_CLAY, "painted", None, "context")
    except Exception as e:  # never block the scene export on the scale figure
        print("mannequin skipped:", e)
    return out


if __name__ == "__main__":
    for p in product_parts():
        print(p["name"], p["group"], p["material"])
