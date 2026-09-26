+++
title = "Leadership Micro Katas"
date = "2026-04-27T01:18:18+00:00"
draft = false
type = "posts"
canonical_url = "https://dev.to/yrizos/leadership-micro-katas-363f"
tags = ["leadership", "learning", "discuss"]
+++

About twenty years ago, I broke production. I was a young developer, the rollback was slow, and for a few hours, I was sure the company would close because of me. In hindsight, the impact was barely worth mentioning. At the time, I was devastated.

A few days later, the team went out for beers. Someone, I no longer remember who, leaned over and said something along these lines:

> Anticipate failure. Write down what might go wrong. Then, hope you never have to think about it again.

For a while, it sat in my head as a nice idea I never got around to. A couple of incidents and near-misses later, though, I decided to act on it. Before any change I cared about, I would list what could go wrong, and sometimes change the plan because of what I had just written down.

I cannot point to the moment it became a habit. By the time I noticed, it already was. That is roughly how a useful practice arrives when nobody is teaching it to you: a throwaway line, a couple of bruises, a slow drift into doing the thing without thinking about it. It works, but the timeline is on the order of years.

## Wax On, Wax Off

I do believe in deliberate practice, and not as a productivity hack or anything I read in a book and decided to import. Long before any of those books, _The Karate Kid_ taught me that repeated, apparently pointless practice becomes useful before the practitioner understands why. Wax on, wax off.

The trouble is that the engineering defaults that benefit most from repetition are the ones that show up after the promotion, not before. There is no compiler for the question I just answered when someone needed to work it through themselves, no failing test for the risk I noticed and chose not to flag.

The feedback loops go quiet. The defaults that worked as an engineer (write code, answer questions, fix things) start to cost more than they pay back.

A short written practice, anchored to a moment I am already in, is one way to manufacture a new loop without waiting for years and bruises to install it. The specificity is what does the work. "Communicate more clearly" gives me nothing to do at 11:42 on a Tuesday. "Write three reasons this could fail in production before you commit to the approach" gives me something to do now.

That second one is, more or less, a kata.

## A Familiar Format

Code and architectural katas have been around for years, and I am building on the same format. Short, repeatable exercises designed to build fluency through repetition, applied this time to the part of tech leadership that does not announce itself.

The label _micro_ is deliberate. Ten to fifteen minutes, alone, no team, no coach, no permission. They can be practised before stepping into a lead role, so the habit is in place before the role asks for it.

