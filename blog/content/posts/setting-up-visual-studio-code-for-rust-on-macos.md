+++
title = "Setting Up Visual Studio Code for Rust on macOS"
date = "2024-11-17T11:50:12+00:00"
draft = false
originalURL = "https://dev.to/yrizos/setting-up-visual-studio-code-for-rust-on-macos-95k"
tags = ["rust", "vscode", "beginners"]
+++

Setting up Visual Studio Code for Rust development is quick and straightforward. While I prefer PHPStorm for larger projects, VS Code is perfect for smaller ones. It’s fast, lightweight, and just works. For this guide, I’m assuming you already have [Rust installed via Homebrew](https://dev.to/yrizos/installing-rust-on-macos-with-homebrew-51fk).

## Step 1: Grab VS Code

Head over to [code.visualstudio.com](https://code.visualstudio.com/) and download VS Code. Follow the installation instructions provided for MacOS to set it up.

## Step 2: Create a Hello World Project with cargo

1. Open Terminal and create a new Rust project:

   ```
   cargo new hello_world
   ```
2. Navigate into the project folder:

   ```
   cd hello_world
   ```
3. Open the project in VS Code:

   ```
   code .
   ```

If this command doesn’t work, you may need to add VS Code to your PATH. Open the Command Palette (⇧ + ⌘ + P), type "Shell Command," and select "Install 'code' command in PATH." Then try again.

## Step 3: Add the Rust Analyzer Extension

1. Open VS Code and press ⇧ + ⌘ + X to open the Extensions view.
2. Search for "Rust Analyzer" and click **Install**.

Rust Analyzer provides features like syntax highlighting, error checking, and improved code navigation.

Once the extension is installed, open the `main.rs` file located in the `src` folder of your project. You should now see:

* Syntax highlighting: Keywords, variables, and functions are coloured differently for better readability.
* Inline error checking: If there are issues in your code, they will be underlined in red, with detailed error messages displayed when you hover over the issue.
* Code completion: Start typing and you’ll see a list of suggestions based on the context.

To test the error checking feature, introduce a simple mistake in your code. For example, change the line:

```
println!("Hello, world!");
```

to:

```
rintln!("Hello, world!");
```

You’ll immediately see an error indicating that Rust cannot find macro `rintln`.

## Step 4: Set up auto-formatting

1. Enable auto-formatting in VS Code:
   * Open the settings (⌘ + ,).
   * Search for "Format On Save."
   * Enable the "Editor: Format On Save" option.

This ensures your code is automatically formatted whenever you save. To test auto-formatting, open `main.rs` and intentionally mess up the formatting. For instance, write:

```
fn main( ){println!("Hello, world!");}
```

Save the file. Auto-formatting will fix it immediately, and your code will look like this:

```
fn main() {
    println!("Hello, world!");
}
```

## Step 5: Run your program with cargo

1. Open the integrated terminal in VS Code by pressing ⌃ + `` ` `` (Control and backtick).
2. Run the program:

   ```
   cargo run
   ```
3. You should see the output:

   ```
   Hello, world!
   ```

And there you have it. Your setup is ready, and you’re all set to dive into Rust development with VS Code. Time to build something amazing!
