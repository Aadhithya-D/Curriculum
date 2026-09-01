#!/usr/bin/env python3
"""Build the Urban Spoken English HTML site and print document."""

from __future__ import annotations

import html
import json
from pathlib import Path

from data_adults import (
    ADULTS_ABSOLUTE,
    ADULTS_EVERYDAY,
    ADULTS_FLUENCY_WORK,
    ADULTS_INTERVIEW,
    SENIOR_NOTE,
)
from data_children import CHILDREN_BEGINNER, CHILDREN_ELEMENTARY
from data_teens import TEENS_BEGINNER, TEENS_INTERMEDIATE, TEENS_UPPER
from data_ya import YA_BEGINNER, YA_FLUENCY, YA_INTERVIEW

ROOT = Path(__file__).resolve().parents[1]
COURSES = ROOT / "courses"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def number_lessons(raw: list[dict]) -> list[dict]:
    out = []
    for i, lesson in enumerate(raw, 1):
        item = dict(lesson)
        item["n"] = i
        item["id"] = f"l{i:02d}"
        out.append(item)
    return out


COURSES_META = [
    {
        "id": "children-beginner",
        "file": "children-beginner.html",
        "age": "child",
        "age_label": "Children 6–10",
        "level": "Absolute Beginner / Beginner",
        "title": "Children · First words that work",
        "blurb": "Names, family, tiffin, park, shop, and school. Games first. Full sentences soon.",
        "hours": "24–72",
        "lessons": number_lessons(CHILDREN_BEGINNER),
        "who": "Urban children aged 6–10 who are new to speaking English, including those who can read a little from school.",
        "done": "The child can greet, name family and school things, buy one item, ask for help, and give a one-minute ‘All about me’.",
        "place": "Place here if the child answers with one word or silence, and needs pictures and movement.",
        "note": "Keep lessons physical. Sit on the floor if that helps. Never make a child perform before they have rehearsed with a partner.",
        "tests": [
            ("Start", "Name, hello, point to three colours or objects."),
            ("Mid (after lesson 24)", "Name, age, family, one polite request, favourite food."),
            ("End", "One-minute talk plus shop or help role-play."),
        ],
    },
    {
        "id": "children-elementary",
        "file": "children-elementary.html",
        "age": "child",
        "age_label": "Children 6–10",
        "level": "Elementary",
        "title": "Children · Longer talk in the city",
        "blurb": "School day, last weekend, doctor, metro, and a two-minute ‘my city life’ talk.",
        "hours": "24–72",
        "lessons": number_lessons(CHILDREN_ELEMENTARY),
        "who": "Children who can already say name, age, and a few likes, and can follow a simple English class.",
        "done": "The child can tell a school day, a weekend, give directions, visit a doctor or canteen in role-play, and speak for two minutes.",
        "place": "Place here if they use short sentences already and can do the Children’s Beginner final test.",
        "note": "Start teaching past time (went, played) and because. Still use pictures. Still play.",
        "tests": [
            ("Start", "40-second ‘me’, describe a picture, last Sunday in two sentences."),
            ("Mid", "School day, directions, last weekend."),
            ("End", "Two-minute city-life talk plus shop or doctor."),
        ],
    },
    {
        "id": "teens-beginner",
        "file": "teens-beginner.html",
        "age": "teen",
        "age_label": "Teens 11–17",
        "level": "Beginner",
        "title": "Teens · School life, spoken",
        "blurb": "Class, tiffin, phone, commute, and a two-minute ordinary day — without baby talk.",
        "hours": "24–72",
        "lessons": number_lessons(TEENS_BEGINNER),
        "who": "Urban teens who understand some English from school but speak very little, or who come from a low-speaking classroom.",
        "done": "The teen can introduce themselves, talk school and weekend, make a phone plan, and repair a rude line.",
        "place": "Place here if they freeze after one word, or if their only English is textbook reading.",
        "note": "Respect their age. No animal songs. Use school, phone, and city. Ban Myself Ravi.",
        "tests": [
            ("Start", "Name, class, one like, how they come to school."),
            ("Mid (after test 1 lesson)", "Intro, weekend, shop or phone."),
            ("End", "Two-minute day-in-my-life plus polite repair."),
        ],
    },
    {
        "id": "teens-intermediate",
        "file": "teens-intermediate.html",
        "age": "teen",
        "age_label": "Teens 11–17",
        "level": "Intermediate fluency",
        "title": "Teens · I understand, but I freeze",
        "blurb": "The largest Indian teen group. Opinions, stories, GD manners, photo talk, less freeze.",
        "hours": "24–72",
        "lessons": number_lessons(TEENS_INTERMEDIATE),
        "who": "Teens who follow English class, films with some help, and written work — but go quiet when they must speak.",
        "done": "They can speak for two minutes, join a kind GD, describe a photo, and disagree without a fight.",
        "place": "Place here if they can do the Teens Beginner test but still plan every word in their head.",
        "note": "Do not reteach is/am/are unless it blocks meaning. Push talking time. Correct after the turn, not during it.",
        "tests": [
            ("Start", "60-second familiar topic. Note the freeze points."),
            ("Mid", "Intro, photo, opinion, tiny GD."),
            ("End", "Speech or GD plus photo. Score fluency and interaction."),
        ],
    },
    {
        "id": "teens-upper",
        "file": "teens-upper.html",
        "age": "teen",
        "age_label": "Teens 11–17",
        "level": "Upper Intermediate",
        "title": "Teens · Longer speech, exam oral, debate",
        "blurb": "Extempore, ASL-style long turns, rebuttal, and a crash path for orals.",
        "hours": "20–72",
        "lessons": number_lessons(TEENS_UPPER),
        "who": "Teens who can already talk about school life and now need structure for exams, debates, and public speaking.",
        "done": "They can do a 3-minute long turn, a pair discussion, a short debate, and handle follow-up questions.",
        "place": "Place here after Intermediate, or if they already argue in English but ramble.",
        "note": "A 2–3 week crash uses only lessons tagged crash. Still rehearse standing.",
        "tests": [
            ("Start", "2-minute opinion with an example and the other side."),
            ("Mid", "ASL-style long turn plus follow-up."),
            ("End", "Speech or debate plus GD."),
        ],
    },
    {
        "id": "ya-beginner",
        "file": "ya-beginner.html",
        "age": "ya",
        "age_label": "Young adults 18–25",
        "level": "Beginner",
        "title": "Young adults · Campus English from the ground",
        "blurb": "College, commute, money, hostel, and a human talk about this year.",
        "hours": "24–72",
        "lessons": number_lessons(YA_BEGINNER),
        "who": "Urban young adults starting spoken English seriously — college, first job, or a gap year.",
        "done": "They can move around campus in English, split a bill, call a classmate, and give a two-minute year talk.",
        "place": "Place here if they still need full-sentence building on adult topics.",
        "note": "Keep the register adult. Money and stress belong in this course. No children’s games unless they ask.",
        "tests": [
            ("Start", "Intro, course or job, area of the city."),
            ("Mid", "Campus help, commute, weekend, opinion."),
            ("End", "Showcase plus problem role-play."),
        ],
    },
    {
        "id": "ya-fluency",
        "file": "ya-fluency.html",
        "age": "ya",
        "age_label": "Young adults 18–25",
        "level": "Intermediate fluency",
        "title": "Young adults · Speak what you already know",
        "blurb": "Kill the freeze. STAR stories, GDs, aunt-test explanations, meeting one-liners.",
        "hours": "24–72",
        "lessons": number_lessons(YA_FLUENCY),
        "who": "Young adults who wrote English for years and still translate every sentence before they speak.",
        "done": "They can talk for three minutes, tell a STAR story, join a GD, and explain their subject in plain English.",
        "place": "The default course for ‘I know English but I can’t speak’ at this age.",
        "note": "No mid-sentence correction. Simpler English is a win. Then send them to Interview if they have placements.",
        "tests": [
            ("Start", "90 seconds on a known topic. Time the first pause."),
            ("Mid", "Intro, STAR, opinion, GD."),
            ("End", "Showcase plus a hard question."),
        ],
    },
    {
        "id": "ya-interview",
        "file": "ya-interview.html",
        "age": "ya",
        "age_label": "Young adults 18–25",
        "level": "Interview speaking",
        "title": "Young adults · Interview and first-job speech",
        "blurb": "Tell me about yourself, STAR, why us, GD, and mocks. Crash option included.",
        "hours": "20–48",
        "lessons": number_lessons(YA_INTERVIEW),
        "who": "Final-year students and first-job hunters who can already hold a conversation.",
        "done": "They can do a 12-minute mock with intro, proof, one STAR, and two questions for HR.",
        "place": "Not for true beginners. Use after Fluency, or if they already speak at Intermediate.",
        "note": "Crash = lessons tagged crash, daily if possible. Never guarantee a job. Guarantee clearer speech.",
        "tests": [
            ("Start", "Current intro, timed. Usually too long or too empty."),
            ("Mid", "Full mock 1."),
            ("End", "Harder mock 2 plus public intro."),
        ],
    },
    {
        "id": "adults-absolute",
        "file": "adults-absolute.html",
        "age": "adult",
        "age_label": "Adults 26–50 · also Seniors 50+",
        "level": "Absolute Beginner",
        "title": "Adults · Start from zero, with dignity",
        "blurb": "Name, shop, doctor, phone, building, school gate. Seniors use the same book, slower.",
        "hours": "24–72",
        "lessons": number_lessons(ADULTS_ABSOLUTE),
        "who": "Urban adults who have little or no spoken English. Homemakers, workers, and seniors are all welcome.",
        "done": "They can greet, shop, ask for help, tell a simple day, and speak for one minute about their life.",
        "place": "Place here if they need the local language for almost every instruction.",
        "note": SENIOR_NOTE,
        "tests": [
            ("Start", "Name and hello only. Smile."),
            ("Mid", "Home, shop, help, Sunday."),
            ("End", "Showcase plus shop or help."),
        ],
    },
    {
        "id": "adults-everyday",
        "file": "adults-everyday.html",
        "age": "adult",
        "age_label": "Adults 26–50 · also Seniors 50+",
        "level": "Elementary / Everyday",
        "title": "Adults · Everyday city English",
        "blurb": "PTA, doctor details, appointments, society, travel, a week in the city.",
        "hours": "24–72",
        "lessons": number_lessons(ADULTS_EVERYDAY),
        "who": "Adults who can already do the Absolute Beginner test, or who have school English but only use it in shops with fear.",
        "done": "They can handle PTA, a clinic story, a complaint, a neighbour chat, and a two-minute week talk.",
        "place": "Place here after Absolute, or if they survive a shop but freeze at school or the doctor.",
        "note": SENIOR_NOTE + " Seniors may skip workplace-like society fights if it drains them; keep guests, park, and doctor.",
        "tests": [
            ("Start", "Neighbour hello, shop, one home sentence."),
            ("Mid", "PTA or doctor, appointment call, complaint."),
            ("End", "Week-in-my-city plus one role-play."),
        ],
    },
    {
        "id": "adults-fluency-workplace",
        "file": "adults-fluency-workplace.html",
        "age": "adult",
        "age_label": "Adults 26–50",
        "level": "Intermediate fluency + workplace",
        "title": "Adults · Fluency and the meeting room",
        "blurb": "Stand-ups, disagreement, client calls, briefings. Return-to-work lives are included.",
        "hours": "24–72",
        "lessons": number_lessons(ADULTS_FLUENCY_WORK),
        "who": "Working adults and return-to-work adults who understand office English but stay quiet in rooms.",
        "done": "They can give a 30-second update, disagree politely, run a short meeting point, and brief a senior for four minutes.",
        "place": "Place here if they can do Everyday English but go silent in meetings — or if they are returning to work.",
        "note": "Replace ‘do the needful’ and ‘kindly revert’ with clear asks. Homemakers returning to work use home operations as proof.",
        "tests": [
            ("Start", "Job talk and one meeting line."),
            ("Mid", "Meeting mock."),
            ("End", "Briefing plus hard question."),
        ],
    },
    {
        "id": "adults-interview",
        "file": "adults-interview.html",
        "age": "adult",
        "age_label": "Adults 26–50",
        "level": "Interview speaking",
        "title": "Adults · Interview speech with dignity",
        "blurb": "Career chapters, gaps, return-to-work, salary, mocks. Crash option included.",
        "hours": "20–48",
        "lessons": number_lessons(ADULTS_INTERVIEW),
        "who": "Adults changing jobs, returning after a break, or facing HR after years of silent competence.",
        "done": "They can tell their life in 90 seconds, prove two strengths, explain a gap, and sit a 15-minute mock.",
        "place": "Not for Absolute Beginners. They must already handle Everyday or Fluency talk.",
        "note": "Delete shame phrases: just a housewife, only a... Never guarantee a job.",
        "tests": [
            ("Start", "Current intro. Time it. Listen for shame words."),
            ("Mid", "Full mock 1."),
            ("End", "Harder mock 2 plus public intro."),
        ],
    },
]


