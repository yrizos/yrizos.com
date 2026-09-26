+++
title = "Two Hours to Find a Swapped String"
date = "2025-11-14T02:16:25+00:00"
draft = false
type = "posts"
canonical_url = "https://dev.to/yrizos/two-hours-to-find-a-swapped-string-4jba"
tags = ["ddd", "valueobject", "types"]
+++

Early in my career, I landed a job where I was finally writing production code that mattered. The company had an ERP system and an e-commerce platform, and needed them to communicate with each other. My job was to build the integration layer that would keep product data flowing between them.

The requirements seemed straightforward enough. The ERP would send product information, my system would translate it, and the store would receive it. Both systems used product codes to identify items, and since those codes looked like ordinary strings, I treated them as ordinary strings. That's what the rest of the codebase did, and it felt like the natural choice.

```ts
function bridgeItem(erpCode: string, storeCode: string) {
  const record = readErp(erpCode);
  return writeStore(storeCode, record);
}
```

The function signatures looked clean. The calls looked reasonable.

```ts
bridgeItem(product.code, mapping.targetCode);
```

As a sidenote, TypeScript didn't exist back then. The actual code was Java, but I _really don't love Java_.

## For a While, Everything Worked Fine

Then, one afternoon, a product stopped appearing in the store. It should have been a quick fix. I expected to find some data validation issue or maybe a network timeout. Instead, I spent nearly two hours jumping between files trying to understand what had gone wrong. The system had multiple layers (controllers, services, helpers, integration adapters) and every function accepted plain strings. Nothing in the signatures gave me any hint about which string represented which concept.

By the time I traced the problem to its source, I discovered I'd passed the store code where the ERP code should have been. The function had accepted both values without complaint because they were both strings. The type system had nothing to say about it. I fixed the bug in about thirty seconds. Then I sat there feeling annoyed that I'd wasted two hours on something so trivial.

I remember thinking there had to be a better way to write this kind of code. Not some grand revelation. Just frustration mixed with the feeling that my tools should have caught this.

## The Pattern Kept Appearing

Once I noticed the problem, I started seeing it everywhere in the codebase. We had product codes from the ERP, internal codes used only within our system, and store codes required by the e-commerce platform. Each type of code followed different validation rules and represented a completely different concept, but they all looked identical to TypeScript's type system.

```ts
type ProductCode = string;
type InternalCode = string;
type StoreCode = string;
```

These type aliases were essentially documentation. They described intent without enforcing anything. The compiler treated them all as interchangeable strings, which meant I could accidentally pass one where another belonged, and the code would compile without warnings.

Boolean flags created similar confusion. One boolean meant the product was ready for sync. Another suggested it was active in the store. Another indicated whether the last sync had completed successfully. The names tried to communicate meaning, but the function signatures offered no protection.

```ts
if (isReady && isActive && isSynced) {
  runSync();
}
```

Numbers presented their own challenges. Some represented milliseconds, others represented seconds, and others represented retry attempts. Without examining the implementation, you couldn't tell which unit a function expected.

```ts
function scheduleRetry(delay: number) {
  setTimeout(runRetry, delay);
}
```

Calling this function with the wrong unit would compile successfully and fail at runtime.

```ts
scheduleRetry(5);
```

The pattern was consistent. I was using primitive types to represent domain concepts, and then compensating by scattering validation logic throughout the codebase.

## Learning It Had a Name

A few years later, I was reading about common code smells when I came across an article on Refactoring Guru that described exactly what I'd been doing. It seems I was [obsessed with primitives](https://refactoring.guru/smells/primitive-obsession):

> Primitive Obsession is a code smell that arises when simple primitive types are used instead of small objects for simple tasks

Reading that article felt like finding out other people had been dealing with the same problem. I hadn't invented a new way to write confusing code. I'd been following a well-documented antipattern. The validation checks I'd scattered everywhere, the confusion about which string meant what, the hours spent tracing values through multiple files: all of it was a predictable consequence of representing meaningful domain concepts as primitive types.

## What I Would Do Differently Now

If I were building that old system today, I'd give each domain concept its own type. A product code wouldn't just be a string. It would be a class that knew how to validate itself and made its purpose explicit. In Domain-Driven Design, these are called Value Objects: small types defined by their attributes rather than any identity.

