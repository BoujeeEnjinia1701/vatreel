"""VatReel parametric model (build123d), TRL 3, constructable design (VTR-DDR-002).

Run from the repo root:
    python cad/src/model.py            export STEP and STL to cad/step and cad/stl
    python cad/src/model.py --check    fit checks: no overlaps, every joint face touching, and the
                                       moving parts clear in the lifted, shallow and deep positions

Axes: X along the pit (the reel turns in the XZ plane), Y across the pit from the near rim
(Y = 0 is the near pit edge, +Y is into the pit, the operator stands at -Y), Z up from the floor and
pit rim (Z = 0). Units mm. The pit modelled is 1,600 mm wide (Y); its end wall is 350 mm behind the
arm pivot (X = -350). Liquor is assumed 150 mm below the rim.

What the model shows: a near stand on the near rim (base frame, bearing tower with the crank, ratchet
and first chain inside it, splash shield, lift screw bracket); a pivot tube from the near stand across
the pit to a far stand on the far rim (with an extension tube for wide pits); a welded arm frame that
swings on the pivot line; the reel (axle, two spiders, six carrier bars) carried at the end of the arms;
a second chain along the near arm from the jackshaft to the reel; and a self-locking lift screw with a
handwheel that sets the arm angle, which sets how deep the reel dips and lifts it clear.

components() returns every made or bought component on its own (for the build plan and the checks);
build_parts() groups them by BOM line (for the concept media, the drawing and the masses). Sizing is in
VTR-CAL-001 (docs/04-calcs/sizing.py), which reads PARAMS and geometry() from here.
CONCEPT, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
from pathlib import Path

# ---------------------------------------------------------------------------
# Parameters (mm, degrees). Edit these, not the geometry below.
# ---------------------------------------------------------------------------
PARAMS = {
    # Site (assumptions, VTR-CAL-001 Table 1)
    "PIT_W": 1600.0,        # pit width spanned (Y), modelled; the frame serves 1,000 to 2,500 mm
    "PIT_END": -350.0,      # pit end wall, X; the arm pivot is 350 mm in from it
    "PIT_LEN": 2100.0,      # pit length shown (X)
    "PIT_DEPTH": 1400.0,
    "LIQUOR": -150.0,       # liquor surface, 150 mm below the rim
    # Arm pivot and arms
    "PIV_Z": 200.0,         # pivot line height above the rim (X = 0)
    "ARM_L": 900.0,         # pivot to reel axle
    "THETA": 20.0,          # arm angle modelled, degrees below horizontal (working, mid depth)
    "THETA_LIFT": -33.7,    # lifted: lowest carrier 150 mm above the rim
    "THETA_SHALLOW": -3.2,  # shallowest working: lowest carrier 300 mm below the rim
    "THETA_DEEP": 46.2,     # deepest working: lowest carrier 1,000 mm below the rim
    "ARM_H": 60.0, "ARM_W": 40.0, "ARM_T": 3.0,      # 60 x 40 x 3 rectangular tube, 316L
    "NEAR_HUB_Y": (95.0, 190.0), "FAR_HUB_Y": (880.0, 940.0),
    "TORQUE_TUBE": (76.1, 3.0), "TORQUE_Y": (95.0, 940.0),   # arms welded to one torque tube round the pivot line
    "NEAR_ARM_Y": (150.0, 190.0), "FAR_ARM_Y": (890.0, 930.0),
    # Lift screw (Tr24 x 5, self-locking) and lever
    "LEVER_R": 250.0,       # lever lug behind the pivot (on the near arm hub)
    "SCREW_PIV": (-250.0, 1080.0),   # upper trunnion (x, z)
    "SCREW_Y": 130.0, "SCREW_D": 24.0, "SCREW_PITCH": 5.0,
    "FORK_Y": ((97.0, 105.0), (155.0, 163.0)),
    "HANDWHEEL_D": 250.0,
    # Reel
    "AXLE_OD": 48.3, "AXLE_T": 3.68, "AXLE_Y": (60.0, 960.0),
    "SPIDER_Y": (240.0, 840.0), "SPOKE_W": 30.0, "SPOKE_T": 6.0, "SPOKE_R": 590.0,
    "TIE_R": 420.0, "RING_W": 25.0,                   # hexagon of flat bar between the spokes
    "RC": 550.0,            # carrier bar pitch radius
    "N_BARS": 6, "BAR_OD": 33.7, "BAR_T": 2.0, "BAR_PLATE_T": 6.0,
    "EYE_Y": (340.0, 540.0, 740.0),
    # Bearings: PTFE (glass filled) in the wet, hot arm-end bearings; UHMW-PE elsewhere
    "HOUSING": (100.0, 90.0),                         # arm-end housing, along the arm x across
    # Shafts and drive (ISO 606 08B-1 chain, 12.7 mm pitch)
    "JACK_D": 40.0, "JACK_Y": (-400.0, 260.0),
    "CRANK_D": 30.0, "CRANK_Z": 1000.0, "CRANK_Y": (-580.0, -68.0), "CRANK_R": 280.0,
    "CHAIN_P": 12.7, "Z_CRANK": 15, "Z_JACK1": 30, "Z_JACK2": 17, "Z_AXLE": 51,
    "CHAIN1_Y": -215.0, "CHAIN2_Y": 80.0,
    # Pivot tube and extension
    "TUBE_A": (60.3, 5.54), "TUBE_A_Y": (195.0, 1400.0),
    "TUBE_B": (48.3, 3.68), "TUBE_B_Y": (280.0, 1830.0),
    # Near stand
    "BASE_X": (-550.0, 1200.0), "BASE_Y": (-700.0, -40.0), "SHS": 40.0, "SHS_T": 2.0, "PAD_T": 10.0,
    "PLATE_T": 5.0, "PLATE_X": 80.0, "PLATE_Y": (-360.0, -70.0), "TOWER_TOP": 1100.0,
    "SHIELD_X": (-120.0, 1200.0), "SHIELD_Z": (60.0, 1450.0), "SHIELD_Y": -67.5,
    # Far stand
    "FAR_Y": 150.0,         # far stand centre line behind the far pit edge
    "FAR_X": (-450.0, 1200.0),
}

P = PARAMS
STEEL = 7930.0      # kg/m3, 304 and 316L stainless
DENS = {"steel": STEEL, "uhmw": 940.0, "ptfe": 2200.0, "pp": 905.0, "epdm": 1150.0, "bronze": 8800.0}


def _b():
    import build123d as bd
    return bd


# ---------------------------------------------------------------------------
# Small geometry helpers
# ---------------------------------------------------------------------------
def box(x0, x1, y0, y1, z0, z1):
    bd = _b()
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * bd.Box(x1 - x0, y1 - y0, z1 - z0)


def cyl_y(r, y0, y1, x, z):
    bd = _b()
    return bd.Pos(x, (y0 + y1) / 2, z) * bd.Rot(90, 0, 0) * bd.Cylinder(r, y1 - y0)


def tube_y(ro, ri, y0, y1, x, z):
    return cyl_y(ro, y0, y1, x, z) - cyl_y(ri, y0 - 1, y1 + 1, x, z)


def cyl_z(r, z0, z1, x, y):
    bd = _b()
    return bd.Pos(x, y, (z0 + z1) / 2) * bd.Cylinder(r, z1 - z0)


def rod(p0, p1, r):
    """Cylinder of radius r from point p0 to point p1."""
    bd = _b()
    v = bd.Vector(*p1) - bd.Vector(*p0)
    return bd.Solid.make_cylinder(r, v.length, bd.Plane(origin=bd.Vector(*p0), z_dir=v.normalized()))


def bar(p0, p1, w, t, up=(0, 1, 0)):
    """Rectangular bar from p0 to p1, width w along 'up' x direction, thickness t along 'up'."""
    bd = _b()
    v = bd.Vector(*p1) - bd.Vector(*p0)
    L = v.length
    d = v.normalized()
    u = bd.Vector(*up)
    xd = u.cross(d).normalized()
    pl = bd.Plane(origin=bd.Vector(*p0), x_dir=xd, z_dir=d)
    return pl * bd.Pos(0, 0, L / 2) * bd.Box(w, t, L)


def shs_x(x0, x1, yc, zc, s, t):
    """Square hollow section along X."""
    return box(x0, x1, yc - s / 2, yc + s / 2, zc - s / 2, zc + s / 2) - box(x0 - 1, x1 + 1, yc - s / 2 + t, yc + s / 2 - t, zc - s / 2 + t, zc + s / 2 - t)


def shs_y(y0, y1, xc, zc, s, t):
    return box(xc - s / 2, xc + s / 2, y0, y1, zc - s / 2, zc + s / 2) - box(xc - s / 2 + t, xc + s / 2 - t, y0 - 1, y1 + 1, zc - s / 2 + t, zc + s / 2 - t)


def shs_z(z0, z1, xc, yc, s, t):
    return box(xc - s / 2, xc + s / 2, yc - s / 2, yc + s / 2, z0, z1) - box(xc - s / 2 + t, xc + s / 2 - t, yc - s / 2 + t, yc + s / 2 - t, z0 - 1, z1 + 1)


def pcd(z, p=None):
    p = p or P["CHAIN_P"]
    return p / math.sin(math.pi / z)


def sprocket(z, y0, x, zc, hub_r=None, hub_y=None, bore=None):
    """Plate sprocket as a toothed disc (teeth drawn as a 2z-sided star), with an optional hub."""
    bd = _b()
    rp = pcd(z) / 2
    ro, rr = rp + 4.0, rp - 4.0
    pts = []
    for k in range(2 * z):
        a = math.pi * k / z
        r = ro if k % 2 == 0 else rr
        pts.append((r * math.cos(a), r * math.sin(a)))
    face = bd.Polygon(*pts, align=None)
    disc = bd.extrude(face, 7.2)                      # in the XY plane, 7.2 thick along +Z
    disc = bd.Pos(x, y0 + 7.2, zc) * bd.Rot(90, 0, 0) * disc   # now spans y0 .. y0 + 7.2
    if hub_r:
        disc = disc + cyl_y(hub_r, hub_y[0], hub_y[1], x, zc)
    if bore:
        disc = disc - cyl_y(bore / 2, y0 - 40, y0 + 50, x, zc)
    return disc


def _hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p_ in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p_) <= 0:
            lo.pop()
        lo.append(p_)
    for p_ in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p_) <= 0:
            hi.pop()
        hi.append(p_)
    return lo[:-1] + hi[:-1]


def stadium_xz(c1, r1, c2, r2, y0, y1, n=48):
    """Solid hull of two circles in the XZ plane (x, z centres), extruded from y0 to y1."""
    bd = _b()
    pts = []
    for (cx, cz), r in ((c1, r1), (c2, r2)):
        for k in range(n):
            a = 2 * math.pi * k / n
            pts.append((round(cx + r * math.cos(a), 4), round(cz + r * math.sin(a), 4)))
    h = _hull(pts)
    face = bd.Polygon(*h, align=None)                 # drawn in XY as (x, z)
    s = bd.extrude(face, y1 - y0)                     # along +Z
    # map (x, y_draw, z_draw) -> (x, z_world, y_world): rotate about X by +90 so draw-y becomes world z
    return _xz_place(s, y0)


def _xz_place(s, y0):
    """A solid drawn in XY (x, z) and extruded along +Z by thickness t becomes a solid in XZ spanning y0..y0+t."""
    bd = _b()
    # Rot(90,0,0) maps (x, y, z) -> (x, -z, y): draw-y -> world z, extrude +Z -> world -Y
    s2 = bd.Rot(90, 0, 0) * s
    bb = s2.bounding_box()
    return bd.Pos(0, y0 - bb.min.Y, 0) * s2


def chain_band(c1, r1, c2, r2, y_mid, w=12.0, t=12.0):
    """Roller chain envelope: band of radial thickness t about the pitch line, width w, in the XZ plane."""
    outer = stadium_xz(c1, r1 + t / 2, c2, r2 + t / 2, y_mid - w / 2, y_mid + w / 2)
    inner = stadium_xz(c1, r1 - t / 2, c2, r2 - t / 2, y_mid - w / 2 - 1, y_mid + w / 2 + 1)
    return outer - inner


def arm_frame(theta=None):
    """Transform from the arm's local frame (pivot at the origin, arm along +X) to the world."""
    bd = _b()
    th = P["THETA"] if theta is None else theta
    return bd.Pos(0, 0, P["PIV_Z"]) * bd.Rot(0, th, 0)