NAV = [
    ("index.html", "Home"),
    ("teacher.html", "How to teach"),
    ("placement.html", "Place a student"),
    ("timelines.html", "Timelines"),
]


def sidebar(active: str = "") -> str:
    blocks = ['<nav class="sidebar" id="sidebar">']
    blocks.append('<h2>Start here</h2>')
    for href, label in NAV:
        cls = " active" if href == active else ""
        blocks.append(f'<a class="{cls.strip()}" href="{href if href.startswith("http") or not active.startswith("courses") else "../"+href}">{esc(label)}</a>')
    # Fix relative paths: if we're in courses/, prefix ../
    prefix = "../" if active.startswith("courses/") or active.endswith(".html") and active not in {n[0] for n in NAV} and active != "print.html" else ""
    # Simpler: pass prefix
    return ""  # replaced by sidebar_html


def sidebar_html(prefix: str, active_file: str) -> str:
    def link(href: str, label: str, extra="") -> str:
        active_name = active_file.replace("courses/", "")
        href_name = href.replace("courses/", "")
        cls = "active" if href_name == active_name else ""
        return f'<a class="{cls} {extra}" href="{prefix}{href}">{esc(label)}</a>'

    parts = [
        '<nav class="sidebar" id="sidebar">',
        '<div class="sidebar-head"><strong>Menu</strong><button class="icon-btn" id="sidebar-close" type="button" aria-label="Close menu">✕</button></div>',
        "<h2>Start here</h2>",
        link("index.html", "Home"),
        link("teacher.html", "How to teach"),
        link("placement.html", "Place a student"),
        link("timelines.html", "Timelines"),
        "<h2>Courses</h2>",
    ]
    last_age = None
    age_names = {"child": "Children", "teen": "Teens", "ya": "Young adults", "adult": "Adults"}
    for c in COURSES_META:
        if c["age"] != last_age:
            parts.append(f'<div class="age {c["age"]}">{age_names[c["age"]]}</div>')
            last_age = c["age"]
        parts.append(link("courses/" + c["file"], c["title"].split("·")[-1].strip(), c["age"]))
    parts.append("</nav>")
    return "\n".join(parts)


