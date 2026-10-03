"""VatReel sizing and first-principles checks (VTR-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Geometry comes from PARAMS and geometry() in
cad/src/model.py; masses come from the model solids; the cost is read from bom/bom.csv. All values are
estimates for a paper design (TRL 3); nothing here is measured.
"""
from __future__ import annotations

import csv
import math
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
import model as m  # noqa: E402

P = m.PARAMS
G = 9.81

# Loads and factors (Table 1 of the note)
LOAD_KG = 25.0          # R2: wet load on the reel (hides or yarn with the liquor they carry)
PROOF = 1.5             # R5: proof factor on the rated load
ETA_CHAIN = 0.95        # each roller chain stage with its plain bearings
MU_PTFE = 0.10          # glass-filled PTFE on stainless, wet
CRANK_RPM = 30.0        # a steady hand-cranking speed

# Materials (minimum 0.2 % proof stress, MPa)
FY_316L_TUBE = 170.0    # 316L tube and sheet, annealed
FY_316_BAR = 205.0      # 316 bar
FY_304 = 205.0          # 304 sections and plate
E_SS = 193e3            # MPa
ALLOW = 1.5             # allowable = yield / 1.5 at the proof load

# Chain ISO 606 08B-1
CHAIN_BREAK = 18.0e3    # N, minimum tensile strength

# Lift screw Tr24 x 5, bronze nut, thrust ball bearing at the top
D2, D3 = 21.5, 18.5     # pitch and root diameters, mm
MU_THREAD = 0.15        # bronze on stainless, wet and dirty (conservative)
FLANK = math.radians(15.0)
T_BEARING = 0.3         # N m, thrust ball bearing at about 2 kN

# Operator and shield (R9)
EYE = (-250.0, -1150.0, 1600.0)   # eye of a 1.75 m operator at the crank (x, y, z)

# Prices are in bom/bom.csv


def tube_z(od, t):
    """Section modulus (mm3) and area (mm2) of a round tube."""
    di = od - 2 * t
    return math.pi * (od ** 4 - di ** 4) / (32 * od), math.pi * (od ** 2 - di ** 2) / 4


def rect_z(h, b, t):
    """Section modulus (mm3) of a rectangular hollow section bent about the axis parallel to b."""
    I = (b * h ** 3 - (b - 2 * t) * (h - 2 * t) ** 3) / 12
    return I / (h / 2)


@lru_cache(maxsize=None)
def _masses():
    return m.masses()


def mass_summary():
    ms = _masses()
    def s(keys):
        return sum(ms[k] for k in keys)
    modules = {
        "Near stand base frame with pads and hooks": s(["base", "pads", "hooks"]),
        "Bearing tower, bare": s(["tower"]),
        "Shafts, sprockets, chain 1, crank and ratchet (fitted in place)": s(["tower_bushes", "jackshaft", "sprocket_j1", "sprocket_j2",
                                                                              "crankshaft", "sprocket_c", "crank", "grip", "ratchet", "pawl",
                                                                              "ratchet_cover", "chain1"]),
        "Tower braces (2)": s(["braces"]),
        "Splash shield": s(["shield_frame", "shield_sheet"]),
        "Lift screw bracket": s(["bracket"]),
        "Lift screw with trunnions and handwheel": s(["screw", "trunnion_up", "trunnion_nut", "handwheel"]),
        "Pivot tube with arm frame on it": s(["tube_a", "plug", "collars", "torque_tube", "near_arm", "far_arm", "near_arm_bush",
                                              "far_arm_bush", "axle_bushes", "keeper"]),
        "Extension tube": s(["tube_b"]),
        "Far stand with sleeve and pads": s(["far_stand", "sleeve", "far_pads"]),
        "Chain 2 guard with chain 2": s(["guard2", "chain2"]),
        "Reel with carrier bars and axle sprocket": s(["axle", "spider_near", "spider_far", "bars", "sprocket_a"]),
    }
    two_person = {"Pivot tube with arm frame on it", "Reel with carrier bars and axle sprocket"}
    per_person = {k: (v / 2 if k in two_person else v) for k, v in modules.items()}
    heavy = max(modules.values())
    reel = s(["axle", "spider_near", "spider_far", "bars", "sprocket_a"])
    moving = s(["torque_tube", "near_arm", "far_arm", "near_arm_bush", "far_arm_bush", "axle_bushes", "keeper", "guard2", "chain2"]) + reel
    return dict(total=sum(ms.values()), modules=modules, per_person=per_person, two_person=two_person,
                heaviest=heavy, heaviest_person=max(per_person.values()), reel=reel, moving=moving,
                arm_frame=s(["torque_tube", "near_arm", "far_arm", "keeper"]))


