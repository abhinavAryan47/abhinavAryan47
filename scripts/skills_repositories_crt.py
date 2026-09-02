from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os, json, urllib.request

W, H = 1200, 1280
OUT = os.environ.get("OUT_DIR", "dist")
os.makedirs(OUT, exist_ok=True)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def f(path, size):
    return ImageFont.truetype(path if os.path.exists(path) else FONT, size)

BIG = f(BOLD, 48)
TITLE = f(BOLD, 24)
HEAD = f(BOLD, 17)
BODY = f(FONT, 15)
SMALL = f(FONT, 13)

# Keep this mapping human-curated: repository discovery is automatic, but
# claiming a skill from code heuristics can easily overstate someone's stack.
skills = [
    ("AI / AGENTIC", "AI AGENTS  ·  MULTI-AGENT SYSTEMS  ·  MCP"),
    ("WORKFLOWS", "AUTOMATION  ·  TASK EXECUTION  ·  HUMAN-IN-THE-LOOP"),
    ("RAG / KNOWLEDGE", "RAG  ·  VECTOR DATABASES  ·  DOCUMENT PIPELINES"),
    ("COMPUTER VISION", "FACE DETECTION  ·  FACE EMBEDDINGS  ·  AUTHENTICATION"),
    ("BACKEND", "PYTHON  ·  DJANGO  ·  FASTAPI  ·  REST APIs"),
    ("FRONTEND", "REACT  ·  WORKSPACE UI  ·  INTERACTIVE SYSTEMS"),
    ("DATA / INFRA", "MONGODB  ·  SQLITE  ·  DOCKER  ·  GIT / GITHUB"),
    ("LLM TOOLING", "LLM / SLM RESEARCH  ·  MODEL TUNING  ·  UNSLOTH"),
]

OWNER = "abhinavAryan47"
API = "https://api.github.com"


def github_get(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "abhinavAryan47-profile-generator",
    })
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def get_public_repos():
    """Fetch every public repository owned by the profile, newest first."""
    repos = []
    page = 1
    while True:
        url = f"{API}/users/{OWNER}/repos?type=public&sort=updated&direction=desc&per_page=100&page={page}"
        batch = github_get(url)
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    # Keep the generator resilient if GitHub briefly fails or returns odd data.
    clean = []
    for repo in repos:
        name = repo.get("name")
        if not name:
            continue
        description = (repo.get("description") or "").replace("\n", " ").strip()
        clean.append((name, "PUBLIC", description or "Public repository"))
    return clean


try:
    repos = get_public_repos()
except Exception as exc:
    print(f"GitHub API lookup failed: {exc}")
    # Never fail the whole profile workflow just because the public API is
    # temporarily unavailable. The image will still render with this marker.
    repos = [("API_UNAVAILABLE", "PUBLIC", "GitHub repository list unavailable")]


def base():
    im = Image.new("RGB", (W, H), (4, 6, 5))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20,20,W-20,H-20), 36, fill=(7,10,8), outline=(120,126,117), width=3)
    d.rounded_rectangle((48,48,W-48,H-48), 24, fill=(2,4,3), outline=(46,51,46), width=2)

    d.text((80,78), "SKILLS // REPOSITORIES", font=BIG, fill=(238,241,233))
    d.text((83,140), "ABHINAV ARYAN  ::  SYSTEM INVENTORY", font=SMALL, fill=(153,160,151))
    d.line((80,170,W-80,170), fill=(100,106,98), width=2)

    d.rounded_rectangle((76,202,1124,700), 14, outline=(72,79,72), width=2)
    d.text((98,222), "01 // SKILL MATRIX", font=TITLE, fill=(225,229,221))
    y = 274
    for name, desc in skills:
        d.text((102,y), f"[ {name:<16} ]", font=HEAD, fill=(238,241,233))
        d.text((345,y+2), desc, font=BODY, fill=(166,173,164))
        d.line((98,y+31,1102,y+31), fill=(25,29,25), width=1)
        y += 52

    d.rounded_rectangle((76,735,1124,1178), 14, outline=(72,79,72), width=2)
    d.text((98,756), "02 // REPOSITORY INDEX", font=TITLE, fill=(225,229,221))
    d.text((970,762), f"{len(repos)} REPOS", font=SMALL, fill=(153,160,151))

    # The panel has room for 14 rows. If more public repos exist, show the
    # most recently updated 14 so the graphic stays clean and uncluttered.
    shown = repos[:14]
    columns = [shown[:7], shown[7:14]]
    for col, items in enumerate(columns):
        y = 808
        for name, vis, desc in items:
            badge = "PUB"
            x = 100 + col * 500
            d.text((x,y), f"[{badge}]", font=SMALL, fill=(218,222,214))
            d.text((x+48,y), name[:32], font=HEAD, fill=(238,241,233))
            d.text((x+48,y+23), desc[:46], font=SMALL, fill=(140,147,138))
            y += 51

    if len(repos) > 14:
        d.text((82,1210), f"SHOWING 14 MOST RECENT PUBLIC REPOS // {len(repos)} TOTAL", font=SMALL, fill=(119,126,117))
    else:
        d.text((82,1210), "PUBLIC REPOSITORIES // AUTO-DISCOVERED FROM GITHUB", font=SMALL, fill=(119,126,117))
    d.text((1020,1210), "CRT // 02", font=SMALL, fill=(165,171,162))
    return im


def crt(im, phase):
    glow = im.filter(ImageFilter.GaussianBlur(6))
    glow = ImageEnhance.Brightness(glow).enhance(0.12)
    out = Image.blend(im, glow, 0.18)
    r,g,b = out.split()
    shift = 1 + (phase % 2)
    r = r.transform((W,H), Image.AFFINE, (1,0,shift,0,1,0))
    b = b.transform((W,H), Image.AFFINE, (1,0,-shift,0,1,0))
    out = Image.merge("RGB", (r,g,b))
    d = ImageDraw.Draw(out, "RGBA")
    for yy in range(50,H-50,4):
        d.line((48,yy,W-48,yy), fill=(0,0,0,48), width=1)
    beam = 80 + ((phase * 190) % (H-160))
    d.rectangle((52,beam-6,W-52,beam+6), fill=(220,230,215,8))
    out = ImageEnhance.Brightness(out).enhance(0.985 + 0.012*math.sin(phase*1.7))
    return out

base_im = base()
frames = [crt(base_im.copy(), i) for i in range(6)]
path = os.path.join(OUT, "skills-repositories-crt.gif")
frames[0].save(path, save_all=True, append_images=frames[1:], duration=140, loop=0, optimize=True, disposal=2)
print(path)
