import hlogin, hoptions
import getter

print("Hocvalamtheoloibac cheat client. Source code available on https://github.com/Neurs12/hvltlb\n")

exam_data = hlogin.request_login()

print("Đăng nhập thành công!\n")

selected_option = hoptions.request_option()

test_result = [getter.test_riel, getter.test_demo][selected_option](exam_data)