def search_index() -> list[dict]:
    items = [
        {"title": "Home", "group": "Guide", "href": "index.html", "hay": "curriculum urban spoken english courses"},
        {"title": "How to teach", "group": "Guide", "href": "teacher.html", "hay": "class formula error correction homework whatsapp"},
        {"title": "Place a student", "group": "Guide", "href": "placement.html", "hay": "placement test level age"},
        {"title": "Timelines", "group": "Guide", "href": "timelines.html", "hay": "6 week 3 month 6 month crash"},
    ]
    for c in COURSES_META:
        items.append({
            "title": c["title"],
            "group": f'{c["age_label"]} · {c["level"]}',
            "href": "courses/" + c["file"],
            "hay": c["blurb"] + " " + c["who"],
        })
        for lesson in c["lessons"]:
            items.append({
                "title": f'L{lesson["n"]:02d} {lesson["title"]}',
                "group": c["title"],
                "href": f'courses/{c["file"]}#{lesson["id"]}',
                "hay": lesson["objective"] + " " + " ".join(lesson["say"]),
            })
    return items


def shell(title: str, prefix: str, active: str, body: str, extra_head: str = "") -> str:
    idx = search_index()
    # Make search hrefs work from courses/
    if prefix == "../":
        for item in idx:
            if not item["href"].startswith("../") and not item["href"].startswith("http"):
                item = item  # we fix in JS by using paths relative to site root via data
    # Better: store two hrefs
    idx_js = []
    for item in search_index():
        href = item["href"]
        if prefix == "../":
            if href.startswith("courses/"):
                href = href[len("courses/"):]
            else:
                href = "../" + href
        idx_js.append({**item, "href": href})

    search_box = """
    <div class="search-wrap desktop-search">
      <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3-3"/></svg>
      <input id="site-search" type="search" placeholder="Search courses and lessons" autocomplete="off">
      <div class="search-results" id="search-results"></div>
    </div>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#0b5459">
  <title>{esc(title)} · Urban Spoken English</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,640&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}css/app.css">
  {extra_head}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="app-header">
    <div class="header-left">
      <button class="icon-btn menu-btn" id="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false">☰</button>
      <a class="brand" href="{prefix}index.html">
        <div class="mark">SE</div>
        <div class="brand-text">
          <strong>Urban Spoken English</strong>
          <span>Teach-from-the-page curriculum</span>
        </div>
      </a>
    </div>
    {search_box}
    <div class="header-actions">
      <button class="icon-btn search-toggle" id="search-toggle" type="button" aria-label="Search">⌕</button>
      <button class="btn print-btn" id="print-page" type="button">Print</button>
      <a class="btn primary" href="{prefix}Spoken-English-Curriculum.pdf">PDF</a>
    </div>
    <div class="search-wrap mobile-search">
      <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3-3"/></svg>
      <input id="site-search-mobile" type="search" placeholder="Search courses and lessons" autocomplete="off">
      <div class="search-results" id="search-results-mobile"></div>
    </div>
  </header>
  <div class="scrim" id="scrim"></div>
  <div class="layout">
    {sidebar_html(prefix, active)}
    <main class="main" id="main">
      {body.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")}
      <p class="footer">Urban Spoken English · For a teacher in an Indian city classroom · Open a lesson and teach today.</p>
    </main>
  </div>
  <script>window.SEARCH_INDEX = {json.dumps(idx_js, ensure_ascii=False)};</script>
  <script src="{prefix}js/app.js"></script>
</body>
</html>
"""


