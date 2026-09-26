+++
title = "Turn the Ship Around!"
date = "2026-08-12T14:25:51+00:00"
draft = false
type = "posts"
canonical_url = "https://medium.com/@yrizos/turn-the-ship-around-af66e0df88df"
image = "images/writing/turn-the-ship-around.png"
imageAlt = "A single submarine floats alone in open, dark water."
tags = ["david-marquet", "engineering-leadership", "engineering-management", "book-review"]
+++

The part of *The Hunt for Red October* that stayed with me was not the defection plot or the torpedo in the final act. It was the control room. A dozen people reading the ocean through sound alone, making calls in seconds that the surface world would have spent a month of meetings on. I did not follow the Cold War politics at all as a child. I followed the room.

That room turns up again in most of what I have loved since about crews who leave the atmosphere instead of the surface. Strip either setting back and the same frame sits underneath, a sealed hull with something outside it that kills on contact, a crew small enough that every person’s competence is load-bearing, and nobody reachable in time to make the decision for them.

Which is roughly the frame I brought to David Marquet’s *Turn the Ship Around*, and it is not the one the book gets shelved under. Marquet took command of a submarine he had not been trained on, with no time left to learn it, and for the first stretch that reads as a coordination problem rather than a leadership one. How does a crew make sound decisions before anyone aboard has had time to become the authority on the boat? The leadership argument arrives once those two questions turn out to be the same question.

## Santa Fe and the Leadership Shift

Marquet had spent close to a year preparing to command a different submarine, learning its systems the way the Navy expects a new captain to. The reassignment to the USS Santa Fe came at the last minute, and it came without a second year attached. He would take over a crew and a set of systems he did not know, on a schedule indifferent to that.

Santa Fe was the worst-performing submarine in the Pacific fleet at the time. Re-enlistment was the lowest anywhere in it, morale was poor, and officers and crew advanced more slowly than their counterparts on better boats.

The stakes on that boat are not the stakes of a software organization, and nothing here treats them as though they were. A submarine crew’s mistakes can kill people within minutes. An engineering team’s worst week, genuinely bad as those get, does not run on that clock and does not carry that cost.

What carries over between the two is narrower and more useful than an analogy. It is the shape of the constraint, a leader with no runway to build expertise before the decisions start arriving anyway.

Marquet’s response to a boat he did not know was not to out-study it. It was to stop requiring that the expertise sit with him at all.

The Navy he had come up through ran on what he calls a leader-follower model. Authority concentrated at the top and instructions moved downward, which works well enough while the person at the top genuinely does know the most about the thing being decided. On Santa Fe that condition was simply false, and a crew trained to wait for orders from someone who could not yet give good ones is a crew that waits.

The leader-leader model he built instead moves authority to wherever the relevant competence and information already sit. Not handed out as a gesture toward autonomy, but relocated to where the knowledge to use it was already sitting.

## The Engineering Bottleneck

The version of that constraint I keep meeting at work has nothing to do with hulls. It shows up as decision latency, the gap between a decision becoming necessary and someone with the authority for it actually being available. A team that has to locate an approver before it can act has built a queue into its own operations, and the queue doesn’t care whether the person at the head of it actually knows the most about what’s waiting.

Incidents make this obvious fastest. Authority to act during an outage belongs with whichever engineer is holding the pager, not with a central approver who has to be found and briefed while the system stays down.

Design review is the slower version of the same question. Whose opinion counts on an RFC is properly a function of who understands the part of the system under discussion, and a process that weights titles instead ends up with documents approved by people who could not have written them.

For anyone promoted because they were the strongest engineer in the room, the uncomfortable part is what Marquet calls the expertise trap. The instinct that earned the promotion, taking the hardest problem personally, becomes the ceiling the team cannot grow past. Engineers around that person stop developing judgment nobody ever asks them to use, and the organization ends up with one deep well of competence and a queue in front of it. A captain whose crew will not submerge without checking first has built the same bottleneck by a different route.

## Control, Competence, Clarity

Relocating authority only works when three conditions hold at once, and most of the book is a study in what breaks when only two of them do. Marquet names them control, competence, and clarity.

Control is the decision right itself, sitting with whoever is closest to the work rather than three levels above it. It is also the cheapest of the three to hand over and the most dangerous to hand over alone, since a decision right given to someone not yet equipped to use it is not empowerment.

Competence is what makes that handover safe rather than reckless, and Santa Fe’s version of it was unglamorous. Sailors qualified for each system they were trusted to make calls about, in front of peers who had already qualified and could ask anything they liked, and a wrong answer meant going back to study rather than being waved through out of politeness. Nobody held authority over a system they could not explain on demand. That is the part of the leader-leader story that gets dropped when the phrase travels on its own.

