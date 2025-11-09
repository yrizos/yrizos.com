---
title: "What We Learned Building AI Features for TalentLMS"
date: "2025-06-18T19:00:00+03:00"
draft: false
type: "talk"

event: "Mindstone Practical AI Meetup"
event_url: "https://www.meetup.com/mindstone-athens-practicalai-meetup/"
venue: "Epignosis HQ, Athens"

slides_pdf: "/slides/ai-features-talentlms-jun2025.pdf"
slides_dir: "speaking/ai-features-talentlms-jun2025"
slide_count: 13

image: "images/speaking/ai-features-talentlms-jun2025/slide-01.png"

description: |
  Practical lessons from building AI features at scale for TalentLMS, presented at the inaugural Mindstone Athens Practical AI Meetup. Why production AI is 95% engineering: architecture, team structure, prompts as code, and designing for failure from day one.
---

The first [Mindstone Athens Practical AI Meetup](https://www.meetup.com/mindstone-athens-practicalai-meetup/) at [Epignosis HQ](https://www.epignosishq.com/) drew a full house. It was the opening event of the Athens chapter of the Global Mindstone Practical AI community, and the energy in the room matched that sense of beginning.

My talk focused on the gap between getting an LLM to produce decent output and delivering something that can serve 25 million users. The distance between those two points is filled with the kind of engineering problems that don’t show up in demos. APIs fail at random, costs can spiral over a weekend, and teams need systems they can maintain without losing their minds.

LLMs behave like no other dependency. They are slow, inconsistent, and expensive to call. They can return different answers to the same question and undermine assumptions that most software architectures rely on. Building with them means rethinking reliability, cost control, and maintainability from the ground up.

We treat that unpredictability as normal. Product teams never interact with LLMs directly. Prompts are versioned and tested like any other code. Failure handling comes first, not last. The boring parts matter most because they keep the system steady when everything else shifts.

I walked through examples from what we’ve shipped so far: authoring tools that help create learning content, systems that translate courses, and engines that map skills. Each depends on LLMs but none rely on them to behave perfectly.

The point I wanted to leave with the audience was that building AI products for real users is an engineering problem, not a prompt-crafting contest. Stability and clarity in the system design decide whether the clever parts survive contact with scale.
