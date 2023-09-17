import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

class SeleBardHelper:
    def init(self):
        print("Đang khởi động trình duyệt tự động hóa...")
        self.prompt_count = 0
        self.driver = uc.Chrome()
        self.driver.get("https://bard.google.com/?hl=en")

        while True:
            try:
                self.driver.find_elements(By.CSS_SELECTOR, "a.gb_wa.gb_gd.gb_Id.gb_ge.gb_j")[0].click()
            except:
                time.sleep(1)
            else:
                break

        input("\n\n--------------------\nĐăng nhập tài khoản Google, khi hoàn tất. Quay lại cửa sổ Console và bấm Enter để tiếp tục.\n--------------------\n\n")
        time.sleep(1)
        while True:
            if len(self.driver.find_elements(By.CSS_SELECTOR, "textarea.textarea")) == 0:
                self.driver.find_elements(By.CSS_SELECTOR, "terms-of-service.tos-button.ng-star-inserted")[0].click()
                while True:
                    try: self.driver.find_elements(By.CSS_SELECTOR, "button.more-button")[0].click()
                    except: time.sleep(1)

                    try: self.driver.find_elements(By.CSS_SELECTOR, "button.agree-button")[0].click()
                    except: time.sleep(1)
                    else: break
                    
                while True:
                    try: self.driver.find_elements(By.CSS_SELECTOR, "button.disclaimer-close-button")[0].click()
                    except: time.sleep(1)
                    else: break
            break

        self.input_field = self.driver.find_elements(By.CSS_SELECTOR, "textarea.textarea")[0]
        self.send_button = self.driver.find_elements(By.CSS_SELECTOR, "div.send-button-container.ng-star-inserted")[0]
    
    def prompt(self, text: str):
        
        self.input_field.send_keys(text)
        self.send_button.click()
        
        time.sleep(1)

        response_text = None
        while True:
            try:
                response_text = self.driver.find_elements(By.CSS_SELECTOR, "div.response-container-content")[self.prompt_count].get_attribute("innerText")
                if response_text != "":
                    break
            except:
                time.sleep(1)
        self.prompt_count += 1

        return response_text
    
    def close(self):
        self.driver.close()