Clarity is the shared purpose and standard that keeps a hundred separate good decisions pointing the same way. Without it, control and competence produce a capable crew whose sensible individual calls do not add up to a coherent boat.

The first mechanism is a change in what officers were permitted to say out loud. Rather than requesting permission to submerge, they stated the intention, and a superior either stopped the sentence or let it stand. An incident commander announcing a rollback instead of paging upward and waiting to be told is running the identical script.

Deliberate action takes the same instinct further. Before doing anything non-trivial the crew said aloud what they were about to do and paused first, which is the pause separating a reread diff from a trusted commit message.

Certify, don’t brief inverts who has to demonstrate understanding. Instead of one person walking a plan past a room that nods, the people closest to the decision had to show they understood it themselves, and anyone present could be asked about any part of it on the spot. A design doc that collects a thumbs-up emoji in a channel has been briefed. One whose author gets asked to walk through its failure modes, live, and does, has been certified. The artifact is identical. The difference is whether anyone was tested against it.

Embrace the inspectors is the one aimed outward. External inspections were treated as free information about the boat rather than an event to survive, which is the posture a mature team already takes toward a security audit.

## Judging the Book

As a book, its strongest quality is honesty, which is rarer in this genre than it should be. Management memoirs tend to arrive pre-polished, the author’s early mistakes edited into foreshadowing. Marquet leaves the false starts in, including orders he gave that turned out to be impossible to carry out, and he mostly resists the vague appeals to vision that pad out the shelf around him.

The mechanisms are also concrete enough to be tried rather than admired. A team could run the intention-stating change on Monday and know by Friday whether anything moved, which very few leadership books can offer.

The sharpest thing in it, though, is that Marquet names the expertise trap himself rather than leaving a reader to work it out. He is explicit that the instinct to be the most capable person in the room is the thing a leader has to give up, and that giving it up feels like a loss while it is happening rather than a promotion. Most books in this category gesture at that much. Naming it plainly is what makes this one generalize past submarines at all, more than any of the four mechanisms manage.

Where it is weaker is in what it takes for granted. The Navy pre-qualifies people against hard technical standards long before they reach a boat, so a large part of Santa Fe’s competence condition was built elsewhere and simply handed to him. Most engineering organizations have no equivalent pipeline and cannot conjure one.

Marquet’s own autonomy was unusual too, and so was his timing. A captain handed the fleet’s worst boat has room to experiment that a captain of a merely mediocre one does not.

The later chapters lose their edge as well. The same three-condition logic gets re-applied to fresh scenes without gaining much from the repetition, and the chapter-end summaries with their reflection questions read less like a memoir than like a training module bolted onto the back of one. I found the first half considerably stronger than the second.

None of which touches the record. Santa Fe went from worst-performing submarine in the Pacific fleet to best-performing in about a year, and the command became an unusual source of officers who went on to lead well elsewhere.

The fact I find hardest to argue with is what happened after Marquet left. The performance held, which is the detail separating a structural change to a boat from one captain’s force of personality.

Marquet is explicit that this does not license copying his mechanisms. The exact wording of an intention statement and the specific shape of a qualification board are local artifacts, and the durable layer beneath them is control, competence, and clarity. Which of those three a given organization is actually missing, and what would have to be built to supply it, is a question the book cannot answer from outside and does not pretend to.

## What Transfers for Engineering Leaders

What an engineering leader can take from this is narrower than three memorable words and narrower than the book’s own enthusiasm. It is a reason to treat decision latency as a design problem rather than a personality one, and a question worth asking of every recurring decision, whether the person making it is the best positioned to make it or merely the one with signing authority. Most organizations have more of the second kind than they would guess.

For a technical leader promoted for exactly the instincts this asks them to set aside, the practical version is smaller than a restructure. It is noticing when a decision has been routed upward out of habit rather than need, and sending it back down to whoever was closest to it.

I had already [designed and run an internal initiative](https://blog.talentlms.io/posts/the-job-before-the-job/) for engineers moving into their first tech lead roles, and I had not read *Turn the Ship Around* when it was being designed. The overlap between what that work kept circling and what Marquet’s three conditions describe was something I noticed afterwards, not a framework I had been building from. Which says more about how reliably that gap appears than about either.

Whether the transfer is ever complete is not something the book settles, and I doubt that it is. What it does supply is a name for the bottleneck, early enough to be recognized before a team has learned to wait.

I’m long overdue a visit to [Proteus](https://averof.hellenicnavy.gr/en/from-proteus-to-nereus-from-mythology-to-the-silent-power-of-the-fleet/), a submarine-turned-museum. It’s not the real thing, but still awesome.
