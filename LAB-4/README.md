# Real-Time Simple Platformer Game

This project is a terminal-based platformer using **Pygame**. It introduces students to interactive game design using object-oriented principles and real-time graphical rendering.

---

## What’s Provided

A partially working version of a platformer with:
Space
- A player-controlled character with left/right movement, gravity, and jumping
- A small hand-built level of platforms with gaps and one hazard
- Score display

You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Clone the repo or download the project folder.
2. Make sure you have Python 3.10+ installed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the game:

```bash
python main.py
```

---


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Refine Collision Detection

> The player sometimes falls straight through a platform instead of landing on it, especially after a long fall. Investigate and enhance collision accuracy so landings register reliably regardless of fall speed.


### Task 2: Implement Game Over Condition

> Add a screen that displays the final score once the player falls off the bottom of the screen or touches a hazard, then gracefully waits for input instead of just printing to the console.


### Task 3: Add Replay Option

> After Game Over, allow the user to play again by choosing a difficulty (Easy, Medium, or Hard gravity/jump strength), or exit.


### Task 4: Add Sound Feedback

> Add basic sound effects for jumping, reaching the goal, and dying.


---

## Expected Behavior

- Smooth left/right movement using `Left`/`Right` or `A`/`D`, and jumping with `Space`/`Up`/`W`
- Gravity pulls the player down and platforms stop the fall when landed on from above
- Touching the hazard or falling off the bottom of the screen ends the game
- Reaching the goal at the right edge increases the score and sends the player back to the start
- Score is visible on screen at all times

---

## Folder Structure

```
simple-platformer-main/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── player.py
│   ├── platform.py
│   └── hazard.py
└── README.md
```

---

## Changes Made

### Task 1: Collision Detection (`game/game_engine.py`)
- Bug: collision was checked only *after* the player moved for the frame, using a plain rect overlap, so a fast fall could carry the player from above a platform to below it in one frame without the rects ever touching (tunneling).
- Fix: swept collision check — compare the player's bottom edge before and after moving (`prev_bottom`, `new_bottom`) against each platform's top, and land whenever the feet crossed the platform's top during that frame's movement, combined with a horizontal overlap check.
- Added a terminal velocity cap (`vy` capped at 20) so fall speed doesn't grow unbounded.

### Task 2: Game Over Screen (`game/game_engine.py`)
- Removed the `print()` debug statement.
- Added `render_game_over()`: dark overlay, "Game Over" title, final score, and an on-screen prompt.
- Added `reset()` and updated `handle_event()` to wait for SPACE/ENTER instead of ending silently.

### Task 3: Replay with Difficulty (`game/game_engine.py`, `main.py`)
- Added a `DIFFICULTIES` mapping (keys 1/2/3 → Easy/Medium/Hard, each with its own gravity and jump strength).
- Game-over screen now shows difficulty options and an ESC-to-exit option.
- `reset()` accepts the chosen difficulty and applies it; `main.py`'s loop checks `engine.quit` to exit cleanly.

### Task 4: Sound Effects (`game/game_engine.py`, `game/sounds/`)
- Generated three short WAV tones (`jump.wav`, `goal.wav`, `death.wav`) from Python's stdlib `wave` module — no external assets needed.
- Added `_load_sounds()` with a silent fallback if no audio device is available.
- Wired sounds: jump on an actual jump, goal chime on reaching the goal, death tone on hazard touch or falling off-screen.

### Other tweaks
- Reduced the hazard's width (100 → 40) and recentered it so it sits fully on its platform.
- Added `chat_history.md` — exported summary of the LLM pair-programming session used for this lab.

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