```ts
class ProductCode {
  private readonly value: string;

  constructor(value: string) {
    if (value.trim() === "") {
      throw new Error("Invalid product code");
    }
    this.value = value;
  }

  raw(): string {
    return this.value;
  }
}
```

With this structure, the function signature communicates much more clearly what it expects.

```ts
function bridgeItem(
  erpProductCode: ProductCode,
  storeProductCode: ProductCode,
) {
  const record = readErp(erpProductCode.raw());
  return writeStore(storeProductCode.raw(), record);
}
```

If I tried to pass a store code where an ERP code belonged, TypeScript would catch it immediately. The type system could finally help instead of staying silent.

The same approach works for other domain concepts. Time values become clearer when they carry their unit with them.

```ts
class Milliseconds {
  private readonly value: number;

  constructor(value: number) {
    if (value < 0) throw new Error("Negative time not allowed");
    this.value = value;
  }

  raw(): number {
    return this.value;
  }
}
```

Now the scheduling function's signature tells you exactly what it needs.

```ts
function scheduleRetry(delay: Milliseconds) {
  setTimeout(runRetry, delay.raw());
}
```

You can't accidentally pass seconds or retry counts. The compiler won't allow it.

Some domain concepts benefit from carrying behavior alongside their data. A dimensions class can validate its inputs and calculate derived values.

```ts
class Dimensions {
  constructor(
    public readonly width: number,
    public readonly height: number,
  ) {
    if (width <= 0 || height <= 0) {
      throw new Error("Invalid dimensions");
    }
  }

  area(): number {
    return this.width * this.height;
  }
}
```

Each class enforces its own invariants. The validation logic lives in one place instead of being duplicated across the codebase.

## Why This Approach Helps

Once you start wrapping primitives in domain-specific types, several things improve. You stop writing the same validation checks in multiple places. You stop worrying about mixing up parameters. Function signatures become self-documenting. The type system starts working with you instead of being indifferent to your mistakes.

Martin Fowler discusses Value Objects in his [summary of the Evans classification](https://martinfowler.com/bliki/EvansClassification.html). The key insight is that Value Objects are defined by their attributes rather than their identity. Two `ProductCode` instances with the same internal value are functionally equivalent, which is exactly what you want for this kind of domain modeling.

A monetary value makes a good example of this pattern in action.

```ts
class Money {
  private readonly amount: number;

  constructor(amount: number) {
    if (amount < 0) throw new Error("Invalid amount");
    this.amount = amount;
  }

  raw(): number {
    return this.amount;
  }
}
```

Functions that work with money become more explicit about their contracts.

```ts
function publish(price: Money, discount: Money) {
  return applyRules(price, discount);
}
```

The signatures tell you what's expected. The classes enforce the rules. The compiler catches mismatches.

## Where This Pattern Fits

This approach scales well across different types of systems. It works in integration layers where data crosses boundaries. It works in domain-rich applications where business rules matter. It works anywhere the cost of confusion exceeds the cost of creating a few extra classes.

Rico Fritzsche demonstrates these patterns in realistic scenarios in his [example-driven walkthrough](https://ricofritzsche.me/value-objects-implementing-domain-driven-design-by-example). His examples show how small domain types compose together in more complex flows.

Here's another example that keeps validation close to the data.

```ts
class EmailAddress {
  private readonly value: string;

  constructor(value: string) {
    if (!value.includes("@")) throw new Error("Invalid email");
    this.value = value;
  }

  raw(): string {
    return this.value;
  }
}
```

Each type makes its constraints explicit. Each type protects its own invariants. The result is code where intent is visible and mistakes are harder to make.

## What I Took From the Experience

I never went back and rewrote that old integration system. By the time I understood the pattern well enough to know how I'd fix it, the project had moved on, and so had I. But the experience stuck with me. Those two hours I spent tracking down a swapped parameter taught me more than any blog post could have.

These days, I try to use Value Objects by default. Not because of some architectural dogma. Not because Domain-Driven Design says so, though that's where they come from. Because the work becomes easier when domain concepts have an explicit structure. The code reads better. The compiler helps more. The bugs show up earlier.

Domain-Driven Design gave Value Objects their formal name and placed them within a larger framework, but the practical benefit stands on its own. When you stop representing meaningful concepts as primitive types, the code becomes easier to reason about.

That's worth the extra few lines of class definition.
