# Mastermind for the TI-84 Evo
# Guess the secret code of 4 colours in 10 tries.
# After each guess:  white = right colour in the right place,
#                    grey  = right colour in the wrong place.
# Keys: LEFT/RIGHT = choose a peg, UP/DOWN = change its colour,
#       enter = check the guess, clear = quit
import random
from ti_draw import clear, set_color, draw_text
from ti_draw import fill_rect as ti_fill_rect
try:
    from ti_draw import get_screen_dim
    SW, SH = get_screen_dim()
except:
    SW, SH = 319, 209

# Keep every box inside the screen and never stop the game over one box.
# The Evo draws boxes 1 pixel too small, so we ask for 1 pixel more.
def fill_rect(x, y, w, h):
    if x < 0:
        w, x = w + x, 0
    if y < 0:
        h, y = h + y, 0
    w, h = min(w, SW - x), min(h, SH - y)
    if w > 0 and h > 0:
        try:
            ti_fill_rect(x, y, w + 1, h + 1)
        except:
            pass
# Draw in a hidden buffer and show the finished picture at once: no flicker
try:
    from ti_draw import use_buffer, paint_buffer
    use_buffer()
except:
    paint_buffer = None
try:
    from ti_system import get_key as read_key
except:
    from ti_system import getKey as read_key
# On the Evo get_key wants one number. Find out once at the start.
try:
    read_key()
    key = read_key
except TypeError:
    def key():
        return read_key(0)
try:
    from ti_system import store_list, recall_list
except:
    store_list = recall_list = None
try:
    from time import sleep
except:
    from ti_system import sleep
try:
    import gc
except:
    gc = None

LEFT = (2, 24)
RIGHT = (1, 26)
UP = (3, 25)
DOWN = (4, 34)
OK = (5, 105)                 # enter
SECOND = (21, 22)             # 2nd, mode
QUIT = (9, 45)                # clear
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
YELLOW = (255, 220, 0)

def paint():
    if paint_buffer:
        paint_buffer()

def write(x, y, s):                    # text that can never stop the game
    try:
        draw_text(x, y, s)
    except:
        pass

def wait_for(keys):
    paint()
    while True:
        k = key()
        if k in keys:
            return k
        sleep(0.05)

# Numbers saved in a calculator list, so they stay after quitting
def load(name, n):
    try:
        l = [int(v) for v in recall_list(name)]
    except:
        l = []
    return (l + [0] * n)[:n]

def save(name, l):
    try:
        store_list(name, l)
    except:
        pass

# Text panel on the right side: rows 30 px high, the whole row is wiped first
def text(row, s, col=WHITE):
    set_color(*BLACK)
    fill_rect(TX, row * 30, SW - TX, 29)
    set_color(*col)
    write(TX, row * 30 + 22, s)

def box_frame(x, y, w, h, t, col):     # a frame t pixels thick
    set_color(*col)
    fill_rect(x, y, w, t)
    fill_rect(x, y + h - t, w, t)
    fill_rect(x, y, t, h)
    fill_rect(x + w - t, y, t, h)

