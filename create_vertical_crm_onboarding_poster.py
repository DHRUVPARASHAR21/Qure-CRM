from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = Path('output/pdf/qure_crm_full_scale_vertical_onboarding_poster.pdf')
ASSET = Path('outputs/qure-life-sciences-crm-qure-styled')
OUT.parent.mkdir(parents=True, exist_ok=True)

# 18 x 72 inch vertical poster: readable at full-size print and on-screen scroll.
W, H = 1296, 5184
BG, PANEL, PANEL2 = HexColor('#0B1926'), HexColor('#112B3E'), HexColor('#0D1E2D')
WHITE, MUTED, LINE = HexColor('#F8FAFC'), HexColor('#A7B6C8'), HexColor('#345068')
CORAL, TEAL = HexColor('#FF6B6B'), HexColor('#14B8A6')

def text(c,x,y,s,size=14,color=WHITE,font='Helvetica'):
    c.setFillColor(color); c.setFont(font,size); c.drawString(x,y,s)

def wrap(c,x,y,s,w,size=14,color=WHITE,font='Helvetica',leading=None):
    leading=leading or size*1.3; c.setFillColor(color); c.setFont(font,size); cursor=y
    for para in s.split('\n'):
        if not para.strip(): cursor -= leading*.42; continue
        words=para.split(); line=''
        for word in words:
            trial=word if not line else line+' '+word
            if stringWidth(trial,font,size)<=w: line=trial
            else: c.drawString(x,cursor,line); cursor-=leading; line=word
        if line: c.drawString(x,cursor,line); cursor-=leading
    return cursor

def section(c, y, kicker, title, sub=''):
    text(c,60,y,kicker.upper(),12,CORAL,'Helvetica-Bold')
    text(c,60,y-38,title,26,WHITE,'Helvetica-Bold')
    if sub: wrap(c,60,y-63,sub,W-120,14,MUTED,'Helvetica',18)
    c.setStrokeColor(LINE); c.setLineWidth(1); c.line(60,y-90,W-60,y-90)

def card(c,x,y,w,h,title,body,accent=TEAL,body_size=13.5):
    c.setFillColor(PANEL); c.roundRect(x,y,w,h,12,stroke=0,fill=1)
    c.setFillColor(accent); c.rect(x+18,y+h-22,45,4,stroke=0,fill=1)
    text(c,x+18,y+h-46,title.upper(),12,MUTED,'Helvetica-Bold')
    wrap(c,x+18,y+h-66,body,w-36,body_size,WHITE,'Helvetica',body_size*1.33)

def numbered(c,x,y,num,title,body,accent=TEAL,w=215):
    c.setFillColor(accent); c.circle(x+18,y+55,18,stroke=0,fill=1)
    text(c,x+13,y+49,str(num),13,BG,'Helvetica-Bold')
    text(c,x+48,y+59,title,15,WHITE,'Helvetica-Bold')
    wrap(c,x+48,y+35,body,w-48,12.4,MUTED,'Helvetica',15.5)

def image_panel(c, path, x, y, w, h, caption):
    c.setFillColor(WHITE); c.roundRect(x,y,w,h,12,stroke=0,fill=1)
    img=ImageReader(str(path)); iw,ih=img.getSize(); margin=14
    scale=min((w-2*margin)/iw,(h-42)/ih); dw,dh=iw*scale,ih*scale
    c.drawImage(img,x+(w-dw)/2,y+28,dw,dh,mask='auto')
    text(c,x+18,y+10,caption,10,MUTED,'Helvetica-Bold')

def arrow(c,x1,x2,y):
    c.setStrokeColor(TEAL); c.setLineWidth(3); c.line(x1,y,x2-12,y)
    c.line(x2-19,y+7,x2-11,y); c.line(x2-19,y-7,x2-11,y)

c=canvas.Canvas(str(OUT),pagesize=(W,H)); c.setTitle('Qure.ai India Life Sciences CRM - Full Scale Vertical Onboarding Poster')
c.setFillColor(BG); c.rect(0,0,W,H,stroke=0,fill=1)