def axle_xz(theta=None):
    th = math.radians(P["THETA"] if theta is None else theta)
    return P["ARM_L"] * math.cos(th), P["PIV_Z"] - P["ARM_L"] * math.sin(th)


def lug_xz(theta=None):
    th = math.radians(P["THETA"] if theta is None else theta)
    return -P["LEVER_R"] * math.cos(th), P["PIV_Z"] + P["LEVER_R"] * math.sin(th)


def geometry(theta=None):
    """Key heights and positions for a given arm angle (used by the calculation note)."""
    th = P["THETA"] if theta is None else theta
    ax, az = axle_xz(th)
    lx, lz = lug_xz(th)
    ux, uz = P["SCREW_PIV"]
    return dict(theta=th, axle_x=ax, axle_z=az, low_bar=az - P["RC"], top_bar=az + P["RC"],
                reel_x0=ax - P["SPOKE_R"], reel_x1=ax + P["SPOKE_R"], reel_top=az + P["SPOKE_R"],
                reel_bottom=az - P["SPOKE_R"], lug=(lx, lz), screw_len=math.hypot(ux - lx, uz - lz))


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------
class C:
    """One component: key, name, shape, colour, BOM line, how it is made, group, explode offset, material."""
    def __init__(self, key, name, shape, color, bom, how, group, explode=(0, 0, 0), mat="steel"):
        self.key, self.name, self.shape, self.color = key, name, shape, color
        self.bom, self.how, self.group, self.explode, self.mat = bom, how, group, explode, mat