def title_screen(name, col, line):
    clear()
    set_color(*BLACK)
    fill_rect(0, 0, SW, SH)
    set_color(*col)
    write(SW // 2 - 80, 25, name)
    set_color(*WHITE)
    write(SW // 2 - 80, 55, line)

# A menu on the start screen. Returns the chosen number, or -1 for clear.
def menu(options, choice, hint):
    x = SW // 2 - 80
    set_color(*BLACK)
    fill_rect(0, 64, SW, SH - 64)
    set_color(*WHITE)
    write(x, 202, hint)
    while True:
        for i in range(len(options)):
            set_color(*BLACK)
            fill_rect(x - 20, 64 + i * 28, 230, 27)
            set_color(*(YELLOW if i == choice else GREY))
            write(x, 90 + i * 28, ("> " if i == choice else "  ") + options[i])
        k = wait_for(UP + DOWN + OK + QUIT)
        if k in QUIT:
            return -1
        if k in OK:
            return choice
        if k in UP:
            choice = (choice - 1) % len(options)
        if k in DOWN:
            choice = (choice + 1) % len(options)

COLORS = [(230, 0, 0), (0, 190, 0), (0, 90, 255), (255, 220, 0), (170, 0, 220), (255, 140, 0)]
PEGS, TRIES = 4, 10
ROW = 20                      # row height
P = 16                        # peg size
X0 = 8
Y0 = (SH - TRIES * ROW) // 2
FX = X0 + PEGS * 22 + 6       # feedback squares
TX = FX + 30                  # text panel (black, so text is fine)
EMPTY = (60, 60, 60)

def peg(row, k, col):
    set_color(*col)
    fill_rect(X0 + k * 22, Y0 + row * ROW + 2, P, P)

def mark(row, k, col):         # small feedback square, 2 x 2 per row
    set_color(*col)
    fill_rect(FX + (k % 2) * 9, Y0 + row * ROW + 2 + (k // 2) * 9, 7, 7)

def frame(row, k, col):
    box_frame(X0 + k * 22 - 2, Y0 + row * ROW, P + 4, P + 4, 2, col)

def check(guess, secret):      # (right place, right colour wrong place)
    exact = sum(1 for k in range(PEGS) if guess[k] == secret[k])
    both = sum(min(guess.count(c), secret.count(c)) for c in range(len(COLORS)))
    return exact, both - exact

def start_screen(stats):
    title_screen("MASTERMIND", COLORS[4], "Won " + str(stats[0]) + " of " + str(stats[1]))
    x = SW // 2 - 80
    for i, s in enumerate(["Guess 4 colours", "in 10 tries.", "White = right place", "Grey = wrong place"]):
        write(x, 90 + i * 25, s)
    set_color(*YELLOW)
    write(x, 200, "ENTER: start")
    return wait_for(OK + QUIT) in OK

def game():                    # returns True win, False lose, None quit
    secret = [random.randrange(len(COLORS)) for k in range(PEGS)]
    clear()
    set_color(*BLACK)
    fill_rect(0, 0, SW, SH)
    for r in range(TRIES):
        for k in range(PEGS):
            peg(r, k, EMPTY)
    text(0, "MASTERMIND")
    text(2, "UP/DOWN:")
    text(3, "colour")
    text(4, "ENTER:")
    text(5, "check")
    text(6, "CLEAR:quit")
    guess = [0] * PEGS
    for row in range(TRIES):
        k = 0
        for j in range(PEGS):
            peg(row, j, COLORS[guess[j]])
        frame(row, k, YELLOW)
        while True:
            paint()
            key_ = key()
            if not key_:
                sleep(0.03)
                continue
            if key_ in QUIT:
                return None
            if key_ in OK:
                break
            frame(row, k, BLACK)
            if key_ in LEFT:
                k = (k - 1) % PEGS
            elif key_ in RIGHT:
                k = (k + 1) % PEGS
            elif key_ in UP:
                guess[k] = (guess[k] + 1) % len(COLORS)
            elif key_ in DOWN:
                guess[k] = (guess[k] - 1) % len(COLORS)
            peg(row, k, COLORS[guess[k]])
            frame(row, k, YELLOW)
        frame(row, k, BLACK)
        exact, near = check(guess, secret)
        for m in range(exact):
            mark(row, m, WHITE)
        for m in range(exact, exact + near):
            mark(row, m, GREY)
        if exact == PEGS:
            return True
    # show the secret code in the panel
    text(2, "The code:")
    for t in (3, 4, 5):
        text(t, "")
    for k in range(PEGS):
        set_color(*COLORS[secret[k]])
        fill_rect(TX + k * 22, 100, P, P)
    return False

# --- start ---
stats = load("MASTR", 2)       # [wins, games]
if start_screen(stats):
    while True:
        won = game()
        if won is None:
            break
        stats[1] += 1
        if won:
            stats[0] += 1
        save("MASTR", stats)
        text(0, "YOU WIN!" if won else "TOO BAD", YELLOW)
        text(6, "ENTER:again")
        if wait_for(OK + QUIT) in QUIT:
            break
paint()
