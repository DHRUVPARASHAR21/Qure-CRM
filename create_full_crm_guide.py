from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(r"C:\Users\pardh\OneDrive\Desktop\Qure")
ASSETS = ROOT / "outputs" / "qure-life-sciences-crm-qure-styled"
OUT = ROOT / "outputs" / "qure-crm-onboarding-field-guide"
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / "qure_crm_india_field_guide.pdf"
W, H = landscape(A4)
BG = "#0B1926"; PANEL = "#0D1E2D"; PANEL2 = "#11283A"; HEADER = "#143145"; WHITE = "#F8FAFC"; MUTED = "#94A3B8"; LINE = "#24445A"; CORAL = "#FF6B6B"; TEAL = "#14B8A6"; TEAL_DARK = "#0F766E"; AMBER = "#F4B740"

def rgb(v):
    h=v.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def fill(c,v): c.setFillColorRGB(*rgb(v))
def stroke(c,v): c.setStrokeColorRGB(*rgb(v))
def text(c,x,y,s,size=9,color=WHITE,font="Helvetica"):
    fill(c,color); c.setFont(font,size); c.drawString(x,y,s)
def wrap(c,x,y,s,width,size=9,color=WHITE,font="Helvetica",leading=None):
    leading=leading or size+3; words=s.split(); line=""; yy=y
    for word in words:
        test=(line+" "+word).strip()
        if stringWidth(test,font,size)<=width: line=test
        else:
            text(c,x,yy,line,size,color,font); yy-=leading; line=word
    if line: text(c,x,yy,line,size,color,font); yy-=leading
    return yy
def rule(c,y): stroke(c,LINE); c.setLineWidth(.7); c.line(36,y,W-36,y)
def label(c,x,y,s,color=CORAL): text(c,x,y,s.upper(),8,color,"Helvetica-Bold")
def pill(c,x,y,s,bg,text_color=BG):
    width=stringWidth(s,"Helvetica-Bold",7.5)+18; fill(c,bg);c.roundRect(x,y,width,18,9,stroke=0,fill=1);text(c,x+9,y+5,s,7.5,text_color,"Helvetica-Bold");return width
def header(c,n,title,subtitle):
    fill(c,BG);c.rect(0,0,W,H,stroke=0,fill=1)
    text(c,36,H-29,"QURE.AI / INDIA LIFE SCIENCES CRM",8.5,CORAL,"Helvetica-Bold")
    text(c,36,H-55,title,18,WHITE,"Helvetica-Bold")
    text(c,36,H-72,subtitle,9,MUTED)
    stroke(c,CORAL);c.setLineWidth(1);c.line(36,H-82,W-36,H-82)
    text(c,36,18,"FIRST-TIMER FIELD GUIDE",7.5,MUTED,"Helvetica-Bold")
    text(c,W-90,18,f"PAGE {n} / 8",7.5,CORAL,"Helvetica-Bold")
def card(c,x,y,w,h,heading,body,accent=TEAL):
    fill(c,PANEL2);c.roundRect(x,y,w,h,7,stroke=0,fill=1)
    stroke(c,accent);c.setLineWidth(1.7);c.line(x+14,y+h-15,x+42,y+h-15)
    text(c,x+14,y+h-33,heading.upper(),8,MUTED,"Helvetica-Bold")
    wrap(c,x+14,y+h-51,body,w-28,8.6,WHITE,"Helvetica",11)
def bullet(c,x,y,title_txt,body,width,accent=TEAL):
    fill(c,accent);c.circle(x+5,y+1,4,stroke=0,fill=1)
    text(c,x+17,y-3,title_txt,8.8,WHITE,"Helvetica-Bold")
    end=wrap(c,x+17,y-16,body,width-17,8.2,MUTED,"Helvetica",11)
    return end-3
def screen(c,file,x,y,w,h,caption):
    fill(c,WHITE);c.roundRect(x,y,w,h,5,stroke=0,fill=1)
    c.drawImage(ImageReader(str(ASSETS/file)),x+3,y+3,w-6,h-6,preserveAspectRatio=True,anchor='c',mask='auto')
    stroke(c,LINE);c.setLineWidth(.8);c.roundRect(x,y,w,h,5,stroke=1,fill=0)
    text(c,x+10,y-12,caption,7.5,MUTED)
def flow(c,x,y,items):
    cursor=x
    for idx,(tag,desc,color) in enumerate(items):
        fill(c,color);c.circle(cursor+12,y,12,stroke=0,fill=1);text(c,cursor+6,y-3,tag,7,WHITE,"Helvetica-Bold")
        wrap(c,cursor+30,y+4,desc,120,8,WHITE,"Helvetica",10)
        if idx<len(items)-1: stroke(c,LINE);c.setLineWidth(1);c.line(cursor+143,y,cursor+165,y)
        cursor+=180