def near_arm_local():
    """Near arm weldment in the arm frame: arm tube, split housing (lower half and cap shown together) and
    the two lever fork plates; all are welded to the torque tube (a separate part)."""
    h, w, t = P["ARM_H"], P["ARM_W"], P["ARM_T"]
    y0, y1 = P["NEAR_ARM_Y"]
    L = P["ARM_L"]
    hx, hz = P["HOUSING"]
    r = P["TORQUE_TUBE"][0] / 2
    arm = box(r, L - hx / 2, y0, y1, -h / 2, h / 2) - box(r - 1, L - hx / 2 + 1, y0 + t, y1 - t, -h / 2 + t, h / 2 - t)
    housing = box(L - hx / 2, L + hx / 2, y0, y1, -hz / 2, hz / 2) - cyl_y(30.0, y0 - 1, y1 + 1, L, 0)
    s = arm + housing
    for (a, b_) in P["FORK_Y"]:
        s = s + box(-P["LEVER_R"] - 30, -r, a, b_, -25, 25)
    return s


def far_arm_local():
    h, w, t = P["ARM_H"], P["ARM_W"], P["ARM_T"]
    y0, y1 = P["FAR_ARM_Y"]
    L = P["ARM_L"]
    hx, hz = P["HOUSING"]
    r = P["TORQUE_TUBE"][0] / 2
    arm = box(r, L - hx / 2, y0, y1, -h / 2, h / 2) - box(r - 1, L - hx / 2 + 1, y0 + t, y1 - t, -h / 2 + t, h / 2 - t)
    # open-topped saddle: the axle drops in from above; a keeper closes the slot
    sad = box(L - hx / 2, L + hx / 2, y0, y1, -hz / 2, 32.0) - cyl_y(30.0, y0 - 1, y1 + 1, L, 0) \
        - box(L - 30.0, L + 30.0, y0 - 1, y1 + 1, 0, 40)
    return arm + sad


def reel_local(theta):
    """Reel parts in the arm frame (axle at local (ARM_L, 0)); carriers set so one is at the top."""
    bd = _b()
    L = P["ARM_L"]
    ro = P["AXLE_OD"] / 2
    axle = tube_y(ro, ro - P["AXLE_T"], *P["AXLE_Y"], L, 0)
    spiders, bars = [], []
    angles = [90.0 + theta + 60.0 * k for k in range(P["N_BARS"])]
    for yc in P["SPIDER_Y"]:
        y0, y1 = yc - P["SPOKE_T"] / 2, yc + P["SPOKE_T"] / 2
        sp = tube_y(30.15, ro, yc - 20, yc + 20, L, 0)          # hub sleeve, 60.3 x 5.54 (bored to fit)
        for a in angles:
            c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
            p0 = (L + 29.5 * c, 0, 29.5 * s_)
            p1 = (L + P["SPOKE_R"] * c, 0, P["SPOKE_R"] * s_)
            sp = sp + bd.Pos(0, yc, 0) * bar(p0, p1, P["SPOKE_W"], P["SPOKE_T"])
        for k, a in enumerate(angles):
            a2 = angles[(k + 1) % len(angles)]
            pa = (L + P["TIE_R"] * math.cos(math.radians(a)), 0, P["TIE_R"] * math.sin(math.radians(a)))
            pb = (L + P["TIE_R"] * math.cos(math.radians(a2)), 0, P["TIE_R"] * math.sin(math.radians(a2)))
            sp = sp + bd.Pos(0, yc, 0) * bar(pa, pb, P["RING_W"], P["SPOKE_T"])
        spiders.append(sp)
    ys0 = P["SPIDER_Y"][0] + P["SPOKE_T"] / 2
    ys1 = P["SPIDER_Y"][1] - P["SPOKE_T"] / 2
    pt = P["BAR_PLATE_T"]
    for a in angles:
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
        cx, cz = L + P["RC"] * c, P["RC"] * s_
        tb = tube_y(P["BAR_OD"] / 2, P["BAR_OD"] / 2 - P["BAR_T"], ys0 + pt, ys1 - pt, cx, cz)
        # end plates 70 x 50 x 6, lying on the inner faces of the spokes
        for (y0, y1) in ((ys0, ys0 + pt), (ys1 - pt, ys1)):
            mid = (L + (P["RC"] + 5) * c, 0, (P["RC"] + 5) * s_)
            pl = bd.Pos(*mid) * bd.Rot(0, -a, 0) * bd.Pos(0, (y0 + y1) / 2, 0) * bd.Box(75, pt, 50)
            tb = tb + pl
        # three eye tabs (6 mm plate, 12 mm hole) welded on the outer side of the bar for snap hooks
        for ye in P["EYE_Y"]:
            mid = (L + (P["RC"] + P["BAR_OD"] / 2 + 10) * c, ye, (P["RC"] + P["BAR_OD"] / 2 + 10) * s_)
            tab = bd.Pos(*mid) * bd.Rot(0, -a, 0) * (bd.Box(22, 6, 30) - bd.Rot(90, 0, 0) * bd.Cylinder(6, 8))
            tb = tb + tab
        bars.append(tb)
    return axle, spiders, bars, angles


