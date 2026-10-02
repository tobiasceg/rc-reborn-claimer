"""Auto-claim Restaurant City Reborn share links.

Paste Discord messages (or bare links) into links.txt, then run:
    python claim.py            # claim every new link
    python claim.py --login    # open the site once so you can log in
"""
import argparse
import re
from pathlib import Path

from playwright.sync_api import TimeoutError as PwTimeout
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
LINKS_FILE = HERE / "links.txt"
DONE_FILE = HERE / "claimed.txt"
PROFILE_DIR = HERE / "browser-profile"  # keeps your login between runs

LINK_RE = re.compile(r"https://rc-reborn\.uk/s/[A-Za-z0-9]+")
CLAIM_BTN = "button.rc-btn.green:has-text('Claim')"


class NotLoggedIn(Exception):
    pass


def read_links():
    text = LINKS_FILE.read_text(encoding="utf-8") if LINKS_FILE.exists() else ""
    return list(dict.fromkeys(LINK_RE.findall(text)))  # dedupe, keep order


def read_done():
    if not DONE_FILE.exists():
        return set()
    return set(DONE_FILE.read_text(encoding="utf-8").split())


def mark_done(url):
    with DONE_FILE.open("a", encoding="utf-8") as f:
        f.write(url + "\n")


def claim(page, url):
    page.goto(url, wait_until="domcontentloaded")
    button = page.locator(CLAIM_BTN).first
    try:
        button.wait_for(state="visible", timeout=8000)
    except PwTimeout:
        if page.locator("a:has-text('Log in to continue')").count():
            raise NotLoggedIn()
        return "skipped (no Claim button)"
    if button.is_disabled():
        return "skipped (already claimed)"
    button.click()
    try:
        page.wait_for_function(
            "el => el.disabled", arg=button.element_handle(), timeout=10000
        )
    except PwTimeout:
        return "clicked, but button never became disabled - check manually"
    return "claimed"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--login", action="store_true", help="open the site to log in")
    parser.add_argument("--headless", action="store_true", help="hide the browser window")
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            PROFILE_DIR, headless=args.headless and not args.login
        )
        page = browser.pages[0] if browser.pages else browser.new_page()

        if args.login:
            page.goto("https://rc-reborn.uk/")
            input("Log in in the browser window, then press Enter here...")
            browser.close()
            return

        done = read_done()
        todo = [u for u in read_links() if u not in done]
        print(f"{len(todo)} new link(s) to process")

        for i, url in enumerate(todo, 1):
            try:
                result = claim(page, url)
            except NotLoggedIn:
                print("Not logged in - run: python claim.py --login")
                break
            except Exception as e:  # one bad link shouldn't stop the run
                result = f"error: {e}"
            print(f"[{i}/{len(todo)}] {url} -> {result}")
            if not result.startswith(("error", "clicked")):
                mark_done(url)

        browser.close()


if __name__ == "__main__":
    main()
