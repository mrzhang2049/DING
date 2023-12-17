from DrissionPage import ChromiumPage
from DataRecorder import Recorder
page = ChromiumPage()
page.get('https://www.cnblogs.com/')
page.get_screenshot(path='tmp.png', left_top= (100, 20), right_bottom=(350, 300))
#page.get_screenshot(path='tmp', full_page=True)