def components(P_=None, theta=None):
    """Every component on its own, arms at THETA (or the angle given). how: make, buy or tool."""
    bd = _b()
    th = P["THETA"] if theta is None else theta
    T = arm_frame(th)
    out = []
    add = lambda *a, **k: out.append(C(*a, **k))  # noqa: E731
    S, St = P["SHS"], P["SHS_T"]
    bx0, bx1 = P["BASE_X"]
    by0, by1 = P["BASE_Y"]
    pad = P["PAD_T"]
    zb0, zb1 = pad, pad + S
    zc = (zb0 + zb1) / 2
    piv = P["PIV_Z"]
    pf, pr = P["PLATE_Y"][1], P["PLATE_Y"][0]       # front plate centre -70, rear -360
    pt = P["PLATE_T"]
    px = P["PLATE_X"]
    top = P["TOWER_TOP"]

    # ---- 1 Near stand base frame (SHS 40 x 40 x 2, 304), on four EPDM pads
    base = shs_x(bx0, bx1, by1 - S / 2, zc, S, St) + shs_x(bx0, bx1, by0 + S / 2, zc, S, St) \
        + shs_x(bx0 + S, bx1 - S, pr, zc, S, St) \
        + shs_y(by0 + S, by1 - S, bx0 + S / 2, zc, S, St) + shs_y(by0 + S, by1 - S, bx1 - S / 2, zc, S, St)
    add("base", "Near stand base frame", base, "#6B7280", 1, "make", "near_stand", (0, -300, -250))
    pads = [box(x - 40, x + 40, y - 40, y + 40, 0, pad) for x in (bx0 + 20, bx1 - 20) for y in (by0 + 20, by1 - 20)]
    add("pads", "Rubber pads (6)", bd.Compound(children=pads), "#1F2937", 15, "buy", "near_stand", (0, -300, -400), "epdm")

    # ---- 2 Bearing tower: two 5 mm plates, side covers, top plate (304)
    jd, cd = P["JACK_D"], P["CRANK_D"]
    def plate(yc):
        s = box(-px, px, yc - pt / 2, yc + pt / 2, zb1, top)
        s = s - cyl_y(25.0, yc - 5, yc + 5, 0, piv) - cyl_y(19.0, yc - 5, yc + 5, 0, P["CRANK_Z"])
        if yc == pr:
            s = s - cyl_y(6.0, yc - 5, yc + 5, 70.0, P["CRANK_Z"] + 75.0)   # pawl pin hole
        return s
    covers = [box(sx * px, sx * (px + 1.5), pr - pt / 2, pf + pt / 2, zb1, top) for sx in (-1, 1)]
    tower = plate(pr) + plate(pf) + box(-px, px, pr - pt / 2, pf + pt / 2, top, top + 6) \
        + box(-px, px, pr + pt / 2, pf - pt / 2, zb1, zb1 + 1.5)       # 1.5 mm bottom sheet closes the chain case
    for c_ in covers:
        tower = tower + c_
    braces = []
    # two side braces (SHS 30 x 30 x 2), bolted from the tower down to the base mid rail, in the rear plate plane
    for sx, xend in ((-1, bx0 + S), (1, bx1 - S)):
        b0 = (sx * (px + 1.5), pr, 880.0)
        b1 = (xend, pr, zb1)
        br = (bar(b0, b1, 30.0, 30.0) - bar(b0, b1, 26.0, 26.0)) - box(-px - 1.5, px + 1.5, pr - 40, pr + 40, 0, 2000) - box(-3000, 3000, pr - 40, pr + 40, -100, zb1)
        if sx < 0:
            br = br - box(-3000, bx0 + S, pr - 40, pr + 40, -100, 2000)
        else:
            br = br - box(bx1 - S, 3000, pr - 40, pr + 40, -100, 2000)
        braces.append(br)
    add("tower", "Bearing tower", tower, "#4B5563", 2, "make", "near_stand", (0, -300, 0))
    add("braces", "Tower braces (2)", braces[0] + braces[1], "#9CA3AF", 2, "make", "near_stand", (0, -300, 0))

    # bushes in the tower plates (UHMW-PE, flanged)
    bushes = []
    for yc, fl in ((pr, -1), (pf, 1)):
        y0, y1 = yc - pt / 2, yc + pt / 2
        fy = (y0 - 2, y0) if fl < 0 else (y1, y1 + 2)
        bushes.append(tube_y(25.0, jd / 2, y0, y1, 0, piv) + tube_y(31.0, jd / 2, fy[0], fy[1], 0, piv))
        bushes.append(tube_y(19.0, cd / 2, y0, y1, 0, P["CRANK_Z"]) + tube_y(25.0, cd / 2, fy[0], fy[1], 0, P["CRANK_Z"]))
    add("tower_bushes", "Tower bushes (4, UHMW-PE)", bd.Compound(children=bushes), "#F5F5F4", 9, "buy", "drive", (0, -300, 0), "uhmw")

    # ---- 3 Jackshaft (40 mm 316 bar) and its sprockets
    jy0, jy1 = P["JACK_Y"]
    add("jackshaft", "Jackshaft", cyl_y(jd / 2, jy0, jy1, 0, piv), "#94A3B8", 3, "make", "drive", (0, 0, 0))
    c1y = P["CHAIN1_Y"]
    add("sprocket_j1", "Jackshaft sprocket, 24 teeth", sprocket(P["Z_JACK1"], c1y - 3.6, 0, piv, 34.0, (c1y + 3.6, c1y + 23.6), jd),
        "#B45309", 10, "buy", "drive", (0, 0, 0))
    c2y = P["CHAIN2_Y"]
    add("sprocket_j2", "Jackshaft sprocket, 12 teeth", sprocket(P["Z_JACK2"], c2y - 3.6, 0, piv, 30.0, (60.0, c2y - 3.6), jd),
        "#B45309", 10, "buy", "drive", (0, 0, 0))

    # ---- 4 Crank shaft, crank and handle, ratchet and pawl
    cy0, cy1 = P["CRANK_Y"]
    cz = P["CRANK_Z"]
    add("crankshaft", "Crank shaft", cyl_y(cd / 2, cy0, cy1, 0, cz), "#94A3B8", 4, "make", "drive")
    add("sprocket_c", "Crank sprocket, 12 teeth", sprocket(P["Z_CRANK"], c1y - 3.6, 0, cz, 24.0, (c1y + 3.6, c1y + 23.6), cd),
        "#B45309", 10, "buy", "drive")
    R = P["CRANK_R"]
    crank = box(-R, 0, -550, -540, cz - 20, cz + 20) + cyl_y(25.0, -560, -530, 0, cz) - cyl_y(cd / 2, -561, -529, 0, cz) \
        + cyl_y(22.0, -560, -540, -R, cz)
    add("crank", "Crank arm with hub", crank, "#0F766E", 4, "make", "drive", (0, -250, 0))
    add("grip", "Crank handle grip", cyl_y(16.0, -680, -560, -R, cz), "#111827", 4, "buy", "drive", (0, -350, 0), "uhmw")
    # ratchet: 24 teeth, 120 mm over the tips, 8 mm 304 plate, behind the rear plate
    ratchet_pts = []
    nt = 24
    for k in range(nt):
        a0 = 2 * math.pi * k / nt
        a1 = 2 * math.pi * (k + 0.85) / nt
        ratchet_pts += [(52 * math.cos(a0), 52 * math.sin(a0)), (60 * math.cos(a1), 60 * math.sin(a1))]
    rw = bd.extrude(bd.Polygon(*ratchet_pts, align=None), 8.0)
    rw = bd.Pos(0, -396.0, cz) * bd.Rot(90, 0, 0) * rw     # spans y -404 .. -396
    rw = rw + cyl_y(22.0, -396, -380, 0, cz) - cyl_y(cd / 2, -405, -379, 0, cz)
    add("ratchet", "Ratchet wheel", rw, "#0D9488", 5, "make", "drive", (0, -200, 0))
    pawl_pts = [(76, cz + 85), (64, cz + 75), (36, cz + 44), (44, cz + 38), (82, cz + 66), (84, cz + 80)]
    pawl = _xz_place(bd.extrude(bd.Polygon(*[(x, z) for x, z in pawl_pts], align=None), 8.0), -404.0)
    pin = cyl_y(6.0, -440.0, pr - pt / 2, 70.0, cz + 75.0)
    knob = box(64.0, 76.0, -440.0, -430.0, cz + 75.0, cz + 130.0)       # release lever outside the cover
    add("pawl", "Pawl on its pin, with release lever", pawl + pin + knob, "#DC2626", 5, "make", "drive", (0, -200, 120))
    rc = box(-75.0, 100.0, -416.0, pr - pt / 2, cz - 70.0, cz + 100.0) - box(-73.5, 98.5, -414.5, pr - pt / 2 + 1, cz - 68.5, cz + 98.5)
    rc = rc - cyl_y(cd / 2 + 1.0, -420.0, -410.0, 0, cz) - cyl_y(7.0, -420.0, -410.0, 70.0, cz + 75.0)
    add("ratchet_cover", "Ratchet cover", rc, "#9CA3AF", 5, "make", "drive", (0, -350, 120))

    # chain 1 (vertical, inside the tower)
    add("chain1", "Chain 1 (08B, crank to jackshaft)", chain_band((0, cz), pcd(P["Z_CRANK"]) / 2, (0, piv), pcd(P["Z_JACK1"]) / 2, c1y),
        "#374151", 11, "buy", "drive")

    # ---- 6 Splash shield: 25 x 25 x 3 angle frame, 4 mm translucent polypropylene sheet
    sx0, sx1 = P["SHIELD_X"]
    sz0, sz1 = P["SHIELD_Z"]
    fy0, fy1 = P["SHIELD_Y"], P["SHIELD_Y"] + 25.0
    a_, ta = 25.0, 3.0      # 25 x 25 x 3 angle: one leg flat behind the sheet, one leg running back to the tower
    frame = box(sx0, sx0 + a_, fy1 - ta, fy1, zb1, sz1) + box(sx0, sx0 + ta, fy0, fy1, zb1, sz1) \
        + box(sx1 - a_, sx1, fy1 - ta, fy1, zb1, sz1) + box(sx1 - ta, sx1, fy0, fy1, zb1, sz1) \
        + box(sx0 + a_, sx1 - a_, fy1 - ta, fy1, sz1 - a_, sz1) + box(sx0 + a_, sx1 - a_, fy0, fy1, sz1 - ta, sz1) \
        + box(sx0 + a_, sx1 - a_, fy1 - ta, fy1, sz0, sz0 + a_) + box(sx0 + a_, sx1 - a_, fy0, fy1, sz0, sz0 + ta)
    add("shield_frame", "Splash shield frame", frame, "#9CA3AF", 6, "make", "near_stand", (0, 250, 0))
    add("shield_sheet", "Splash shield sheet (polypropylene)",
        box(sx0 + 25, sx1 - 25, fy1, fy1 + 4, sz0 + 25, sz1 - 25) - cyl_y(26.0, fy1 - 1, fy1 + 5, 0, piv),
        "#BFDBFE", 6, "buy", "near_stand", (0, 300, 0), "pp")

    # ---- 7 Lift screw bracket (SHS 50 x 50 x 3) with fork plates, bolted on the tower top
    ux, uz = P["SCREW_PIV"]
    m1 = shs_x(-330.0, 60.0, -125.0, top + 6 + 25, 50.0, 3.0)
    m2 = shs_y(-100.0, 165.0, -305.0, top + 6 + 25, 50.0, 3.0)
    brk = m1 + m2
    for (a, b_) in P["FORK_Y"]:
        brk = brk + box(-330.0, -215.0, a, b_, uz - 40.0, top + 6)
    add("bracket", "Lift screw bracket", brk, "#4B5563", 7, "make", "lift", (0, 0, 300))

    # ---- 8 Lift screw, trunnion blocks, handwheel
    lx, lz = lug_xz(th)
    sy = P["SCREW_Y"]
    d = bd.Vector(ux - lx, 0, uz - lz).normalized()
    up_end = bd.Vector(ux, sy, uz) + d * 140.0
    low_end = bd.Vector(ux, sy, uz) - d * 1100.0
    add("screw", "Lift screw, Tr24 x 5", rod(tuple(low_end), tuple(up_end), P["SCREW_D"] / 2), "#CBD5E1", 8, "buy", "lift")
    ang = math.degrees(math.atan2(d.X, d.Z))
    fy = P["FORK_Y"]
    blk = lambda x, z: bd.Pos(x, sy, z) * bd.Rot(0, ang, 0) * (bd.Box(50, fy[1][0] - fy[0][1], 50) - bd.Cylinder(P["SCREW_D"] / 2, 60))  # noqa: E731
    add("trunnion_up", "Upper trunnion block with thrust bearing", blk(ux, uz), "#64748B", 8, "make", "lift", (0, 0, 300))
    add("trunnion_nut", "Nut trunnion block with bronze nut", blk(lx, lz), "#B08D57", 8, "make", "lift", (0, 0, 0))
    hw_c = bd.Vector(ux, sy, uz) + d * 110.0
    pl = bd.Plane(origin=hw_c, z_dir=d)
    hr = P["HANDWHEEL_D"] / 2
    wheel = pl * (bd.Cylinder(hr, 18) - bd.Cylinder(hr - 16, 20)) + pl * bd.Cylinder(22, 30)
    for k in range(3):
        wheel = wheel + pl * bd.Rot(0, 0, 120 * k) * bd.Pos((hr - 8) / 2 + 10, 0, 0) * bd.Box(hr - 18, 14, 10)
    wheel = wheel + pl * bd.Pos(hr - 8, 0, 9 + 40) * bd.Cylinder(12, 80)
    wheel = wheel - pl * bd.Cylinder(P["SCREW_D"] / 2, 80)
    add("handwheel", "Handwheel, 250 mm", wheel, "#111827", 8, "buy", "lift", (0, 0, 400))

    # ---- 9 Pivot tube A with its plug, extension tube B, collars
    ao, at = P["TUBE_A"]
    ay0, ay1 = P["TUBE_A_Y"]
    tubeA = tube_y(ao / 2, ao / 2 - at, ay0, ay1, 0, piv)
    plug = tube_y(ao / 2 - at, jd / 2, ay0, ay0 + 70, 0, piv)
    add("tube_a", "Pivot tube", tubeA, "#9CA3AF", 12, "make", "frame", (0, 0, 0))
    add("plug", "Pivot tube plug with bush", plug, "#F5F5F4", 12, "make", "frame", (0, 0, 0), "uhmw")
    bo, bt = P["TUBE_B"]
    by0_, by1_ = P["TUBE_B_Y"]
    add("tube_b", "Extension tube", tube_y(bo / 2, bo / 2 - bt, by0_, by1_, 0, piv), "#A3A3A3", 13, "make", "frame", (0, 500, 0))
    fh0, fh1 = P["FAR_HUB_Y"]
    collars = tube_y(34.0, ao / 2, fh0 - 15, fh0, 0, piv) + tube_y(45.0, ao / 2, fh1, fh1 + 15, 0, piv)
    add("collars", "Shaft collars (2)", collars, "#111827", 12, "buy", "frame", (0, 0, 0))

    # ---- 10 Far stand: crossbeam, legs, feet, clamp block and split sleeve, pads
    W = P["PIT_W"]
    fyc = W + P["FAR_Y"]
    fx0, fx1 = P["FAR_X"]
    far = shs_x(fx0, fx1, fyc, 135.0, 50.0, 3.0)
    for xl in (fx0 + 25, fx1 - 25):
        far = far + shs_z(16.0, 110.0, xl, fyc, 50.0, 3.0) + box(xl - 50, xl + 50, fyc - 50, fyc + 50, pad, 16.0)
    clamp = box(-45, 45, fyc - 30, fyc + 30, 160.0, 250.0) - cyl_y(ao / 2, fyc - 31, fyc + 31, 0, piv)
    far = far + clamp
    add("far_stand", "Far stand with clamp", far, "#6B7280", 14, "make", "far_stand", (0, 400, -150))
    add("sleeve", "Split sleeve", tube_y(ao / 2, bo / 2, fyc - 30, fyc + 30, 0, piv), "#D6D3D1", 14, "make", "far_stand", (0, 400, -150))
    fpads = [box(xl - 50, xl + 50, fyc - 50, fyc + 50, 0, pad) for xl in (fx0 + 25, fx1 - 25)]
    add("far_pads", "Rubber pads, far stand (2)", bd.Compound(children=fpads), "#1F2937", 15, "buy", "far_stand", (0, 400, -300), "epdm")

    # ---- 11 Arm frame: torque tube round the pivot line, near arm with lever plates, far arm; bushes, collars
    tto, ttt = P["TORQUE_TUBE"]
    t0, t1 = P["TORQUE_Y"]
    nh0, nh1 = P["NEAR_HUB_Y"]
    add("torque_tube", "Torque tube", T * tube_y(tto / 2, tto / 2 - ttt, t0, t1, 0, 0), "#14B8A6", 16, "make", "arms", (0, 0, 250))
    add("near_arm", "Near arm with lever plates", T * near_arm_local(), "#0F766E", 16, "make", "arms", (0, 0, 250))
    add("far_arm", "Far arm with open saddle", T * far_arm_local(), "#0F766E", 16, "make", "arms", (0, 0, 250))
    add("near_arm_bush", "Torque tube bush on the jackshaft (UHMW-PE)", T * tube_y(tto / 2 - ttt, jd / 2, nh0, nh1, 0, 0),
        "#F5F5F4", 9, "buy", "arms", (0, 0, 250), "uhmw")
    add("far_arm_bush", "Torque tube bush on the pivot tube (UHMW-PE)", T * tube_y(tto / 2 - ttt, ao / 2, fh0, fh1, 0, 0),
        "#F5F5F4", 9, "buy", "arms", (0, 0, 250), "uhmw")
    L = P["ARM_L"]
    hx, hz = P["HOUSING"]
    add("axle_bushes", "Axle bushes (2, glass-filled PTFE)",
        T * (tube_y(30.0, P["AXLE_OD"] / 2, *P["NEAR_ARM_Y"], L, 0) + tube_y(30.0, P["AXLE_OD"] / 2, *P["FAR_ARM_Y"], L, 0)),
        "#E7E5E4", 9, "buy", "arms", (0, 0, 250), "ptfe")
    keeper = box(L - 40, L + 40, *P["FAR_ARM_Y"], 32.0, 40.0)
    add("keeper", "Saddle keeper", T * keeper, "#DC2626", 16, "make", "arms", (0, 0, 400))
    # chain 2 guard: a closed case of 1.5 mm 316 sheet round the chain (two side plates and a rim strip),
    # bolted to the near arm on two spacer tubes
    gy0, gy1 = 55.0, 92.0
    guard = stadium_xz((0, 0), 56.0, (L, 0), 125.0, gy0, gy1) - stadium_xz((0, 0), 54.5, (L, 0), 123.5, gy0 + 1.5, gy1 - 1.5)
    guard = guard - cyl_y(22.0, gy0 - 1, gy1 + 1, 0, 0) - cyl_y(26.0, gy1 - 3, gy1 + 1, L, 0)
    for xs in (300.0, 600.0):
        guard = guard + cyl_y(8.0, gy1, P["NEAR_ARM_Y"][0], xs, 0)
    add("guard2", "Chain 2 guard", T * guard, "#A8A29E", 17, "make", "arms", (0, -350, 250))

    # ---- 12 Reel: axle, spiders, carrier bars; chain 2 and axle sprocket
    axle, spiders, bars, angles = reel_local(th)
    add("axle", "Reel axle", T * axle, "#CBD5E1", 18, "make", "reel", (0, 0, 650))
    add("spider_near", "Reel spider, near", T * spiders[0], "#64748B", 18, "make", "reel", (0, 0, 650))
    add("spider_far", "Reel spider, far", T * spiders[1], "#64748B", 18, "make", "reel", (0, 0, 650))
    add("bars", "Carrier bars (6)", T * bd.Compound(children=bars), "#0EA5E9", 19, "make", "reel", (0, 0, 900))
    add("sprocket_a", "Axle sprocket, 36 teeth", T * sprocket(P["Z_AXLE"], c2y - 3.6, L, 0, 35.0, (62.0, c2y - 3.6), P["AXLE_OD"]),
        "#B45309", 10, "buy", "reel", (0, 0, 650))
    add("chain2", "Chain 2 (08B, jackshaft to reel)", T * chain_band((0, 0), pcd(P["Z_JACK2"]) / 2, (L, 0), pcd(P["Z_AXLE"]) / 2, c2y),
        "#374151", 11, "buy", "arms", (0, -200, 250))

    # ---- 20 Loading hooks (2), stored across the base frame
    hooks = []
    for yh in (by0 + 8.0, by0 + 32.0):
        zh = zb1 + 14.0
        h = rod((-480.0, yh, zh), (1020.0, yh, zh), 6.0)                 # 1.5 m of 12 mm rod
        h = h + rod((1020.0, yh, zh), (1020.0, yh, zh + 60.0), 6.0)       # the hook end
        h = h + rod((-600.0, yh, zh), (-480.0, yh, zh), 14.0)             # handle
        hooks.append(h)
    add("hooks", "Loading hooks (2)", bd.Compound(children=hooks), "#B91C1C", 20, "make", "tools", (0, -400, 0))
    return out


