from app.forms import validate_contact


def csrf_token(client):
    client.get("/contact")
    with client.session_transaction() as session:
        return session["csrf_token"]


def test_invalid_contact_values_are_rejected():
    errors, _ = validate_contact({"name": "", "email": "nope", "message": "short"})
    assert set(errors) == {"name", "email", "message"}


def test_valid_contact_values_are_accepted():
    errors, values = validate_contact({"name": "Ada Lovelace", "email": "ada@example.com", "message": "I would like to discuss a junior developer opportunity."})
    assert errors == {}
    assert values["name"] == "Ada Lovelace"


def test_contact_rejects_missing_csrf(client):
    response = client.post("/contact", data={"name": "Ada", "email": "ada@example.com", "message": "A sufficiently long message."})
    assert response.status_code == 400


def test_valid_form_discloses_delivery_limitation(client):
    response = client.post("/contact", data={"csrf_token": csrf_token(client), "name": "Ada", "email": "ada@example.com", "message": "A sufficiently long message for validation."})
    assert response.status_code == 200
    assert b"email delivery is not configured" in response.data
