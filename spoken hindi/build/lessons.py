"""Compact lesson helper used by all course data files."""

def L(title, timelines, objective, say, warmup, teach, guided, free,
      mistakes, homework, materials="Board, a few pictures or real objects, and space for pair work.",
      polish="Invite two or three students to speak. Correct only the target sentences. End with a class repeat."):
    return {
        "title": title,
        "timelines": timelines,
        "objective": objective,
        "say": say,
        "materials": materials,
        "warmup": warmup,
        "teach": teach,
        "guided": guided,
        "free": free,
        "polish": polish,
        "mistakes": mistakes,
        "homework": homework,
    }