# Hero
text(c,60,H-72,'QURE.AI / INDIA LIFE SCIENCES BUSINESS DEVELOPMENT',15,CORAL,'Helvetica-Bold')
text(c,60,H-132,'CRM onboarding',44,WHITE,'Helvetica-Bold')
text(c,60,H-179,'The full operating guide',44,WHITE,'Helvetica-Bold')
wrap(c,60,H-223,'A detailed, evidence-first system for turning India life sciences research into coverage, credible conversations, and measurable next actions.',W-120,18,MUTED,'Helvetica',24)
c.setStrokeColor(CORAL); c.setLineWidth(3); c.line(60,H-277,W-60,H-277)
card(c,60,H-468,360,144,'What this CRM is','A shared decision system - not an address book. It records account hypotheses, public professional roles, opportunity logic, activity outcomes, and source evidence.',CORAL,14)
card(c,468,H-468,360,144,'The discipline','Every priority record needs a source, a clear verification status, an owner, and a dated next action. Unknown is acceptable; invented data is not.',TEAL,14)
card(c,876,H-468,360,144,'The result','Use the dashboard to focus, the sheets to preserve context, and the activity log to make each relationship move traceable and repeatable.',TEAL,14)

# Operating loop
section(c,H-550,'01 / THE MENTAL MODEL','One signal. One hypothesis. One next move.','The CRM works as a closed loop: research creates an account hypothesis; contacts make the stakeholder map real; an opportunity tests commercial relevance; activity records the proof and the next decision.')
y=H-765; x=60; stepw=226
steps=[('DASHBOARD','Find the work that matters.'),('ACCOUNT','State why Qure.ai should play.'),('CONTACT','Map who can influence the decision.'),('OPPORTUNITY','Test the use case and deal path.'),('ACTIVITY','Log outcome and set the next move.')]
for i,(t,b) in enumerate(steps):
    numbered(c,x+i*244,y,i+1,t,b,CORAL if i in (0,3) else TEAL,226)
    if i<4: arrow(c,x+i*244+220,x+(i+1)*244-8,y+55)
card(c,60,H-970,1176,96,'The non-negotiable rule','Do not begin generic outreach from an incomplete record. First establish the account thesis, decision-maker coverage, evidence source, and a reason that the timing is useful.',CORAL,15)

# Dashboard
section(c,H-1050,'02 / DASHBOARD','Start here: find the highest-value work','The dashboard is the work queue. It rolls up accounts, contacts, stages, coverage, freshness, and next-action deadlines so that attention follows evidence instead of noise.')
image_panel(c,ASSET/'Dashboard.png',60,H-1515,690,300,'Dashboard: use filters, KPI cards, and distributions to choose the next account or research task.')
card(c,780,H-1285,456,130,'Read the KPI stack','1. Total accounts and contacts: scope.\n2. High-priority leads: who merits tailored time.\n3. Accounts with coverage: whether a target has mapped decision-makers.\n4. Freshness: whether the data is safe to act on.',TEAL,13.6)
card(c,780,H-1430,456,130,'Turn signal into action','If a Tier 1 account has zero coverage, research comes before outreach. If a lead scores 4.5+, draft a role-specific concept. If research is stale, refresh the source before using the title or role.',CORAL,13.6)
card(c,60,H-1655,1176,110,'Example insight: portfolio gap','If pharma contains most contacts while diagnostics or imaging has few mapped leaders, the conclusion is not "we have enough leads." Create a focused sourcing task: identify one clinical/diagnostics leader, one digital or innovation leader, and one commercial sponsor for each priority gap.',TEAL,14)