# ---------------------------------------------------------------------------
# BOM grouping
# ---------------------------------------------------------------------------
BOM_NAMES = {
    1: ("Near stand base frame", "#6B7280", (0, -500, -250)),
    2: ("Bearing tower with braces", "#4B5563", (0, -500, 0)),
    3: ("Jackshaft", "#94A3B8", (0, -250, -200)),
    4: ("Crank shaft, crank and grip", "#0F766E", (0, -750, 150)),
    5: ("Ratchet and pawl", "#0D9488", (0, -650, 350)),
    6: ("Splash shield", "#BFDBFE", (0, -700, 300)),
    7: ("Lift screw bracket", "#4B5563", (0, 0, 650)),
    8: ("Lift screw, trunnions and handwheel", "#CBD5E1", (-400, 0, 650)),
    9: ("Bushes (UHMW-PE and PTFE)", "#F5F5F4", (0, 0, 0)),
    10: ("Sprockets (4)", "#B45309", (0, 0, 0)),
    11: ("Roller chains (2)", "#374151", (0, 0, 0)),
    12: ("Pivot tube with plug and collars", "#9CA3AF", (0, 250, -300)),
    13: ("Extension tube", "#A3A3A3", (0, 700, -300)),
    14: ("Far stand with clamp and sleeve", "#6B7280", (0, 900, -300)),
    15: ("Rubber pads (6)", "#1F2937", (0, 0, -400)),
    16: ("Arm frame (torque tube, two arms, keeper)", "#0F766E", (0, 0, 350)),
    17: ("Chain 2 guard", "#A8A29E", (0, -450, 350)),
    18: ("Reel (axle and two spiders)", "#64748B", (700, 300, 700)),
    19: ("Carrier bars (6)", "#0EA5E9", (1400, 300, 700)),
    20: ("Loading hooks (2)", "#B91C1C", (0, -900, 0)),
}