def depth_table():
    rows = []
    for name, th in (("Lifted", P["THETA_LIFT"]), ("Shallowest working", P["THETA_SHALLOW"]),
                     ("Modelled (mid depth)", P["THETA"]), ("Deepest working", P["THETA_DEEP"])):
        g = m.geometry(th)
        rows.append(dict(name=name, theta=th, axle_x=g["axle_x"], axle_z=g["axle_z"], low=g["low_bar"], top=g["top_bar"],
                         x0=g["reel_x0"], x1=g["reel_x1"], screw=g["screw_len"]))
    return rows


def drive():
    """Worst case: the whole wet load on one carrier bar level with the axle, buoyancy and drag ignored."""
    ms = mass_summary()
    t_load = LOAD_KG * G * P["RC"] / 1000.0
    radial = (ms["reel"] + LOAD_KG) * G
    t_fric = MU_PTFE * radial * (P["AXLE_OD"] / 2) / 1000.0
    t_reel = t_load + t_fric
    r2 = P["Z_AXLE"] / P["Z_JACK2"]
    r1 = P["Z_JACK1"] / P["Z_CRANK"]
    t_jack = t_reel / r2 / ETA_CHAIN
    t_crank = t_jack / r1 / ETA_CHAIN
    force = t_crank / (P["CRANK_R"] / 1000.0)
    tens2 = t_jack / (m.pcd(P["Z_JACK2"]) / 2000.0)
    tens1 = t_crank / (m.pcd(P["Z_CRANK"]) / 2000.0)
    reel_rpm = CRANK_RPM / (r1 * r2)
    bar_speed = 2 * math.pi * P["RC"] / 1000.0 * reel_rpm / 60.0
    return dict(load_kg=LOAD_KG, t_load=t_load, t_fric=t_fric, t_reel=t_reel, t_jack=t_jack, t_crank=t_crank,
                crank_force=force, ratio=r1 * r2, eff=ETA_CHAIN ** 2, tens1=tens1, tens2=tens2,
                sf1=CHAIN_BREAK / (tens1 * PROOF), sf2=CHAIN_BREAK / (tens2 * PROOF), reel_rpm=reel_rpm,
                bar_speed=bar_speed, rev_s=60.0 / reel_rpm)


def brake():
    """R5: the ratchet on the crank shaft holds 1.5 x the worst load torque with no efficiency credit."""
    r = P["Z_JACK1"] / P["Z_CRANK"] * P["Z_AXLE"] / P["Z_JACK2"]
    t_hold = PROOF * LOAD_KG * G * P["RC"] / 1000.0 / r
    f_tooth = t_hold / 0.056
    bearing = f_tooth / (8.0 * 6.0)          # 8 mm plate, 6 mm tooth contact
    pin_shear = f_tooth / (math.pi * 6.0 ** 2)
    tau_crank = 16 * t_hold * 1e3 / (math.pi * P["CRANK_D"] ** 3)
    tau_jack = 16 * t_hold * 2 * 1e3 / (math.pi * P["JACK_D"] ** 3)
    return dict(t_hold=t_hold, f_tooth=f_tooth, bearing=bearing, pin_shear=pin_shear, tau_crank=tau_crank, tau_jack=tau_jack)


def arm_moment(theta, with_load=True):
    """Moment of the arm frame, guard, reel (and load) about the pivot line, N m."""
    ms = mass_summary()
    th = math.radians(theta)
    m_end = ms["reel"] + ms["arm_frame"] * 0.0 + _masses()["axle_bushes"] + (LOAD_KG if with_load else 0.0)
    # arms, guard and chain 2: centre of mass at about 45 % of the arm length
    m_mid = _masses()["near_arm"] + _masses()["far_arm"] + _masses()["guard2"] + _masses()["chain2"]
    return G * (m_end * P["ARM_L"] + m_mid * 0.45 * P["ARM_L"]) * math.cos(th) / 1000.0


