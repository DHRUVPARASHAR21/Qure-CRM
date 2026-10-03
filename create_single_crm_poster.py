from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = Path('output/pdf/qure_crm_single_page_operating_poster.pdf')
OUT.parent.mkdir(parents=True, exist_ok=True)
W, H = landscape(A3)

BG = HexColor('#0B1926')
PANEL = HexColor('#112B3E')
PANEL_2 = HexColor('#0D1E2D')
WHITE = HexColor('#F8FAFC')
MUTED = HexColor('#A7B6C8')
LINE = HexColor('#365168')
CORAL = HexColor('#FF6B6B')
TEAL = HexColor('#14B8A6')

def box(c, x, y, w, h, title, body, accent=TEAL, title_size=12, body_size=10.2, pad=18):
    c.setFillColor(PANEL)
    c.roundRect(x, y, w, h, 10, stroke=0, fill=1)
    c.setFillColor(accent)
    c.rect(x+pad, y+h-20, 42, 3, stroke=0, fill=1)
    text(c, x+pad, y+h-39, title.upper(), title_size, MUTED, 'Helvetica-Bold')
    wrap(c, x+pad, y+h-61, body, w-2*pad, body_size, WHITE, 'Helvetica', body_size*1.32)

def text(c, x, y, s, size=10, color=WHITE, font='Helvetica'):
    c.setFont(font, size); c.setFillColor(color); c.drawString(x, y, s)

def wrap(c, x, y, s, width, size=10, color=WHITE, font='Helvetica', leading=None):
    leading = leading or size*1.28
    c.setFont(font, size); c.setFillColor(color)
    cursor = y
    for paragraph in s.split('\n'):
        if not paragraph.strip():
            cursor -= leading * 0.35
            continue
        words=paragraph.split(); lines=[]; line=''
        for word in words:
            trial = word if not line else line+' '+word
            if stringWidth(trial,font,size) <= width: line=trial
            else: lines.append(line); line=word
        if line: lines.append(line)
        for line in lines:
            c.drawString(x, cursor, line)
            cursor -= leading
    return cursor

def arrow(c, x1, y, x2, color=TEAL):
    c.setStrokeColor(color); c.setLineWidth(2); c.line(x1,y,x2-8,y)
    c.setFillColor(color); c.setStrokeColor(color)
    c.line(x2-12,y+5,x2-6,y); c.line(x2-12,y-5,x2-6,y)

c=canvas.Canvas(str(OUT),pagesize=(W,H)); c.setTitle('Qure.ai India Life Sciences CRM - Operating Poster')
c.setFillColor(BG); c.rect(0,0,W,H,stroke=0,fill=1)

# Header
text(c,54,H-46,'QURE.AI / INDIA LIFE SCIENCES',12,CORAL,'Helvetica-Bold')
text(c,54,H-86,'CRM Operating Poster',30,WHITE,'Helvetica-Bold')
text(c,54,H-111,'One evidence-backed system for deciding who matters, what to do next, and when to do it.',13,MUTED)
c.setStrokeColor(CORAL); c.setLineWidth(2); c.line(54,H-128,W-54,H-128)

# Workflow strip
text(c,54,H-159,'THE OPERATING LOOP',12,WHITE,'Helvetica-Bold')
steps=[
 ('1. DASHBOARD','Find the priority signal','Review overdue work, Tier 1 coverage, lead scores, and stale research.'),
 ('2. ACCOUNT','State the hypothesis','Record why Qure.ai is relevant, the best use case, tier, owner, and source.'),
 ('3. CONTACT','Map buying influence','Capture only public, verified professional information. Score relevance and role.'),
 ('4. OPPORTUNITY','Test the use case','Define clinical trials, RWE, biomarkers, diagnostics, or integration path.'),
 ('5. ACTIVITY','Move it forward','Log the outcome, assign one owner, and set one dated next action.'),
]
x0=54; gap=14; sw=(W-108-4*gap)/5; sy=H-302
for i,(label,head,body) in enumerate(steps):
    accent = CORAL if i in (0,3) else TEAL
    box(c,x0+i*(sw+gap),sy,sw,112,label,head+'\n'+body,accent,10.3,9.2,14)
    # redraw differentiated headline after generic body makes it included as body just enough
    if i<4: arrow(c,x0+(i+1)*sw+i*gap+4,sy+56,x0+(i+1)*(sw+gap)-7)

