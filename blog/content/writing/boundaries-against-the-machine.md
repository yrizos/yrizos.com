+++
title = "Boundaries Against the Machine"
date = "2025-12-08T00:00:00+00:00"
draft = false
type = "posts"
canonical_url = "https://blog.talentlms.io/posts/boundaries-against-the-machine/"
image = "images/writing/boundaries-against-the-machine.png"
imageAlt = "Two abstract painted figures seated at a desk studying multiple maps with boundaries and routes on a warm background"
tags = ["legacy-systems", "software-architecture", "domain-driven-design"]
+++

**DDD Europe 2020, Amsterdam.** For a COVID-era hire like me, this was the first time meeting several colleagues in person whom I had been working with daily for months. I kept noticing how familiar everyone sounded and how unfamiliar they looked. An odd sense of delayed recognition. We had paired on code over Google Meet, argued about bounded contexts in Slack, but never shared the same room. The talks, the workshops, the hallway conversations with practitioners who had been doing this for years. We absorbed everything we could.

This was not a one-off. Over the next five-plus years, Epignosis doubled down on more conferences, internal training programs, external consultants, workshops, books, the works. The investment was significant. The business case was clear. Align our code with our business. Make the codebase maintainable as we scale. Enable domain experts and developers to speak the same language.

What we did not anticipate five years ago, in that Amsterdam conference hall, was that we were also preparing our codebase for a future where AI would help us write it.

## What We Built

The first fruits came when we built the new TalentLMS API. This is where Domain-Driven Design stopped being conference theory and became operational practice. We established Ubiquitous Language with domain experts. I remember the shift when conversations with product became faster because we had finally stopped translating ideas back and forth. No more translation layer between what product teams said and what engineers built.

We introduced Value Objects to replace primitives. A CourseStatus is a CourseStatus with its own validation and behavior. Some engineers hesitated at first because what we were now calling [*primitive obsession*](https://refactoring.guru/smells/primitive-obsession) had been the norm for years. That hesitation faded once the constraints started catching real issues. No more passing around strings and hoping they were the right kind of string.

The Anti-Corruption Layer became the cornerstone of our refactoring strategy. We were building new code alongside what was, at the time, a 12-year-old system. We could not afford to let old assumptions bleed into the new model. I could feel the team relax once they realized the new model would stay protected from old assumptions. The ACL created a boundary, a translation layer that let us move forward without being dragged backward by legacy constraints.

Legacy systems demand clarity at every layer. When domain experts and engineers speak different languages, features get built wrong. When boundaries blur, technical debt compounds. At our scale, DDD was not optional. It was operational necessity.

After the API project, we restructured the codebase around domain concepts. We moved from a technical organization to a domain one. Now you do not just know where the models, the views, and the controllers are. You know where the *Learning Paths* are. Where *Talent Library* lives. Where to look for *Reports*.

## How AI Reads It

Today, when I ask AI to add a feature to *Notifications*, it enters the module as if it already understands the territory. It reads the surrounding files, forms a picture of the local concepts, and uses those patterns to shape its first draft. The result is not perfect, but the model moves through the module with a level of confidence that only appeared once the structure became consistent.

AI tools work with limited context. Your current file plus nearby files. This turns domain-based organization from nice to have into critical. When AI is working in the Notifications module, the files it can see are notification concepts, not random controllers. Proximity becomes a semantic relationship instead of accidental collocation.

AI consumes our DDD structure through multiple channels. File and directory names reflect domain concepts. When AI scans the Notifications module, it sees how we handle trigger conditions, execution schedules, and result tracking. Architectural Decision Records document why certain boundaries exist and what alternatives we considered.

Value Object type signatures make constraints explicit in method signatures. When AI sees a function that takes NotificationsTitle instead of a string, it recognizes a constraint. The Ubiquitous Language we established means the model encounters terms that carry domain meaning, not generic technical jargon.

The Anti-Corruption Layer shows AI where boundaries are. It will not couple new feature code directly to legacy database schemas. The ACL is a boundary, a wall you cannot walk through without noticing.

The first time AI added code that matched the existing module structure, it felt like the model had finally learned the shape of our system. That was the moment when the link between our boundaries and the model’s output stopped being theoretical and became visible in daily work.

## Was It Worth It?

DDD is not free. Introducing Value Objects means wrapping primitives. Defining aggregates means thinking hard about consistency boundaries. Building an Anti-Corruption Layer means accepting the overhead of translation between old and new.

In a greenfield project, you can build with DDD from day one. In a legacy codebase, you are retrofitting. You are making incremental changes while keeping the system running. Every change needs careful migration. Every boundary you introduce might break something. Restructuring a codebase around domains when you have more than a decade of technical organization is months of work.

Maximalists argue we should wait for better models. Models are improving fast. By the time you have spent six months on DDD, maybe AI will not need that structure anymore. Maybe it will figure things out. These are not unreasonable positions.

But TalentLMS is not a prototype; it is not something you build at a [3-day hackathon](https://www.starttech.vc/blog/2025/from-ancient-theater-to-modern-hackathlon/). It serves more than 20 million users. That means edge cases accumulated over more than a decade that are not in any training data. Business logic that reflects real-world complexity, not textbook examples. Performance optimizations that look odd but exist because a specific query pattern was crushing the database back in 2014. Regulatory requirements across different countries. Integrations with dozens of third-party tools, each with its own quirks. Data migrations that took months to plan and execute.

AI cannot hold this in its context window. Even the largest models. You cannot fit years of accumulated decisions, trade-offs, and reasons for odd behavior into a prompt. Seeing AI miss a detail that every senior engineer at TalentLMS knew by heart reminded me how much of our system lives outside documentation. Kent Beck frames it clearly in [Programming Deflation](https://tidyfirst.substack.com/p/programming-deflation):

> *In a world of abundant cheap code, what becomes scarce? Understanding. Judgment. The ability to see how pieces fit together. The wisdom to know what not to build.*

## What We Are Seeing

Features that would have taken days now take hours. AI-generated code fits our architecture more consistently. I cannot tell whether the improvement comes from our structure, better prompts, or rapid model progress. I only know the change is visible in daily work.

Structure that helps humans navigate complexity seems to help machines navigate it too. Whether that is causal or correlation, we will know in the near future. For now, we are paying close attention.

But the shift is real. When AI writes the boilerplate, what remains are the decisions that matter. Where boundaries go. What invariants hold the system together. How capabilities compose. Which trade-offs we are willing to accept and why.

In the good old days, we spent mental energy on low-level questions. How to implement a validation. How to write a specific query. With AI, that energy can be reserved for higher-level reasoning. What invariants an aggregate must protect. Where a capability belongs in the architecture. Same mental load, different altitude. More time on structure. Less on mechanics.

At 100 million requests per hour, architectural decisions compound. A poor boundary creates operational problems. A missing invariant risks data integrity. AI can help you move faster, but only if your architecture can guide it. Without that, AI only helps you make mistakes faster.

## Five Years Later

Standing in that Amsterdam conference hall, we were learning DDD to build better software. The investment was about aligning code with business language, about creating boundaries that made sense, about sustainable complexity management.

Today, that same investment pays dividends we never anticipated. Our domain modules. Our explicit boundaries. Our Ubiquitous Language. The Anti-Corruption Layer that keeps old assumptions from bleeding into new code. None of it was built with AI in mind, yet all of it matters for AI effectiveness.

I look back at that conference trip now with a sense of quiet irony because none of us imagined what those early choices would enable. Those workshops and late-night debates about aggregate boundaries were not only about maintainability. They were shaping the maps that modern development tools now rely on.

Not a bad return on investment for a conference trip.
