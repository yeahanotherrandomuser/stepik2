import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption("--language", action="store", default="en",
                     help="Browser interface language, e.g. --language=en")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run Chrome without a window")


@pytest.fixture(scope="function")
def browser(request):
    language = request.config.getoption("language")
    options = Options()
    options.add_experimental_option("prefs", {"intl.accept_languages": language})
    options.add_argument("--window-size=1400,1000")
    if request.config.getoption("headless"):
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
