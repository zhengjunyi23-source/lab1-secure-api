# -*- coding: utf-8 -*-
"""Generate the Lab 1 report as a Word (.docx) document."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

EA = "宋体"
HEI = "黑体"
KAI = "楷体"
LAT = "Times New Roman"

PROJ = r"C:\Users\ROG\Doubao\chats\2026-10-26\new-chat\lab1-secure-api"
OUT = os.path.join(PROJ, "report", "Lab1_Report_Work1_Zheng_Junyi.docx")


def set_run(r, text=None, east=EA, lat=LAT, size=10.5, bold=False, color=(0,0,0)):
    if text is not None:
        r.text = text
    r.font.name = lat
    r._element.rPr.rFonts.set(qn("w:eastAsia"), east)
    r.font.size = Pt(size)
    r.font.bold = bold
    if color:
        r.font.color.rgb = RGBColor(*color)


def para(doc, text, east=EA, size=10.5, bold=False, align=None,
         indent=True, line=1.5, before=0, after=0, lat=LAT):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    if align is not None:
        pf.alignment = align
    pf.line_spacing = line
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if indent:
        pf.first_line_indent = Pt(size * 2)  # 2 字符
    set_run(p.add_run(), text, east, lat, size, bold)
    return p


def heading(doc, text, level, page_break=False):
    p = doc.add_paragraph(style=f"Heading {level}")
    pf = p.paragraph_format
    pf.keep_with_next = True
    if page_break:
        pf.page_break_before = True
    sizes = {1: 14, 2: 12, 3: 10.5}
    set_run(p.add_run(), text, HEI, LAT, sizes[level], True)
    return p


def code_block(doc, text):
    for i, line in enumerate(text.split("\n")):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing = 1.0
        pf.space_after = Pt(0)
        pf.space_before = Pt(0)
        pf.left_indent = Pt(6)
        set_run(p.add_run(), line, "Consolas", "Consolas", 9, color=(40,40,40))
    return


def bullet(doc, text, size=10.5):
    p = doc.add_paragraph(style="List Bullet")
    pf = p.paragraph_format
    pf.line_spacing = 1.3
    set_run(p.add_run(), text, EA, LAT, size)
    return p


def numbered(doc, text, size=10.5):
    p = doc.add_paragraph(style="List Number")
    pf = p.paragraph_format
    pf.line_spacing = 1.3
    set_run(p.add_run(), text, EA, LAT, size)
    return p


def add_table(doc, header, rows):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for j, h in enumerate(header):
        c = hdr[j]
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(c.paragraphs[0].add_run(), h, HEI, LAT, 10, True)
        # set cantSplit + header repeat
        trPr = t.rows[0]._tr.get_or_add_trPr()
        el = OxmlElement("w:tblHeader")
        el.set(qn("w:val"), "true")
        trPr.append(el)
    for row in rows:
        cells = t.add_row().cells
        for j, v in enumerate(row):
            c = cells[j]
            set_run(c.paragraphs[0].add_run(), str(v), EA, LAT, 10)
    for r_ in t.rows:
        trPr = r_._tr.get_or_add_trPr()
        cs = OxmlElement("w:cantSplit")
        trPr.append(cs)
    return t


# ---------------- build document ----------------
doc = Document()

# page setup A4, margins 2.5cm
for sec in doc.sections:
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2.5)

# Normal style baseline
normal = doc.styles["Normal"]
normal.font.name = LAT
normal._element.rPr.rFonts.set(qn("w:eastAsia"), EA)
normal.font.size = Pt(10.5)

# ================= Title page =================
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(60)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run(), "HANGZHOU DIANZI UNIVERSITY", HEI, LAT, 16, True)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run(), "Faculty of Computer Science", HEI, LAT, 13, True)

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(40)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run(), "Laboratory Work 1", HEI, LAT, 22, True)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run(), "Secure REST API Development with CI/CD and\nReal CVE Vulnerability Analysis", HEI, LAT, 16, True)

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(30)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run(), "Variant number: CVE-2020-1938", KAI, LAT, 13, True)

info = [("Surname and Name", "Zheng Junyi"),
        ("HDU number", "23320127")]
for k, v in info:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run(), f"{k}: ", EA, LAT, 13, True)
    set_run(p.add_run(), v, EA, LAT, 13, False)

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(30)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run(), "Date: October 26, 2026", EA, LAT, 12, False)

# page break into body
doc.add_page_break()

# ================= 1. Purpose =================
heading(doc, "1. Purpose of the Work", 1)
para(doc, "The purpose of this work is to gain practical, end-to-end experience in building a "
          "secure backend application with automated vulnerability checking, and in analyzing and "
          "remediating a real-world vulnerability in a controlled environment. The work covers the "
          "full security lifecycle: designing protection against the OWASP Top 10 (notably A01 – "
          "Broken Access Control, A03 – Injection, A07 – Identification and Authentication Failures), "
          "integrating security tools into a CI/CD pipeline, reproducing a known CVE with Vulhub, "
          "identifying its root cause, and verifying the fix.")

# ================= 2. Stack & init =================
heading(doc, "2. Choosing a Stack and Initializing the Project", 1)
para(doc, "A Python + Flask stack was chosen. The project is managed with pip inside a virtual "
          "environment; data is stored in SQLite through the SQLAlchemy ORM; authentication uses "
          "PyJWT and bcrypt. The source directory is initialised as a git repository. The project is "
          "linked to a public GitHub repository for the CI/CD part.")
bullet(doc, "Language: Python 3.13 + Flask 3.1.3; ORM: Flask-SQLAlchemy 3.1.1; JWT: PyJWT 2.15.1; password hashing: bcrypt 5.0.0.")
bullet(doc, "Package manager: pip (python -m pip). Dependencies are pinned in requirements.txt.")
bullet(doc, "Version control: git repository initialised locally and linked to GitHub (repository URL: 【待补：GitHub 仓库链接】).")

# ================= 3. Functional API =================
heading(doc, "3. Developing a Functional API", 1)
para(doc, "The API exposes three endpoints, all implemented in app/routes.py:")
add_table(doc,
    ["Method", "Endpoint", "Auth", "Description"],
    [["POST", "/auth/login", "No", "Authenticate with username + password; returns a signed JWT"],
     ["GET", "/api/data", "Yes (JWT)", "Returns the list of all users"],
     ["GET", "/api/me", "Yes (JWT)", "Returns the profile of the currently authenticated user"]])
para(doc, "SQLite is used for simplicity. Demo users are seeded on first run (alice / bob / mallory). "
          "mallory deliberately stores an unsafe <script> string in her about field so the XSS "
          "protection can be demonstrated. The endpoint behaviour is verified by 7 pytest tests, all passing:")
code_block(doc, "$ pytest -q\n.  [100%]\n7 passed in 8.55s")

# ================= 4. Security measures =================
heading(doc, "4. Implementing Basic Security Measures", 1)

heading(doc, "4.1 Protection against SQL injection (SQLi)", 2)
para(doc, "All database access goes through the SQLAlchemy ORM, which always binds user input as "
          "bound parameters (prepared statements). No SQL string is assembled by concatenation. "
          "For example, the login lookup is:")
code_block(doc, "user = User.query.filter_by(username=username).first()")
para(doc, "The test test_sqli_parameterised confirms that a payload such as `' OR '1'='1' --` does not "
          "bypass authentication (the request is rejected with 401).")

heading(doc, "4.2 Protection against Cross-Site Scripting (XSS)", 2)
para(doc, "Every string returned to the client is passed through an output-encoding gate "
          "(app/security.py::xss_safe), which recursively HTML-escapes all string values using "
          "html.escape(..., quote=True). A stored payload <script>alert('XSS')</script> is therefore "
          "returned as &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt; and cannot execute in a "
          "victim's browser. This is verified by test_xss_escaped_on_output.")

heading(doc, "4.3 Protection against Broken Authentication", 2)
bullet(doc, "Passwords are never stored in plaintext — they are hashed with bcrypt (salted, adaptive) in User.set_password / check_password.")
bullet(doc, "On successful login a JWT (HS256) is issued (app/security.py::create_token) with sub, iat, exp and iss claims.")
bullet(doc, "A JWT-verification middleware @require_token protects every restricted endpoint and returns 401 without a valid Bearer token.")
bullet(doc, "Failed logins return a generic message, so an attacker cannot tell a wrong username from a wrong password (no user enumeration).")

# ================= 5. CI/CD =================
heading(doc, "5. Setting Up a CI/CD Pipeline with Security Scanners", 1)
para(doc, "A GitHub Actions workflow .github/workflows/ci.yml runs on every push to main and on every "
          "pull request. It performs: (1) pytest functional tests; (2) SAST with Bandit, producing "
          "bandit-report.html; (3) SCA with Safety, auditing requirements.txt and producing "
          "safety-report.json; (4) uploading the reports as artifacts.")
para(doc, "Local verification of the exact pipeline commands:")
code_block(doc, "$ bandit -r app\nNo issues identified.\nTotal issues (by severity): Low 0, Medium 0, High 0\n"
               "$ safety check -r requirements.txt\n0 vulnerabilities reported\nNo known security vulnerabilities reported.")
para(doc, "GitHub Actions run result and scanner-report screenshots: 【待补：最后一次 pipeline run 链接及 SAST/SCA 报告截图】.")

# ================= 6-7 Vulnerable env & reproduction =================
heading(doc, "6. Selecting and Preparing a Vulnerable Environment", 1)
para(doc, "The chosen vulnerability is CVE-2020-1938 (Apache Tomcat AJP \u201cGhostcat\u201d). The Vulhub "
          "repository was cloned and the directory vulhub/tomcat/CVE-2020-1938 (Apache Tomcat 9.0.30) was used.")
code_block(doc, "$ git clone https://github.com/vulhub/vulhub.git\n$ cd vulhub/tomcat/CVE-2020-1938")

heading(doc, "7. Launching the Vulnerable Environment and Reproducing the Attack", 1)
para(doc, "The environment was started and both the HTTP (8080) and AJP (8009) ports were exposed:")
code_block(doc, "$ docker compose up -d\nNAMES  ...  PORTS\ncve-2020-1938-tomcat-1  0.0.0.0:8009->8009/tcp, 0.0.0.0:8080->8080/tcp  Up")
para(doc, "The Ghostcat PoC (a crafted AJP forward request) was then used to read the WEB-INF/web.xml "
          "file, which must never be reachable from outside. The AJP port 8009 was confirmed reachable and "
          "the request succeeded:")
code_block(doc, "$ python poc.py 127.0.0.1 -p 8009 -f WEB-INF/web.xml\n"
               "Getting resource at ajp13://127.0.0.1:8009/asdf\n----------------------------\n"
               "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
               "<web-app xmlns=\"http://xmlns.jcp.org/xml/ns/javaee\" ...>\n"
               "  <display-name>Welcome to Tomcat</display-name>\n"
               "  ...\n</web-app>")
para(doc, "This proves arbitrary file read without any authentication. The PoC sends an AjpForwardRequest "
          "carrying the attributes javax.servlet.include.path_info = <file> and servlet_path = /, which "
          "Tomcat's JspServlet honours and uses to read the requested file.")

# ================= 8 root cause =================
heading(doc, "8. Analyzing the Root Cause of the Vulnerability", 1)
para(doc, "CVE-2020-1938 affects Apache Tomcat 6.x/7.x/8.x/9.x: because the AJP connector is exposed "
          "without authentication, an attacker can read or include arbitrary files inside the web "
          "application (e.g. source code, WEB-INF/web.xml) and, combined with a file-upload feature, "
          "potentially achieve remote code execution. The root cause is a configuration/input-handling "
          "weakness:")
bullet(doc, "The AJP/1.3 Connector is enabled by default on port 8009 (conf/server.xml).")
bullet(doc, "It is not bound to localhost (address not set) and has no secret / requiredSecret attribute — no authentication at all.")
bullet(doc, "Tomcat fully trusts the path, servlet and request attributes supplied by an AJP client, so a remote client can point JspServlet at any webapp file.")
para(doc, "The vulnerable declaration in conf/server.xml:")
code_block(doc, "<!-- Define an AJP 1.3 Connector on port 8009 -->\n<Connector port=\"8009\" protocol=\"AJP/1.3\" redirectPort=\"8443\" />")

# ================= 9 fix =================
heading(doc, "9. Developing and Applying Protection Measures", 1)
para(doc, "Because this deployment has no Apache front-end (mod_jk / mod_proxy_ajp), the AJP connector is "
          "not required. The fix therefore disables the AJP connector in conf/server.xml and stops exposing "
          "port 8009 in docker-compose.yml. The fixed files are provided in the cve-2020-1938-fix/ folder "
          "(server.xml, Dockerfile, docker-compose.yml, FIX-README.md).")
code_block(doc, "$ docker compose down\n$ docker compose up --build -d   # rebuild with hardened server.xml")
para(doc, "Alternative remediations are discussed in the README (bind AJP to localhost and require a secret, "
          "or upgrade Tomcat to a patched version ≥ 9.0.31).")

# ================= 10 verify =================
heading(doc, "10. Verifying the Fix", 1)
bullet(doc, "AJP port 8009 is no longer reachable: Test-NetConnection 127.0.0.1 -Port 8009 → False.")
bullet(doc, "Re-running the same PoC now fails: ConnectionRefusedError: [WinError 10061] (connection refused).")
bullet(doc, "Regression — the web application still works: GET http://127.0.0.1:8080/ returns HTTP 200 (Apache Tomcat welcome page).")
para(doc, "These results demonstrate that the attack no longer succeeds while the main functionality remains intact.")

# ================= 11 submissions =================
heading(doc, "11. Submissions (What Students Submit)", 1)
bullet(doc, "Public git repository with the project code: 【待补：GitHub 仓库链接】")
bullet(doc, "README.md in the repository (project & API description, security measures, scanner screenshots, CVE analysis and fix).")
bullet(doc, "Link to the last successful pipeline run: 【待补：Actions 运行链接】")
bullet(doc, "Folder with the fixes: cve-2020-1938-fix/ (server.xml, Dockerfile, docker-compose.yml).")

# ================= Control questions =================
heading(doc, "Appendix A. Control Questions", 1)
qa = [
 ("1. Why is password hashing with bcrypt preferable to using SHA-256?",
  "SHA-256 is a fast, general-purpose hash, so an attacker can brute-force or use rainbow tables on it "
  "quickly; bcrypt is deliberately slow (cost factor) and automatically salted, which makes offline "
  "cracking far more expensive and protects identical passwords from being stored identically."),
 ("2. Main difference between SAST and DAST?",
  "SAST analyses source code statically (without running the app), finding issues early but with false "
  "positives; DAST tests the running application dynamically via real requests, finding exploitable "
  "issues but only in paths the scanner exercises."),
 ("3. How does a JWT token work, and how is it verified?",
  "A JWT contains a header (algorithm), a payload (claims such as sub, exp, iss) and a signature. The "
  "server signs it with a secret (HS256) and, on protected requests, recomputes the signature and checks "
  "exp/iss; only a valid signature yields the payload."),
 ("4. Risks of not auditing third-party dependencies?",
  "Known vulnerabilities in dependencies can be exploited (e.g. RCE, XSS), and you may unknowingly "
  "ship vulnerable versions. Auditing (SCA) detects and tracks these."),
 ("5. Advantages of Docker/Vulhub over installing vulnerable software directly?",
  "Isolation (no harm to the host), easy setup/teardown, consistent versions, reproducible environments, "
  "and the ability to experiment safely with real CVE targets."),
 ("6. Difference between a vulnerability and an exploit; which were you reproducing?",
  "A vulnerability is a weakness/defect in a system; an exploit is code that uses that weakness to cause "
  "an effect. In this work I reproduced an exploit of CVE-2020-1938 (reading an arbitrary file via AJP)."),
 ("7. Why is regression testing critical after a patch?",
  "A fix can break functionality that was previously working; regression testing confirms the attack is "
  "blocked while the main features still work."),
 ("8. How does reproducing known CVEs help a security specialist?",
  "It builds practical knowledge of attack mechanics and indicators, supports detection and hardening, "
  "helps write accurate signatures/rules, and improves incident response and remediation skill."),
]
for q, a in qa:
    para(doc, q, HEI, 10.5, True, indent=True)
    para(doc, a)

# ================= References =================
heading(doc, "Appendix B. References", 1)
refs = [
 "[1] OWASP Foundation. OWASP Top 10 – 2021. https://owasp.org/www-project-top-ten/",
 "[2] Auth0. Introduction to JSON Web Tokens. https://jwt.io/introduction",
 "[3] Vulhub. Aapache Tomcat AJP Arbitrary File Read (CVE-2020-1938). https://github.com/vulhub/vulhub/tree/master/tomcat/CVE-2020-1938",
 "[4] NVD. CVE-2020-1938 Detail. https://nvd.nist.gov/vuln/detail/CVE-2020-1938",
 "[5] Apache Software Foundation. Announcement of the Ghostcat (AJP) fix. https://tomcat.apache.org/security-9.html",
 "[6] Chaitin Tech. Ghostcat. https://www.chaitin.cn/en/ghostcat",
]
for r in refs:
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.3
    pf.left_indent = Pt(24)
    pf.first_line_indent = Pt(-24)
    set_run(p.add_run(), r, EA, LAT, 10)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print("saved:", OUT)