def build_parts(comps=None, theta=None):
    """Components grouped by BOM line: a list of (name, shape, color, bom_no, explode_offset)."""
    bd = _b()
    comps = comps or components(theta=theta)
    parts = []
    for bom, (name, color, exp) in BOM_NAMES.items():
        kids = [c.shape for c in comps if c.bom == bom]
        if kids:
            parts.append((name, bd.Compound(kids), color, bom, exp))
    return parts


def assembly(parts=None):
    bd = _b()
    parts = parts or build_parts()
    return bd.Compound([p[1] for p in parts])


def pit_context(P_=None):
    """The pit, its rim and the liquor, for pictures only (not part of VatReel)."""
    W = P["PIT_W"]
    x0, x1 = P["PIT_END"], P["PIT_END"] + P["PIT_LEN"]
    D = P["PIT_DEPTH"]
    slab = box(x0 - 700, x1 + 300, -1300, W + 500, -D - 100, 0) - box(x0, x1, 0, W, -D, 1)
    liquor = box(x0, x1, 0, W, -D, P["LIQUOR"])
    return slab, liquor


# ---------------------------------------------------------------------------
# Fit checks
# ---------------------------------------------------------------------------
CONTACTS = [
    ("pads", "base"), ("tower", "base"), ("braces", "tower"), ("braces", "base"), ("tower_bushes", "tower"), ("jackshaft", "tower_bushes"),
    ("crankshaft", "tower_bushes"), ("sprocket_j1", "jackshaft"), ("sprocket_j2", "jackshaft"),
    ("sprocket_c", "crankshaft"), ("crank", "crankshaft"), ("grip", "crank"), ("ratchet", "crankshaft"),
    ("pawl", "tower"), ("ratchet_cover", "tower"), ("shield_frame", "base"), ("shield_frame", "tower"), ("shield_sheet", "shield_frame"),
    ("bracket", "tower"), ("trunnion_up", "bracket"), ("screw", "trunnion_up"), ("screw", "trunnion_nut"),
    ("trunnion_nut", "near_arm"), ("handwheel", "screw"),
    ("plug", "jackshaft"), ("plug", "tube_a"), ("tube_b", "tube_a"), ("collars", "tube_a"),
    ("sleeve", "tube_b"), ("sleeve", "far_stand"), ("far_pads", "far_stand"),
    ("near_arm_bush", "jackshaft"), ("near_arm_bush", "torque_tube"), ("far_arm_bush", "tube_a"), ("far_arm_bush", "torque_tube"),
    ("near_arm", "torque_tube"), ("far_arm", "torque_tube"), ("axle_bushes", "near_arm"), ("axle_bushes", "far_arm"),
    ("axle", "axle_bushes"), ("keeper", "far_arm"), ("guard2", "near_arm"),
    ("spider_near", "axle"), ("spider_far", "axle"), ("bars", "spider_near"), ("bars", "spider_far"),
    ("sprocket_a", "axle"), ("hooks", "base"),
]

