"""Automated tests for index.html.

These tests read the HTML file as text and inspect it with Python's
built-in HTMLParser, so no browser is needed.
Run with:  python -m pytest -v
"""

from html.parser import HTMLParser
from pathlib import Path

import pytest

HTML_FILE = Path(__file__).parent / "index.html"


class FormParser(HTMLParser):
    """Collects the <form> tag, <input> tags and <button> tags of the page."""

    def __init__(self):
        super().__init__()
        self.forms = []
        self.inputs = []
        self.buttons = []
        self._in_button = False
        self._current_button = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)  # a bare attribute like "required" becomes None
        if tag == "form":
            self.forms.append(attributes)
        elif tag == "input":
            self.inputs.append(attributes)
        elif tag == "button":
            self._in_button = True
            self._current_button = {"attrs": attributes, "text": ""}

    def handle_data(self, data):
        if self._in_button:
            self._current_button["text"] += data

    def handle_endtag(self, tag):
        if tag == "button" and self._in_button:
            self.buttons.append(self._current_button)
            self._in_button = False
            self._current_button = None


@pytest.fixture(scope="module")
def page():
    """Parse index.html once and share the result with all tests."""
    parser = FormParser()
    parser.feed(HTML_FILE.read_text(encoding="utf-8"))
    return parser


def find_input(page, field_id):
    """Return the attributes of the <input> with the given id, or None."""
    for attributes in page.inputs:
        if attributes.get("id") == field_id:
            return attributes
    return None


def test_html_file_exists():
    assert HTML_FILE.is_file(), "index.html was not found"


def test_page_contains_form(page):
    assert len(page.forms) >= 1, "No <form> tag found in index.html"


def test_name_input_exists(page):
    field = find_input(page, "name")
    assert field is not None, "Name input (id='name') not found"
    assert field.get("type") == "text"
    assert field.get("name") == "name"


def test_email_input_exists(page):
    field = find_input(page, "email")
    assert field is not None, "Email input (id='email') not found"
    assert field.get("type") == "email", "Email input must use type='email'"
    assert field.get("name") == "email"


def test_contact_input_exists(page):
    field = find_input(page, "contact")
    assert field is not None, "Contact Number input (id='contact') not found"
    assert field.get("type") == "tel"
    assert field.get("name") == "contact"


def test_submit_button_exists(page):
    submit_buttons = [
        b for b in page.buttons if b["attrs"].get("type") == "submit"
    ]
    submit_inputs = [i for i in page.inputs if i.get("type") == "submit"]
    assert submit_buttons or submit_inputs, "No submit button found"
    if submit_buttons:
        assert submit_buttons[0]["text"].strip() == "Submit"


@pytest.mark.parametrize("field_id", ["name", "email", "contact"])
def test_required_attribute_present(page, field_id):
    field = find_input(page, field_id)
    assert field is not None, f"Input '{field_id}' not found"
    assert "required" in field, f"Input '{field_id}' must have the 'required' attribute"


def test_contact_number_validation(page):
    field = find_input(page, "contact")
    assert field is not None
    assert field.get("pattern") == "[0-9]{10}", "Contact needs pattern='[0-9]{10}'"
    assert field.get("maxlength") == "10", "Contact needs maxlength='10'"