c=canvas.Canvas(str(PDF),pagesize=landscape(A4))

# 1. Cover / orientation
header(c,1,"CRM Field Guide","A detailed operating manual for building, qualifying, and advancing Qure.ai India Life Sciences relationships.")
text(c,36,H-118,"What this CRM is for",13,WHITE,"Helvetica-Bold")
wrap(c,36,H-136,"Use it to convert public research, account context, and intentional outreach into a visible next step. It is not an address book. It is a shared decision system.",455,10,MUTED,"Helvetica",14)
screen(c,"Dashboard.png",500,H-351,305,205,"The Dashboard is the daily starting point.")
card(c,36,H-265,142,90,"1. Research","Capture a source-backed company or role signal. If it cannot be verified, label it clearly.",TEAL)
card(c,191,H-265,142,90,"2. Qualify","Score relevance, clarify buying influence, and write the most plausible Qure.ai use case.",CORAL)
card(c,346,H-265,142,90,"3. Advance","Log one owner, one next action, and one deadline. Follow-up status drives the operating cadence.",TEAL)
text(c,36,H-294,"The current workspace at a glance",13,WHITE,"Helvetica-Bold")
card(c,36,H-391,142,64,"25 Accounts","India-relevant pharma, biotech, diagnostics, imaging, and provider targets.",CORAL)
card(c,191,H-391,142,64,"100 Contacts","Public professional records aligned to decision-maker functions.",TEAL)
card(c,346,H-391,142,64,"82 Verified","Official-source roles. Re-check remaining records before outreach.",TEAL)
card(c,36,H-469,220,60,"Golden rule","Before a record can drive outreach, it needs a source, a verification status, an owner, and a next date.",CORAL)
card(c,268,H-469,220,60,"Four habits","Start on the dashboard. Work Tier 1 first. Avoid inferred contact details. Keep every action traceable.",TEAL)
c.showPage()

# 2 Dashboard
header(c,2,"Dashboard: find the work that matters","This sheet summarizes volume, coverage, evidence quality, and pipeline posture. Use it before opening a detail tab.")
screen(c,"Dashboard.png",36,H-378,490,230,"Read the KPI stack from top to bottom before scanning the distribution charts.")
card(c,547,H-177,122,70,"Volume","Total accounts and contacts show the breadth of the workspace. More records are not automatically more coverage.",TEAL)
card(c,681,H-177,122,70,"Priority","High-priority leads and Tier 1 accounts show where tailored time should be concentrated.",CORAL)
card(c,547,H-260,122,70,"Coverage","Accounts with coverage exposes where a target account has no mapped decision-maker yet.",CORAL)
card(c,681,H-260,122,70,"Freshness","Research freshness and verified contacts show whether the data is safe enough to act on.",TEAL)
text(c,547,H-294,"How to produce an insight",12,WHITE,"Helvetica-Bold")
y=H-314
y=bullet(c,547,y,"Notice a concentration.","The dashboard shows 88 contacts in pharma and 12 in biotech. That is focus, but it is also a potential segment gap.",255,CORAL)
y=bullet(c,547,y,"Pair it with a business question.","If diagnostics or imaging is strategic, ask which accounts and roles are missing - then turn that into a sourcing sprint.",255,TEAL)
y=bullet(c,547,y,"Choose one action.","For example: add a validated technical evaluator and economic buyer to each uncovered Tier 1 account by the next weekly review.",255,TEAL)
text(c,36,54,"Do not treat a chart as the conclusion. Pair its signal with an account hypothesis, a named owner, and a dated action.",8.5,MUTED,"Helvetica-Bold")
c.showPage()

# 3 Accounts
header(c,3,"Accounts: decide where Qure.ai should play","Each row is an account-level thesis. It should explain why this organization is relevant, who owns it, and how much coverage exists.")
screen(c,"Accounts.png",36,H-362,500,215,"Accounts: tier, strategic hypothesis, owner, source URL, research date, and coverage score.")
text(c,557,H-116,"Required account thinking",12,WHITE,"Helvetica-Bold")
y=H-140
y=bullet(c,557,y,"Name the value hypothesis.","Use the opportunity-hypothesis field to describe a concrete pathway: clinical-trial imaging, RWE, imaging biomarkers, diagnostics workflow, or MedTech integration.",245,TEAL)
y=bullet(c,557,y,"Use tier intentionally.","Tier 1 means focused attention, not just company size. A Tier 1 account needs a senior mapped contact and an active next step.",245,CORAL)
y=bullet(c,557,y,"Read coverage as a risk indicator.","A low or zero coverage score means the CRM has insufficient decision-maker context. Research is the next action - not generic outreach.",245,CORAL)
card(c,557,74,245,72,"Example","A Tier 1 diagnostics account with zero coverage: create one research task to identify a diagnostics/imaging leader, a digital leader, and a commercial sponsor. Add only verified roles.",CORAL)
text(c,36,47,"Quality bar: if someone reads the Account row alone, they should understand why Qure.ai is relevant and what the next research or relationship move is.",8.5,MUTED,"Helvetica-Bold")
c.showPage()