def lift():
    """The self-locking screw that sets the arm angle (depth) and lifts the reel clear."""
    ux, uz = P["SCREW_PIV"]
    lead = P["SCREW_PITCH"]
    lam = math.atan(lead / (math.pi * D2))
    rho = math.atan(MU_THREAD / math.cos(FLANK))
    rows = []
    for name, th in (("Lifted", P["THETA_LIFT"]), ("Shallowest", P["THETA_SHALLOW"]), ("Modelled", P["THETA"]),
                     ("Deepest", P["THETA_DEEP"])):
        lx, lz = m.lug_xz(th)
        dx, dz = ux - lx, uz - lz
        L = math.hypot(dx, dz)
        ux_, uz_ = dx / L, dz / L
        rx, rz = lx - 0.0, lz - P["PIV_Z"]
        arm = abs(rx * uz_ - rz * ux_) / 1000.0
        M = arm_moment(th) * PROOF
        F = M / arm
        T = F * (D2 / 2000.0) * math.tan(lam + rho) + T_BEARING
        rows.append(dict(name=name, theta=th, length=L, arm=arm * 1000, moment=M, force=F, torque=T,
                         wheel=T / (P["HANDWHEEL_D"] / 2000.0)))
    stroke = max(r["length"] for r in rows) - min(r["length"] for r in rows)
    fmax = max(r["force"] for r in rows)
    I = math.pi * D3 ** 4 / 64
    Lb = max(r["length"] for r in rows)
    p_cr = math.pi ** 2 * E_SS * I / Lb ** 2
    sigma = fmax / (math.pi * D3 ** 2 / 4)
    return dict(rows=rows, stroke=stroke, turns=stroke / lead, lam=math.degrees(lam), rho=math.degrees(rho),
                self_locking=lam < rho, fmax=fmax, p_cr=p_cr, buckling_sf=p_cr / fmax, sigma=sigma,
                wheel_max=max(r["wheel"] for r in rows))


def structure():
    """Stresses at the proof load (1.5 x) in the parts that carry it."""
    ms = mass_summary()
    out = {}
    # carrier bar: the whole wet load on one bar, spread along it, simply supported between the spiders
    span = (P["SPIDER_Y"][1] - P["SPIDER_Y"][0]) / 1000.0
    w = PROOF * LOAD_KG * G
    Z, _ = tube_z(P["BAR_OD"], P["BAR_T"])
    out["bar"] = (w * span / 8 * 1e3 / Z, FY_316L_TUBE)
    # spoke: half that load at the spoke tip, cantilever from the hub, no help from the hexagon ties
    Zs = P["SPOKE_T"] * P["SPOKE_W"] ** 2 / 6
    out["spoke"] = (w / 2 * (P["RC"] - 30.0) / 1000.0 * 1e3 / Zs, FY_316L_TUBE)
    # reel axle: torque and bending between the arm bearings with the load at mid span
    Za, _ = tube_z(P["AXLE_OD"], P["AXLE_T"])
    span_a = (P["FAR_ARM_Y"][0] + P["FAR_ARM_Y"][1] - P["NEAR_ARM_Y"][0] - P["NEAR_ARM_Y"][1]) / 2000.0
    Wr = PROOF * (ms["reel"] + LOAD_KG) * G
    Ma = Wr * span_a / 4
    Ta = PROOF * LOAD_KG * G * P["RC"] / 1000.0
    out["axle"] = (math.sqrt((Ma * 1e3 / Za) ** 2 + 3 * (Ta * 1e3 / (2 * Za)) ** 2), FY_316L_TUBE)
    # arm: half the reel and load at the end, cantilever from the torque tube, arm horizontal
    Zarm = rect_z(P["ARM_H"], P["ARM_W"], P["ARM_T"])
    out["arm"] = (Wr / 2 * P["ARM_L"] / 1000.0 * 1e3 / Zarm, FY_316L_TUBE)
    # torque tube: the far arm's moment carried in torsion to the lever on the near end
    tto, ttt = P["TORQUE_TUBE"]
    Am = math.pi * ((tto - ttt) / 2) ** 2
    Tt = arm_moment(0.0) * PROOF / 2
    out["torque_tube"] = (math.sqrt(3) * Tt * 1e3 / (2 * ttt * Am), FY_316L_TUBE)
    # jackshaft: overhang from the front tower bearing carrying the near bush and the pivot tube plug
    Wtot = PROOF * (ms["moving"] + LOAD_KG) * G
    yb = -70.0
    y_near = sum(P["NEAR_HUB_Y"]) / 2
    y_far = sum(P["FAR_HUB_Y"]) / 2
    y_cg = sum(P["SPIDER_Y"]) / 2
    near = Wtot * (y_far - y_cg) / (y_far - y_near)
    far = Wtot - near
    y_plug = P["TUBE_A_Y"][0] + 35.0
    y_clamp = P["PIT_W"] + P["FAR_Y"]
    plug = far * (y_clamp - y_far) / (y_clamp - y_plug) + _masses()["tube_a"] * G * PROOF / 2
    Mj = (near * (y_near - yb) + plug * (y_plug - yb)) / 1000.0
    out["jackshaft"] = (32 * Mj * 1e3 / (math.pi * P["JACK_D"] ** 3), FY_316_BAR)
    # pivot tube A, simply supported between the plug and the far clamp, load at the far bush (W = 2.5 m pit, worst)
    y_clamp_w = 2500.0 + P["FAR_Y"]
    a_, b_ = y_far - y_plug, y_clamp_w - y_far
    MA = far * a_ * b_ / (a_ + b_) / 1000.0
    ZA, _ = tube_z(*P["TUBE_A"])
    out["pivot_tube"] = (MA * 1e3 / ZA, FY_304)
    # lift screw bracket: the screw force at 255 mm from the bolted member, SHS 50 x 50 x 3
    Zb = rect_z(50.0, 50.0, 3.0)
    out["bracket"] = (lift()["fmax"] * 0.255 * 1e3 / Zb, FY_304)
    res = {k: dict(stress=v[0], fy=v[1], sf=v[1] / v[0], ok=v[0] <= v[1] / ALLOW) for k, v in out.items()}
    res["_loads"] = dict(near=near, far=far, plug=plug, Mj=Mj, MA=MA)
    return res


