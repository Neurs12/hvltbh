from getpass import getpass
import requests, json

def request_login() -> dict:
    email = ""
    while email == "":
        email = input("Nhập tài khoản HVLTLB: ")

    password = ""
    while password == "":
        password = getpass("Nhập mật khẩu: ")
    
    login = json.loads(requests.post("https://api.hocvalamtheobac.vn/v1/auth/login", json={"email": email, "password": password}).text)

    if login["result"] == False:
        print("Lỗi: {} Vui lòng thử lại.\n\n".format(login["data"]))
        return request_login()

    if login["data"]["user"]["completed"] == False:
        print("Vui lòng cập nhật thông tin trên trang để tiếp tục!\n\n")
        return request_login()
    
    print("Đang tải thông tin...")

    dashboard_data = json.loads(requests.get("https://api.hocvalamtheobac.vn/v1/users/dashboard", headers={"Authorization": "Bearer {}".format(login["data"]["token"])}).text)

    if dashboard_data["real_exam"] == {}:
        print("Tài khoản đã hết lượt thi! Thử tài khoản khác.\n\n")
        return request_login()

    return {
        "token": login["data"]["token"],
        "exam_user_id": dashboard_data["real_exam"]["exam_user_id"]
    }