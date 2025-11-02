+++
title = "The Mars Rover Challenge in Rust: Let's Get Moving!"
date = "2024-11-18T11:52:37+00:00"
draft = false
canonical_url = "https://dev.to/yrizos/the-mars-rover-challenge-in-rust-lets-get-moving-3a32"
tags = ["r", "u", "s", "t", ",", " ", "b", "e", "g", "i", "n", "n", "e", "r", "s", ",", " ", "k", "a", "t", "a"]
+++

Now that the challenge is clear, it's time to start coding.

To kick things off, I got my project set up using Cargo – nothing fancy, just the basics:

```bash
cargo new mars-rover-rust
cd mars-rover-rust
```

## Charting the Course: Defining Directions

First up, I needed to figure out how our little rover would know which way it's facing. I went with the classics here – good old North, East, South, and West. Here's how I set that up in Rust:

```rust
// src/direction.rs
#[derive(Debug, PartialEq)]
pub enum Direction {
    NORTH,
    EAST,
    SOUTH,
    WEST,
}
```

Pretty straightforward, right? I added those `Debug` and `PartialEq` traits since I knew we'd want to peek at these values during debugging and compare them in our tests.

## Steering the Rover: Implementing Turns

Now for the fun part – teaching our rover how to turn! I created a `Rover` struct and gave it some basic turning abilities:

```rust
// src/rover.rs
use crate::direction::Direction;

#[derive(Debug, PartialEq)]
pub struct Rover {
    x: i32,
    y: i32,
    direction: Direction,
}

impl Rover {
    pub fn new(x: i32, y: i32, direction: Direction) -> Self {
        Rover { x, y, direction }
    }

    pub fn turn_left(&mut self) {
        self.direction = match self.direction {
            Direction::NORTH => Direction::WEST,
            Direction::WEST => Direction::SOUTH,
            Direction::SOUTH => Direction::EAST,
            Direction::EAST => Direction::NORTH,
        };
    }

    pub fn turn_right(&mut self) {
        self.direction = match self.direction {
            Direction::NORTH => Direction::EAST,
            Direction::EAST => Direction::SOUTH,
            Direction::SOUTH => Direction::WEST,
            Direction::WEST => Direction::NORTH,
        };
    }
}
```

Of course, I had to make sure our rover could actually turn properly, so I wrote some tests to put it through its paces:

```rust
// src/rover.rs
#[cfg(test)]
mod tests {
    use super::*;
    use crate::direction::Direction;

    #[test]
    fn test_turn_left() {
        let mut rover = Rover::new(0, 0, Direction::NORTH);
        rover.turn_left();
        assert_eq!(rover.direction, Direction::WEST);
        rover.turn_left();
        assert_eq!(rover.direction, Direction::SOUTH);
        rover.turn_left();
        assert_eq!(rover.direction, Direction::EAST);
        rover.turn_left();
        assert_eq!(rover.direction, Direction::NORTH);
    }

    #[test]
    fn test_turn_right() {
        let mut rover = Rover::new(0, 0, Direction::NORTH);
        rover.turn_right();
        assert_eq!(rover.direction, Direction::EAST);
        rover.turn_right();
        assert_eq!(rover.direction, Direction::SOUTH);
        rover.turn_right();
        assert_eq!(rover.direction, Direction::WEST);
        rover.turn_right();
        assert_eq!(rover.direction, Direction::NORTH);
    }
}
```

A quick `cargo test` lets us know if everything's working as planned.

## Mapping the Terrain: Setting Up the Plateau

Here's where things got interesting – I realized our rover needed some boundaries to roam within. Can't have it wandering off into space! So I created a `Plateau` to keep it in check:

```rust
// src/plateau.rs
#[derive(Debug, PartialEq)]
pub struct Plateau {
    width: i32,
    height: i32,
}

impl Plateau {
    pub fn new(width: i32, height: i32) -> Self {
        Plateau { width, height }
    }

    pub fn is_within_bounds(&self, x: i32, y: i32) -> bool {
        x >= 0 && x <= self.width && y >= 0 && y <= self.height
    }
}
```

