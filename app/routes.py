import secrets
from datetime import date
from flask import Blueprint, abort, current_app, render_template, request, session, url_for

from app.content import (COURSES, EDUCATION, EXPERIENCE, INTERESTS, LANGUAGES,
                         PROFILE, PROJECTS, SKILLS, SUMMARY)
from app.forms import validate_contact

portfolio = Blueprint("portfolio", __name__)


@portfolio.app_context_processor
def inject_globals():
    return {"profile": PROFILE, "current_year": date.today().year, "configured_profiles": {k: v for k, v in PROFILE["profiles"].items() if v}}


def page(template, title, description, **context):
    return render_template(template, page_title=title, page_description=description, **context)


@portfolio.route("/")
def index():
    return page("index.html", PROFILE["site_title"], PROFILE["site_description"], summary=SUMMARY, skills=SKILLS[:6], projects=PROJECTS[:3])


@portfolio.route("/about")
def about():
    return page("about.html", "About | " + PROFILE["name"], "Work history, education, skills, and learning for Milad Ahmad Hakimi.", summary=SUMMARY, experience=EXPERIENCE, education=EDUCATION, skills=SKILLS, courses=COURSES, languages=LANGUAGES, interests=INTERESTS)


@portfolio.route("/projects")
def projects():
    return page("projects.html", "Projects | " + PROFILE["name"], "A growing collection of verified programming projects by Milad Ahmad Hakimi.", projects=PROJECTS)


@portfolio.route("/contact", methods=["GET", "POST"])
def contact():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    errors, values, notice = {}, {}, None
    if request.method == "POST":
        if not secrets.compare_digest(request.form.get("csrf_token", ""), session["csrf_token"]):
            abort(400)
        # Honeypot field: bots fill it; normal visitors never see it.
        if request.form.get("website"):
            return page("contact.html", "Contact | " + PROFILE["name"], "Get in touch with Milad Ahmad Hakimi.", errors={}, values={}, notice="Thanks. Please use the email link below to get in touch.")
        errors, values = validate_contact(request.form)
        if not errors:
            notice = "Your message is valid, but email delivery is not configured. Please use the email link below to send it directly."
    return page("contact.html", "Contact | " + PROFILE["name"], "Get in touch with Milad Ahmad Hakimi.", errors=errors, values=values, notice=notice, csrf_token=session["csrf_token"])


@portfolio.route("/robots.txt")
def robots():
    sitemap_url = (PROFILE["domain"].rstrip("/") + "/sitemap.xml") if PROFILE["domain"] else url_for("portfolio.sitemap", _external=True)
    return render_template("robots.txt", sitemap_url=sitemap_url), 200, {"Content-Type": "text/plain; charset=utf-8"}


@portfolio.route("/sitemap.xml")
def sitemap():
    urls = [url_for("portfolio.index", _external=True), url_for("portfolio.about", _external=True), url_for("portfolio.projects", _external=True), url_for("portfolio.contact", _external=True)]
    return render_template("sitemap.xml", urls=urls), 200, {"Content-Type": "application/xml; charset=utf-8"}


@portfolio.app_errorhandler(404)
def not_found(error):
    return page("404.html", "Page not found | " + PROFILE["name"], "The page you requested could not be found."), 404


@portfolio.app_errorhandler(400)
def bad_request(error):
    return page("500.html", "Request problem | " + PROFILE["name"], "The request could not be processed."), 400


@portfolio.app_errorhandler(500)
def server_error(error):
    current_app.logger.error("Unexpected server error")
    return page("500.html", "Something went wrong | " + PROFILE["name"], "An unexpected error occurred."), 500
