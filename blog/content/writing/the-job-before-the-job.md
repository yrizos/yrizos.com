+++
title = "The Job Before the Job"
date = "2026-06-22T00:00:00+00:00"
draft = false
type = "posts"
canonical_url = "https://blog.talentlms.io/posts/the-job-before-the-job/"
image = "images/writing/the-job-before-the-job.png"
imageAlt = "Painterly planning wall covered with layered papers, loose diagrams, connecting lines, and sticky notes."
tags = ["engineering-leadership", "engineering-mangement", "professional-development"]
+++

Back in January, I sat across from a tech lead on a video call and asked what had surprised them most about the role. The answer came back without hesitation: “Nobody tells you that writing code stops being the job.” Then they added the part that lingered: “And nobody tells you that you’ll miss it.”

I ran five of these interviews with our tech leads, each built around the same handful of questions. What do you wish you had known? What took the longest to learn? Where did you feel least prepared?

The answers overlapped far more than I expected. Every one of them named some version of the same gap. The skills that earned the promotion were not the skills the job turned out to need. They had been promoted for being excellent engineers, and the role was quietly asking them to become something else.

That gap is not ours alone. It is the defining structural problem of technical leadership across the industry. You reward someone for individual excellence, hand them a team, and hope the rest follows. Sometimes it does, and often it does not.

That is the problem Tech Lead School was built to address. Not to manufacture a tech lead in four weeks, which would be absurd. The aim was smaller and more honest: to give engineers a place to practice the work before the work depended on them getting it right.

## The Shift

