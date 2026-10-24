"""Small dependency-free validation for the contact form."""
from email.utils import parseaddr


def validate_contact(data):
    errors = {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()
    if not 2 <= len(name) <= 100:
        errors["name"] = "Please enter a name between 2 and 100 characters."
    if len(email) > 254 or "@" not in parseaddr(email)[1]:
        errors["email"] = "Please enter a valid email address."
    if not 10 <= len(message) <= 2000:
        errors["message"] = "Please enter a message between 10 and 2,000 characters."
    return errors, {"name": name, "email": email, "message": message}
