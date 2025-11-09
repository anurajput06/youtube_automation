# tests/conftest.py
import os
import pytest

# will hold reference to pytest-html plugin
pytest_html = None

def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    On test failure, save screenshot (if there is a 'driver' fixture)
    and attach it to the HTML report using pytest-html extras.image.
    """
    outcome = yield
    report = outcome.get_result()

    # only act when the test call finished and it failed
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")  # our fixture name
        if driver:
            # ensure folder exists
            screenshots_dir = os.path.join(os.path.dirname(__file__), "..", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            # screenshot file name
            screenshot_path = os.path.join(screenshots_dir, f"screenshot_{item.name}.png")

            try:
                driver.save_screenshot(screenshot_path)
            except Exception as e:
                print(f"Could not save screenshot: {e}")
                return

            # attach to html report (if plugin available)
            if pytest_html:
                try:
                    extra = getattr(report, "extra", [])
                    # use pytest_html.extras.image to embed image
                    extra.append(pytest_html.extras.image(screenshot_path))
                    report.extra = extra
                except Exception as e:
                    print(f"Could not attach screenshot to report: {e}")