def chips(course: dict) -> str:
    return (
        f'<div class="meta-row">'
        f'<span class="chip">{esc(course["age_label"])}</span>'
        f'<span class="chip">{esc(course["level"])}</span>'
        f'<span class="chip">{len(course["lessons"])} lessons</span>'
        f'<span class="chip">{esc(course["hours"])} hours depending on timeline</span>'
        f'</div>'
    )


def calendar_rows(course: dict) -> str:
    lessons = course["lessons"]
    def names(tag: str) -> str:
        picked = [f'{l["n"]:02d} {l["title"]}' for l in lessons if tag in l["timelines"].split()]
        return "; ".join(picked) if picked else "—"

    crash = [l for l in lessons if "crash" in l["timelines"].split()]
    crash_row = ""
    if crash:
        crash_row = f"<tr><th>2–3 week crash</th><td>About 20 hours, daily if you can</td><td>{esc(names('crash'))}</td></tr>"

    n6w = sum(1 for l in lessons if "6w" in l["timelines"].split())
    n3m = sum(1 for l in lessons if "3m" in l["timelines"].split())
    n6m = len(lessons)
    return f"""
    <table>
      <tr><th>Timeline</th><th>How to run it</th><th>Lessons (in order)</th></tr>
      <tr><th>6-week starter</th><td>Two 60-minute classes a week · about 12 classes · {n6w} lessons tagged 6-week</td><td>{esc(names("6w"))}</td></tr>
      <tr><th>3-month core</th><td>Two 60-minute classes a week · about 24 classes · {n3m} lessons tagged 3-month</td><td>{esc(names("3m"))}</td></tr>
      <tr><th>6-month foundation</th><td>Two 60-minute classes a week · teach every lesson · {n6m} lessons</td><td>All lessons, 01 to {n6m:02d}</td></tr>
      {crash_row}
    </table>
    <p>If a week has a school exam or a wedding, skip a 6-month-only lesson, not a 6-week lesson. The 6-week set is the spine.</p>
    """


def lesson_html(course_id: str, lesson: dict) -> str:
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in lesson["timelines"].split())
    chunks = "".join(f'<span class="chunk">{esc(s)}</span>' for s in lesson["say"])
    mistakes = "".join(
        f'<div class="mistake"><span>Not this: {esc(a)}</span><span>Say this: {esc(b)}</span></div>'
        for a, b in lesson["mistakes"]
    )
    return f"""
    <article class="lesson" id="{lesson["id"]}" data-timelines="{esc(lesson["timelines"])}">
      <div class="lesson-head">
        <div class="lesson-num">{lesson["n"]:02d}</div>
        <div>
          <h3>{esc(lesson["title"])}</h3>
          <p>{esc(lesson["objective"])}</p>
          <div class="tags">{tags}</div>
        </div>
        <label class="taught"><input type="checkbox"> Taught</label>
      </div>
      <div class="lesson-body">
        <p><strong>Say this today</strong></p>
        <div class="chunks">{chunks}</div>
        <p><strong>Bring</strong> {esc(lesson["materials"])}</p>
        <dl class="flow">
          <dt>0–8 min</dt><dd><strong>Warm-up.</strong> {esc(lesson["warmup"])}</dd>
          <dt>8–18 min</dt><dd><strong>New language.</strong> {esc(lesson["teach"])}</dd>
          <dt>18–30 min</dt><dd><strong>Guided practice.</strong> {esc(lesson["guided"])}</dd>
          <dt>30–48 min</dt><dd><strong>Speak freely.</strong> {esc(lesson["free"])}</dd>
          <dt>48–55 min</dt><dd><strong>Polish.</strong> {esc(lesson["polish"])}</dd>
          <dt>55–60 min</dt><dd><strong>Homework.</strong> {esc(lesson["homework"])}</dd>
        </dl>
        <p><strong>Common slips</strong></p>
        <div class="mistakes">{mistakes}</div>
      </div>
    </article>
    """