If I had to name the one concept that landed hardest, it would be the shift in identity from maker to multiplier. Pat Kua’s [framing of that transition](https://www.patkua.com/blog/maker-vs-multiplier/) was the takeaway nearly every participant reached for first.

The recognition came quickly, and it was uncomfortable. The job is to make the people around you more effective, rather than to be the most effective individual in the room. That reads cleanly on the page. It is far less clean when you have spent years being rewarded for solving the hardest problems yourself.

One participant put it plainly:

> *I still measure my productivity by code output. If I am not shipping code, I feel unproductive, but the job asks me to make others more productive.*

That sentence is the whole transition. A tech lead does not stop being technical. They stop using their own output as the main proof that they are doing the job.

The same recognition shows up a level higher. In [The Subtraction Job](https://blog.talentlms.io/posts/the-subtraction-job/), Konstantinos Chatzinikolakis opens with the manager’s version of it:

> *For most of my first decade as a manager, I measured myself by what I added.*

A tech lead feels it as code shipped, a manager as comments and rewrites added, yet it is the same trap underneath. The work changes before the identity has time to catch up.

I am not writing this as someone who has it all figured out. I delivered five of the presentations myself, across four sessions. I wanted to, and handing them off would have meant watching someone else run them. The whole program was about stepping back, and I would not step back from it. It is hard to demonstrate the trap more clearly than that.

That tension does not resolve in a single session. It resolves over months, as you keep choosing to unblock someone else instead of writing the code yourself. The harder part is coming to believe that the unblocking was the real work all along.

## The Shape of the Job

Before building anything, I needed a map.

The five interviews produced one, and it lined up closely with the formal role definition we already had. Together they named six areas of responsibility that a tech lead has to operate across at the same time.

![Six equal hexagonal panels form a ring around an empty center, showing the six core responsibility areas of a Tech Lead: Technical Leadership, Team Support, Delivery Ownership, Strategic Involvement, Reliability, and Cross-functional Coordination.](https://cdn-images-1.medium.com/max/900/0*TH6GDYjAcgHzaM5s.png)

The breadth is the whole point. A senior engineer can afford to go deep in one or two of these areas. A tech lead does not get that luxury. Technical Leadership, Team Support, Delivery Ownership, Strategic Involvement, Reliability, and Cross-functional Coordination all land in the same week, and that breadth is exactly what nobody practices before stepping into the role.

Most engineers are promoted because they have proven they can handle difficult technical work. Then the role asks them to hold a far wider field in view. The architecture still matters and the code still matters, but so do the estimates, the reviews, the tradeoffs, the team dynamics, the customer impact, the operational risk, and the conversations happening well outside engineering.

## The School

The program ran in March 2026: eight sessions across four weeks, twenty-three hours in total, with ten participants drawn from teams across engineering. Seventeen people contributed, four of them from outside engineering, in Product, Compliance, Customer Support, and Marketing.

Several of the participants had come up through *Dev Academy*, an internal program on SDLC basics that we ran back in 2021 for interns and junior engineers. None of us planned it as a route into technical leadership. It became one anyway.

The design followed from the role itself. Every hour had to map to one of the six responsibility areas. Nothing earned a place in the curriculum because it seemed interesting. Everything was there because the role demanded it.

It also had to be practical. Participants made decisions, produced artifacts, and defended their tradeoffs. The exercises carried ambiguity, time pressure, competing priorities, and incomplete information, because clean problems with clean solutions prepare nobody for the actual job.

The practice stayed concrete. Participants ran a Domain Storytelling workshop and worked through an Elephant Carpaccio slicing exercise as live sessions. In smaller exercises they classified real debt with Fowler’s Technical Debt Quadrant and pulled apart an actual PRD. Take-home work asked them to diagram a greenfield system using the C4 Model, write ADRs, and practice Opportunity Solution Trees and RICE scoring.

The contributors came to show how they actually do the work, not to read from slides. An architect walked through how they approach a C4 diagram. A product manager explained how they really write PRDs and what they need from engineering in return. A senior tech lead described what changes once you stop measuring yourself by code output.

The contributors from outside engineering covered the parts of the role engineers rarely see up close. Compliance walked through what a tech lead has to sign off on, and why it matters. Support showed the thankless work that happens long before a ticket ever reaches an engineer. Marketing explained how we reach the real people who use the software, a question most engineers never have to ask.

## The First Signals

The clearest signals were not the comments people offered at the end of the program. They were the things that shifted inside their teams almost immediately after. These are early signals rather than proof, and the real test is still ahead, but they are the kind worth trusting.

**Estimation changed daily behavior.** The most reported change had less to do with technique than with understanding what an estimate is actually for. One participant put it this way:

> *Estimation is not about getting the number right, it is about surfacing what you do not know.*

That distinction stuck. A commitment is a promise, while a prediction is only a forecast, and most teams quietly treat the second as if it were the first, then wonder why trust erodes.

**Code review changed first.** One participant described the shift:

> *I stopped writing vague comments like ‘this could be cleaner’ and started naming the actual risk, like ‘if this dual-update is missed, state becomes silently inconsistent.’*

The comments moved from opinion to observation, from preference to consequence. And they showed up in pull requests within days rather than weeks.

That is the kind of change I care about most. Not whether someone can recite the name of a framework, but whether the next estimate, review, or team discussion comes out a little more precise because of it.

## The Failure

I am more interested in what failed than in what succeeded, because the failures are where the design problems actually live.

The program contradicted one of its own beliefs. We knew leadership development needs practice inside real work, and then we ran two sessions a week for four weeks. New concepts kept landing before anyone had applied the last ones, which was the most consistent complaint we heard and the most warranted.

The activities themselves were fine. What we squeezed out was the room around them, the space to test the ideas against real work and let them settle.

The evidence was not subtle. Participants described drifting during back-to-back sessions and asked for more time on exercises that got cut short. One put it as wanting “30% concepts, 70% simulations and real scenarios,” and we had that ratio backwards. The pressure reached the people running the sessions too, and in the worst case I finished my own slides a minute before one began.

If I could change one decision, I would spread the same material across eight weeks instead of four. The research is clear that training without on-the-job application produces very little lasting change. We knew that going in, and the timeline talked us out of it.

Cohort 2 will not repeat the mistake. We have taken everything the program produced and started building a Tech Lead Foundations learning path inside our internal installation of TalentLMS, so the next group has plenty to work through before any live session begins. That frees the synchronous hours for what Cohort 1 kept asking for: discussion and hands-on practice instead of presentation.

## The Honest Version

Twenty-three hours will never make someone a tech lead, and I never expected them to. What the program can produce is engineers who have practiced the work before the pressure arrives, who have language for the problems ahead, and who have seen the full breadth of the role before anyone asks them to operate across it.

That time, multiplied across ten participants and seventeen contributors, is a fair thing to question. None of it paused the work. For participants and contributors alike, the program ran alongside business as usual.

The honest comparison is not against the hours we spent. It is against the lead who never got to practice, the one who quietly becomes the bottleneck nobody named, whose team learns to wait, who keeps paying a cost that never arrives as an invoice.

The gap between what earns the promotion and what the job demands does not close in four weeks. It does close faster when people have already made the decisions, met the frameworks, and felt the discomfort of the shift before a team depends on them getting it right.

## The Work Before the Work

Five years separate the interns in that first Dev Academy session from the engineers now preparing to lead teams. None of it paid back on the schedule I expected, and that is the part I keep relearning. The investment compounds quietly, in people, long after you have stopped watching for it.

Building this was hard and slow, and worth every hour. Not because it produced a program, or a next version of something we had already built, but because it created the conditions for people to grow into responsibilities they could not yet name.

The job will change. Parts of it will be harder than they expect, and parts of it will be difficult precisely because they will miss what they are leaving behind.

This time, at least, someone told them early enough to practice.

P.S. For a taste of Tech Lead School, I made our [Leadership Micro Katas](https://github.com/yrizos/leadership-micro-katas) public. Small deliberate-practice exercises for engineers not yet in the role. Contributions welcome.
