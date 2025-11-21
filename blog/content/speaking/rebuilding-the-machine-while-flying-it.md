---
title: "How We Rebuilt the Machine While Flying It"
date: "2025-11-21T10:00:00+02:00"
draft: false
type: "talk"

event: "Open Conf 2025"
event_url: "https://open-conf.gr/"
venue: "Dais Events center, Athens"

slides_pdf: "/slides/how-we-rebuilt-the-machine-while-flying-it.pdf"
slides_dir: "speaking/how-we-rebuilt-the-machine-while-flying-it"
slide_count: 15

image: "images/speaking/how-we-rebuilt-the-machine-while-flying-it/slide-01.png"

description: |
  How do you modernize a platform when 20 million people depend on it not breaking? Five years of rebuilding TalentLMS's interface and infrastructure while the product kept growing. The stories behind treating every small dysfunction as something fixable, and why multi-year projects fail when teams stop asking "How do we fix this?"
tags:
  [
    "talk",
    "software-engineering",
    "engineering-leadership",
    "legacy",
    "culture",
  ]
---

I spoke at [Open Conf 2025](https://open-conf.gr/) about a problem that doesn't fit neatly into sprint planning: how do you modernize a platform when 20 million people depend on it not breaking?

My talk traced five years of work rebuilding [TalentLMS](https://www.talentlms.com/)'s interface and infrastructure while the product kept growing. The pandemic had accelerated user growth exponentially, and we were left with a decade-old codebase that had become a bottleneck for everything we wanted to ship.

The early stories revealed deeper problems than outdated UI. Knowledge lived in silos. A Docker setup existed in three places, shared with nobody. Test environments called "bleedings" couldn't actually bleed without someone getting an earful. When our first beta release drew harsh feedback, we panicked and threw Brooks's Law out the window, adding everyone to a project that was already struggling.

What made the difference wasn't heroic rescues or grand architectural visions. It was treating every small dysfunction as something fixable. The contraband database dumps became a shared local environment. The fragile bleedings became isolated sandboxes for safe experimentation. The testing vacuum became 20K automated tests. Time to first PR dropped from a month to a week.

We invested in automation across the board: linting, static analysis, CI/CD. We invested in people through training and mentorship programs. We introduced event-driven architecture and leveled up our documentation with ADRs and PRDs. All of this happened while continuing to serve those 20 million users.

The release itself was rough. Three years of work met with resistance to change and the inevitable issues that come with big releases. But once we started shipping new features on top of the modernized foundation, the mood shifted. A year later, customers were consistently positive about both the UX upgrade and the pace of new capabilities. A team that struggled for three years to deliver the UI redesign shipped over 50+ new features in the year that followed.

The point I wanted to leave with the audience was that multi-year projects don't fail from technical complexity. They fail when teams stop asking "How do we fix this?" about the small problems. Every silly story, every frustrating blocker, every moment of friction is a signal. The teams that survive these projects are the ones that treat those signals as things they can actually change.

We're now months away from our next multi-year adventure. We haven't solved every problem, but we've proven we don't hide from them. That's the foundation that matters most.
