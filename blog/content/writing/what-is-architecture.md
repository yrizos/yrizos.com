+++
title = "What Is Architecture?"
date = "2026-03-02T00:00:00+00:00"
draft = false
type = "posts"
canonical_url = "https://blog.talentlms.io/posts/what-is-architecture/"
image = "images/writing/what-is-architecture.png"
imageAlt = "A fork in the road: one path splitting into six branches, representing optionality and the capacity to choose direction."
tags = ["software-architecture"]
+++

The deceptively simple question came at [Open Conf](https://open-conf.gr/) last November, when a curious young engineer approached me at the conference’s mentorship corner. We were going to get a fresh cup of coffee when she asked: **What is architecture?**

It should have been easy terrain for someone who has spent years inside the problem, but what came out was a few sentences that gestured at decisions and trade-offs without ever landing anywhere. She nodded in the way people nod when they are being polite to someone who has just disappointed them. Almost four months later, I am still turning the question over, which is either embarrassing or instructive.

I have decided to treat it as the latter and write up what I owe her.

## The Short Answer Problem

The resistance to a clean answer shows up immediately when you go looking for a definition. The closest thing to a satisfying formulation belongs to Ralph Johnson, one of the four authors of *Design Patterns*, the book that shaped how the industry thinks about software structure. After all that engagement with the problem, Johnson arrived at something that sounds almost flippant:

> *Architecture is about the important stuff, whatever that is.*

Martin Fowler, who often returns to this line, treats the deliberate vagueness as a feature rather than a bug. The longer I’ve spent on architectural problems, the more I think he is right.

Whenever I’ve tried to give a more precise version of that formulation, something slips. “Architecture is about structure” works until you notice that a pile of undifferentiated code has structure too, and most of it isn’t architectural. “Architecture is about decisions,” works until you ask which ones count, and where you draw that line depends entirely on context. “Architecture is the decisions that are hard to reverse” is closer, but reversibility is partly a function of how the rest of the system is built, which puts you in a loop before you’ve arrived anywhere.

I’m not alone in this struggle. The Software Engineering Institute maintains a compiled [catalogue of definitions](https://www.sei.cmu.edu/library/what-is-your-definition-of-software-architecture/) across modern, classic, and bibliographic sources, and the fact that such a catalogue exists and keeps growing is itself data. That is not a gap in the literature waiting to be filled.

It is signal about the nature of the thing.

## What Architecture Is Not

The space left by every failed definition does not stay empty for long. A few specific misconceptions keep filling it, and each one was invited by some shorter version that came before it.

The first, my favorite, is that architecture is the diagrams. UML, C4 models, whiteboard sessions and ADRs are representations of architecture, and useful ones, but they are not the thing itself. A decision shapes what is possible, what is difficult, and what is effectively ruled out, regardless of whether anyone drew it on a whiteboard or wrote it down. You can tear up the whiteboard. The structural commitment has already been made.

The second misconception is that architecture is a phase. You do the architecture work, hand it off, and then engineering builds the thing. That model comes from construction, where you can hand off a completed design and step back, but software never reaches a completion state. It keeps changing; the structure that shapes it needs to keep being shaped, and a system left without active tending decays. Entropy is not a metaphor for codebases. It is the normal trajectory of any system that nobody is attending to.

The third misconception is that architecture lives in a role. One person or a small group owns the structural decisions, and everyone else builds inside them without needing to understand or influence them. This is the most consequential of the three because it concentrates exactly the wrong thing in exactly the wrong place. An architect who owns all the decisions has also insulated themselves from the feedback that would improve those decisions. The engineers closest to implementation are the ones who will live with the consequences, and cutting them out of the process means cutting out the most important signal in the room.

## Deciding Which Tension to Accept

Clearing those misconceptions away is useful, but it still leaves the original question open. What I’ve found myself reaching for, when people push past the misconceptions and ask what architecture actually is, is this:

> *The practice of deciding which tensions to accept and which to release.*

Every structural decision trades something: consistency against availability, deployability against performance, team autonomy against system coherence, and there is no configuration that resolves all of these simultaneously.

If you think you’ve found something without a trade-off, you just haven’t found it yet. Nobody opts out.

The right trade-off is always context-specific. The skill is not knowing the right tension to accept in the abstract but recognizing which tensions a specific context can absorb, which ones will compound painfully over time, and being deliberate about the choice rather than stumbling into it.

That relocation is the point. As the old adage goes, complexity cannot be destroyed, only relocated. The architect’s job is to decide where it lives and why that location is better than the alternatives, and no short answer can carry that much context without losing most of what matters.

## The Organization Is the Architecture

One of the things it loses almost every time is the organizational dimension, and that loss is not trivial. Any definition of architecture that stops at the technical is incomplete. In 1968, Melvin Conway made an observation that reads almost like a complaint about a frustrating project: any organization that designs a system will produce a design whose structure is a copy of the organization’s communication structure.

This may be hard to believe today, but Harvard Business Review actually rejected the paper (for lack of evidence). Decades later, a [Harvard Business School study](https://www.hbs.edu/faculty/Pages/item.aspx?num=32217) confirmed exactly what Conway described, and subsequent research at MIT, the University of Maryland, and Tampere University of Technology validated it independently.

Conway illustrated the dynamic with a story from a compiler project he assigned to eight engineers, five to COBOL and three to ALGOL. Nobody decided how many phases each compiler would have, yet the COBOL compiler ended up with five phases and the ALGOL compiler with three. The structure of the output matched the structure of the team that built it, as an unintended emergent outcome, without anyone planning it.

If you’ve spent time inside a large engineering organization and wondered why the system looks the way it does, that story will feel less surprising than it should. The uncomfortable version of the observation is that the relationship runs in both directions. The organization shapes the system, and then the system shapes the organization. Teams form around modules, and modules persist because teams formed around them. Technical and organizational concerns co-evolve in ways that make it impossible to cleanly separate them, which is another reason any short definition falls apart. It leaves out half of what is actually happening.

## Separating Decision from Construction

That missing half also reshapes how we need to think about the architect’s role. The broken metaphor at the center of how the field thinks about the architectural role is the building architect: design first, hand off to construction, step back.

The word itself comes from the Greek *arkitekton*, meaning chief builder, and the original was not a separate designer standing apart from construction. The chief builder was the most skilled person on the site, someone who understood the full problem from the inside. The software industry borrowed the building architecture metaphor wholesale and quietly erased that origin, replacing it with a designer insulated from consequence.

Erik Dörnenburg identified this as a [structural information problem](https://erik.doernenburg.com/2014/12/new-recording-of-architecture-without-architects/), not a cultural one. When the decision-maker is systematically insulated from the feedback loop that would otherwise correct bad choices, the design drifts from the reality it is supposed to serve. The distinction Dörnenburg draws is between being aware of consequences and having to live with them, and that gap is where architectural decisions quietly degrade. The moment you separate design from construction, you are separating decision from consequence.

This leads to a formulation that still surprises people when they hear it:

> *An architect’s value is inversely proportional to the number of decisions they make.*

The goal of architectural leadership is to build the capacity for good structural decisions to happen across the teams doing the work, not to own those decisions permanently. This often gets misread as architecture without accountability, which couldn’t be further from the truth. It requires far more architectural maturity, not less, because teams need to maintain decision records, argue trade-offs honestly, and hold themselves to a standard.

The concept only works where that maturity exists, and building that maturity is itself one of the architect’s main jobs.

## The Elevator and the Engine Room

What that job looks like across an entire organization is something Gregor Hohpe captures in a [metaphor](https://martinfowler.com/articles/architect-elevator.html) I’ve returned to more than almost anything else in this field. Large organizations are tall buildings. The IT engine room is in the basement: the systems, the infrastructure, the code. The executive penthouse is at the top: the strategy, the resourcing decisions, the market bets. Between them are floors of management, and each floor is a translation layer where information degrades as it moves in either direction, telephone game dynamics at the organizational scale. The architect’s job is to *ride the elevator*, carrying meaning intact in both directions across those translation layers.

I run an [Architecture Modernization Enabling Team (AMET)](https://esilva.net/amet) at Epignosis, and this is what the work actually looks like in practice. The problems that determine whether a modernization succeeds are not purely technical. They are questions about which teams have capacity for which changes, how organizational constraints shape what sequences of work are even possible, and where leadership understanding needs to deepen before a technical choice can be made safely.

Architecture that stays in the engine room is working with half its inputs. Hohpe puts it plainly:

> *Excessive complexity is nature’s punishment for organizations that are unable to make decisions.*

Architecture is also about options, the right to defer a decision while locking in key parameters. In volatile conditions option value increases, and a system locked by deep coupling has had its options foreclosed. Modernization, in this framing, is not paying off the past. It is rebuilding the capacity to choose.

That framing also redefines what an enabling team is for. An enabling team exists to build capability in the teams doing the product work, not to own the work permanently.

The AMET model applies this logic specifically to modernization, as a bell curve of involvement that increases as capability is built and decreases as teams internalize it, until the enabling team eventually dissolves. That lifecycle is not the failure mode. The failure mode is an enabling team that never dissolves because it keeps doing the work instead of transferring the capacity.

There is a second failure mode that gets less attention, which is the team that dissolves before the capability transfer is genuine. The downslope of the bell curve only resolves correctly when the skills and confidence are actually there, and premature dissolution looks like success until the teams are on their own and discover what they did not actually internalize.

Both these failure modes point at the same thing from different directions: architecture done well is partly an exercise in making itself unnecessary. That is not something you can fit into two sentences without losing everything that makes it true.

## The Foundation and What It Enable

What it makes possible is the part of the argument that gets framed backwards almost every time I hear it.

The common version treats modernization as competing with innovation, time spent on the foundation is time not spent building new things, and every sprint on the former feels like something stolen from the latter.

What this misses is that a system that has not been modernized does not just move slowly. It actively constrains which questions engineers are allowed to ask, and when every change requires deep knowledge of how the system currently holds together, the mental load shifts from “what should we build?” to “what can we build without breaking everything?” That is not a resource problem. It is a cognitive constraint that narrows the product imagination of the entire organization.

What modernization actually enables is *optionality*: the capacity to change direction without foreclosing the future, to experiment in one slice of the system without risking another, to run multiple hypotheses simultaneously because the boundaries are clean enough to hold them.

The features you could not build on the old foundation leave no trace, and nobody wrote them on a roadmap. The innovation that never happened is invisible, which is precisely why modernization is chronically undervalued: **its benefits are counterfactual, and counterfactuals do not appear in sprint reports.**

## The Question Persists

The same invisible cost applies to the question itself. An engineer without language for what architecture is will still make structural decisions, and that gap accumulates silently, below the threshold of any report, in exactly the same way as the features that never got built.

Which brings me to the part where I go against everything in this article and add to the pile:

> *Architecture is the practice of maintaining the conditions under which better decisions remain possible.*

You can probably drill more holes in it than in most short definitions. But it happens to be the one I *like* the most, and the one I wish I had at the ready four months ago. It would not have been a *satisfactory* answer, of course.

But it might, just might, have saved me from that polite nod.