# Lower columns
col_gap=18; cw=(W-108-2*col_gap)/3; ytop=H-340
text(c,54,ytop,'1. HOW TO READ THE DASHBOARD',13,WHITE,'Helvetica-Bold')
box(c,54,ytop-183,cw,157,'Start here every day',
    'High-priority lead + no next action = fix now.\n\nZero account coverage = research before outreach.\n\nResearch older than 90 days = refresh source, title, and hypothesis.',CORAL,11,10.8)
text(c,54,ytop-205,'TURN A CHART INTO AN ACTION',10,MUTED,'Helvetica-Bold')
wrap(c,54,ytop-224,'Example: if pharma dominates contact coverage but diagnostics has few mapped roles, create a sourcing task for the missing diagnostics and imaging decision-makers.',cw,10.5,WHITE,'Helvetica',14)

x2=54+cw+col_gap
text(c,x2,ytop,'2. BUILD RECORDS THAT ARE SAFE TO USE',13,WHITE,'Helvetica-Bold')
box(c,x2,ytop-92,cw,66,'Account','Tier + owner + India-market relevance + use-case hypothesis + source URL + research date.',TEAL,10.8,10.4)
box(c,x2,ytop-170,cw,66,'Contact','Current public title + function + seniority + buying influence + source + verification date.',CORAL,10.8,10.4)
box(c,x2,ytop-248,cw,66,'Opportunity','Use case + stage + stakeholder map + risk + next best action + expected action date.',TEAL,10.8,10.4)
text(c,x2,ytop-273,'QUALITY RULE',10,MUTED,'Helvetica-Bold')
wrap(c,x2,ytop-292,'Never infer a work email, phone number, LinkedIn URL, or current role. If it cannot be verified from a public source, label it unverified and re-check it.',cw,10.4,WHITE,'Helvetica',13.5)

x3=x2+cw+col_gap
text(c,x3,ytop,'3. USE THE RIGHT STAKEHOLDER LENS',13,WHITE,'Helvetica-Bold')
box(c,x3,ytop-116,cw,90,'Economic buyer','Can authorize budget or commercial commitment. Show a credible strategic and economic case.',CORAL,10.8,10.4)
box(c,x3,ytop-218,cw,90,'Champion + evaluator','Champion mobilizes support; technical evaluator validates clinical, data, workflow, and integration feasibility.',TEAL,10.8,10.4)
text(c,x3,ytop-244,'PERSONALISATION EXAMPLE',10,MUTED,'Helvetica-Bold')
wrap(c,x3,ytop-263,'A verified Medical Affairs leader may care about evidence generation and RWE. Pair that conversation with a technical evaluator before proposing a solution path.',cw,10.4,WHITE,'Helvetica',13.5)

# Bottom action band
by=72
c.setFillColor(PANEL_2); c.roundRect(54,by,W-108,111,10,stroke=0,fill=1)
text(c,72,by+84,'WHEN YOU SEE THIS',10,MUTED,'Helvetica-Bold')
text(c,300,by+84,'DO THIS NEXT',10,MUTED,'Helvetica-Bold')
triggers=[
 ('No contact coverage','Create a research task; do not send generic outreach.',CORAL),
 ('Lead score 4.5+','Draft a role-specific outreach concept and confirm buying influence.',TEAL),
 ('Opportunity has no next action','Set a dated discovery, research, or relationship action immediately.',CORAL),
]
for i,(trigger,action,color) in enumerate(triggers):
    yy=by+60-i*24
    c.setFillColor(color); c.roundRect(72,yy-6,198,18,4,stroke=0,fill=1)
    text(c,81,yy,trigger,8.8,BG,'Helvetica-Bold')
    text(c,300,yy,action,9.7,WHITE)

text(c,54,36,'CADENCE: 10 min daily - 30 min weekly - 45 min monthly',10,MUTED,'Helvetica-Bold')
text(c,W-54-stringWidth('QURE.AI INTERNAL OPERATING GUIDE', 'Helvetica-Bold', 10),36,'QURE.AI INTERNAL OPERATING GUIDE',10,CORAL,'Helvetica-Bold')
c.save(); print(OUT)
