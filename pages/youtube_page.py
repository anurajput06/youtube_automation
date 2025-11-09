# pages/youtube_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.config_reader import read_config

class YouTubePage:
    # selectors
    SEARCH_BOX = (By.NAME, "search_query")
    SEARCH_BOX_ALT = (By.NAME, "search")
    VIDEO_RENDERER = (By.XPATH, "//ytd-video-renderer")
    VIDEO_TITLE_ANCHOR = (By.CSS_SELECTOR, "a#video-title")
    THUMBNAIL_LINK = (By.CSS_SELECTOR, "ytd-thumbnail a")

    def __init__(self, driver, timeout=None):
        self.driver = driver
        cfg = read_config()
        # default explicit wait from config or fallback to 20s
        default_timeout = cfg.getint("explicit_wait", 25) if timeout is None else timeout
        self.wait = WebDriverWait(driver, default_timeout)

    def open_home(self, base_url):
        self.driver.get(base_url)
        # small pause to allow scripts to start
        time.sleep(1)
        self.try_accept_cookies()

    def try_accept_cookies(self):
        # basic cookie/consent attempts
        cookie_selectors = [
            (By.XPATH, "//button[contains(., 'Accept all')]"),
            (By.XPATH, "//button[contains(., 'I agree')]"),
            (By.XPATH, "//button[contains(., 'Accept')]"),
            (By.XPATH, "//ytd-button-renderer//paper-button[contains(., 'I agree')]")
        ]
        for sel in cookie_selectors:
            try:
                btn = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(sel))
                btn.click()
                time.sleep(0.5)
                return
            except Exception:
                pass

    def _find_search_box(self):
        for sel in (self.SEARCH_BOX, self.SEARCH_BOX_ALT):
            try:
                el = self.wait.until(EC.presence_of_element_located(sel))
                # ensure visible/clickable
                self.wait.until(EC.element_to_be_clickable(sel))
                return el
            except Exception:
                continue
        raise Exception("Search box not found")

    def search_video(self, keyword):
        box = self._find_search_box()
        try:
            box.clear()
        except Exception:
            pass
        box.send_keys(keyword)
        box.send_keys(Keys.RETURN)

        # Wait strategy after pressing Enter:
        # 1) wait for results container presence
        # 2) wait for at least one video title to be visible
        try:
            # presence of renderer means results are returned
            self.wait.until(EC.presence_of_element_located(self.VIDEO_RENDERER))
        except Exception:
            # fallback short sleep
            time.sleep(3)

        # ensure at least one visible and clickable video title (longer wait)
        try:
            self.wait.until(EC.visibility_of_element_located(self.VIDEO_TITLE_ANCHOR))
            # extra: wait until the first anchor is clickable
            self.wait.until(EC.element_to_be_clickable(self.VIDEO_TITLE_ANCHOR))
        except Exception:
            # if it still fails, do a short incremental polling fallback
            end = time.time() + (self.wait._timeout if hasattr(self.wait, "_timeout") else 20)
            while time.time() < end:
                elems = self.driver.find_elements(*self.VIDEO_TITLE_ANCHOR)
                if elems and elems[0].is_displayed():
                    break
                time.sleep(0.5)

    def get_video_titles(self):
        try:
            self.wait.until(EC.presence_of_all_elements_located(self.VIDEO_TITLE_ANCHOR))
        except Exception:
            pass
        elems = self.driver.find_elements(*self.VIDEO_TITLE_ANCHOR)
        titles = [e.text.strip() for e in elems if e.text.strip()]
        return titles

    def click_first_video(self):
        # Wait for at least one renderer & anchor to be visible/clickable
        self.wait.until(EC.presence_of_element_located(self.VIDEO_RENDERER))
        self.wait.until(EC.visibility_of_element_located(self.VIDEO_TITLE_ANCHOR))
        self.wait.until(EC.element_to_be_clickable(self.VIDEO_TITLE_ANCHOR))

        elems = self.driver.find_elements(*self.VIDEO_TITLE_ANCHOR)
        if not elems:
            raise Exception("No video anchors found")
        first = elems[0]
        # scroll into view and click (with JS fallback)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first)
            time.sleep(0.3)
            first.click()
            # wait for video url
            self.wait.until(EC.url_contains("watch"))
            return
        except Exception:
            try:
                self.driver.execute_script("arguments[0].click();", first)
                self.wait.until(EC.url_contains("watch"))
                return
            except Exception as e:
                # final fallback: open href directly
                href = first.get_attribute("href")
                if href:
                    self.driver.get(href)
                    self.wait.until(EC.url_contains("watch"))
                    return
                raise Exception("Failed to open first video: " + str(e))
