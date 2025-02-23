import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='en',
                     help='Choose language: en, ru, fr, etc...')

@pytest.fixture(scope='function')
def browser(request):
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")
    browser = None
    
    if browser_name == 'chrome':
        print('\nstart chrome browser for test..')
        options = ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
    elif browser_name == 'firefox':
        print('\nstart firefox browser for test..')
        options = FirefoxOptions()
        options.set_preference("intl.accept_languages", user_language)
        service = Service(GeckoDriverManager().install())
        browser = webdriver.Firefox(service=service, options=options)
    else:
        raise pytest.UsageError('--browser_name should be chrome or firefox')
    
    yield browser
    print('\nquit browser..')
    browser.quit()

