import hlogin, hoptions
import getter

print("Hocvalamtheoloibac cheat client. Source code available on https://github.com/Neurs12/hvltlb\n")

exam_data = hlogin.request_login()

if hoptions.request_confirm():
    getter.test_riel(exam_data)