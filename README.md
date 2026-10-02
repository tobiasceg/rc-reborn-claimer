# rc-reborn-claimer

Opens Restaurant City Reborn share links (`https://rc-reborn.uk/s/...`) and clicks **Claim**.

## Setup (once)
```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m playwright install chromium
.venv\Scripts\python claim.py --login     # log in in the window, then press Enter
```

## Use
1. In Discord, select the messages and copy them. Paste them into `links.txt`. Any text is fine; only the links are used.
2. Run `.venv\Scripts\python claim.py` (add `--headless` to hide the browser).

Links that are claimed, already claimed, or have no Claim button are written to `claimed.txt` and skipped on later runs.
