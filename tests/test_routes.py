import pytest


@pytest.mark.parametrize("path", ["/", "/about", "/projects", "/contact"])
def test_core_pages_return_success(client, path):
    assert client.get(path).status_code == 200


def test_homepage_has_identity_and_navigation(client):
    response = client.get("/")
    assert b"Milad Ahmad" in response.data
    assert b"Junior Python Developer | Backend &amp; Automation" in response.data
    assert b"Explore projects" in response.data


def test_projects_has_honest_empty_state(client):
    response = client.get("/projects")
    assert b"No verified public projects yet" in response.data


def test_unknown_path_uses_custom_404(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert b"This page has wandered off" in response.data


def test_seo_endpoints(client):
    assert b"User-agent" in client.get("/robots.txt").data
    assert b"urlset" in client.get("/sitemap.xml").data


def test_unexpected_error_is_safe(app):
    @app.route("/_test-error")
    def test_error_route():
        raise RuntimeError("private implementation detail")

    app.config.update(TESTING=False, PROPAGATE_EXCEPTIONS=False)
    response = app.test_client().get("/_test-error")
    assert response.status_code == 500
    assert b"private implementation detail" not in response.data
    assert b"Something went wrong" in response.data
