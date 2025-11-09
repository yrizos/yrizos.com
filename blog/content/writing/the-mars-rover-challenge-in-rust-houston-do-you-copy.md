+++
title = "The Mars Rover Challenge in Rust: Houston, Do You Copy?"
date = "2024-11-18T11:59:45+00:00"
draft = false
type = "posts"
canonical_url = "https://dev.to/yrizos/the-mars-rover-challenge-in-rust-houston-do-you-copy-334o"
tags = ["rust", "beginners", "kata"]
+++

Our rover navigation system is ready for its maiden voyage, but first, it needs to know where to go! The mission parameters have provided specific test scenarios to validate our implementation. My rover needs to interpret these commands:

```plaintext
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

And respond with precise positional data:

```plaintext
1 3 N
5 1 E
```

## Establishing Communication: Receiving User Input 

My first challenge was creating a communication channel with Mission Control. I turned to Rust's powerful `std::io` module to establish this vital link:

```rust
// src/main.rs
mod direction;
mod instruction;
mod plateau;
mod rover;

use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();

    for line in lines {
        match line {
            Ok(content) => println!("{}", content),
            Err(error) => eprintln!("Error reading line: {}", error),
        }
    }
}
```

This foundational setup acts as our mission control interface. Think of it as a radio receiver - it picks up incoming transmissions (user input) and echoes them back for confirmation. The `std::io` module serves as our communications array, carefully monitoring each incoming signal and reporting any transmission errors.

To verify our communication systems, I ran some basic diagnostic tests:

```sh
cargo build
```

Followed by:

```sh
cargo run
```

Perfect clarity - the system faithfully relays every message it receives, confirming our communication link is operational.

## Mapping the Terrain: Parsing Plateau Dimensions

A rover without terrain data is like a ship without a map. I needed to interpret the first transmission - the dimensions of our Martian plateau:

```rust
// src/main.rs

// ...

fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();

    if let Some(Ok(plateau_dimensions)) = lines.next() {
        let plateau_parts: Vec<i32> = plateau_dimensions
            .split_whitespace()
            .map(|s| s.parse().unwrap())
            .collect();
        println!("Plateau dimensions: {:?}", plateau_parts);
    }
}
```

The process here is like a surveyor reading coordinates. When Mission Control transmits the plateau dimensions, my code acts as a digital cartographer. It takes the raw input string, splits it at the spaces (like separating latitude and longitude), and converts each piece into a numerical value our rover can understand. The result? A precise digital map of our operational territory.

## Setting the Scene: Parsing Rover's Initial State

With our terrain mapped, it's time to establish our rover's starting position. Each rover deployment needs three crucial pieces of information - its x and y coordinates on our digital map, and which way it's facing when it touches down:

```rust
// src/main.rs

// ...

fn main() {
    // ...

    if let Some(Ok(rover_initial)) = lines.next() {
        let rover_parts: Vec<&str> = rover_initial.split_whitespace().collect();
        let x: i32 = rover_parts[0].parse().unwrap();
        let y: i32 = rover_parts[1].parse().unwrap();
        let direction = match rover_parts[2] {
            "N" => Direction::NORTH,
            "E" => Direction::EAST,
            "S" => Direction::SOUTH,
            "W" => Direction::WEST,
            _ => panic!("Invalid direction"),
        };
        println!("Rover initial position: ({}, {}), Direction: {:?}", x, y, direction);
    }
}
```

This setup phase is like a pre-launch checklist. The code carefully parses the deployment coordinates, treating them like a spacecraft's landing coordinates. The direction indicator - N, E, S, or W - gets translated into our rover's internal compass, ensuring it knows exactly which way it's facing when it begins its mission.

## Commanding the Rover: Parsing Movement Instructions

Next came the most critical part of our mission control interface - interpreting the sequence of movement commands. Each instruction is like a carefully choreographed dance move, telling our rover to pirouette left (L), right (R), or march forward (M):

```rust
// src/main.rs

// ...

fn main() {
    // ...

    if let Some(Ok(instructions_line)) = lines.next() {
        let instructions: Vec<Instruction> = instructions_line
            .chars()
            .filter_map(Instruction::from_char)
            .collect();
        println!("Rover instructions: {:?}", instructions);
    }
}
```

Think of this as our rover's mission sequence - each character in the instruction line represents a specific maneuver. The code transforms these simple letters into actionable commands our rover can understand, like translating Morse code into clear instructions.

## Synchronizing the Mission: Integrating Components

With all our systems ready, it was time to bring everything together into a coordinated mission control center. Like launching a space mission, every component needs to work in perfect harmony:

```rust
// src/main.rs

mod direction;
mod instruction;
mod plateau;
mod rover;

