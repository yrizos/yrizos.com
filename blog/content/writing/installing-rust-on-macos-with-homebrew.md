+++
title = "Installing Rust on macOS with Homebrew"
date = "2024-11-17T09:28:59+00:00"
draft = false
canonical_url = "https://dev.to/yrizos/installing-rust-on-macos-with-homebrew-51fk"
tags = ["r", "u", "s", "t", ",", " ", "h", "o", "m", "e", "b", "r", "e", "w", ",", " ", "b", "e", "g", "i", "n", "n", "e", "r", "s"]
+++

This Sunday, I had a bit of extra time, so I decided to brush up on [Rust](https://www.rust-lang.org/). Whether you are a seasoned developer or just starting out, getting your tools set up is always the first step.

While Rust’s official installation tool, `rustup`, is excellent and versatile, I prefer using [Homebrew](https://brew.sh/) whenever possible. It is simple, familiar, and keeps everything neatly managed in one place. 

## Step 1: Install Rust

Launch the terminal and run the following command to install Rust:

```sh
brew install rust
```

This will install both Rust and Cargo, Rust’s package manager and build system. Cargo simplifies managing dependencies, building projects, and running tests in Rust. It is an essential tool for any Rust developer.

## Step 2: Verify the Installation

After installation, confirm everything is set up correctly by checking the Rust version:

```sh
rustc --version
cargo --version
```

If the command returns the Rust version number, you are all set!

## Step 3: Keeping Rust Updated

Homebrew makes it easy to update Rust when new versions are released. Periodically run the following commands to keep Rust up to date:

```sh
brew update
brew upgrade rust
```

That is it, you are ready to code in Rust! 🎉
