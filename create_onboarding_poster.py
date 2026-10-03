from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(r"C:\Users\pardh\OneDrive\Desktop\Qure")
OUT = ROOT / "outputs" / "qure-crm-onboarding-poster"
ASSETS = ROOT / "outputs" / "qure-life-sciences-crm-qure-styled"
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / "qure_crm_first_timer_onboarding_poster.pdf"

W, H = landscape(A4)
BG = "#0B1926"; PANEL = "#0D1E2D"; PANEL2 = "#11283A"; WHITE = "#F8FAFC"; MUTED = "#94A3B8"; LINE = "#24445A"; CORAL = "#FF6B6B"; TEAL = "#14B8A6"; TEAL_DARK = "#0F766E"

def rgb(hexv):
    h = hexv.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def fill(c, color): c.setFillColorRGB(*rgb(color))
def stroke(c, color): c.setStrokeColorRGB(*rgb(color))
def text(c, x, y, value, size=9, color=WHITE, font="Helvetica"):
    fill(c,color); c.setFont(font,size); c.drawString(x,y,value)
def fit_text(c, x, y, value, max_width, size=9, color=WHITE, font="Helvetica"):
    words=value.split(); line=""; offset=0
    for word in words:
        trial=(line+" "+word).strip()
        if stringWidth(trial,font,size)<=max_width: line=trial
        else:
            text(c,x,y-offset,line,size,color,font); offset += size+3; line=word
    if line: text(c,x,y-offset,line,size,color,font)
    return offset+size
def card(c,x,y,w,h,label,body,accent=TEAL):
    fill(c,PANEL2); c.roundRect(x,y,w,h,7,stroke=0,fill=1)
    stroke(c,accent); c.setLineWidth(1.8); c.line(x+14,y+h-14,x+42,y+h-14)
    text(c,x+14,y+h-32,label.upper(),7.5,MUTED,"Helvetica-Bold")
    fit_text(c,x+14,y+h-50,body,w-28,9,WHITE,"Helvetica")
def pill(c,x,y,label,fill_color,text_color=BG):
    width=stringWidth(label,"Helvetica-Bold",7.5)+18
    fill(c,fill_color);c.roundRect(x,y,width,17,8,stroke=0,fill=1)
    text(c,x+9,y+5,label,7.5,text_color,"Helvetica-Bold")
    return width
def screenshot(c,path,x,y,w,h):
    fill(c,WHITE);c.roundRect(x,y,w,h,5,stroke=0,fill=1)
    c.drawImage(ImageReader(str(path)),x+3,y+3,w-6,h-6,preserveAspectRatio=True,anchor='c',mask='auto')
    stroke(c,LINE);c.setLineWidth(.7);c.roundRect(x,y,w,h,5,stroke=1,fill=0)

c=canvas.Canvas(str(PDF),pagesize=landscape(A4))
fill(c,BG);c.rect(0,0,W,H,stroke=0,fill=1)

# Header
text(c,38,H-42,"Qure.ai CRM / FIRST-TIMER GUIDE",10,CORAL,"Helvetica-Bold")
text(c,38,H-70,"Turn India Life Sciences research into clear, compliant next steps.",21,WHITE,"Helvetica-Bold")
text(c,38,H-88,"Read the signals, pick one action, and keep the evidence trail current.",10,MUTED)
pill(c,38,H-116,"1. UNDERSTAND",TEAL); pill(c,154,H-116,"2. DECIDE",CORAL); pill(c,245,H-116,"3. ACT",WHITE,BG)
stroke(c,CORAL);c.setLineWidth(1);c.line(38,H-128,W-38,H-128)

# Dashboard map
text(c,38,H-151,"1  Start on the Dashboard",13,WHITE,"Helvetica-Bold")
text(c,38,H-166,"Scan the KPI stack first, then use the breakdowns to find concentration, gaps, and urgent follow-up.",8.5,MUTED)
screenshot(c,ASSETS / "Dashboard.png",38,H-338,470,155)
text(c,48,H-330,"Dashboard screenshot: KPI stack = current workload; tables/charts = where to focus.",7.5,MUTED)

# Insight cards
card(c,527,H-205,132,65,"Coverage","15 Tier 1 accounts, but only 12 currently have contact coverage. Close the coverage gap before expanding the long tail.",CORAL)
card(c,671,H-205,132,65,"Evidence","82 contacts are verified on official sources. Treat the remaining unverified roles as a research task, not an outreach list.",TEAL)
card(c,527,H-282,132,65,"Focus","88 contacts are in pharma and 12 in biotech. If imaging/diagnostics is strategic, deliberately build that missing segment.",CORAL)
card(c,671,H-282,132,65,"Priority","Route lead scores of 4.5+ to a tailored message with one relevant Qure.ai use case and a single next action.",TEAL)

# Lower process
text(c,38,H-365,"2  Use this 5-minute operating loop",13,WHITE,"Helvetica-Bold")
steps=[("01","FILTER","Tier 1 + high lead score"),("02","VERIFY","Title, source, and last verified date"),("03","QUALIFY","Use case + buying influence"),("04","ACT","Log one next action and deadline")]
x=38
for n,label,detail in steps:
    fill(c,CORAL if n in ("01","04") else TEAL_DARK);c.circle(x+13,H-397,13,stroke=0,fill=1)
    text(c,x+6,H-400,n,7,WHITE,"Helvetica-Bold")
    text(c,x+32,H-390,label,8,WHITE,"Helvetica-Bold")
    fit_text(c,x+32,H-404,detail,128,7.5,MUTED)
    if n!="04": stroke(c,LINE);c.setLineWidth(1);c.line(x+145,H-397,x+164,H-397)
    x += 188

# Contacts screenshot + legend / example
text(c,38,H-453,"3  Read the Contacts sheet as your evidence-backed worklist",13,WHITE,"Helvetica-Bold")
text(c,38,H-468,"Never infer emails, phone numbers, or profile links. Use the source URL and verification status to decide what must be checked first.",8.5,MUTED)
screenshot(c,ASSETS / "Contacts.png",38,45,500,120)

fill(c,PANEL);c.roundRect(555,45,248,120,7,stroke=0,fill=1)
text(c,573,146,"THE SIGNAL KEY",9,WHITE,"Helvetica-Bold")
pill(c,573,123,"CORAL",CORAL);text(c,640,128,"Priority / unverified",8.2,MUTED)
pill(c,573,99,"TEAL",TEAL);text(c,633,104,"Verified / progress",8.2,MUTED)
pill(c,573,75,"SLATE",MUTED,BG);text(c,640,80,"Context / source detail",8.2,MUTED)
text(c,573,59,"NEXT MOVE",8,TEAL,"Helvetica-Bold")
fit_text(c,573,46,"Verify source -> tailor one message -> set a next date.",212,8.3,WHITE,"Helvetica")

text(c,38,18,"CRM hygiene rule: every meaningful update needs a source, a verification status, an owner, and a next date.",8.5,MUTED,"Helvetica-Bold")
text(c,W-151,18,"QURE.AI | INDIA BD",8.5,CORAL,"Helvetica-Bold")
c.save()
print(PDF)