def course_page(course: dict) -> str:
    tests = "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in course["tests"])
    lessons = "\n".join(lesson_html(course["id"], l) for l in course["lessons"])
    crash_btn = ""
    if any("crash" in l["timelines"].split() for l in course["lessons"]):
        crash_btn = '<button type="button" data-timeline="crash">2–3 week crash</button>'
    body = f"""
    <div class="hero">
      <div class="kicker">{esc(course["age_label"])} · {esc(course["level"])}</div>
      <h1>{esc(course["title"])}</h1>
      <p class="lede">{esc(course["blurb"])}</p>
      {chips(course)}
    </div>
    <section class="section">
      <h2>Who this is for</h2>
      <p>{esc(course["who"])}</p>
      <p><strong>They are done when:</strong> {esc(course["done"])}</p>
      <p><strong>Place a student here when:</strong> {esc(course["place"])}</p>
      <div class="callout teal">{esc(course["note"])}</div>
    </section>
    <section class="section">
      <h2>Speaking tests</h2>
      <table>{tests}</table>
    </section>
    <section class="section">
      <h2>Pick a timeline</h2>
      {calendar_rows(course)}
    </section>
    <section class="section">
      <h2>Lessons</h2>
      <p>Click a lesson to open the 60-minute plan. Tick <em>Taught</em> so you know where you stopped. The tick stays on this browser.</p>
      <div class="timeline-bar">
        <button type="button" data-timeline="6w">6-week view</button>
        <button type="button" data-timeline="3m">3-month view</button>
        <button type="button" data-timeline="6m">6-month view</button>
        {crash_btn}
        <button type="button" data-timeline="all">All lessons</button>
        <button type="button" class="btn" id="open-all">Open all</button>
        <button type="button" class="btn" id="close-all">Close all</button>
      </div>
      {lessons}
    </section>
    """
    return shell(course["title"], "../", "courses/" + course["file"], body)


def index_page() -> str:
    cards = []
    for c in COURSES_META:
        cards.append(
            f'''<a class="card" href="courses/{c["file"]}">
              <div class="bar {c["age"]}"></div>
              <div class="kicker">{esc(c["age_label"])}</div>
              <h3>{esc(c["title"])}</h3>
              <p>{esc(c["blurb"])}</p>
              <p style="margin-top:10px"><strong>{len(c["lessons"])} lessons</strong> · {esc(c["level"])}</p>
            </a>'''
        )
    body = f"""
    <div class="hero">
      <div class="kicker">A teacher’s book for an Indian city classroom</div>
      <h1>Urban Spoken English</h1>
      <p class="lede">Twelve teach-from-the-page courses for children, teens, young adults, and adults. Open a lesson. Teach it today. No extra workbook required.</p>
      <div class="meta-row">
        <span class="chip">Spoken only</span>
        <span class="chip">Urban India</span>
        <span class="chip">60-minute lessons</span>
        <span class="chip">6-week · 3-month · 6-month</span>
      </div>
    </div>
    <section class="section">
      <h2>How to use this</h2>
      <ol class="steps">
        <li>Read <a href="teacher.html">How to teach</a> once. It is the method for every course.</li>
        <li>Use <a href="placement.html">Place a student</a> for a 10-minute speaking check.</li>
        <li>Open the matching course. Choose a <a href="timelines.html">timeline</a>.</li>
        <li>Teach the next lesson. Tick <em>Taught</em>. Give the voice-note homework.</li>
      </ol>
      <div class="callout">This is not a grammar course and not an accent course. The aim is clear, confident speech for real city life: school, home, metro, shop, campus, office, and interviews.</div>
    </section>
    <section class="section">
      <h2>All twelve courses</h2>
      <div class="grid cards">{''.join(cards)}</div>
    </section>
    """
    return shell("Home", "", "index.html", body)


