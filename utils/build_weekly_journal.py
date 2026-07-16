"""Build a 12-page weekly reflective journal from the UIU template.

One journal page per week (Week 1..12), Date left blank. Each week is a short
description followed by a few bullet points, in plain human language.
Output: docx -> PDF (12 pages).
"""
import copy
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

TEMPLATE = "JOURNAL ENTRY Your ID.docx"
OUT_DOCX = "Weekly_Journal_12_Weeks.docx"
ENTRY_PT = 12  # body text size in points

# Student info for the header grid (Date is left empty on purpose).
STUDENT_NAME = "Ikramul Hasan Moral"
STUDENT_ID = "0112230489"
STUDENT_GROUP = "261-025"
STUDENT_SEC = "D"

# Each week: a short lead line, then bullet points.
# Weeks 5-11 follow weekly_reports (1).pdf; weeks 1-4 and 12 cover the lead-in
# and the defense at the same level of detail.
ENTRIES = {
    1: ("We started the project this week and set our direction.", [
        "Formed our team and met the supervisor for the first time",
        "Talked over a few possible ideas with him",
        "Chose a topic that uses neural networks to model a chaotic system",
        "Got a clear direction and a list of things to read",
    ]),
    2: ("We spent the week building our background on the topic.", [
        "Read papers linked to our project",
        "Worked out the main problem and the maths behind the chaotic system",
        "Looked at how others handled similar work",
        "Settled on our research question and wrote down the objectives",
    ]),
    3: ("We began writing the first chapter.", [
        "Drafted Chapter 1, the Introduction",
        "Wrote the problem statement, the motivation, and the objectives",
        "Added the scope of the work",
        "Shared the draft in the team and made small fixes",
    ]),
    4: ("We refined the introduction and planned the rest of the work.", [
        "Got the supervisor's feedback on Chapter 1",
        "Corrected the parts he pointed out",
        "Made the introduction easier to follow",
        "Planned the next chapters and split the work among the team",
    ]),
    5: ("We started two chapters at once on our teacher's advice.", [
        "Began Chapter 2 (Background and Literature Review)",
        "Began Chapter 5 (Standards and Design Constraints)",
        "Divided the work between team members",
        "Finished about 80% of both chapters by the end of the week",
    ]),
    6: ("We acted on the teacher's feedback and finished both chapters.", [
        "Fixed the parts he mentioned in Chapter 2 and Chapter 5",
        "Drew the diagrams needed for the documentation",
        "Completed both chapters by the end of the week",
    ]),
    7: ("We checked our progress with the supervisor and presented in class.", [
        "Met the supervisor to review our overall progress",
        "Made a few changes based on his feedback",
        "Prepared the slides for the class presentation",
        "Presented our work without any trouble",
    ]),
    8: ("We worked on the project design this week.", [
        "Talked with the supervisor about how to approach the design",
        "Shared our ideas and plans with him",
        "Wrote Chapter 3 (Project Design) following his instructions",
        "Finished the chapter by the end of the week",
    ]),
    9: ("Our teacher reviewed everything and we applied his changes.", [
        "Got feedback on diagram formatting, task allocation, and the Gantt chart",
        "Applied all of his suggestions",
        "Completed those parts during the week",
        "Started the Conclusion chapter",
    ]),
    10: ("We finalised the full paper this week.", [
        "Showed the full paper to the course teacher",
        "Got his final review",
        "Made the changes he asked for",
        "Had the complete FYDP paper ready to submit",
    ]),
    11: ("We finished the syllabus and got ready for the defense.", [
        "Prepared the final presentation for the last class",
        "Studied the whole project again for the defense",
        "Revised the main background topics",
        "Got ready to answer the panel's questions",
    ]),
    12: ("We gave our final defense and finished FYDP 1.", [
        "Presented the project to the panel",
        "Answered the questions they asked",
        "Noted their remarks and made the last small corrections",
        "Submitted the final version of the paper",
    ]),
}


