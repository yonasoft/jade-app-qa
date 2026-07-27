# Jade QA Suite

Automated end-to-end test suite for [Jade Dictionary](https://jadedictionary.com/) — a Chinese-English dictionary web app — built with **Playwright** and **Pytest**.

This suite is a living project. Coverage is being built out incrementally, prioritized by core user value first. See [Coverage Status](#coverage-status) below for what's tested today vs. planned.

---

## Tech Stack

- **Python 3.14**
- **Playwright** (sync API) — browser automation
- **pytest** + **pytest-playwright** — test runner and Playwright/pytest integration
- **pytest-timeout** — guards against hanging tests
- **Ruff** — linting and formatting

---

## Project Structure

```
jade-qa/
├── conftest.py                 # shared fixtures (start_home_page, practice_page, list_with_five_words, etc.)
├── pytest.ini                  # pytest config (base_url, timeout, etc.)
├── components/
│   └── page_search_bar.py      # shared search bar component (used across Home, Search page, Practice)
├── pages/
│   ├── base_page.py            # shared base class for Page Objects
│   └── home_page.py            # HomePage Page Object
├── tests/
│   ├── home_and_search/
│   │   ├── test_links.py       # navigation links, external links (Play Store, Support), Word of the Day
│   │   └── test_search.py      # multi-mode search (Chinese/pinyin/English, numbered & toned pinyin)
│   └── practice/
│       ├── setup/
│       │   ├── test_setup_hsk.py       # HSK-level word bank setup
│       │   ├── test_setup_lists.py     # word bank from user Lists
│       │   ├── test_setup_search.py    # word bank via in-Practice search
│       │   └── test_setup_combined.py  # combining multiple sources, dedup checks
│       ├── modes/               # one file per practice mode (flashcard, multiple-choice, etc.)
│       ├── test_practice_session.py    # TBA — shared session mechanics
│       ├── test_practice_results.py    # TBA — results screen
│       ├── test_smart_review.py        # TBA
│       └── test_weak_review.py         # TBA
└── test_data/                   # structured test data (e.g. nav link tables)
```

---

## Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install pytest-playwright playwright pytest-timeout -U
python -m playwright install
```

## Running Tests

```powershell
# run everything
python -m pytest

# run a specific file
python -m pytest tests/home_and_search/test_search.py

# watch it run in a real browser, slowed down
python -m pytest --headed --slowmo=500

# debug a failure with full trace
python -m pytest --tracing=retain-on-failure
playwright show-trace trace.zip
```

---

## Coverage Status

### ✅ Covered
- **Navigation** — all main nav links, footer links, external links (Android/Play Store, Support) with correct new-tab handling
- **Word of the Day** — navigation and content-match verification against the homepage card
- **Search** — Home page search bar, multi-mode (Smart / Chinese / Pinyin / English), numbered vs. toned pinyin handling, result pagination
- **Practice — word bank setup** — HSK level selection (count & browse modes, randomized selection), My Lists source, in-Practice search source, combined-source deduplication

### 🚧 In Progress
- **Practice modes** — Flashcard and Multiple Choice (deep coverage); Listening, Match, Tones, Handwriting (shallow smoke tests)
- **Practice session mechanics** — shared start/answer/exit flow
- **Practice results screen** — score, retry, "study missed words"

### 📋 Planned (TBA)
- Translate page
- Sign in / auth flows
- Lists page (full CRUD — create/rename/delete lists and folders, not just the setup-fixture usage in Practice)
- Stats page
- Settings page
- Search modal (shared popup search accessible from non-home pages)
- Smart Review (`/practice/review`) and Weak Review (`/practice/weak`) entry points
- CI/CD integration (GitHub Actions) — **not yet wired up**, tests currently run locally only
- Custom HTML/Allure test reporting

---

## Notes & Known Limitations

- Tests currently run against the **live production site** (`app.jadedictionary.com`), not a staging/local environment — occasional flakiness has been traced to live-site responsiveness rather than test bugs.
- Some locators fall back to CSS class selectors where no accessible role/label/`data-testid` exists on the underlying component; these are more brittle to UI/styling changes than role-based locators and are flagged for `data-testid` follow-up in the app itself.
- `get_all_search_results()` (full pagination sweep) exists but is not used by default in most tests due to runtime cost — most tests use `get_search_results()` (first page only).
- Chromium only for now — cross-browser (Firefox/WebKit) runs not yet part of the regular suite.

---

## Why This Project Exists

Built as a hands-on portfolio project to demonstrate real-world Playwright/Pytest test automation — Page Object Model architecture, fixture-based test isolation, parametrized testing, and independent debugging of real automation defects (locator ambiguity, same-tab vs. new-tab navigation, inconsistent DOM structure across dynamic content).