def teacher_page() -> str:
    body = """
    <div class="hero">
      <div class="kicker">Teacher handbook</div>
      <h1>How to teach this curriculum</h1>
      <p class="lede">One method for every age. The topics change. The shape of the hour does not.</p>
    </div>
    <article class="prose section">
      <h2>The 60-minute hour</h2>
      <p>Every lesson in this book uses the same clock. When you are tired, trust the clock.</p>
      <table>
        <tr><th>Time</th><th>Name</th><th>What you do</th></tr>
        <tr><td>0–8</td><td>Warm-up</td><td>Easy speech they already know. Get voices in the room.</td></tr>
        <tr><td>8–18</td><td>New language</td><td>A few sentences. You say them. They repeat. You show meaning with action or a picture.</td></tr>
        <tr><td>18–30</td><td>Guided practice</td><td>They use the new sentences with a partner, with support.</td></tr>
        <tr><td>30–48</td><td>Speak freely</td><td>A role-play, story, or opinion. This is the heart. Do not steal this time for grammar notes.</td></tr>
        <tr><td>48–55</td><td>Polish</td><td>Two or three students speak to the group. Fix only the target sentences.</td></tr>
        <tr><td>55–60</td><td>Homework</td><td>A voice note or a real-life line. Always spoken.</td></tr>
      </table>
      <h2>The talk-time rule</h2>
      <p>In a speaking class, students should speak more than the teacher after the first ten minutes. If you hear your own voice for a long stretch, stop and give a pair task.</p>
      <h2>When to correct</h2>
      <ul>
        <li><strong>During warm-up and free speaking:</strong> do not stop them for small grammar. Write a slip on a pad.</li>
        <li><strong>During guided practice:</strong> correct the target sentence of the day, kindly, then let them try again.</li>
        <li><strong>Never correct accent as if it were dirt.</strong> Correct only what blocks understanding: wrong word, missing word, a sound that changes the meaning.</li>
        <li><strong>Never mock a student.</strong> If the class laughs at a mistake, stop and protect the speaker.</li>
      </ul>
      <h2>Mother tongue in the room</h2>
      <p>This is a spoken English class, not an English-only police station. At Beginner, you may give instructions in the local language. The <em>output</em> you want is still English. From Intermediate up, stay in English and keep a rescue line: <em>Please say that again slowly.</em></p>
      <h2>Group size</h2>
      <p>Six to twelve students is ideal. If you have more, put them in pairs every day so each person still speaks. One-to-one works with the same lessons; stretch the free-speaking part.</p>
      <h2>WhatsApp homework</h2>
      <p>Create a class group or take private notes. Students send a short voice note after class. You reply with one glow (what was good) and one grow (one sentence to try again). Do not type a grammar essay.</p>
      <h2>Materials you actually need</h2>
      <ul>
        <li>A board or a large paper</li>
        <li>A phone for voice notes and a timer</li>
        <li>A few pictures (your phone gallery is enough: street, park, classroom, market)</li>
        <li>Chairs you can move for pair work</li>
      </ul>
      <h2>Children, teens, adults</h2>
      <ul>
        <li><strong>Children:</strong> change activity when energy drops. Movement is not a waste of time.</li>
        <li><strong>Teens:</strong> respect. No baby topics. Let “I don’t know yet” be a full answer about the future.</li>
        <li><strong>Adults:</strong> dignity. Never treat a beginner adult like a child. Homemaking and return-to-work are serious lives.</li>
        <li><strong>Seniors:</strong> slower, more repeat, sit if they wish, everyday topics only.</li>
      </ul>
      <h2>What we do not teach as a goal</h2>
      <p>British or American accent training, long grammar lectures, and essays. Clear Indian English is the model. If a student later needs IELTS, use the Upper Intermediate and Interview habits as a base, then add an exam book.</p>
    </article>
    """
    return shell("How to teach", "", "teacher.html", body)


def placement_page() -> str:
    body = """
    <div class="hero">
      <div class="kicker">10 minutes</div>
      <h1>Place a student</h1>
      <p class="lede">Do this as a conversation, not a written exam. Smile. If they freeze, that is information, not failure.</p>
    </div>
    <article class="prose section">
      <h2>Step 1 · Age first</h2>
      <table>
        <tr><th>Age</th><th>Open this family of courses</th></tr>
        <tr><td>6–10</td><td>Children Beginner or Children Elementary</td></tr>
        <tr><td>11–17</td><td>Teens Beginner, Intermediate, or Upper</td></tr>
        <tr><td>18–25</td><td>Young adults Beginner, Fluency, or Interview</td></tr>
        <tr><td>26–50</td><td>Adults Absolute, Everyday, Fluency + workplace, or Interview</td></tr>
        <tr><td>50+</td><td>Adults Absolute or Everyday, slower. Read the senior note on those pages.</td></tr>
      </table>
      <h2>Step 2 · Ask, then wait</h2>
      <p>Ask these in order. Stop when they cannot go on. You may use the local language to explain the task, not to give the answers.</p>
      <ol>
        <li>Hello. What’s your name? How are you?</li>
        <li>Tell me about your family or the people you live with.</li>
        <li>Tell me about a normal day. (School / college / work / home.)</li>
        <li>What did you do last Sunday?</li>
        <li>What are you going to do this weekend?</li>
        <li>Look at a photo of a street or a classroom. What can you see?</li>
        <li>What do you think: should school / offices start later? Why?</li>
        <li>For older students only: Tell me about a time you worked in a team. Or: Why do you want this job?</li>
      </ol>
      <h2>Step 3 · Match the speech you heard</h2>
      <table>
        <tr><th>What you heard</th><th>Course</th></tr>
        <tr><td>Silence, one word, or only the local language</td><td>Absolute Beginner / Beginner for that age</td></tr>
        <tr><td>Short sentences, present time only, heavy help</td><td>Beginner or Elementary / Everyday</td></tr>
        <tr><td>Understands you easily, answers are short, long pauses, they say “I know but I can’t speak”</td><td>Intermediate Fluency (teens, YA, or adults workplace)</td></tr>
        <tr><td>Can tell a story and give an opinion, wants polish, exams, or interviews</td><td>Upper Intermediate (teens) or Interview (YA / adults)</td></tr>
      </table>
      <div class="note">When in doubt, start one level easier. Confidence grows faster when the first week feels possible.</div>
      <h2>Step 4 · Purpose</h2>
      <ul>
        <li>School orals, debates, ASL → Teens Intermediate or Upper</li>
        <li>Campus life only → Young adults Beginner or Fluency</li>
        <li>Placements → Fluency first if they freeze, then Interview. Interview alone if they already talk.</li>
        <li>PTA, doctor, building, market → Adults Everyday</li>
        <li>Meetings and clients → Adults Fluency + workplace</li>
        <li>Return to work or a job change → Everyday or Fluency, then Adults Interview</li>
      </ul>
      <h2>A simple score pad</h2>
      <p>Mark 1–5 for each: <strong>Understand</strong> · <strong>Sentences</strong> · <strong>Keep going</strong> · <strong>Clear enough</strong>. You do not need a percentage. Date the pad. Repeat at mid and end.</p>
    </article>
    """
    return shell("Place a student", "", "placement.html", body)