def frame_support():
    """How the weight is shared between the two stands, and how far the centre of mass is inside the feet."""
    ms = mass_summary()
    rows = []
    for name, th in (("Lifted", P["THETA_LIFT"]), ("Deepest", P["THETA_DEEP"])):
        g = m.geometry(th)
        x_cg = g["axle_x"]
        rows.append(dict(name=name, x=x_cg, inside_near=min(x_cg - P["BASE_X"][0], P["BASE_X"][1] - x_cg),
                         inside_far=min(x_cg - P["FAR_X"][0], P["FAR_X"][1] - x_cg)))
    W = (ms["moving"] + LOAD_KG) * G
    y_cg = sum(P["SPIDER_Y"]) / 2
    rows_w = []
    for Wp in (1000.0, 1600.0, 2500.0):
        yf = Wp + P["FAR_Y"]
        yn = sum(P["BASE_Y"]) / 2
        far = W * (y_cg - yn) / (yf - yn)
        rows_w.append(dict(width=Wp, far=far, near=W - far))
    return dict(rows=rows, widths=rows_w)


def shield_check():
    """R9: every straight line from the reel's top half to the operator's eye passes through the splash shield."""
    worst = []
    sx0, sx1 = P["SHIELD_X"]
    sz0, sz1 = P["SHIELD_Z"]
    ys = P["SHIELD_Y"] + 25.0
    for th in (P["THETA_LIFT"], P["THETA_SHALLOW"], P["THETA"], P["THETA_DEEP"]):
        g = m.geometry(th)
        for a in range(0, 181, 15):
            px = g["axle_x"] + P["SPOKE_R"] * math.cos(math.radians(a))
            pz = g["axle_z"] + P["SPOKE_R"] * math.sin(math.radians(a))
            for py in (P["SPIDER_Y"][0], sum(P["SPIDER_Y"]) / 2, P["SPIDER_Y"][1]):
                t = (ys - py) / (EYE[1] - py)
                x = px + t * (EYE[0] - px)
                z = pz + t * (EYE[2] - pz)
                # below the rim the line runs into the near pit wall; otherwise it must meet the shield
                worst.append((z < 0.0 or (sx0 <= x <= sx1 and sz0 <= z <= sz1), x, z, th))
    ok = all(w[0] for w in worst)
    zmax = max(w[2] for w in worst)
    zmin = min(w[2] for w in worst if w[2] >= 0.0)
    xr = (min(w[1] for w in worst), max(w[1] for w in worst))
    return dict(ok=ok, zmax=zmax, zmin=zmin, xrange=xr, n=len(worst), misses=[w for w in worst if not w[0]])