# Pairs that share volume on purpose: a chain envelope round its sprocket teeth, a pawl in a ratchet tooth
ALLOWED = {frozenset(p) for p in (("chain1", "sprocket_c"), ("chain1", "sprocket_j1"), ("chain2", "sprocket_j2"),
                                  ("chain2", "sprocket_a"), ("pawl", "ratchet"))}


def _solids(shape):
    try:
        return list(shape.solids()) or [shape]
    except Exception:
        return [shape]


def _bb_apart(A, B, pad=0.0):
    return (A.min.X > B.max.X + pad or B.min.X > A.max.X + pad or A.min.Y > B.max.Y + pad or B.min.Y > A.max.Y + pad
            or A.min.Z > B.max.Z + pad or B.min.Z > A.max.Z + pad)


def check_fits(comps=None, tol=1.0, verbose=True, contacts=None, label=""):
    """No two components may overlap (more than tol mm3), and every CONTACTS pair must touch (gap at most
    0.6 mm, a sliding fit). Returns (overlaps, gaps)."""
    comps = comps or components()
    sol = {c.key: [(s_, s_.bounding_box()) for s_ in _solids(c.shape)] for c in comps}
    bbs = {c.key: c.shape.bounding_box() for c in comps}
    overlaps = []
    for i, a in enumerate(comps):
        for b_ in comps[i + 1:]:
            if frozenset((a.key, b_.key)) in ALLOWED or _bb_apart(bbs[a.key], bbs[b_.key]):
                continue
            v = 0.0
            for sa, ba in sol[a.key]:
                if _bb_apart(ba, bbs[b_.key]):
                    continue
                for sb, bb_ in sol[b_.key]:
                    if _bb_apart(ba, bb_):
                        continue
                    r = sa & sb
                    try:
                        v += r.volume if r is not None else 0.0
                    except Exception:
                        pass
            if v >= tol:
                overlaps.append((a.key, b_.key, v))
    gaps = []
    for ka, kb in (CONTACTS if contacts is None else contacts):
        if ka not in sol or kb not in sol:
            continue
        near = [(sa, sb) for sa, ba in sol[ka] for sb, bb_ in sol[kb] if not _bb_apart(ba, bb_, 1.0)]
        d = min(sa.distance_to(sb) for sa, sb in near) if near else 99.0
        if d > 0.6:
            gaps.append((ka, kb, d))
    if verbose:
        print(f"fit check{label}: {len(comps)} components; {len(overlaps)} overlaps; {len(gaps)} missing contacts")
        for o in overlaps:
            print(f"  OVERLAP {o[0]} / {o[1]}: {o[2]:.1f} mm3")
        for g_ in gaps:
            print(f"  NO CONTACT {g_[0]} / {g_[1]}: {g_[2]:.2f} mm apart")
    return overlaps, gaps