def timelines_page() -> str:
    body = """
    <div class="hero">
      <div class="kicker">Hours matter more than calendar days</div>
      <h1>Course timelines</h1>
      <p class="lede">Every course has a 6-week, 3-month, and 6-month path. Interview and teen public-speaking courses also have a crash path.</p>
    </div>
    <article class="prose section">
      <table>
        <tr><th>Name</th><th>Hours</th><th>Typical calendar</th><th>Use it when</th></tr>
        <tr><td>6-week starter</td><td>24–30</td><td>2 classes a week, 60 minutes</td><td>A first batch, a term slice, or a trial</td></tr>
        <tr><td>3-month core</td><td>36–48</td><td>2 classes a week</td><td>The default full course for one level</td></tr>
        <tr><td>6-month foundation</td><td>60–72</td><td>2 classes a week, all lessons</td><td>Beginners, seniors, and anyone who needs repeat</td></tr>
        <tr><td>2–3 week crash</td><td>about 20</td><td>Daily or near-daily</td><td>Interview or exam oral only, Intermediate+</td></tr>
      </table>
      <div class="callout teal">A true beginner will not become fluent in 30 days. A grammar-rich student can become noticeably braver in six weeks if they speak every class.</div>
      <h2>How the tags work</h2>
      <p>Open any course and tap <strong>6-week view</strong>, <strong>3-month view</strong>, or <strong>6-month view</strong>. Lessons hide or show. Teach the visible lessons in number order.</p>
      <h2>If you miss a class</h2>
      <p>Do not cram two free-speaking lessons into one hour. Skip a 6-month-only lesson, or send that lesson as a voice-note challenge.</p>
      <h2>Class length</h2>
      <p>Plans are written for 60 minutes. If you have 45, cut the warm-up to 4 minutes and the free task to 12. If you have 90, repeat the free task with new partners and add a second voice recording.</p>
    </article>
    """
    return shell("Timelines", "", "timelines.html", body)