## Advancing the Rover: Moving Forward

With our playground set up, it was time to teach our rover how to actually move around:

```rust
// src/rover.rs
use crate::plateau::Plateau;

impl Rover {
    pub fn move_forward(&mut self, plateau: &Plateau) {
        let (new_x, new_y) = match self.direction {
            Direction::NORTH => (self.x, self.y + 1),
            Direction::EAST => (self.x + 1, self.y),
            Direction::SOUTH => (self.x, self.y - 1),
            Direction::WEST => (self.x - 1, self.y),
        };

        if plateau.is_within_bounds(new_x, new_y) {
            self.x = new_x;
            self.y = new_y;
        }
    }
}
```

And naturally, we needed to make sure it behaves:

```rust
// src/rover.rs
#[cfg(test)]
mod tests {
    use super::*;
    use crate::plateau::Plateau;

    #[test]
    fn test_move_forward_within_bounds() {
        let plateau = Plateau::new(5, 5);
        let mut rover = Rover::new(0, 0, Direction::NORTH);
        rover.move_forward(&plateau);
        assert_eq!(rover.x, 0);
        assert_eq!(rover.y, 1);
    }

    #[test]
    fn test_move_forward_out_of_bounds() {
        let plateau = Plateau::new(5, 5);
        let mut rover = Rover::new(0, 0, Direction::SOUTH);
        rover.move_forward(&plateau);
        assert_eq!(rover.x, 0);
        assert_eq!(rover.y, 0);
    }
}
```

## Commanding the Rover: Processing Instructions

Finally, the piece that brings it all together – teaching our rover to follow commands:

```rust
// src/rover.rs
impl Rover {
    pub fn execute_commands(&mut self, commands: &str, plateau: &Plateau) {
        for command in commands.chars() {
            match command {
                'L' => self.turn_left(),
                'R' => self.turn_right(),
                'M' => self.move_forward(plateau),
                _ => {},
            }
        }
    }
}
```

And here's the grand finale of our test suite:

```rust
// src/rover.rs
#[cfg(test)]
mod tests {
    use super::*;
    use crate::direction::Direction;
    use crate::plateau::Plateau;
    use crate::instruction::Instruction;

    // Existing tests...

    #[test]
    fn test_execute_instructions() {
        let plateau = Plateau::new(5, 5);
        let mut rover = Rover::new(1, 2, Direction::NORTH, &plateau);
        let instructions = [
            Instruction::LEFT, Instruction::MOVE, Instruction::LEFT, Instruction::MOVE,
            Instruction::LEFT, Instruction::MOVE, Instruction::LEFT, Instruction::MOVE,
            Instruction::MOVE
        ];
        rover.execute_instructions(&instructions);
        assert_eq!(rover.x, 1);
        assert_eq!(rover.y, 3);
        assert_eq!(rover.direction, Direction::NORTH);

        let mut rover = Rover::new(3, 3, Direction::EAST, &plateau);
        let instructions = [
            Instruction::MOVE, Instruction::MOVE, Instruction::RIGHT, Instruction::MOVE,
            Instruction::MOVE, Instruction::RIGHT, Instruction::MOVE, Instruction::RIGHT,
            Instruction::RIGHT, Instruction::MOVE
        ];
        rover.execute_instructions(&instructions);
        assert_eq!(rover.x, 5);
        assert_eq!(rover.y, 1);
        assert_eq!(rover.direction, Direction::EAST);
    }
}
```

---

And there you have it! Our Mars Rover is now ready to explore its virtual plateau. I've got to say, as someone still getting their feet wet with Rust, seeing this all come together has been incredibly satisfying. The code might not be perfect by Rust standards, but hey, it works!

Next up on my list is handling user input and prettifying the output. But that's a story for another day!
