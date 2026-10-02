# rc-reborn-claimer

Automatically claims [Restaurant City Reborn](https://rc-reborn.uk) share links (`https://rc-reborn.uk/s/...`).

Paste a chunk of Discord chat into a text file and the script will:
1. Pick out every share link. Names, timestamps and duplicate links are ignored.
2. Open each link in Chrome and click the green **Claim** button.
3. Skip links that are already claimed or have no Claim button.
4. Remember finished links so they're never opened twice.

## Requirements

- [Python 3.10+](https://www.python.org/downloads/) (on Windows, tick "Add python.exe to PATH" when installing)
- [Google Chrome](https://www.google.com/chrome/)
- [Git](https://git-scm.com/downloads), or use **Code → Download ZIP** on GitHub instead
- A Restaurant City Reborn account

## Setup (once)

Open a terminal (PowerShell on Windows) and run:

```
git clone https://github.com/tobiasceg/rc-reborn-claimer.git
cd rc-reborn-claimer
python -m venv .venv
```

Then install the dependencies.

**Windows:**
```
.venv\Scripts\python -m pip install -r requirements.txt
```

**macOS / Linux:**
```
.venv/bin/python -m pip install -r requirements.txt
```

## Log in (once)

**Windows:** `.venv\Scripts\python claim.py --login`
**macOS / Linux:** `.venv/bin/python claim.py --login`

A Chrome window opens on rc-reborn.uk. Log in there (Discord login works), then go back to the terminal and press **Enter**.
Your login is saved in the `browser-profile/` folder, so you only do this again if it expires.

> **Discord login sends you to the Discord app instead of an "Authorize" page?**
> That's normal the first time. In the same window, go to `https://rc-reborn.uk/login` and click the Discord login again. The Authorize button will appear.

## Claim links

1. In Discord, select the messages with the links and copy them (Ctrl+C).
2. Paste them into a file called `links.txt` in this folder. Messy text is fine, and you can keep adding to the same file over time.
3. Run:

**Windows:** `.venv\Scripts\python claim.py`
**macOS / Linux:** `.venv/bin/python claim.py`

Add `--headless` to run without showing the browser window.

Example output:
```
3 new link(s) to process
[1/3] https://rc-reborn.uk/s/... -> claimed
[2/3] https://rc-reborn.uk/s/... -> skipped (already claimed)
[3/3] https://rc-reborn.uk/s/... -> skipped (no Claim button)
```

If it prints `Not logged in`, run the `--login` step again.

## Files

| File | What it is | Share it? |
|---|---|---|
| `claim.py` | The script | yes |
| `links.txt` | Your pasted Discord text | no (git-ignored) |
| `claimed.txt` | Links already handled | no (git-ignored) |
| `browser-profile/` | **Your saved login.** Anyone with this folder can use your account | **never** (git-ignored) |

## Notes

- Fan-made helper, not affiliated with Restaurant City Reborn, Playfish or EA. Use it responsibly and follow the site's terms.
- The script only reads links you paste in. It does not connect to your Discord account.
