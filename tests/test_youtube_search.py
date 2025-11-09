# tests/test_youtube_search.py
import pytest
import time
from selenium.webdriver.common.by import By
from utils.driver_factory import get_driver, read_config
from pages.youtube_page import YouTubePage

@pytest.fixture
def driver():
    d = get_driver()
    yield d
    d.quit()

def test_youtube_search_and_open_first(driver):
    cfg = read_config()
    base_url = cfg.get("base_url")
    keyword = cfg.get("search_keyword")

    yt = YouTubePage(driver)
    yt.open_home(base_url)
    yt.search_video(keyword)

    # print top 3 titles for debug
    titles = yt.get_video_titles()
    print("Found titles:", titles[:5])

    # Try normal click first (uses your page object's method)
    try:
        yt.click_first_video()
    except Exception as e:
        print("click_first_video() failed with:", e)
        print("Falling back to href navigation...")

        # FALLBACK: locate the first anchor and navigate directly to its href
        anchors = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
        if not anchors:
            raise Exception("No video anchors found to open via href fallback")
        first_href = anchors[0].get_attribute("href")
        if not first_href:
            raise Exception("First anchor has no href attribute")
        print("Navigating directly to:", first_href)
        driver.get(first_href)

    # wait a bit to let video page load
    time.sleep(4)
    assert "watch" in driver.current_url, f"Expected video page, got {driver.current_url}"
    print("Video page opened successfully:", driver.current_url)
