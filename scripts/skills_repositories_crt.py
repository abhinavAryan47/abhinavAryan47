from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os

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

repos = [
    ("surge-suite", "PUBLIC", "AI workspace / agentic platform"),
    ("Agentic_ai", "PUBLIC", "Agentic AI experiments & MCP"),
    ("CSW2-Django-2026", "PUBLIC", "Django coursework"),
    ("csw_assignments", "PUBLIC", "Django / web assignments"),
    ("abhinavAryan47", "PUBLIC", "Profile / CRT interface"),
    ("Learning-Stuff", "PRIVATE", "Learning workspace"),
    ("Lessons-CSharp", "PRIVATE", "C# practice"),
    ("Java_Practice", "PRIVATE", "Java practice"),
    ("experimenting", "PRIVATE", "Experiments"),
    ("commclassprac", "PRIVATE", "Communication coursework"),
    ("valentine", "PRIVATE", "Creative project"),
    ("valentines", "PRIVATE", "Creative project"),
    ("valentines22", "PRIVATE", "Creative project"),
    ("one-year-anniv", "PRIVATE", "Creative project"),
]

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
    d.text((960,762), "14 REPOS", font=SMALL, fill=(153,160,151))
    for col in range(2):
        y = 808
        for name, vis, desc in repos[col*7:(col+1)*7]:
            badge = "PUB" if vis == "PUBLIC" else "PRV"
            d.text((100+col*500,y), f"[{badge}]", font=SMALL, fill=(218,222,214) if vis == "PUBLIC" else (112,118,110))
            d.text((148+col*500,y), name, font=HEAD, fill=(238,241,233))
            d.text((148+col*500,y+23), desc, font=SMALL, fill=(140,147,138))
            y += 51

    d.text((82,1210), "PUBLIC PROJECTS ARE ACCESSIBLE // PRIVATE REPOSITORIES SHOWN FOR INVENTORY ONLY", font=SMALL, fill=(119,126,117))
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