use direction::Direction;
use instruction::Instruction;
use plateau::Plateau;
use rover::Rover;
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();

    let plateau_dimensions = lines.next().unwrap().unwrap();
    let plateau_parts: Vec<i32> = plateau_dimensions
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect();

    let rover_initial = lines.next().unwrap().unwrap();
    let rover_parts: Vec<&str> = rover_initial.split_whitespace().collect();
    let x: i32 = rover_parts[0].parse().unwrap();
    let y: i32 = rover_parts[1].parse().unwrap();
    let direction = match rover_parts[2] {
        "N" => Direction::NORTH,
        "E" => Direction::EAST,
        "S" => Direction::SOUTH,
        "W" => Direction::WEST,
        _ => panic!("Invalid direction"),
    };

    let instructions_line = lines.next().unwrap().unwrap();
    let instructions: Vec<Instruction> = instructions_line
        .chars()
        .filter_map(Instruction::from_char)
        .collect();

    let plateau = Plateau::new(plateau_parts[0], plateau_parts[1]);
    let mut rover = Rover::new(x, y, direction, &plateau);

    rover.execute_instructions(&instructions);
}
```

Like a well-orchestrated space mission, each piece plays its crucial role. First, we establish our terrain parameters, then position our rover, and finally load its mission instructions. Every component - from the plateau dimensions to the rover's directional systems - comes together in a seamless integration.

## Broadcasting the Results: Sharing Rover Outcomes

After each successful mission, Mission Control needs accurate position reports. I added some eyes to our rover:

```rust
// src/main.rs

// ...

fn main() {
    // ...

    println!("{} {} {:?}", rover.x(), rover.y(), rover.direction());
}
```

When I put this to the test with a sample mission:

```plaintext
5 5
1 2 N
LMLMLMLMM
```

The rover reported back:

```plaintext
1 3 NORTH
```

## Tuning the Details: Refining Output Format

Mission Control protocols are strict - they expect position reports in a specific format. `1 3 NORTH` wouldn't do - they need `1 3 N`. Time for some message formatting:

```rust
// src/direction.rs
#[derive(Debug, PartialEq)]
pub enum Direction {
    NORTH,
    EAST,
    SOUTH,
    WEST,
}

impl Direction {
    pub fn as_char(&self) -> char {
        match self {
            Direction::NORTH => 'N',
            Direction::EAST => 'E',
            Direction::SOUTH => 'S',
            Direction::WEST => 'W',
        }
    }
}
```

A quick update to our transmission format:

```rust
// src/main.rs

// ...

fn main() {
    // ...

    println!("{} {} {}", rover.x(), rover.y(), rover.direction().as_char());
}
```

## Final Touches: Managing Multiple Rovers

The real challenge emerged when Mission Control revealed their master plan - coordinating multiple rovers! Each rover would receive its own set of instructions:

```plaintext
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

Like an air traffic controller managing multiple aircraft, I needed to coordinate multiple rover operations:

```rust
// src/main.rs

// ...

fn main() {
    // ...

    let mut i = 1;
    while i < lines.len() {
        if i + 1 >= lines.len() {
            break;
        }

        let rover_initial = &lines[i];
        let rover_parts: Vec<&str> = rover_initial.split_whitespace().collect();
        let x: i32 = rover_parts[0].parse().unwrap();
        let y: i32 = rover_parts[1].parse().unwrap();
        let direction = match rover_parts[2] {
            "N" => Direction::NORTH,
            "E" => Direction::EAST,
            "S" => Direction::SOUTH,
            "W" => Direction::WEST,
            _ => panic!("Invalid direction"),
        };

        let instructions_line = &lines[i + 1];
        let instructions: Vec<Instruction> = instructions_line
            .chars()
            .filter_map(Instruction::from_char)
            .collect();

        let mut rover = Rover::new(x, y, direction, &plateau);
        rover.execute_instructions(&instructions);

        println!("{} {} {}", rover.x(), rover.y(), rover.direction().as_char());

        i += 2;
    }
}
```

When put to the test with our multi-rover scenario:

```plaintext
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

Mission accomplished! Each rover reported its position perfectly:

```plaintext
1 3 N
5 1 E
```

## Verifying the Expedition: Writing Integration Tests

Success is great, but in space exploration, we verify everything twice. I needed comprehensive tests to ensure our multi-rover coordination system worked flawlessly under all conditions:

```rust
// tests/integration_test.rs
use std::process::{Command, Stdio};
use std::io::Write;

#[test]
fn test_multiple_rovers() {
    let mut child = Command::new("cargo")
        .arg("run")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .expect("Failed to start cargo run");

    {
        let stdin = child.stdin.as_mut().expect("Failed to open stdin");
        let input = b"5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM\n";
        stdin.write_all(input).expect("Failed to write to stdin");
    }

    let output = child.wait_with_output().expect("Failed to read stdout");

    let expected_output = "1 3 N\n5 1 E\n";
    let actual_output = String::from_utf8_lossy(&output.stdout);

    assert_eq!(actual_output, expected_output);
}
```

This test suite acts like a mission simulator. It sends commands just like Mission Control would and verifies that our rovers respond exactly as expected. Think of it as a dress rehearsal for the real Mars mission - every command must execute perfectly, every position report must be precise.

I run the full battery of tests with:

```sh
cargo test
```

When every test passes, I know our rovers are ready for their Martian adventure. The integration tests confirm that our entire command and control system - from receiving instructions to coordinating multiple rovers to reporting positions - works in perfect harmony. This comprehensive testing approach ensures that when our rovers touch down on Mars, they'll execute their missions flawlessly, navigating the red planet's terrain with precision and reliability.

---

The journey through this challenge has finally reached its conclusion, and what a gratifying experience it turned out to be. While Rust Analyzer flags a couple of minor issues, the robust test suite provides confidence that these will be straightforward fixes.

The code is available for [perusal on Github](https://github.com/yrizos/mars-rover-rs), marking the end of this rewarding coding adventure.
