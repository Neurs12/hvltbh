import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import bardapi

class SeleBardHelper:
    def init(self):
        print("Đang khởi động trình duyệt tự động hóa...")
        driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("https://accounts.google.com/ServiceLogin?passive=true&continue=https://bard.google.com/")

        input("\n\n------------------------------------------------------------------------------------------------------------------------\nĐăng nhập tài khoản Google, chấp nhận điều khoản và vào trang chính, khi hoàn tất. Quay lại cửa sổ console và bấm Enter để tiếp tục.\n------------------------------------------------------------------------------------------------------------------------\n\n")

        cookies = driver.get_cookies()

        target_token = ""

        for cookie in cookies:
            if cookie["name"] == "__Secure-1PSID":
                target_token = cookie["value"]

        self.bardInter = bardapi.Bard(token=target_token)

        driver.close()
    
    def prompt(self, text: str):
        res = self.bardInter.get_answer(text)["content"]
        print("\n\n------------------------------------------------------ DEBUG RESPONSE ------------------------------------------------------\n\n")
        print(res, end="\n\n")
        print("\n------------------------------------------------------ DEBUG RESPONSE ------------------------------------------------------\n")
        return res
