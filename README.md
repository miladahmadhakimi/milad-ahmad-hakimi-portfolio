# Milad Ahmad Hakimi — Developer Portfolio

A dark-first, server-rendered portfolio for **Milad Ahmad Hakimi**, a Junior Python Developer focused on backend development and automation. It presents CV-backed information accurately and intentionally leaves unverified projects and profile URLs unpublished.

## Stack and features

- Python, Flask, Jinja2, HTML, CSS, and small vanilla JavaScript interaction
- Responsive Home, About, Projects, and Contact pages; custom 404/500 pages
- Centralized profile and project content in `app/content.py`
- Downloadable CV, accessible mobile menu, skip link, visible focus states, and reduced-motion support
- Server-side form validation, CSRF token, honeypot, secure cookie defaults, security headers, sitemap, and robots file
- pytest route and form tests

## Structure

```text
app/                 Flask package, templates, CSS, JavaScript, CV
  content.py         Editable personal details, profile URLs, and project list
  routes.py          Page routes, validation flow, error and SEO endpoints
tests/               Automated tests
scripts/check_project.py  Basic structure and Python compilation check
app.py               Development entry point
config.py            Environment-aware application settings
```

## Run locally

Requires Python 3.10+.

```bash
cd /home/hakimi-milad-ahmad/Desktop/My_Python/Pro
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. `app.py` enables debug mode only for local development; use Gunicorn in production.

## Test and check

```bash
python -m pytest
python scripts/check_project.py
```

## Update content

Edit `app/content.py`:

- Set a verified `GitHub`, `LinkedIn`, `X`, or `Stack Overflow` URL in `PROFILE["profiles"]`. Empty values stay hidden deliberately.
- Set `PROFILE["domain"]` after purchasing/configuring a production domain; this enables canonical and Open Graph URLs.
- Add only verified work to `PROJECTS`. A project record should include `name`, `description`, `problem`, `technologies`, `features`, `learned`, `github`, optional `demo`, and `status`. Label course exercises clearly.
- Replace `app/static/files/milad-ahmad-hakimi-cv.pdf` only with the CV intended for public download.

## Contact form and security

The form validates data but **does not send or store messages**. It tells visitors to use the email link, avoiding misleading delivery claims. Before adding mail delivery, choose a reputable provider, use environment variables for credentials, and document retention/privacy practices.

Set a strong production key outside source control:

```bash
export SECRET_KEY='a-long-random-secret-value'
export FLASK_ENV=production
```

Jinja autoescaping remains enabled. The app limits request size, validates form values server-side, uses CSRF and a honeypot, and applies basic response headers. HTTPS belongs at the hosting platform or reverse proxy.

## Deploy with Render

1. Commit this folder to a GitHub repository (do not commit `.env`).
2. Create a **Web Service** in Render and connect the repository.
3. Use build command: `pip install -r requirements.txt`.
4. Use start command: `gunicorn --bind 0.0.0.0:$PORT app:app`.
5. Add a random `SECRET_KEY` and `FLASK_ENV=production` under Render environment variables.
6. Configure a custom domain in Render, update `PROFILE["domain"]`, redeploy, and verify pages, CV download, HTTPS, and form behavior.

## Content review checklist

- Supply verified social-profile URLs and a production domain.
- Add public projects only once their repositories and descriptions are ready.
- Confirm the future-dated course entries (June–October 2026) remain accurate when publishing; they are retained exactly as the CV states.
- Confirm that the included CV is suitable for public download.

## How it works

Flask receives a request and selects a route in `app/routes.py`. The route reads CV-backed content from `app/content.py` and renders a Jinja template. Templates share navigation, metadata, and footer through `base.html`; CSS and the small JavaScript file handle the visual layout and mobile navigation. This separation lets you update facts and projects without rewriting page layouts.

## Known limitations and future ideas

No verified public project entries, social URLs, production domain, email delivery, deployment, or formal accessibility audit exist yet. Good next improvements are adding original projects, configuring profiles/domain, integrating a privacy-conscious contact provider, adding visual accessibility checks, and expanding tests.