def _run(text, preserve=False):
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rf = OxmlElement('w:rFonts')
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
        rf.set(qn(a), 'Times New Roman')
    rPr.append(rf)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), str(ENTRY_PT * 2)); rPr.append(sz)
    r.append(rPr)
    t = OxmlElement('w:t')
    if preserve:
        t.set(qn('xml:space'), 'preserve')
    t.text = text
    r.append(t)
    return r


def make_paragraph(text, bullet=False):
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    if bullet:
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'), '360')
        ind.set(qn('w:hanging'), '360')
        pPr.append(ind)
        spc = OxmlElement('w:spacing'); spc.set(qn('w:after'), '60'); pPr.append(spc)
        p.append(pPr)
        p.append(_run('•  ' + text, preserve=True))
    else:
        jc = OxmlElement('w:jc'); jc.set(qn('w:val'), 'both'); pPr.append(jc)
        spc = OxmlElement('w:spacing'); spc.set(qn('w:after'), '120'); pPr.append(spc)
        p.append(pPr)
        p.append(_run(text))
    return p


def _label_run(text):
    """A bold Times New Roman 12pt run matching the form's field labels."""
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rf = OxmlElement('w:rFonts')
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
        rf.set(qn(a), 'Times New Roman')
    rPr.append(rf)
    rPr.append(OxmlElement('w:b'))
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '24'); rPr.append(sz)
    r.append(rPr)
    t = OxmlElement('w:t'); t.set(qn('xml:space'), 'preserve'); t.text = text
    r.append(t)
    return r


def fill_info(tbl, n):
    """Fill Name / ID / Group / Sec / Week. Date is left empty."""
    for t in tbl.iter(qn('w:t')):
        s = (t.text or '').strip()
        if s.startswith('Name'):
            t.text = 'Name: ' + STUDENT_NAME
        elif s.startswith('Sec'):
            t.text = 'Sec: ' + STUDENT_SEC
        elif s.startswith('Group'):
            t.text = 'Group: ' + STUDENT_GROUP
        elif s.startswith('Week'):
            t.text = f'Week: {n}'
        # 'Date:' is intentionally left blank
    # ID goes in the blank middle cell of the first row
    r0_tcs = tbl.findall(qn('w:tr'))[0].findall(qn('w:tc'))
    id_tc = r0_tcs[1]
    p = id_tc.find(qn('w:p'))
    if p is None:
        p = OxmlElement('w:p')
        id_tc.append(p)
    p.append(_label_run('ID: ' + STUDENT_ID))


def fill_block(elems, n):
    tbls = [e for e in elems if e.tag == qn('w:tbl')]
    fill_info(tbls[0], n)
    desc, bullets = ENTRIES[n]
    content_tc = tbls[1].findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    # clear existing paragraphs in the content cell (keep cell properties)
    for p in content_tc.findall(qn('w:p')):
        content_tc.remove(p)
    content_tc.append(make_paragraph(desc))
    for b in bullets:
        content_tc.append(make_paragraph(b, bullet=True))
    # a cell must end with a paragraph; the last bullet already is one


def page_break_para():
    p = OxmlElement('w:p')
    r = OxmlElement('w:r')
    br = OxmlElement('w:br'); br.set(qn('w:type'), 'page')
    r.append(br); p.append(r)
    return p


def main():
    doc = Document(TEMPLATE)
    body = doc.element.body
    sectPr = body.find(qn('w:sectPr'))

    block = [c for c in list(body) if c is not sectPr]
    for c in block:
        body.remove(c)

    for n in range(1, 13):
        if n > 1:
            sectPr.addprevious(page_break_para())
        new_block = [copy.deepcopy(c) for c in block]
        fill_block(new_block, n)
        for e in new_block:
            sectPr.addprevious(e)

    doc.save(OUT_DOCX)
    print("Saved", OUT_DOCX)


if __name__ == "__main__":
    main()
