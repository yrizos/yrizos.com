+++
title = "One Bloody Character"
date = "2026-04-15T12:53:04+00:00"
draft = false
type = "posts"
canonical_url = "https://medium.com/@yrizos/one-bloody-character-9d3d3ad45861"
image = "images/writing/one-bloody-character.png"
imageAlt = "Abstract painted figure, arms raised in fury, facing empty space. The target is gone. The energy has nowhere to go."
tags = ["software-development", "personal-growth", "artificial-intelligence", "future-of-work"]
+++

The fix was a single character, and I was furious for the rest of the evening.

Cursor had written a perfect expectiminimax evaluator, all tests green. Or so I thought. The scores seemed slightly off on certain paths. Not obviously wrong. It made sensible decisions on most inputs. On the ones where it did not, the wrongness was faint enough that I was almost convinced I was misreading my own algorithm.

Forty minutes of uninterrupted time is what a Tuesday evening gives me after putting my baby girl to bed. I had already burned most of it staring at traces that looked *fine* when I pressed the tool to investigate. It found the sign flip in minutes, explained the inversion, and applied the fix.

*One bloody character*.

I went back and looked at the test. It had been encoding the buggy sign from the start. The code and the test had been wrong in exactly the same way, and the green build had been proof of nothing. Mechanical compliance.

Objectively, I lost less than an hour. The tool handed most of it back. The evaluator worked. By any reasonable measure, this was a trivial issue with a speedy recovery. I was livid, and I knew the anger made no sense at all.

But I was livid anyway.

## **The Window**

The time for building had been shrinking for years. Architectural work, cross-functional coordination, the organizational lifting that never shows up on any dashboard but quietly consumes most of a working week: none of it was going away. What remained were fragments. The hour after bedtime. A Saturday morning before the house wakes up. Not days. Hours.

