There really isn’t a “memory-corruption” or “integer-overflow” trick hiding in `score` — it’s just a plain Python integer in MicroPython, so:

1. **No overflow/underflow**: Python ints auto–grow, so you can’t wrap it around.
2. **Not externally writable**: it lives entirely inside the game’s local frame; there’s no API or global that lets you stomp on it.
3. **Only way to change it** is via the two code-paths the author put in:

   * **+1 per line** under normal play
   * **+1 and flip into “1000-per-line” mode** if you enter the secret control sequence

In short, the only “shortcut” is the built-in secret multiplier Easter-egg. There’s no unintended vulnerability in `score` itself — just that author-designed cheat code.


The “secret multiplier” is actually gated behind the classic **Konami code**.  Under the hood the game:

1. Keeps a rolling buffer of the last 10 button events in a list called `FAST32`.
2. At startup it builds a hidden sequence of ten control‐IDs by slicing two embedded strings (“HELP ME I AM BEING ENSLAVED …” and “ITS MY FIRST DAY …”), feeding those chars through `ord(c)-65`, and storing the result in `FAST36`.
3. On every move it does:

   ```python
   FAST32.append(current_button_id)
   FAST32.pop(0)
   ```
4. Then it checks

   ```python
   if FAST32 == FAST36[::-1]:
       # SECRET MULTIPLIER ACTIVE!
       score += 1
       increment = 1000
   ```

   And from then on each dropped block adds `increment` (1000) points instead of 1.

When you decode those ten chars you get

```
FAST36[::-1]  == [1,1,3,3,0,4,0,4,6,5]
```

which maps to

```
[up, up, down, down, left, right, left, right,  B,  A]
   ↑      ↑      ↓       ↓      ←       →    ←      →     B    A
```

So **to turn on the 1000-point multiplier**, simply enter:

```
Up, Up, Down, Down, Left, Right, Left, Right, B, A
```

Once you see

```
SECRET MULTIPLIER ACTIVE!
```

drop one or two bricks (so your score jumps past 9 998), and you’ll immediately get the `grey{go_do_this_on_stage}` message.
