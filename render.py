#!/usr/bin/env python3
"""Render the News 24 front page: THE WORLD IN ONE DAY - TUESDAY 24 NOVEMBER 2026.

Draws a 1024x1024 newspaper front page from the 34 verified 24-Nov-2026
stories in SOURCES.md v3. Standard library + Pillow only. Deterministic:
same input always produces byte-identical output.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (245, 238, 220)
INK = (26, 23, 18)
MUTED = (107, 93, 67)
RULE = (43, 33, 24)
CARD = (253, 249, 238)
CARDBORDER = (198, 180, 143)
LIGHT = (235, 228, 203)
REDBG = (243, 226, 220)
RED = (158, 43, 37)
GREEN = (46, 125, 50)
AMBER = (176, 120, 20)
BLUE = (29, 78, 158)
MAPLAND = (226, 212, 178)
MAPLINE = (138, 122, 82)
GRAT = (219, 209, 184)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FD, name), size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)           # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = fnt.size + 2
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- map data
# Simplified continent outlines (lon, lat). Rough but recognisable.
NORTH_AMERICA = [(-168, 66), (-156, 71), (-140, 70), (-128, 71), (-115, 69),
                 (-100, 69), (-90, 69), (-85, 66), (-80, 73), (-72, 62),
                 (-64, 60), (-60, 55), (-55, 47), (-60, 44), (-65, 44),
                 (-70, 42), (-75, 38), (-76, 35), (-80, 32), (-81, 26),
                 (-84, 30), (-89, 30), (-91, 19), (-96, 19), (-97, 16),
                 (-94, 16), (-91, 14), (-87, 13), (-83, 9), (-79, 9),
                 (-81, 13), (-86, 16), (-90, 14), (-92, 15), (-97, 16),
                 (-105, 20), (-110, 23), (-114, 28), (-120, 34),
                 (-124, 40), (-124, 48), (-130, 55), (-135, 58),
                 (-145, 60), (-155, 58), (-162, 55), (-168, 66)]
SOUTH_AMERICA = [(-79, 9), (-77, 7), (-72, 12), (-64, 10), (-59, 8),
                 (-52, 5), (-50, 0), (-44, -3), (-35, -8), (-37, -13),
                 (-39, -17), (-40, -22), (-48, -27), (-52, -32),
                 (-57, -35), (-62, -39), (-65, -41), (-68, -46),
                 (-69, -52), (-70, -55), (-73, -50), (-73, -44),
                 (-73, -37), (-71, -30), (-70, -20), (-75, -15),
                 (-77, -12), (-81, -6), (-81, -3), (-80, 1), (-79, 9)]
AFRICA = [(-17, 15), (-16, 20), (-13, 27), (-10, 30), (-6, 35), (-2, 35),
          (5, 37), (10, 37), (15, 32), (20, 32), (25, 32), (30, 31),
          (32, 31), (34, 28), (37, 22), (39, 18), (43, 12), (48, 11),
          (51, 11), (51, 6), (48, 0), (44, -5), (40, -10), (40, -16),
          (37, -20), (33, -26), (29, -30), (26, -34), (20, -35),
          (17, -32), (15, -27), (13, -22), (12, -18), (13, -12),
          (9, -1), (9, 4), (4, 6), (-3, 5), (-8, 5), (-13, 8), (-17, 15)]
EURASIA = [(-10, 36), (-9, 38), (-9, 43), (-4, 48), (-2, 49), (-1, 51),
           (2, 51), (4, 53), (7, 54), (8, 57), (10, 59), (12, 56),
           (18, 56), (21, 55), (24, 58), (26, 59), (28, 60), (30, 62),
           (30, 66), (32, 70), (36, 68), (44, 68), (50, 69), (55, 68),
           (60, 69), (66, 69), (68, 73), (75, 73), (80, 73), (90, 75),
           (100, 76), (110, 74), (120, 73), (130, 72), (140, 72),
           (150, 70), (160, 70), (170, 67), (178, 66), (178, 64),
           (170, 60), (162, 56), (158, 52), (156, 51), (150, 59),
           (142, 55), (142, 50), (140, 44), (138, 38), (135, 34),
           (132, 33), (130, 31), (127, 34), (124, 39), (122, 37),
           (120, 32), (122, 28), (120, 22), (115, 22), (110, 20),
           (109, 18), (108, 12), (106, 10), (104, 9), (101, 7),
           (100, 8), (98, 10), (97, 15), (94, 17), (92, 21), (89, 22),
           (88, 22), (86, 20), (83, 18), (80, 15), (80, 13), (77, 8),
           (76, 10), (73, 16), (72, 20), (70, 21), (67, 25), (64, 25),
           (61, 25), (58, 26), (56, 26), (54, 27), (52, 27), (51, 28),
           (50, 29), (48, 30), (47, 30), (44, 29), (42, 29), (40, 31),
           (39, 31), (36, 36), (35, 36), (33, 36), (30, 36), (27, 37),
           (26, 38), (23, 36), (22, 37), (20, 39), (19, 42), (16, 44),
           (14, 45), (12, 44), (10, 44), (8, 44), (6, 43), (3, 43),
           (1, 40), (0, 39), (-2, 37), (-5, 36), (-6, 36), (-9, 37),
           (-10, 36)]
UK = [(-5, 50), (-4, 53), (-5, 56), (-4, 58), (-2, 57), (-1, 57),
      (0, 53), (1, 51), (0, 51), (-2, 51), (-4, 50), (-5, 50)]
JAPAN = [(130, 31), (131, 33), (133, 34), (135, 34), (136, 35),
         (138, 35), (139, 37), (140, 38), (141, 40), (141, 42),
         (143, 42), (145, 44), (143, 45), (142, 44), (141, 42),
         (140, 40), (139, 38), (138, 36), (136, 35), (134, 34),
         (132, 33), (130, 31)]
INDONESIA = [(95, 5), (98, 4), (100, 0), (102, -2), (105, -5), (108, -7),
             (111, -7), (114, -8), (117, -9), (120, -10), (123, -10),
             (126, -9), (128, -7), (130, -4), (132, -2), (135, -3),
             (138, -4), (141, -6), (141, -8), (138, -8), (135, -6),
             (132, -2), (130, -1), (128, 1), (126, 1), (124, 0),
             (121, 0), (119, 1), (117, 3), (115, 4), (112, 2),
             (110, 0), (108, 1), (105, 1), (103, 1), (100, 2), (98, 4),
             (95, 5)]
NEW_GUINEA = [(131, -1), (134, -2), (137, -2), (141, -3), (144, -4),
              (147, -6), (150, -9), (147, -9), (144, -8), (141, -8),
              (138, -8), (135, -7), (133, -4), (131, -1)]
AUSTRALIA = [(113, -22), (114, -28), (115, -32), (116, -35), (120, -34),
             (124, -33), (129, -32), (132, -32), (134, -33), (136, -35),
             (138, -35), (140, -38), (143, -39), (146, -39), (150, -37),
             (152, -35), (153, -32), (153, -28), (151, -24), (149, -20),
             (146, -19), (144, -15), (142, -11), (141, -13), (139, -17),
             (136, -12), (135, -12), (132, -12), (130, -13), (127, -14),
             (124, -15), (122, -17), (120, -20), (117, -21), (114, -22),
             (113, -22)]
NZ = [(167, -45), (169, -43), (171, -42), (173, -41), (175, -40),
      (177, -38), (178, -38), (176, -37), (174, -37), (173, -39),
      (172, -41), (170, -43), (168, -45), (167, -45)]
MADAGASCAR = [(44, -16), (46, -15), (49, -15), (50, -16), (50, -19),
              (48, -22), (47, -25), (45, -25), (44, -22), (43, -20),
              (44, -16)]
ICELAND = [(-22, 64), (-20, 63), (-17, 63), (-14, 64), (-15, 66),
           (-18, 66), (-21, 66), (-22, 64)]

CONTINENTS = [NORTH_AMERICA, SOUTH_AMERICA, AFRICA, EURASIA, UK, JAPAN,
              INDONESIA, NEW_GUINEA, AUSTRALIA, NZ, MADAGASCAR, ICELAND]

# Map frame
MX0, MX1, MY0, MY1 = 12, 1012, 172, 332


def proj(lon, lat):
    x = MX0 + (lon + 180.0) / 360.0 * (MX1 - MX0)
    y = MY0 + (78.0 - lat) / 136.0 * (MY1 - MY0)
    return x, y


# ---------------------------------------------------------------- stories
# pin: (lon, lat, dx, dy) pixel nudge; flag: (fdx, fdy) relative to pin centre
# pill: REPORTED (green) / CLAIMED (amber) / TONIGHT (blue)
STORIES = [
    # n, region, headline, fact, source, pill, pin lon/lat, nudge, flag nudge
    (2, "ECONOMY", "Brent slips to fresh 3-month low",
     "Near $89 as glut fears outweigh Hormuz risk", "Reuters", "REPORTED",
     (57.0, 2.0), (16, -10), (-26, -4)),
    (3, "ECONOMY", "US confidence jumps to 103.3",
     "Highest since January 2025, post-midterms optimism", "Conf. Board", "REPORTED",
     (38.9, -77.0), (0, 0), (10, -4)),
    (4, "ECONOMY", "Mexico inflation hits 3.96%",
     "Six-month high; core eases to 3.68%", "Reuters", "REPORTED",
     (19.4, -99.1), (0, 0), (10, -4)),
    (5, "ECONOMY", "Brazil confidence falls to 83.5",
     "Lowest since August 2022 as budgets tighten", "Rio Times", "REPORTED",
     (-15.8, -47.9), (0, 0), (10, -4)),
    (17, "POLITICS", "Hasina plans return on 16 Dec",
     "Dhaka minister: she will be 'brought back in handcuffs'", "Reuters", "REPORTED",
     (23.8, 90.4), (0, 0), (10, -4)),
    (18, "POLITICS", "Japan pays full 2027 ICC bill early",
     "PM Takaichi acts before US sanctions bite", "Reuters", "REPORTED",
     (35.7, 139.7), (0, 0), (10, -4)),
    (19, "POLITICS", "Sweden votes 30 Nov on PM",
     "Parliament to settle gridlock since Sept election", "Reuters", "REPORTED",
     (59.3, 18.1), (-8, -6), (10, -4)),
    (20, "POLITICS", "Latvia: war may tip to Russia's defeat",
     "President Rinkevics sees a tipping point next year", "Reuters", "REPORTED",
     (56.9, 24.1), (8, 6), (0, -14)),
    (21, "POLITICS", "Australia: tech giants face 5% fines",
     "Digital duty of care; users gain right to sue", "AP", "REPORTED",
     (-35.3, 149.1), (0, 0), (10, -4)),
    (22, "POLITICS", "Australia-Singapore CO2 treaty signed",
     "First transboundary carbon-capture deal, in Canberra", "Straits Times", "REPORTED",
     (1.35, 103.8), (0, 0), (10, -4)),
    (23, "TECH", "Microsoft declares 'Code Red'",
     "After its historic 12-13 Nov outage, overhaul ordered", "Reuters", "REPORTED",
     (47.6, -122.3), (6, -6), (10, -4)),
    (24, "TECH", "S. Korea: $375,000 to catch AI cheats",
     "Rewards offered over exam cheating in CSAT", "WSJ", "REPORTED",
     (36.0, 127.5), (-4, 16), (-14, 10)),
    (25, "TECH", "Chinese AI push 'to sway Taiwan vote'",
     "Coordinated social-media campaign, US report finds", "NYT", "REPORTED",
     (25.0, 121.6), (-12, 0), (-26, -4)),
    (26, "DISASTERS", "~175 migrants unaccounted off Senegal",
     "Contact lost with Europe-bound boat from Dakar", "Reuters", "REPORTED",
     (14.7, -17.4), (0, 0), (10, -4)),
    (27, "DISASTERS", "Iowa lead-azide: evacuation ordered",
     "Blast set for Wed 25 Nov ~09:00 CST; zone cleared", "USA Today", "REPORTED",
     (41.5, -91.5), (0, 0), (10, -4)),
    (28, "SPORT", "Champions League: Madrid hit five",
     "FT: Bod\u00f8/Glimt 1-0 LASK \u00b7 Gala 1-0 Villa \u00b7 Arsenal 1-1 Dortmund \u00b7 Man City 2-2 Napoli \u00b7 Real 5-1 PSV", "UEFA", "TONIGHT",
     (51.5, -0.1), (0, 0), (10, -4)),
    (29, "SPORT", "Davis Cup: Czechia beats Canada",
     "Machac beats Draxl 6-2 3-6 6-2 in quarter-final", "Reuters", "REPORTED",
     (50.1, 14.4), (-20, 16), (-26, 10)),
    (30, "SPORT", "England beat Australia by 8 wickets",
     "Donald 85 off 32, Salt 58; T20 series level 1-1", "Reuters", "REPORTED",
     (-28.0, 153.4), (0, -12), (10, -4)),
    (31, "CULTURE", "Shenzhou-24 crew named",
     "Pakistan's first astronaut aboard; launches tomorrow", "Xinhua", "REPORTED",
     (39.9, 116.4), (0, 0), (10, -4)),
    (32, "CULTURE", "Guru Nanak Jayanti",
     "Banks closed in many Indian states for the festival", "India", "REPORTED",
     (31.6, 74.9), (0, 0), (10, -4)),
    (33, "CULTURE", "Japan holds first Ebola drill",
     "Response exercise amid the DRC outbreak", "Japan Times", "REPORTED",
     (35.0, 140.5), (12, 12), (12, 10)),
    (34, "CULTURE", "SpaceX Falcon 9 launches USSF-266",
     "Classified launch 16:08 UTC; booster lands (29th flight)", "vcstar", "REPORTED",
     (34.7, -120.6), (-10, 8), (10, -4)),
]

CONFLICT = [
    (6, "Zaporizhzhia hit overnight", "2 killed, 40 wounded, incl. 4 children", "Reuters", "REPORTED", (47.8, 35.2), (0, 0), (10, -4)),
    (7, "Germany first into Ukraine's Delta", "Letter of intent signed in Berlin", "Kyiv Independent", "REPORTED", (52.5, 13.4), (0, 10), (14, 0)),
    (8, "Russian jets enter S. Korea ADIZ", "Seoul scrambles jets, summons attach\u00e9", "AP / WSJ", "REPORTED", (38.0, 129.0), (14, -10), (10, -14)),
    (9, "Iran: Hormuz shut 'day by day'", "2 more tankers hit mines; Qatar presses talks", "Interfax / IRNA", "REPORTED", (35.7, 51.4), (0, 0), (10, -4)),
    (10, "Iraq PM orders ministry to run Kurdish fields", "Deepens Baghdad-Kurdistan tensions", "Reuters", "REPORTED", (33.3, 44.4), (-6, -8), (10, -4)),
    (11, "UN urges probe into Benghazi attacks", "Port and offshore strikes on Sunday", "UN News", "REPORTED", (32.1, 20.1), (0, 0), (10, -4)),
    (12, "Villavicencio car bomb: 23 hurt", "Blast 02:30 UTC outside governor's office", "AP / UPI", "REPORTED", (4.1, -73.6), (0, 0), (10, -4)),
    (13, "Amnesty: Tigray strikes 'war crimes'", "Artillery on urban areas must be probed", "Reuters", "REPORTED", (13.5, 39.5), (0, 0), (10, -4)),
    (14, "Somali Speaker accuses Kenya, Ethiopia, Uganda", "Claims they side with Al-Shabaab", "Somali Guardian", "CLAIMED", (2.0, 45.3), (0, 0), (10, -4)),
    (15, "MSF halts Yei River work", "Suspended 3+ months after an abduction", "PANA", "REPORTED", (4.1, 30.7), (0, 0), (10, -4)),
    (16, "Houthi projectile hits Riyadh PIF Tower", "11 injured; 2nd strike in under a week", "Reuters", "REPORTED", (24.7, 46.7), (12, 10), (10, -4)),
]

# Lead pin + flag (Seoul)
LEAD_PIN = (37.5, 127.0, 0, 0, 14, 10)

FLAGS = {1: "KR", 2: "GB", 3: "US", 4: "MX", 5: "BR", 6: "UA", 7: "DE",
         8: "KR", 9: "IR", 10: "IQ", 11: "LY", 12: "CO", 13: "ET",
         14: "SO", 15: "SS", 16: "SA", 17: "BD", 18: "JP", 19: "SE",
         20: "LV", 21: "AU", 22: "SG", 23: "US", 24: "KR", 25: "TW",
         26: "SN", 27: "US", 28: "GB", 29: "CZ", 30: "AU", 31: "CN",
         32: "IN", 33: "JP", 34: "US"}

UTC_STRIP = ("01:30 Asia rally \u00b7 01:47 Brent low \u00b7 02:30 Villavicencio blast \u00b7 "
             "07:05 MSF halts Yei work \u00b7 09:09 Hormuz order \u00b7 11:36 Digital duty deal \u00b7 "
             "12:09 Ebola drill \u00b7 13:08 Mexico CPI \u00b7 15:00 US confidence \u00b7 "
             "16:08 Falcon 9 launch \u00b7 17:01 Riyadh strike \u00b7 20:00 UCL kick-off \u00b7 "
             "22:00 UCL finals")

PILL_COLORS = {"REPORTED": GREEN, "CLAIMED": AMBER, "TONIGHT": BLUE}


def pill(draw, x, y, text):
    fnt = SANS_B(7)
    w = int(draw.textlength(text, font=fnt)) + 10
    h = 11
    draw.rounded_rectangle([x, y, x + w, y + h], radius=5,
                           fill=PILL_COLORS[text])
    draw.text((x + 5, y + 1.5), text, font=fnt, fill=(255, 255, 255))
    return w


def pin(draw, x, y, n, flag, fdx, fdy):
    r = 8
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255),
                 outline=INK, width=2)
    fnt = SANS_B(9)
    tw = draw.textlength(str(n), font=fnt)
    draw.text((x - tw / 2, y - 6.5), str(n), font=fnt, fill=INK)
    fx, fy = x + fdx, y + fdy
    draw.rectangle([fx - 6, fy - 4, fx + 6, fy + 4], fill=(255, 255, 255),
                   outline=INK, width=1)
    ff = SANS_B(6)
    tw = draw.textlength(flag, font=ff)
    draw.text((fx - tw / 2, fy - 3.5), flag, font=ff, fill=INK)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 4], fill=INK)
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(44)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 10), title, font=tf, fill=INK)
    date = "TUESDAY 24 NOVEMBER 2026"
    df = SANS_B(19)
    tw = d.textlength(date, font=df)
    d.text(((W - tw) / 2, 58), date, font=df, fill=INK)
    sub = "34 stories, 7 regions, one day \u2014 every story first reported 24 November 2026 (UTC)."
    sf = SANS(13)
    tw = d.textlength(sub, font=sf)
    d.text(((W - tw) / 2, 82), sub, font=sf, fill=MUTED)
    d.line([12, 100, 1012, 100], fill=RULE, width=2)

    # ---- lead hero (#1) ----
    d.rounded_rectangle([12, 106, 1012, 166], radius=6, fill=CARD,
                        outline=CARDBORDER, width=1)
    d.text((24, 112), "1", font=SANS_B(30), fill=RED)
    d.text((52, 114), "ASIA'S MARKETS ROAR BACK", font=SANS_B(21), fill=INK)
    d.text((52, 140), "Seoul's surge triggers a buy-side sidecar; chip stocks lead the AI rebound.",
           font=SANS(11), fill=MUTED)
    d.text((52, 153), "Nvidia's +31.5% jump was Mon 23 Nov \u2014 not today's news.",
           font=SANS(10), fill=MUTED)
    stats = [("KOSPI", "+6.3%", "5,006"), ("NIKKEI", "+3.9%", "58,645"),
             ("TAIEX", "+9.0%", "40,122")]
    sx = 620
    for name, val, lvl in stats:
        d.text((sx, 112), name, font=SANS_B(9), fill=MUTED)
        d.text((sx, 122), val, font=SANS_B(24), fill=GREEN)
        d.text((sx, 148), lvl, font=SANS_B(10), fill=INK)
        sx += 105
    pill(d, 940, 112, "REPORTED")
    d.text((940, 130), "Reuters", font=SANS(9), fill=MUTED)

    # ---- world map ----
    d.rectangle([MX0, MY0, MX1, MY1], outline=RULE, width=1)
    for lon in range(-150, 181, 30):
        x, _ = proj(lon, 0)
        d.line([x, MY0, x, MY1], fill=GRAT, width=1)
    for lat in range(-60, 79, 30):
        _, y = proj(0, lat)
        d.line([MX0, y, MX1, y], fill=GRAT, width=1)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=MAPLAND, outline=MAPLINE)
    # Map label: drawn AFTER the continents on a solid paper backing strip,
    # so no coastline or land fill can strike through the text. The strip
    # matches the map's paper background; text keeps its original position.
    # Measured text width is ~250px at SANS_B(10); the strip gives >=5px
    # clearance on every side (glyphs occupy roughly y 179-187, x 18-268).
    d.rectangle([MX0 + 1, MY0 + 2, MX0 + 6 + 250 + 8, MY0 + 4 + 11 + 8],
                fill=PAPER)
    d.text((MX0 + 6, MY0 + 4), "THE WORLD \u2014 34 STORIES, NUMBERED 1\u201334",
           font=SANS_B(10), fill=MUTED)
    # pins: lead first, then conflict, then the rest
    # (stored tuples are (lat, lon); proj takes (lon, lat))
    plat, plon, dx, dy, fdx, fdy = LEAD_PIN
    x, y = proj(plon, plat)
    pin(d, x + dx, y + dy, 1, FLAGS[1], fdx, fdy)
    for s in CONFLICT:
        n, _, _, _, _, (clat, clon), (cdx, cdy), (cfdx, cfdy) = s
        x, y = proj(clon, clat)
        pin(d, x + cdx, y + cdy, n, FLAGS[n], cfdx, cfdy)
    for s in STORIES:
        n, _, _, _, _, _, (slat, slon), (sdx, sdy), (sfdx, sfdy) = s
        x, y = proj(slon, slat)
        pin(d, x + sdx, y + sdy, n, FLAGS[n], sfdx, sfdy)

    # ---- THE DAY IN UTC strip ----
    d.text((12, 340), "THE DAY IN UTC", font=SANS_B(11), fill=INK)
    lines = wrap(d, UTC_STRIP, SANS(10), 860)
    y = 340
    # first line sits right of the label
    first = lines[0] if lines else ""
    d.text((140, 340), first, font=SANS(10), fill=INK)
    y = 354
    for ln in lines[1:]:
        d.text((12, y), ln, font=SANS(10), fill=INK)
        y += 12
    d.text((12, y + 2), "All other stories first reported 24 NOV (UTC) \u2014 times confirmed from source reports.",
           font=SANS(9), fill=MUTED)
    d.line([12, 388, 1012, 388], fill=RULE, width=1)

    # ---- CONFLICT WATCH panel (#6-16) ----
    py = 394
    d.rounded_rectangle([12, py, 1012, 562], radius=6, fill=REDBG,
                        outline=RED, width=1)
    d.text((24, py + 6), "CONFLICT WATCH", font=SANS_B(13), fill=RED)
    d.text((170, py + 8), "11 stories \u2014 one muted red panel; the rest of the day keeps normal colours",
           font=SANS(10), fill=MUTED)
    d.line([24, py + 26, 1000, py + 26], fill=RED, width=1)
    col_w = (1000 - 24 - 8) // 2
    for i, s in enumerate(CONFLICT):
        n, head, fact, src, pl, _, _, _ = s
        col = i % 2
        row = i // 2
        cx = 24 + col * (col_w + 8)
        cy = py + 30 + row * 23
        d.text((cx, cy), str(n), font=SANS_B(11), fill=RED)
        d.text((cx + 20, cy), head, font=SANS_B(10), fill=INK)
        pw = pill(d, cx + col_w - 52, cy, pl)
        d.text((cx + 20, cy + 12), fact + "  \u00b7  " + src,
               font=SANS(9), fill=MUTED)

    # ---- region grid: the other 22 stories ----
    cols = [STORIES[0:8], STORIES[8:16], STORIES[16:22]]
    gy = 568
    card_h, gap = 42, 4
    col_w = (1000 - 16) // 3
    for ci, col in enumerate(cols):
        cx = 12 + ci * (col_w + 8)
        for ri, s in enumerate(col):
            n, region, head, fact, src, pl, _, _, _ = s
            cy = gy + ri * (card_h + gap)
            bg = LIGHT if n in (28, 29, 30, 31, 32, 33, 34) else CARD
            d.rounded_rectangle([cx, cy, cx + col_w, cy + card_h], radius=4,
                                fill=bg, outline=CARDBORDER, width=1)
            d.text((cx + 6, cy + 3), str(n), font=SANS_B(12), fill=INK)
            hw = col_w - 30 - 58
            hl = wrap(d, head, SANS_B(10), hw)
            draw_wrapped(d, cx + 28, cy + 3, hl[:2], SANS_B(10), INK, 11)
            pill(d, cx + col_w - 56, cy + 3, pl)
            fy2 = cy + 3 + len(hl[:2]) * 11 + 1
            fl = wrap(d, fact, SANS(9), col_w - 12)
            nfl = min(len(fl), 2 if len(hl[:2]) == 1 else 1)
            for k in range(nfl):
                d.text((cx + 6, fy2 + k * 10), fl[k], font=SANS(9),
                       fill=MUTED)
            d.text((cx + col_w - 60, fy2 + (nfl - 1) * 10), src,
                   font=SANS(8), fill=MUTED)

    # ---- footer: DATE CHECK ----
    fy = 938
    d.line([12, fy, 1012, fy], fill=RULE, width=2)
    d.text((12, fy + 8), "DATE CHECK", font=SANS_B(11), fill=INK)
    dc = ("Every story above was first reported 24 Nov 2026 (UTC). Left out on purpose: "
          "Puigdemont amnesty (23 Nov), Peru quake (20 Nov), CrowdStrike\u2013Zscaler deal "
          "(23 Nov). No Israel / Gaza stories, by standing rule.")
    lines = wrap(d, dc, SANS(10), 1000)
    y = fy + 24
    for ln in lines:
        d.text((12, y), ln, font=SANS(10), fill=INK)
        y += 13
    d.text((12, y + 4), "Sources on every card \u00b7 Drawn from 34 verified first reports \u00b7 News 24 \u00b7 make.fun",
           font=SANS(9), fill=MUTED)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "./output")
    os.makedirs(out_dir, exist_ok=True)
    img = render()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", compress_level=6)
    return path


if __name__ == "__main__":
    print(main())