I had no plan to write them down. Earlier this year, we started training the next batch of tech leads at [Epignosis](https://www.epignosishq.com/), and twenty years of informal habit had to become something I could hand to someone else. The catalogue came out of that.

## The Catalogue

I extracted the katas from my internal presentation to a [public repository](https://github.com/yrizos/leadership-micro-katas) you can clone, fork, or argue with.

| #   | Kata                                                                                                                             | Behavior                                                          |
| --- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| 001 | [Assumption Inventory](https://github.com/yrizos/leadership-micro-katas/blob/main/katas/001-assumption-inventory.md)             | Surface hidden assumptions before they become surprises           |
| 002 | [Pre-Mortem Minute](https://github.com/yrizos/leadership-micro-katas/blob/main/katas/002-pre-mortem-minute.md)                   | Anticipate failure before momentum silences doubt                 |
| 003 | [Opinion or Observation](https://github.com/yrizos/leadership-micro-katas/blob/main/katas/003-opinion-or-observation.md)         | Ground feedback in evidence, not preference                       |
| 004 | [The Blocker Brief](https://github.com/yrizos/leadership-micro-katas/blob/main/katas/004-blocker-brief.md)                       | Explain a technical constraint so a non-engineer can act on it    |
| 005 | [The Tradeoff Statement](https://github.com/yrizos/leadership-micro-katas/blob/main/katas/005-tradeoff-statement.md)             | Articulate what a decision costs, not just what it gains          |
| 006 | [The Question Before the Answer](https://github.com/yrizos/leadership-micro-katas/blob/main/katas/006-question-before-answer.md) | Develop others by resisting the urge to solve for them            |
| 007 | [The Line Before the Pressure](https://github.com/yrizos/leadership-micro-katas/blob/main/katas/007-line-before-pressure.md)     | Turn escalation from a stress response into a deliberate decision |
| 008 | [The Thing You Did Not Say](https://github.com/yrizos/leadership-micro-katas/blob/main/katas/008-thing-you-did-not-say.md)       | Say on paper what you would not say out loud                      |
| 009 | [The Debt Sentence](https://github.com/yrizos/leadership-micro-katas/blob/main/katas/009-debt-sentence.md)                       | Write down what is wrong before you ship it                       |

Each kata follows the same shape: one trigger, one short practice, one written output. The trigger is a moment already present in your engineering work, and the practice is short enough to run before that moment passes.

## Pre-Mortem Minute

The kata that grew out of those beers twenty years ago is #002 (no idea why I didn't list it first):

> You are about to commit to a technical approach.
>
> - Write: "This has failed in production. Why?"
> - List 3 specific reasons
> - Check if your plan addresses the most plausible one
>
> **Risk is visible before momentum makes it impolite to raise it.**

The trigger is the moment you are about to commit to a technical approach. The kata applies most when you feel confident. It is not for moments of genuine unease; if you are uneasy, the answer is not a kata, it is a conversation. The kata is for the times when momentum is gathering, and the question of what could go wrong is starting to feel impolite.

If "I feel confident" is too soft to act on, give yourself an objective trigger as well. Any change that touches more than one system. Any change you would describe as straightforward. Any time you are about to mark a design doc as decided. Pick one of those, or one of your own, and let the kata fire on it without negotiation.

1. Write the failure statement first. _This has failed in production. Why?_ Past tense matters; it puts you on the other side of the failure, looking back.
2. Write three reasons in plain language. Short, specific, the way you would describe the problem to a colleague at the next desk. Not "scalability concerns."
3. Do it before momentum closes the door. Five minutes after the decision is announced, the cost of raising risk has already gone up.

What you are left with is a note to your future self, not an Asana task, not a postmortem, not a runbook entry. Something close to this:

```plaintext
This has failed in production. Why?

- The new feature flag defaults to "on" for everyone, not just the cohort
  we agreed to roll out to. We notice when support tickets spike.
- The third-party we call inside the new endpoint rate-limits us under
  load. The retry loop turns one bad minute into ten.
- The cache key we changed is shared with the older service. We start
  serving stale data to customers, we have not even rolled out to yet.

Most plausible: the flag default. The PR currently flips it on at deploy.
Add a config check that requires the cohort list to be non-empty.
```

When the note surfaces something useful, it is usually an unexamined assumption, a dependency you took for granted, or a rollback that depends on a state you cannot guarantee. Sometimes nothing surfaces and the plan is fine. The note still has value next week, when you can see what you considered before you committed.

## The Note I Did Not Write

Which brings me back to that change twenty years ago. If I had run the kata against it, the most plausible reason on the list would have been the one that bit me. Something close to:

> The change includes a schema migration that runs on deploy, and there is no tested reverse migration. If anything goes wrong, the rollback is not a redeploy, it is a manual recovery.

The mitigation would have been to split the migration from the code change and run it ahead of time.

I do not know with certainty that I would have caught it. I know I never gave myself the chance to. That is the loop the kata closes. Not every time, not as a guarantee, but often enough that the ten minutes are repaid in the cases it does catch.

## Try One

I am not going to promise results. I have seen these katas work, sometimes for me, sometimes for others I have passed them to over the years; I have also seen variants that worked for me fail to land for someone else, and I have abandoned a few myself.

Pick one and stay with it for a week. For each time the trigger comes up, write down three things:

- Did the moment arise?
- What did I do?
- What would I change?

If it never came up, that is also worth knowing. Either way, you will have spent a week practising something the role usually teaches over years.
