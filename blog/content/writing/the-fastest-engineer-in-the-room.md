+++
title = "The Fastest Engineer in the Room"
date = "2026-03-13T16:44:20+00:00"
draft = false
type = "posts"
canonical_url = "https://medium.com/@yrizos/the-fastest-engineer-in-the-room-44168a7570b8"
image = "images/writing/the-fastest-engineer-in-the-room.png"
imageAlt = "A large tornado tears through the centre of the scene, scattering debris in every direction. In the foreground, a group of people stand facing the tornado with their arms raised in celebration. One of them holds a trophy above their head. They are cheering the destruction on."
tags = ["engineering-leadership", "software-design", "software-architecture", "technical-debt"]
+++

A colleague mentioned the **tactical tornado** the other day. The phrase landed in a way it hadn’t in years, and I found myself back in two places at once: the pages of John Ousterhout’s [*A Philosophy of Software Design*](https://www.amazon.com/Philosophy-Software-Design-2nd/dp/173210221X), and a meeting room where someone was asking me, as diplomatically as they could, to please slow down.

I have… opinions about the book. Some of its prescriptions feel too neat for the messy reality of production systems. But the tactical tornado was a direct hit. Ousterhout named something I had seen repeatedly but never had a clean language for.

And more uncomfortably, he named something I had been.

## Visible Output Wins

Ousterhout’s central thesis is that complexity is the root problem of software and that it accumulates incrementally. Nobody decides to build a complex system. It emerges from hundreds of small decisions, each seemingly harmless, each adding a thin layer of friction that the next developer will have to work through.

The tactical tornado is the human embodiment of this accumulation: someone who makes those small decisions faster than anyone else, and always in the direction of more complexity.

Ousterhout draws a distinction between tactical and strategic programming. Tactical optimizes for the next feature, the next fix, the next thing that needs to ship. Strategic treats working code as necessary but insufficient; the real goal is a great design that also happens to work. The tornado is the extreme case of the tactical mindset: zero investment in design, maximum visible output, and a trail of shallow abstractions left behind for others to navigate.

Tactical tornadoes often get praised and promoted because their output is visible and their damage is not. The engineers who clean up after them appear to be making slower progress by comparison. This is how the incentive structure ends up working against the people doing the harder, more valuable work.

It does so reliably enough that you can predict the outcome: the tornado rises, the maintainers burn out, and the codebase degrades.

## Built for the System

As I have already mentioned, I’m not writing this from the outside.

I have been the person called into a meeting and asked to slow down. The conversations were polite. The message was clear. I was producing code faster than anyone around me, and the wake I left behind was becoming a problem for the team.

At the time, I understood the feedback intellectually while feeling, somewhere deeper, that the real issue was everyone else’s inability to keep up.

That feeling is what makes the tactical tornado so difficult to correct. The speed is real. The output is real. The praise is real. The damage is real, too, but it is distributed across other people’s schedules, other people’s frustration, and future sprints that haven’t happened yet. The feedback loop that would correct the behaviour is delayed long enough that the behaviour gets reinforced instead.

I am not alone in this recognition. In an [SE Radio interview](https://se-radio.net/2022/07/episode-520-john-ousterhout-on-a-philosophy-of-software-design/), Jeff Doolittle told Ousterhout that there is a whole unnamed category of *recovering tactical tornadoes*, people who were never acting out of malice but responding to the incentives around them.

That framing matters.

The tornado is not a villain. They are often the person most adapted to survive in the system they are in.

If you treat the tornado as a character flaw, the solution is coaching or removal. If you treat it as a system outcome, the solution is to redesign the incentives. Both may be necessary, but only the second one prevents the next tornado from forming.

## Deeper Than Code

Most commentary on the tactical tornado stays at the level of code quality. The tornado writes messy code, others clean it up, and complexity grows. That framing is accurate but incomplete, because it misses the organizational dimension entirely.

Conway’s Law runs in both directions. The organization shapes the system, and then the system shapes the organization back. The tactical tornado exploits this bidirectional dynamic in a way that is rarely discussed.

When a tornado moves through a codebase, other engineers route around the damage rather than engaging with it. They build interfaces that insulate their own work from the tornado’s output. Over time, this avoidance becomes structural. The team’s actual communication topology starts to reflect not the ideal architecture but the boundaries of the tornado’s impact area.

The tornado’s code is shaping the organization.

Even after the tornado moves on, or slows down, or gets promoted out of the code, the team carries the scar tissue. People still avoid those modules. Knowledge remains siloed in whoever was brave enough to touch it. New engineers inherit not just the messy code but the organizational habits that formed around it: the workarounds, the *unwritten rules* about which parts of the system you simply do not touch.

That is what makes the tornado problem an architectural problem, not just a code quality problem. The damage is sociotechnical. Refactoring the code is necessary but insufficient. You also have to refactor the team’s relationship to the code, which is a much harder and longer process.

Code can be rewritten in a quarter. Organizational scar tissue takes years to heal.

The effect is, of course, amplified when the tornado is also a senior engineer or a team lead. Their design decisions carry organizational weight. Their module boundaries become team boundaries. Their shortcuts become conventions. The system calcifies around their tactical choices, and what started as one person’s speed becomes the entire organization’s constraint.

The tactical tornado is not just a complexity accelerator. They are an organizational architect, designing the team’s communication structure without realizing it, and without anyone reviewing the design.

## Mess, Accelerated

All this was already true long before augmented coding entered the room. What AI adds to the mess is scale.

Ousterhout himself, in a recent [conversation with Gergely Orosz](https://newsletter.pragmaticengineer.com/p/the-philosophy-of-software-design), described current AI coding tools as tactical tornadoes. They produce code fast, fix issues fast, and generate technical debt at speed. That characterization is sharp, but the deeper problem is not that AI acts like a tornado. It is that AI pulls the human toward tornado behaviour.

[Facundo Olano](https://olano.dev/blog/tactical-tornado) makes this argument clearly. LLMs operate task by task, diff by diff. There is no big-picture thinking in the process, no consideration of conceptual integrity. The human is supposed to supply those things, but the tool actively works against that mindset. The more detached you become from the low-level code, the harder it is to maintain a tight mental model of the system’s design and runtime behaviour.

I recognize this tension from my own work. The feeling of speed that AI provides is the same one I had in my code-writing days, the one that got me called into meetings. The difference is that now the speed is available to everyone, and the organizational structures that might have caught the damage are under pressure to get out of the way because they slow things down.

Code review, design discussions, and architectural governance. All of them feel like friction when AI can produce a working implementation in minutes.

There is also a troubling productivity question. Who gets a greater boost from AI coding tools: the strategic developer who invests in documentation, context, and design, or the tactical tornado who fires prompts and ships? [One analysis](https://positive-antagonist.com/tactical-tornadoes-in-the-age-of-ai-assisted-coding/) suggests the tornado gets a higher multiplier because AI is already good at reaching a working state with minimum effort. If that is true, the share of tactically produced code will rise, and technical debt will accelerate across the industry.

The Conway’s Law dimension makes this exponentially worse. If AI-generated code shapes organizational communication patterns the way human-written code does, and there is no reason to think it would not, then the sociotechnical damage compounds faster than any team can address.

We are not just scaling the tornado’s code output. We are scaling the organizational distortion that follows it.

## Speed Is a Choice

Having been the tornado myself, I can deliver this counterargument without hedging.

Speed is not inherently destructive. There are moments when tactical programming is the correct choice. A proof of concept that needs to validate a hypothesis before anyone invests further. A time-bound market opportunity where being second means being irrelevant. An incident response where the priority is stopping the bleeding, not writing elegant code.

Even Facebook’s engineering motto evolved over the years, from celebrating breakage to demanding stable infrastructure, which suggests the industry’s relationship with tactical speed is still being negotiated, not settled.

The problem is not speed itself but the failure to recognize when speed has become the default mode rather than a deliberate choice. The tornado does not choose to be tactical. They simply never switch out of it. And the organization, by rewarding their output, never gives them a reason to.

Ousterhout suggests investing 10 to 20 percent of development time in design improvement. That number is less important than the principle behind it: strategic thinking is not a separate activity from coding. It is a continuous investment, a small tax on every task that pays compound returns over time.

The tornado invests zero. They are not failing to invest. They are *actively divesting*, extracting design capital from the codebase, and converting it into visible output.

The question every team should ask is not whether they have a tactical tornado. It is whether their incentive structure would produce one.

## Listen to the Room

Being asked to slow down did not feel like a gift at the time. It felt like a misunderstanding. I was producing more than anyone around me. The metrics confirmed it. The feedback from stakeholders confirmed it. The only people who seemed unhappy were the engineers working alongside me, and I could not yet see that their unhappiness was the most important signal in the room.

Understanding came later, gradually, through years of working on systems shaped by the same behaviour I had exhibited. Through inheriting code that was fast to write and brutal to maintain. Through watching teams route around modules that nobody dared touch. Through seeing, from the other side, how the tornado’s speed becomes the organization’s constraint.

Ousterhout gave me the language. The colleagues who pulled me aside gave me the correction. Both were necessary. Neither was sufficient on its own. The language lets you see the pattern. The correction lets you feel its cost.

If someone has pulled you into a meeting to ask you to slow down, do not treat it as criticism. Treat it as information about your impact, the kind that no metric will ever capture and no AI tool will ever flag.

Trust me, the feedback is far more useful than it will feel at the time.
