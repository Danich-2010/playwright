Assertions
Introduction
Playwright includes web-specific assertions that automatically retry until the expected condition is met. Consider the following example:

expect(page.get_by_test_id("status")).to_have_text("Submitted")


Playwright will re-test the element with the test ID of status until it has the "Submitted" text. It will re-fetch the element and check it repeatedly until the condition is met or the timeout is reached.

By default, the timeout for assertions is 5 seconds.

Auto-retrying assertions
The following assertions will retry until the assertion passes or the assertion timeout is reached.

Assertion	Description
expect(locator).to_be_attached()	Element is attached
expect(locator).to_be_checked()	Checkbox is checked
expect(locator).to_be_disabled()	Element is disabled
expect(locator).to_be_editable()	Element is editable
expect(locator).to_be_empty()	Container is empty
expect(locator).to_be_enabled()	Element is enabled
expect(locator).to_be_focused()	Element is focused
expect(locator).to_be_hidden()	Element is not visible
expect(locator).to_be_in_viewport()	Element intersects viewport
expect(locator).to_be_visible()	Element is visible
expect(locator).to_contain_class()	Element has specified CSS classes
expect(locator).to_contain_text()	Element contains text
expect(locator).to_have_accessible_description()	Element has a matching accessible description
expect(locator).to_have_accessible_name()	Element has a matching accessible name
expect(locator).to_have_attribute()	Element has a DOM attribute
expect(locator).to_have_class()	Element has a class property
expect(locator).to_have_count()	List has exact number of children
expect(locator).to_have_css()	Element has CSS property
expect(locator).to_have_id()	Element has an ID
expect(locator).to_have_js_property()	Element has a JavaScript property
expect(locator).to_have_role()	Element has a specific ARIA role
expect(locator).to_have_text()	Element matches text
expect(locator).to_have_value()	Input has a value
expect(locator).to_have_values()	Select has options selected
expect(locator).to_match_aria_snapshot()	Element matches provided Aria snapshot
expect(page).to_have_title()	Page has a title
expect(page).to_have_url()	Page has a URL
expect(response).to_be_ok()	Response has an OK status
Soft assertions
By default, failed assertion will terminate test execution. Playwright also supports soft assertions: failed soft assertions do not terminate test execution, but mark the test as failed.

# Make a few checks that will not stop the test when failed...
expect.soft(page.get_by_test_id("status")).to_have_text("Success")
expect.soft(page.get_by_test_id("eta")).to_have_text("1 day")

# ... and continue the test to check more things.
page.get_by_role("link", name="next page").click()
expect.soft(page.get_by_role("heading", name="Make another order")).to_be_visible()


Note that soft assertions only work with the pytest-playwright (or pytest-playwright-asyncio) plugin, version 0.8.0 or newer.

Custom Expect Message
You can specify a custom expect message as a second argument to the expect function, for example:

expect(page.get_by_text("Name"), "should be logged in").to_be_visible()


When expect fails, the error would look like this:

    def test_foobar(page: Page) -> None:
>       expect(page.get_by_text("Name"), "should be logged in").to_be_visible()
E       AssertionError: should be logged in
E       Actual value: None
E       Call log:
E       LocatorAssertions.to_be_visible with timeout 5000ms
E       waiting for get_by_text("Name")
E       waiting for get_by_text("Name")

tests/test_foobar.py:22: AssertionError


Setting a custom timeout
You can specify a custom timeout for assertions either globally or per assertion. The default timeout is 5 seconds.

Global timeout
conftest.py
from playwright.sync_api import expect

expect.set_options(timeout=10_000)

Per assertion timeout
test_foobar.py
from playwright.sync_api import expect

def test_foobar(page: Page) -> None:
    expect(page.get_by_text("Name")).to_be_visible(timeout=10_000)