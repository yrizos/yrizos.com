---
title: "What We Learned Building AI Features For TalentLMS"
date: "2025-06-18T19:00:00+03:00"
draft: false
type: "talk"

event: "Mindstone Practical AI Meetup"
event_url: "https://www.meetup.com/mindstone-athens-practicalai-meetup/"
venue: "Epignosis HQ, Athens"

slides_pdf: "/slides/ai-features-talentlms-jun2025-yrizos.pdf"
slides_dir: "speaking/ai-features-talentlms-jun2025-yrizos"
slide_count: 13

image: "images/speaking/ai-features-talentlms-jun2025-yrizos/slide-01.png"

description: |
  Practical lessons from building AI features at scale for TalentLMS, presented at the inaugural Mindstone Athens Practical AI Meetup. Why production AI is 95% engineering: architecture, team structure, prompts as code, and designing for failure from day one.
---

Opening the first [Mindstone Athens Practical AI Meetup](https://www.meetup.com/mindstone-athens-practicalai-meetup/) at [Epignosis HQ](https://www.epignosishq.com/) was a blast. First talk of the night, first Athens event of the global [Mindstone](https://www.mindstone.com/) Practical AI community.

My talk was about building AI features that _actually work in production_. When you have 25 million users depending on your work, getting an LLM to generate decent output isn't the problem. Keeping it reliable when the API decides to take a nap is. Preventing your costs from exploding over a weekend is. Building something your team can actually ship and maintain is.

LLMs are weird dependencies. They're slow and unpredictable. They give you different answers to the same question. They cost money every time you call them. This breaks most of the assumptions baked into how we normally build software, which means you need to rethink your architecture from the ground up.

So we treat failure as the default, not the exception. Product teams never touch LLMs directly. Prompts go in version control and get tested. The boring stuff matters more than the clever stuff.

I walked through real examples from what we've shipped: authoring tools, course translations, skills mapping. Not demos or prototypes.

The main takeaway? If you're building AI features for real users, spend less time on prompts and more time on plumbing. That's where the actual work is.