Augmented coding changed whether those fragments were worth starting. I [wrote a while back](https://medium.com/@yrizos/the-end-of-coding-as-we-know-it-f5446f6c7806) that this looked like progress, and I stand by it. The tool gave me something I had almost stopped expecting: a second life in the code.

I could pick up an unfamiliar technology in the evening and have something running before midnight. Barriers that once required a couple of days simply disappeared. I remember the first time a fragment actually produced something real, not a half-started sketch I would need to re-enter the following week, but a working service in a language I had barely touched.

The feeling was not productivity. It was closer to relief. The part of me that builds things, the part that had been going quiet under the weight of everything else a senior role demands, was still there. Augmented coding did not just make the hour more efficient. It made the hour possible.

When a single-character bug eats the hour and the tool finds and applies the fix in minutes, the question is not just why I am furious at midnight. It is what exactly was lost that makes a trivial bug, in a recovered hour, in a personal project that nobody depends on, feel like something worth being furious about at all.

## **What the Old Failures Left Behind**

I have been doing this for over twenty years. I have had my share of production incidents. Systems down for hours. Features rolled back on a Friday evening. Bugs that took days to trace, not because they were clever but because understanding them required understanding the system, and there was no shortcut to it.

Those were objectively worse than a sign flip in a personal project on a Tuesday night. They cost more, took longer, and hurt more people.

They did not make me this angry.

When those incidents were over, there was something on the other side. A part of the codebase that was now known in a way it had not been before. The hour spent staring at a wrong function signature was also an hour spent learning why the abstraction had been shaped that way. The debugging revealed the design.

The frustration was not separate from the learning. It was the mechanism through which the learning happened. I am not going to romanticize this. Those sessions were brutal, and anyone who has inherited a system that took days to understand just to fix a single defect knows there was nothing pleasant about the process.

But the knowledge that came out of it was durable. It lived in the hands. You could feel it when you touched that part of the code again months later, the quiet confidence of having been inside the problem and coming out the other side knowing how it held together.

The mess was the learning. That is what the old failures left behind. The new ones do not.

## **What Gets Compressed**

Augmented coding compresses the process. What gets compressed is not the debugging but the slow hours where the code becomes familiar through building.

Wax on, wax off.

In a [conversation with Lex Fridman](https://www.youtube.com/watch?v=vagyIcmIGOQ), DHH described competence draining from his fingers. He found himself asking the AI for the same syntax patterns over and over, never learning them because he never typed them.

Alexandru Nedelcu catalogues the same loss in [AI Sucks the Joy Out of Programming](https://alexn.org/blog/2025/10/27/ai-sucks-the-joy-out-of-programming/): an LLM-driven workflow that delivers all the bad parts, the stress of not being in control, the desperate trial-and-error, and none of the gratification that comes from the journey itself.

The slow, frustrating work of the good old days was not waste to be eliminated. That was where psychological ownership of the work was built. Not just knowing what the code does, but the felt sense of having shaped it from the inside, of being the person who wrestled it into its current form.

The fun of building was in the building itself. When that process is compressed, the understanding that would have come from it does not arrive through some other channel. It simply does not arrive.

And the anger I felt staring at a one-character fix at eleven on a Tuesday night was not really about the bug. It was about the absence of everything that used to follow.

## **The Drift**

There is another texture to the loss, and it comes with its own particular absurdity.

Ask the tool to fix something specific and it may not adjust the specific thing. It may reimagine the surrounding structure entirely, like asking someone to move a chair and coming back to find they have redecorated the room. The result looks plausible, passes a quick scan, and is absolutely not what was intended.

Ask again and it overcorrects in a different direction. You are now chasing the output rather than steering it, trying to recover a shape that existed three iterations ago and is gone.

There is also a discipline to this nobody warned you about: you have to be calm. The moment your feedback carries any trace of frustration, the model interprets it as a signal that *everything* is wrong. Measured, specific, almost zen-like correction is what works. Anything that reads like impatience triggers a panicked reimagining that leaves you further from where you started.

The tool is at its most destructive precisely when you are at your least patient, which, if you have forty minutes and the code just drifted sideways for the third time, is most of the time.

Simon Willison has a [rule](https://simonwillison.net/2025/Mar/19/vibe-coding/) for this:

> do not commit code you cannot explain to someone else

The rule sounds simple. It is considerably harder to follow when the window is almost closed and the tool has just produced something that appears to work.

A couple of weeks after the green test incident, an agent ran a destructive git restore mid-session. The safety protocols I had configured did precisely nothing. Gone. Everything I had built that session, gone. And the tool rebuilt it in minutes. That was somehow the worst part. The loss that had felt catastrophic was already undone, the fury left hanging with nowhere to land, because you cannot stay enraged at something that fixed itself before you finished swearing at it.

Neither incident lasted more than a few hours. Neither left behind the durable knowledge that the old failures used to produce. They were small enough that there was nothing to learn from them, and the fury that followed was not proportionally small. That is the paradox. Augmented coding makes failures smaller, faster, and cheaper to recover from. The smaller failures feel worse than the expensive ones used to.

## **Responsibility Without Authorship**

The knowing disappears. The responsibility does not go with it. I shipped the evaluator.

I am accountable for it. That accountability has nothing to do with how much of the code I personally understood at the moment I committed it. Nobody downstream will ask whether the green test was machine-generated or hand-written. The failure belongs to the person who shipped it.

Addy Osmani calls this the knowledge paradox in [The 70% Problem](https://addyo.substack.com/p/the-70-problem-hard-truths-about). AI tools help experienced developers more than beginners, because experienced developers can evaluate and constrain the output. But that same experienced developer is now evaluating output they did not build, and the understanding that would have come from building it was compressed out along with the process. The gap between what was shipped and what was understood widens with every cycle. The accountability does not narrow to match.

You begin to feel like a reviewer of your own work. Not the builder who shaped the code, but the bureaucrat who approved it.

It is impostor syndrome, except the impostor is real. You genuinely did not write most of this. You are genuinely uncertain whether you could have. The tool is lightning fast and you… a bottleneck?

The thought that follows, the one you push away because it is irrational and premature, is that the tool that introduced the bug might eventually make you unnecessary. The fear does not survive examination. It survives anyway. And it colours everything else: the sign flip is not just a sign flip when part of you wonders whether you are watching your own obsolescence in slow motion.

## **Both Live in the Same Hour**

It is late on a Tuesday, the house quiet and the editor open. The hour is running out, the way it always does.

The gains that made this hour worth starting are not rhetorical. Augmented coding gave me back something that was genuinely slipping away. I can pick up where I left off without the long re-entry cost that used to consume half the window. I can reach technologies that would have taken weeks to approach. The second life in the code is real, and I am not willing to give it up.

What I cannot hold at the same time is how the hour feels when something goes wrong. Not worse in any absolute sense. Worse in the specific sense that matters: the mess is no longer the learning. The small failures leave no knowledge behind, no ownership, no quiet confidence for next time.

A sign flip and a rogue git restore. Those are the only two incidents that came to mind across months of augmented building. Two small disruptions, both recovered in minutes. By any honest measure, the tool is doing its job. I am still furious.

I have [written before](https://medium.com/@yrizos/the-fastest-engineer-in-the-room-44168a7570b8) about the cost that speed imposes on the organization around the maker. This is the cost it imposes on the maker. What building means when the tool works and the anger persists and neither fact explains the other, I do not yet know.

The window is closing. I start anyway.
