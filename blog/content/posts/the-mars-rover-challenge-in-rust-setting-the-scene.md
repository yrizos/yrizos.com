+++
title = "The Mars Rover Challenge in Rust: Setting the Scene"
date = "2024-11-18T11:52:03+00:00"
draft = false
originalURL = "https://dev.to/yrizos/the-mars-rover-challenge-in-rust-setting-the-scene-49l8"
tags = ["rust", "beginners", "kata"]
+++

As a Rust beginner, I was looking for a project that would both teach me the language fundamentals and keep me engaged. The Mars Rover Challenge fits perfectly - it's an intriguing problem that simulates robotic exploration of Mars while introducing key programming concepts.

## Setting the Scene

Imagine controlling rovers tasked with exploring the Martian terrain. These rovers need to navigate a rectangular plateau while sending visual data back to Earth. The challenge involves translating simple commands into precise rover movements, and dealing with positioning, orientation, and grid-based navigation.

## The Challenge

A squad of robotic rovers is to be landed by NASA on a plateau on Mars.

This plateau, which is curiously rectangular, must be navigated by the rovers so that their onboard cameras can get a complete view of the surrounding terrain to send back to Earth. A rover's position is represented by a combination of x and y co-ordinates and a letter representing one of the four cardinal compass points. The plateau is divided up into a grid to simplify navigation. An example position might be `0, 0, N`, which means the rover is in the bottom left corner and facing North.

In order to control a rover, NASA sends a simple string of letters. The possible letters are `L`, `R`, and `M`. `L` and `R` make the rover spin 90 degrees left or right respectively, without moving from its current spot.

`M` means move forward one grid point and maintain the same heading.

Assume that the square directly North from `(x, y)` is `(x, y+1)`.

### Input:

The first line of input is the upper-right coordinates of the plateau. The lower-left coordinates are assumed to be `0,0`.  
The rest of the input is information pertaining to the rovers that have been deployed. Each rover has two lines of input. The first line gives the rover's position, and the second line is a series of instructions telling the rover how to explore the plateau.  
The position is made up of two integers and a letter separated by spaces, corresponding to the x and y coordinates and the rover's orientation.

Each rover will be finished sequentially, which means that the second rover won't start to move until the first one has finished moving.

### Output:

The output for each rover should be its final coordinates and heading.

### Test Input:

```
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

### Test Output:

```
1 3 N
5 1 E
```

## Breaking Down the Requirements

Let's analyze what we're dealing with:

1. **The Environment**

   * A rectangular plateau defined by coordinates
   * Grid-based movement system
   * Origin point (0,0) at bottom-left
2. **Rover Capabilities**

   * Position tracking (x,y coordinates)
   * Cardinal direction orientation (N,E,S,W)
   * Three basic commands:
     + Rotate left 90° (L)
     + Rotate right 90° (R)
     + Move forward one grid unit (M)
3. **System Behavior**

   * Sequential rover movement (one at a time)
   * Position updates after each move
   * Boundary awareness required
   * Final position reporting

## Why This is Great for Learning

This challenge touches on several fundamental Rust concepts:

* Enums (for directions and commands)
* Structs (for rover and plateau representation)
* Error handling (for boundary violations)
* String parsing
* Vector operations
* Testing

P.S. If you'd like to dive straight into the code, you can find the implementation on [GitHub](https://github.com/yrizos/mars-rover-rs).
