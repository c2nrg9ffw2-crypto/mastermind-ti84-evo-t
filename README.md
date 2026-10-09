# Mastermind for the TI-84 Evo-T

The code-breaking game **Mastermind** for the **TI-84 Evo-T** graphing calculator, written in Python.

> **Made with AI:** this game and this README were created with the help of AI (Claude by Anthropic).
> Everything was tested on a real TI-84 Evo-T.

## What is Mastermind?

The calculator hides a **secret code** of **4 colours**. You have **10 tries** to guess it.

- The colours are: red, green, blue, yellow, purple and orange.
- A colour **can appear more than once** in the code.
- After each guess, small squares tell you how close you are.

## What the small squares mean

| Square | Meaning |
|---|---|
| ⬜ **White** | One colour is **right** and in the **right place** |
| ◻️ **Grey** | One colour is **right**, but in the **wrong place** |
| (nothing) | The other colours aren't in the code |

The squares don't tell you **which** peg they mean. That's the puzzle!

### An example

Secret code: 🔴 🟢 🔵 🟡

Your guess: 🔴 🔵 🟠 🟠

Result: **1 white, 1 grey**
- 🔴 is right and in the right place → **white**
- 🔵 is in the code, but in the wrong place → **grey**
- 🟠 isn't in the code → nothing

**4 white squares = you win!** If you run out of tries, the calculator shows the code.

## What you need

- A **TI-84 Evo-T** calculator
- A USB cable to connect it to your computer
- **Google Chrome** or **Microsoft Edge** (Safari and Firefox do not work with the TI tool)
- The file [`mastmind.py`](mastmind.py) from this repo

The file is called **mastmind** because calculator program names can have at most 8 letters.

## Setup

1. Download [`mastmind.py`](mastmind.py) to your computer.
2. Connect the calculator to your computer with the USB cable.
   Leave the calculator on the **home screen**.
3. Open **https://connectevo.ti.com** in **Chrome** or **Edge**.
4. Connect to your calculator in the page and allow access when the browser asks.
5. Drag `mastmind.py` onto the page to send it to the calculator.
6. **Choose RAM** to play right away.
   The Python app on the Evo-T only shows files that are in RAM.
   (Want to keep the game safe? See [Don't lose the game](#dont-lose-the-game).)

> **Already sent it to Archive?** On the **home screen** (not in the Python app) press **2nd → mem → Mem Management**,
> find **MASTMIND** and press **enter**. The `*` in front of the name disappears, which means
> it is now in RAM.

## Start the game

1. Open the **Python** app on the calculator.
2. Choose **MASTMIND** and run it.
3. Press **enter** on the start screen.

## Keys

Your guess is the row with the **yellow frame**.

| Key | What it does |
|---|---|
| ◀ ▶ | Move the frame to another of the 4 pegs |
| ▲ ▼ | Change that peg's colour |
| enter | Check your guess |
| clear | Quit |

## Tips

1. **Start simple:** try 🔴 🔴 🟢 🟢. Then you know how many reds and greens are in the code.
2. **Change one thing at a time,** so you can see what made the result better or worse.

## Don't lose the game

The Evo-T **deletes RAM** when it stays turned off for a while.
A normal turn-off is fine, but after some time the game is gone.

**Best way:**

1. Keep the game in **Archive**. Archive is never deleted.
2. Go to the **home screen**. If you are in the Python app, leave it with **2nd → quit**
   (quit is above the **mode** key). In the Python app, **2nd → mem** does nothing.
3. Press **2nd → mem** (mem is above the **+** key) and choose **2: Mem Management**.
4. Choose the list with Python programs (or **All**).
5. Find **MASTMIND** and press **enter**. The `*` disappears, which means the game is now in RAM.
6. Open the **Python** app and play.

Programs can't move files between Archive and RAM by themselves, so this step can't be automatic.
The wins list **MASTR** is in RAM too, so it can be deleted the same way.

## Wins

Your wins and games are saved in a calculator list called **MASTR**, so they stay after you quit.
The start screen shows them.

- To reset them, delete the list **MASTR** in **2nd → mem → Mem Management** (on the home screen).
- A calculator reset (RAM clear) also resets them.

## Good to know

- Keep `mastmind.py` on your computer too, so you can always send it again.
- Made for the TI-84 Evo-T. Other TI-84 models are not tested.