# Accounts
section(c,H-1735,'03 / ACCOUNTS','Build an account thesis before you build outreach','The Accounts sheet turns a company name into an intentional point of view: why this organization matters, what Qure.ai could help solve, who owns the relationship, and what needs to happen next.')
image_panel(c,ASSET/'Accounts.png',60,H-2100,720,280,'Accounts: tier, market relevance, strategic hypothesis, owner, relationship status, source URL, research date, and coverage score.')
card(c,810,H-1925,426,102,'Tier with intent','Tier 1 means focused time, not simply company size. A Tier 1 account should have a named owner, a credible Qure.ai use case, senior coverage, and a next action.',CORAL,13.3)
card(c,810,H-2040,426,102,'Write the hypothesis','Use one testable sentence: "Qure.ai may help [account] improve [clinical, evidence, imaging, diagnostic, or integration outcome] through [specific pathway]."',TEAL,13.3)
card(c,810,H-2155,426,102,'Coverage is a risk signal','Low coverage does not mean low value. It means insufficient stakeholder context. Research is the action; generic messages are not.',CORAL,13.3)
card(c,60,H-2295,1176,112,'Account quality checklist','Before treating an account as active: confirm sector/sub-sector and India relevance; set Tier 1, 2, or 3; write a source-backed use-case hypothesis; assign an account owner; add a source URL and date; map at least one senior contact for Tier 1.',TEAL,14)

# Contacts
section(c,H-2375,'04 / CONTACTS','Turn public roles into a stakeholder map','Contacts are research-backed professional records, not personal-data profiles. They explain what conversation to have, who can mobilize support, and whose information must be verified again.')
image_panel(c,ASSET/'Contacts.png',60,H-2740,760,275,'Contacts: title, function, seniority, geography, influence, use case, source, verification status, last-verified date, and lead score.')
card(c,850,H-2528,386,96,'Function + seniority','Function shapes the conversation. Seniority helps prioritize the role in a buying process. Use Director, VP, SVP, C-suite, Global Head, or BU Head when verified.',TEAL,12.8)
card(c,850,H-2636,386,96,'Buying influence','Economic buyer: authorizes budget. Champion: mobilizes support. Technical evaluator: tests fit. End user: uses it. Blocker: needs risk resolution early.',CORAL,12.8)
card(c,850,H-2744,386,96,'Lead score','Score relevance and influence to decide where to spend research and personalization time. A high score is a prompt to tailor; it is never permission to send a generic pitch.',TEAL,12.8)
card(c,60,H-2885,1176,115,'Verification and safe handling','Use a public professional profile only where verified. Capture a work email only if explicitly published by the organization. Never infer email patterns, phone numbers, LinkedIn URLs, or job titles. Record source URL, source type, verification status, and last verified date.',CORAL,14)

# Opportunities
section(c,H-2965,'05 / OPPORTUNITIES','Make the commercial hypothesis testable','Create an opportunity once a credible use case emerges. The opportunity is not a promise of revenue; it is a shared record of what must be learned, who must be involved, and what could stop progress.')
image_panel(c,ASSET/'Opportunities.png',60,H-3330,700,278,'Opportunities: account/contact link, use case, value band, stage, probability, expected close, stakeholders, risks, and next best action.')
card(c,790,H-3091,446,100,'Use-case menu','Clinical trials, real-world evidence, imaging biomarkers, diagnostics workflow, MedTech integration, medical affairs evidence, radiology workflow, or commercial partnership.',TEAL,13)
card(c,790,H-3203,446,100,'Stage discipline','Research -> Qualified -> Discovery -> Solution fit -> Proposal -> Negotiation -> Closed. Advance only when the stakeholder, use case, and next evidence gate are clear.',CORAL,13)
card(c,790,H-3315,446,100,'Risk and dependency','State what must be true: data access, clinical validation, integration feasibility, regulatory pathway, budget, internal champion, or procurement alignment.',TEAL,13)
card(c,60,H-3470,1176,110,'Opportunity example','A Medical Affairs champion signals a need for evidence generation. Create an RWE opportunity, identify a technical evaluator who can validate data feasibility, assign an owner, list the data or governance dependency, and schedule a discovery action. Do not jump directly to a proposal.',CORAL,14)