# 4 Contacts
header(c,4,"Contacts: turn public roles into stakeholder maps","Contacts are a research-backed worklist. No personal data should be guessed or inferred.")
screen(c,"Contacts.png",36,H-356,768,205,"Contacts: function, seniority, relevance, buying influence, use case, source, verification, and lead score.")
text(c,36,H-390,"How to read the core fields",12,WHITE,"Helvetica-Bold")
card(c,36,H-486,180,70,"Function + seniority","Function tells you the conversation to have. Seniority helps decide whether the person is an economic buyer, champion, evaluator, or end user.",TEAL)
card(c,228,H-486,180,70,"Buying influence","Economic buyer: owns budget. Champion: mobilizes internally. Technical evaluator: tests fit. End user: uses the solution. Blocker: needs early risk resolution.",CORAL)
card(c,420,H-486,180,70,"Lead score","Use relevance and influence to prioritize. A high score is an invitation to personalize, not permission to send a generic pitch.",TEAL)
card(c,612,H-486,192,70,"Verification","Teal indicates verified official-source data. Coral indicates an unverified role or attention item. Re-check it before outreach.",CORAL)
text(c,36,47,"Example: A verified VP in Medical Affairs with a 4.5+ score may be a strong champion for RWE or clinical evidence. Pair them with a technical evaluator before proposing a solution path.",8.5,MUTED,"Helvetica-Bold")
c.showPage()

# 5 Opportunities
header(c,5,"Opportunities: make the commercial hypothesis testable","Create an opportunity after a credible use case emerges. The purpose is to coordinate discovery, not to make premature forecasts.")
screen(c,"Opportunities.png",36,H-360,520,215,"Opportunities: link the account and contact, state the use case, then make risk and next action explicit.")
text(c,578,H-120,"Use-case menu",12,WHITE,"Helvetica-Bold")
flow(c,578,H-153,[('A','Clinical trials / imaging biomarkers',TEAL),('B','RWE / evidence generation',CORAL),('C','Diagnostics / MedTech integration',TEAL)])
text(c,578,H-196,"Stage discipline",12,WHITE,"Helvetica-Bold")
y=H-218
y=bullet(c,578,y,"Research","Evidence exists, but no validated sponsor or scoped problem yet.",210,TEAL)
y=bullet(c,578,y,"Qualified","A sponsor and specific use case are identified. Confirm constraints, alternatives, and stakeholder roles.",210,CORAL)
y=bullet(c,578,y,"Discovery to proposal","Use only when a real conversation, evaluation path, or scoped request is logged in Activities.",210,TEAL)
card(c,578,78,226,70,"Real insight example","If 25 opportunities sit in Research, the immediate goal is not pipeline inflation. Select the highest-fit Tier 1 accounts and graduate a small number through validated discovery.",CORAL)
text(c,36,47,"Every opportunity must have a primary contact, a next best action, an expected close date used as a planning signal, and documented risks or dependencies.",8.5,MUTED,"Helvetica-Bold")
c.showPage()

# 6 Activities
header(c,6,"Outreach and Activities: run the CRM as a cadence","This is the operating ledger. A record is only progressing when the next action and date are visible and owned.")
screen(c,"Outreach___Activities.png",36,H-358,500,215,"Outreach & Activities: document what happened, what is next, who owns it, and whether follow-up is due.")
text(c,558,H-116,"Daily workflow",12,WHITE,"Helvetica-Bold")
flow(c,558,H-148,[('1','Open overdue / due follow-ups',CORAL),('2','Complete the next action',TEAL),('3','Log outcome + next date',TEAL)])
text(c,558,H-191,"What good logging looks like",12,WHITE,"Helvetica-Bold")
y=H-213
y=bullet(c,558,y,"Outcome is factual.","Write what happened: 'Source reviewed', 'Intro request sent', 'Meeting accepted', or 'No response'. Avoid vague updates such as 'followed up'.",245,TEAL)
y=bullet(c,558,y,"Next action is specific.","Use a single verb and a decision owner: 'Draft oncology imaging note for Medical Affairs leader' is better than 'Follow up'.",245,CORAL)
y=bullet(c,558,y,"Deadline is real.","A next-action date should make it easy for a teammate to see whether help or a decision is needed.",245,TEAL)
text(c,36,47,"Coral is an attention signal and teal indicates healthy progress, but the status text - not color alone - is always the source of truth.",8.5,MUTED,"Helvetica-Bold")
c.showPage()