MOVING = ("torque_tube", "near_arm", "near_arm_bush", "far_arm", "far_arm_bush", "axle_bushes", "keeper", "guard2",
          "axle", "spider_near", "spider_far", "bars", "sprocket_a", "chain2", "screw", "trunnion_nut",
          "trunnion_up", "handwheel")


def check_positions(verbose=True):
    """Rebuild the arms, reel and screw at the lifted, shallow and deep angles and check that nothing
    collides with the frame or the pit walls (the pit is checked as a solid)."""
    bad = []
    slab, _ = pit_context()
    for name, th in (("lifted", P["THETA_LIFT"]), ("shallowest", P["THETA_SHALLOW"]), ("deepest", P["THETA_DEEP"])):
        comps = components(theta=th)
        ov, gp = check_fits(comps, verbose=verbose, label=f" ({name}, arms {th:+.1f} deg)")
        bad += [(name,) + o for o in ov] + [(name,) + g for g in gp]
        hit = []
        for c in comps:
            if c.key in MOVING:
                r = c.shape & slab
                try:
                    v = r.volume if r is not None else 0.0
                except Exception:
                    v = 0.0
                if v > 1.0:
                    hit.append(c.key)
        if verbose:
            print(f"  pit walls touched by moving parts: {', '.join(hit) if hit else 'none'}")
        bad += [(name, "pit", h) for h in hit]
    return bad


def masses(comps=None):
    """Mass of each component (kg) from its solid volume and material density."""
    comps = comps or components()
    out = {}
    for c in comps:
        try:
            v = sum(s_.volume for s_ in _solids(c.shape))
        except Exception:
            v = c.shape.volume
        out[c.key] = v * 1e-9 * DENS.get(c.mat, STEEL)
    return out


if __name__ == "__main__":
    import sys
    from build123d import Compound, export_step, export_stl
    comps = components()
    if "--check" in sys.argv:
        ov, gp = check_fits(comps)
        bad = check_positions()
        ok = not (ov or gp or bad)
        print("constructability checks:", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    parts = build_parts(comps)
    export_step(assembly(parts), str(root / "step" / "vatreel-assembly.step"))
    by = {c.key: c.shape for c in comps}
    for stem, keys in [("near-arm", ["near_arm"]), ("far-arm", ["far_arm"]), ("reel", ["axle", "spider_near", "spider_far"]),
                       ("carrier-bars", ["bars"]), ("bearing-tower", ["tower"]), ("far-stand", ["far_stand"])]:
        shp = Compound(children=[by[k] for k in keys])
        export_step(shp, str(root / "step" / f"{stem}.step"))
        export_stl(shp, str(root / "stl" / f"{stem}.stl"))
    bb = assembly(parts).bounding_box()
    g = geometry()
    print(f"envelope {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.max.Z:.0f} mm above the rim; reel reaches {g['reel_bottom']:.0f} mm")
    m = masses(comps)
    print(f"mass {sum(m.values()):.1f} kg")
    print("wrote cad/step/*.step and cad/stl/*.stl")