def print_document() -> str:
    """Single-file print/PDF document with internal links."""
    toc = ['<ol class="toc">']
    toc.append('<li><a href="#how">How to teach</a></li>')
    toc.append('<li><a href="#place">Place a student</a></li>')
    toc.append('<li><a href="#times">Timelines</a></li>')
    for c in COURSES_META:
        toc.append(f'<li><a href="#{c["id"]}">{esc(c["title"])}</a> — {len(c["lessons"])} lessons</li>')
    toc.append("</ol>")

    parts = [f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Urban Spoken English · Full curriculum</title>
<style>
  @page {{
    size: A4;
    margin: 16mm 14mm 18mm 14mm;
    @bottom-center {{
      content: "Urban Spoken English  ·  " counter(page);
      font-family: "Liberation Sans", sans-serif;
      font-size: 9pt;
      color: #4a453c;
    }}
  }}
  :root {{ --ink:#1c1914; --teal:#0b5459; --line:#d9d0be; --paper:#f7f1e4; }}
  body {{ margin:0; font-family: "Liberation Serif", "Times New Roman", Georgia, serif; color:var(--ink); line-height:1.45; font-size: 11pt; }}
  h1,h2,h3,h4 {{ font-weight:600; page-break-after: avoid; }}
  h1 {{ font-size: 28pt; line-height:1.15; }}
  h2 {{ font-size: 16pt; color: var(--teal); margin-top: 1.4em; }}
  h3 {{ font-size: 13pt; }}
  a {{ color: var(--teal); text-decoration: none; }}
  .cover {{ min-height: 220mm; padding: 22mm 10mm 16mm; background: #efe6d2; page-break-after: always; }}
  .cover .k {{ letter-spacing:.16em; text-transform:uppercase; color:#c2561a; font-size:11pt; font-family: "Liberation Sans", sans-serif; }}
  .cover p {{ font-size: 13pt; max-width: 36em; }}
  .page-break {{ page-break-before: always; }}
  .toc {{ font-size: 11.5pt; }}
  .toc li {{ margin: .35em 0; }}
  table {{ width:100%; border-collapse: collapse; font-size: 10.5pt; }}
  th,td {{ border:1px solid var(--line); padding: 6px 8px; vertical-align: top; text-align:left; }}
  th {{ background:#efe6d2; }}
  .lesson {{ border:1px solid var(--line); padding: 8px 10px; margin: 8px 0; page-break-inside: avoid; background:#fff; }}
  .lesson h3 {{ margin:0 0 4px; }}
  .say {{ font-style: italic; }}
  .muted {{ color:#4a453c; }}
  .chip {{ display:inline-block; border:1px solid #b7d9d9; background:#e7f3f3; color:var(--teal); padding:1px 7px; border-radius: 999px; font-size: 9pt; font-family: "Liberation Sans", sans-serif; }}
  header.run {{ font-family: "Liberation Sans", sans-serif; font-size: 9pt; color:#4a453c; border-bottom:1px solid var(--line); margin-bottom: 10px; padding-bottom:4px; }}
</style>
</head>
<body>
<section class="cover">
  <div class="k">Curriculum · Urban India · Spoken only</div>
  <h1>Urban Spoken English</h1>
  <p>A teach-from-the-page curriculum for children, teens, young adults, and adults. Written so a teacher can open a lesson and start the same day.</p>
  <p>Twelve courses. Three timelines on every course. Crash paths for interviews and exam orals. Clear Indian English. No accent theatre.</p>
  <p class="muted">Use the contents list to jump. In the PDF, those lines are links.</p>
</section>
<section class="page-break">
  <header class="run">Urban Spoken English · Contents</header>
  <h2>Contents</h2>
  {''.join(toc)}
</section>
"""]

    parts.append("""
<section class="page-break" id="how">
  <header class="run">Urban Spoken English · How to teach</header>
  <h2>How to teach</h2>
  <p>Every lesson is 60 minutes: warm-up 8, new language 10, guided practice 12, free speaking 18, polish 7, homework 5. After the first ten minutes, students should speak more than the teacher.</p>
  <p>Correct the day’s target sentences during guided practice. Do not stop a story for small grammar. Never mock a student. Never treat adult beginners like children. Mother-tongue instructions are allowed at Beginner; the speech you want back is English.</p>
  <p>Homework is a voice note or a real line in the city. Reply with one glow and one grow.</p>
</section>
<section class="page-break" id="place">
  <header class="run">Urban Spoken English · Placement</header>
  <h2>Place a student</h2>
  <p>Age first, then a 10-minute talk: name, family, a normal day, last Sunday, next weekend, a photo, an opinion. For older students, a team story or why this job.</p>
  <p>Silence or one word → Beginner. Short present sentences → Elementary / Everyday. Understands but freezes → Fluency. Can argue and wants polish → Upper or Interview. When in doubt, start easier.</p>
</section>
<section id="times">
  <h2>Timelines</h2>
  <p>6-week starter: two hours a week, only lessons tagged 6-week (the spine). 3-month core: lessons tagged 3-month. 6-month: every lesson. Crash: daily, only crash-tagged lessons, for Interview and teen orals.</p>
</section>
""")

    for c in COURSES_META:
        parts.append(f"""
<section class="page-break" id="{c["id"]}">
  <header class="run">Urban Spoken English · {esc(c["title"])}</header>
  <h2>{esc(c["title"])}</h2>
  <p><span class="chip">{esc(c["age_label"])}</span> <span class="chip">{esc(c["level"])}</span> <span class="chip">{len(c["lessons"])} lessons</span></p>
  <p>{esc(c["blurb"])}</p>
  <p><strong>Who:</strong> {esc(c["who"])}</p>
  <p><strong>Done when:</strong> {esc(c["done"])}</p>
  <p><strong>Place here when:</strong> {esc(c["place"])}</p>
  <p><strong>Teacher note:</strong> {esc(c["note"])}</p>
  <h3>Tests</h3>
  <table>
    {''.join(f'<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>' for a,b in c["tests"])}
  </table>
  <h3>Lessons</h3>
""")
        for l in c["lessons"]:
            tags = ", ".join(l["timelines"].split())
            say = " · ".join(l["say"])
            slips = "; ".join(f"{a} → {b}" for a, b in l["mistakes"])
            parts.append(f"""
  <article class="lesson">
    <h3>Lesson {l["n"]:02d} · {esc(l["title"])} <span class="chip">{esc(tags)}</span></h3>
    <p>{esc(l["objective"])}</p>
    <p class="say">Say this: {esc(say)}</p>
    <p><strong>Warm-up.</strong> {esc(l["warmup"])} <strong>Teach.</strong> {esc(l["teach"])} <strong>Guided.</strong> {esc(l["guided"])} <strong>Free.</strong> {esc(l["free"])} <strong>Polish.</strong> {esc(l["polish"])}</p>
    <p><strong>Homework.</strong> {esc(l["homework"])}</p>
    <p class="muted"><strong>Slips.</strong> {esc(slips)}</p>
  </article>
""")
        parts.append("</section>")

    parts.append("</body></html>")
    return "".join(parts)


def main() -> None:
    COURSES.mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(index_page(), encoding="utf-8")
    (ROOT / "teacher.html").write_text(teacher_page(), encoding="utf-8")
    (ROOT / "placement.html").write_text(placement_page(), encoding="utf-8")
    (ROOT / "timelines.html").write_text(timelines_page(), encoding="utf-8")
    for c in COURSES_META:
        (COURSES / c["file"]).write_text(course_page(c), encoding="utf-8")
    (ROOT / "print.html").write_text(print_document(), encoding="utf-8")
    counts = {c["id"]: len(c["lessons"]) for c in COURSES_META}
    print("Wrote site. Lesson counts:", counts)
    print("Total lessons:", sum(counts.values()))


if __name__ == "__main__":
    main()