# 7 Sources and News signals
header(c,7,"Research Sources and news signals: keep the evidence trail usable","Every research-backed change must be traceable to an official or credible public source. Use a news event as a prompt to investigate, never as proof of fit.")
screen(c,"Research_Sources.png",36,H-360,480,215,"Research Sources: capture the URL, extracted information, date accessed, and confidence level.")
text(c,538,H-116,"Signal-to-action framework",12,WHITE,"Helvetica-Bold")
flow(c,538,H-150,[('1','News or company event',CORAL),('2','Why it may matter',TEAL),('3','CRM action',TEAL)])
text(c,538,H-196,"Examples to capture",12,WHITE,"Helvetica-Bold")
y=H-218
y=bullet(c,538,y,"Clinical trial or label milestone","Potential need: imaging endpoint strategy, evidence generation, or medical affairs support. Action: identify the development/medical leader and record the official source.",245,CORAL)
y=bullet(c,538,y,"India market expansion or new partnership","Potential need: commercial evidence, local validation, diagnostics workflow, or alliance conversations. Action: update the account hypothesis before finding contacts.",245,TEAL)
y=bullet(c,538,y,"Digital, AI, diagnostics, or imaging announcement","Potential need: integration conversation. Action: map the digital/technical evaluator and the relevant business-unit sponsor.",245,TEAL)
card(c,538,74,266,70,"Evidence rule","The source date, source URL, and verification status are mandatory. 'LinkedIn says' or inferred email formats are not valid CRM evidence.",CORAL)
text(c,36,47,"News is useful when it changes the hypothesis, stakeholder map, timing, or next action. Otherwise, it is background context - not a lead signal.",8.5,MUTED,"Helvetica-Bold")
c.showPage()

# 8 Operating rhythm / glossary
header(c,8,"Operating rhythm, triggers, and glossary","A small, repeatable cadence turns the CRM from a list into an internal operating system.")
text(c,36,H-116,"Recommended cadence",12,WHITE,"Helvetica-Bold")
card(c,36,H-205,184,70,"Daily - 10 minutes","Review overdue items. Finish or reschedule next actions. Log outcomes immediately after meaningful outreach or research.",CORAL)
card(c,234,H-205,184,70,"Weekly - 30 minutes","Review Tier 1 coverage, high-score contacts, aging sources, and opportunities stuck in Research. Assign one next move per priority account.",TEAL)
card(c,432,H-205,184,70,"Monthly - 45 minutes","Check portfolio balance by sector and use case. Retire stale assumptions, update account tiers, and agree sourcing priorities.",TEAL)
text(c,36,H-238,"Trigger playbook",12,WHITE,"Helvetica-Bold")
data=[
('No contact coverage','Create an account research task; do not begin generic outreach.',CORAL),
('Unverified role','Re-check the company source; update verification status and date.',CORAL),
('Lead score 4.5+','Draft one role-specific outreach concept and confirm buying influence.',TEAL),
('Research older than 90 days','Refresh source, title, and account hypothesis before relying on the record.',CORAL),
('Opportunity has no next action','Set a dated discovery, research, or relationship action immediately.',TEAL),
]
y=H-260
for trigger,action,color in data:
    fill(c,color);c.roundRect(36,y-13,142,22,5,stroke=0,fill=1);text(c,45,y-6,trigger,7.8,BG,"Helvetica-Bold");wrap(c,194,y-5,action,410,8.5,WHITE,"Helvetica",11);y-=37
text(c,36,103,"Glossary",12,WHITE,"Helvetica-Bold")
card(c,36,58,184,65,"Coverage","Relevant contacts mapped to an account.",TEAL)
card(c,234,58,184,65,"Champion","A stakeholder who can mobilize internal support for a useful solution.",CORAL)
card(c,432,58,184,65,"Technical evaluator","Validates clinical, data, workflow, or integration feasibility.",TEAL)
card(c,630,58,174,65,"Economic buyer","Can authorize budget or commercial commitment.",CORAL)
c.save()
print(PDF)