def spans():
    W_min, W_max = 1000.0, 2500.0
    a0, a1 = P["TUBE_A_Y"]
    b_len = P["TUBE_B_Y"][1] - P["TUBE_B_Y"][0]
    far_hub_end = P["FAR_HUB_Y"][1] + 15.0
    min_w = far_hub_end + 50.0 - P["FAR_Y"] + 30.0      # far clamp (60 wide) clear of the outer collar
    reach_a = a1 - 30.0                                  # clamp centre at most 30 mm in from the tube end
    reach_b = a1 + b_len - 250.0 - 30.0                  # 250 mm of the extension left inside the pivot tube
    return dict(min_width=max(W_min, far_hub_end + 30.0 + 30.0 - P["FAR_Y"] + 50.0), a_only=(W_min, reach_a - P["FAR_Y"]),
                with_b=(reach_a - P["FAR_Y"], reach_b - P["FAR_Y"]), max_width=reach_b - P["FAR_Y"],
                pit_len=P["ARM_L"] + P["SPOKE_R"] - P["PIT_END"] + 50.0, drum=P["SPIDER_Y"][1] - P["SPIDER_Y"][0],
                far_arm_out=P["FAR_HUB_Y"][1] + 15.0)


def cost():
    rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
    total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
    target = 1500.0
    return dict(rows=rows, total=total, target=target, delta=total - target)


def setup_time():
    """R8: first setup over a pit, minutes, by step (estimates for two people who have done it once)."""
    steps = [("Check the rims and place the near stand base and pads", 3), ("Bolt the tower and braces to the base", 4),
             ("Bolt on the shield", 2), ("Place the far stand on the far rim", 1),
             ("Carry the pivot tube and arm frame across and slide it onto the jackshaft", 3),
             ("Push the extension tube out, pin it, clamp the far stand", 2), ("Fit the lift screw and bracket", 4),
             ("Raise the arms, carry the reel across on the assembly bar, drop it into the bearings", 3),
             ("Close the near cap and the keeper, fit chain 2 and its guard", 5), ("Lower to the working depth and check", 2)]
    return dict(steps=steps, total=sum(s[1] for s in steps))


