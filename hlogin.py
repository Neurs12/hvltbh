from getpass import getpass
import requests, json

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"

def request_login() -> dict:
    email = ""
    while email == "":
        email = input("Nhập tài khoản HVLTLB: ")

    password = ""
    while password == "":
        password = getpass("Nhập mật khẩu: ")

    login = json.loads(requests.post("https://api.hocvalamtheobac.vn/v1/auth/login", headers={"User-Agent": USER_AGENT}, json={"email": email, "password": password}).text)

    if login["result"] == False:
        print(f"Lỗi: {login['data']} Vui lòng thử lại.\n\n")
        return request_login()

    if login["data"]["user"]["completed"] == False:
        print("Vui lòng cập nhật thông tin trên trang để tiếp tục!\n\n")
        return request_login()
    
    print("Đang tải thông tin...\n")

    dummy = requests.get("https://api.hocvalamtheobac.vn/v1/users/dashboard", headers={"User-Agent": USER_AGENT, "Authorization": f"Bearer {login['data']['token']}"}).text
    print(dummy)
    dashboard_data = json.loads(dummy)
    dummy = requests.get("https://api.hocvalamtheobac.vn/v1/users/results", headers={"User-Agent": USER_AGENT, "Authorization": f"Bearer {login['data']['token']}"}).text
    print(dummy)
    current_results = json.loads(dummy)

    print(f"\nTên: {dashboard_data['real_exam']['full_name']}\nVòng thi hiện tại: {dashboard_data['real_exam']['exam_name']}\nSố lượt thi thật còn lại: {dashboard_data['real_exam']['remaining_shot']}\n")

    if current_results["result"]:
        for overall in current_results['data']['results']:
            print(f"Kết quả {overall['round_name']}:")
            for result in overall["result"]:
                print(f"{result['title']} | {result['score']}")
            print()

    if dashboard_data["real_exam"] == {}:
        print("Tài khoản đã hết lượt thi! Thử tài khoản khác.\n\n")
        return request_login()

    return {
        "token": login["data"]["token"],
        "exam_user_id": dashboard_data["real_exam"]["exam_user_id"]
    }