# Activities
section(c,H-3550,'06 / OUTREACH AND ACTIVITIES','Make each touchpoint change the record','The activity log is the operating memory. It captures what happened, whether the response advanced the relationship, and the exact next move. A good CRM entry makes a handover possible without a verbal briefing.')
image_panel(c,ASSET/'Outreach___Activities.png',60,H-3918,710,282,'Outreach & Activities: date, type, owner, target, outcome, next action, date, meeting notes, follow-up status, and automated overdue flag.')
card(c,800,H-3712,436,110,'After every meaningful interaction','Log the outcome in plain language. What changed? Which assumption was validated or challenged? Which stakeholder is now relevant? What must happen next?',TEAL,13.1)
card(c,800,H-3834,436,110,'One next action, one date','A record with multiple vague next moves often has none. Choose the next best action, assign an owner, and set a date. Overdue flags are prompts to finish, reschedule, or close the loop.',CORAL,13.1)
card(c,60,H-4055,1176,118,'Outreach example','For a verified VP of Medical Affairs: reference the specific evidence or RWE hypothesis; ask a short discovery question; log whether the person is a champion, evaluator, or neither; capture the outcome; then add a dated action such as "identify technical evaluator" or "refresh evidence source."',TEAL,14)

# Research Sources
section(c,H-4250,'07 / RESEARCH SOURCES AND NEWS SIGNALS','Treat sources as the evidence layer','Every research-backed account or contact must point to a traceable public source. News is useful only when it changes the account hypothesis, stakeholder map, timing, or next action.')
image_panel(c,ASSET/'Research_Sources.png',60,H-4600,710,260,'Research Sources: source URL, type, linked company/contact, extracted detail, access date, verification, and confidence rating.')
card(c,800,H-4393,436,112,'What a good source row contains','The exact public URL, source type, linked company or contact, the factual extract, access date, and a verification/confidence rating. This makes each record auditable.',TEAL,13)
card(c,800,H-4517,436,112,'Convert news into an action','A clinical milestone, India expansion, diagnostic launch, digital-health partnership, or imaging initiative may be a useful signal. Capture the source, state the changed hypothesis, identify a relevant role, and create a dated research or outreach action.',CORAL,13)
card(c,60,H-4740,1176,108,'Evidence hierarchy','Strongest: company leadership page, annual report, press release, regulator filing, conference speaker profile, or explicitly published organizational contact page. Weak or incomplete source? Preserve it, mark the record unverified, and do not treat it as outreach-ready.',CORAL,14)

# Closing playbook
section(c,H-4830,'08 / OPERATING CADENCE','Keep the CRM current enough to trust','The value of the system comes from consistent small updates, not occasional bulk data entry.')
card(c,60,160,360,126,'Daily - 10 minutes','Review overdue activities. Finish, reschedule, or close the loop. Log outcomes immediately after meaningful outreach or research.',CORAL,14)
card(c,468,160,360,126,'Weekly - 30 minutes','Review Tier 1 coverage, high-score leads, stale sources, and opportunities stuck in Research. Assign one next move per priority account.',TEAL,14)
card(c,876,160,360,126,'Monthly - 45 minutes','Check balance by sector and use case. Refresh assumptions, update account tiers, and agree sourcing priorities for the next cycle.',TEAL,14)
text(c,60,92,'THE TEST OF A GOOD CRM RECORD',12,CORAL,'Helvetica-Bold')
wrap(c,60,65,'Can a teammate understand why the account matters, who matters, what evidence supports the view, what has happened, and exactly what should happen next? If not, the record is incomplete.',W-120,16,WHITE,'Helvetica-Bold',21)
text(c,60,28,'QURE.AI INTERNAL OPERATING GUIDE - INDIA LIFE SCIENCES CRM',11,MUTED,'Helvetica-Bold')
c.save(); print(OUT)