def report():
    ms = mass_summary()
    print("VatReel sizing (VTR-CAL-001); all values are estimates for a paper design")
    print("\n1. Depth and positions (arm angle below horizontal; heights from the rim, + up)")
    for r in depth_table():
        print(f"  {r['name']}: arms {r['theta']:+.1f} deg; axle at x {r['axle_x']:.0f}, z {r['axle_z']:+.0f}; lowest bar {r['low']:+.0f}; "
              f"top bar {r['top']:+.0f}; reel from x {r['x0']:.0f} to {r['x1']:.0f}; screw {r['screw']:.0f}")
    sp = spans()
    print(f"\n2. Spans: pits {sp['a_only'][0]:.0f} to {sp['a_only'][1]:.0f} mm wide on the pivot tube alone; "
          f"{sp['with_b'][0]:.0f} to {sp['with_b'][1]:.0f} mm with the extension; pit length needed {sp['pit_len']:.0f} mm; "
          f"drum {sp['drum']:.0f} mm long; far arm and collar end {sp['far_arm_out']:.0f} mm in from the near edge")
    d = drive()
    print(f"\n3. Drive: load torque {d['t_load']:.1f} N m + friction {d['t_fric']:.1f} = {d['t_reel']:.1f} N m on the reel; "
          f"ratio {d['ratio']:.1f}; jackshaft {d['t_jack']:.1f} N m; crank {d['t_crank']:.1f} N m; "
          f"hand force {d['crank_force']:.0f} N at {P['CRANK_R']:.0f} mm")
    print(f"  chain 1 tension {d['tens1']:.0f} N (SF {d['sf1']:.0f} at proof); chain 2 tension {d['tens2']:.0f} N (SF {d['sf2']:.0f} at proof)")
    print(f"  at {CRANK_RPM:.0f} rpm on the crank: reel {d['reel_rpm']:.1f} rpm, carrier bars {d['bar_speed']:.2f} m/s, "
          f"{d['rev_s']:.0f} s per turn")
    b = brake()
    print(f"\n4. Ratchet (R5, 1.5 x, no efficiency credit): {b['t_hold']:.1f} N m on the crank shaft; tooth force {b['f_tooth']:.0f} N; "
          f"bearing {b['bearing']:.1f} MPa; pawl pin shear {b['pin_shear']:.1f} MPa; crank shaft {b['tau_crank']:.1f} MPa; "
          f"jackshaft {b['tau_jack']:.1f} MPa in shear")
    lf = lift()
    print(f"\n5. Lift screw Tr24 x 5: lead angle {lf['lam']:.2f} deg, friction angle {lf['rho']:.2f} deg, "
          f"{'self-locking' if lf['self_locking'] else 'NOT self-locking'}; stroke {lf['stroke']:.0f} mm = {lf['turns']:.0f} turns")
    for r in lf["rows"]:
        print(f"  {r['name']}: screw {r['length']:.0f} mm, lever arm {r['arm']:.0f} mm, moment {r['moment']:.0f} N m (1.5 x), "
              f"screw force {r['force']:.0f} N, torque {r['torque']:.1f} N m, handwheel rim force {r['wheel']:.0f} N")
    print(f"  buckling: Euler load {lf['p_cr'] / 1000:.1f} kN against {lf['fmax'] / 1000:.2f} kN (SF {lf['buckling_sf']:.1f}); "
          f"root stress {lf['sigma']:.1f} MPa")
    st = structure()
    print("\n6. Stresses at the proof load (1.5 x), against yield / 1.5")
    for k, v in st.items():
        if k.startswith("_"):
            continue
        print(f"  {k}: {v['stress']:.0f} MPa; yield {v['fy']:.0f}; factor on yield {v['sf']:.1f}; {'OK' if v['ok'] else 'TOO HIGH'}")
    ld = st["_loads"]
    print(f"  loads: near bush {ld['near']:.0f} N, far bush {ld['far']:.0f} N, plug {ld['plug']:.0f} N; jackshaft moment {ld['Mj']:.0f} N m; "
          f"pivot tube moment {ld['MA']:.0f} N m")
    fs = frame_support()
    print("\n7. Support")
    for r in fs["rows"]:
        print(f"  {r['name']}: reel centre at x {r['x']:.0f}; inside the near stand feet by {r['inside_near']:.0f} mm, "
              f"far stand by {r['inside_far']:.0f} mm")
    for r in fs["widths"]:
        print(f"  pit {r['width']:.0f} mm: near stand {r['near']:.0f} N, far stand {r['far']:.0f} N (reel loaded)")
    print("\n8. Masses (kg)")
    for k, v in ms["modules"].items():
        tag = " (two-person carry, %.1f each)" % (v / 2) if k in ms["two_person"] else ""
        print(f"  {k}: {v:.1f}{tag}")
    print(f"  total {ms['total']:.1f}; heaviest single carry {ms['heaviest']:.1f}; heaviest per person {ms['heaviest_person']:.1f}; "
          f"reel with bars {ms['reel']:.1f}; moving parts {ms['moving']:.1f}")
    su = setup_time()
    print(f"  setup time estimate: {su['total']} min")
    sh = shield_check()
    print(f"\n9. Shield (R9): {sh['n']} sight lines from the reel's top half to the eye; all through the shield: {sh['ok']}; "
          f"crossings from {sh['zmin']:.0f} to {sh['zmax']:.0f} mm above the rim (shield {P['SHIELD_Z'][0]:.0f} to {P['SHIELD_Z'][1]:.0f}); x from {sh['xrange'][0]:.0f} to {sh['xrange'][1]:.0f}")
    c = cost()
    print(f"\n10. Cost: USD {c['total']:.0f} against the USD {c['target']:.0f} value-engineering target "
          f"(USD {abs(c['delta']):.0f} {'over' if c['delta'] > 0 else 'under'})")


if __name__ == "__main__":
    report()
