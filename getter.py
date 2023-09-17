import requests, json, seleAI, re, time

def test_riel(exam_data: dict):
    return run_test(exam_data["token"], f"https://api.hocvalamtheobac.vn/v1/exams/prepare?exam_user_id={exam_data['exam_user_id']}")

def test_demo(exam_data: dict):
    return run_test(exam_data["token"], "https://api.hocvalamtheobac.vn/v1/exams/testing")
    

def run_test(token, url):
    print("Đang thiết lập...")
    exam = json.loads(requests.get(url, headers={"Authorization": f"Bearer {token}"}).text)
    questions_options_raw = []

    for question in exam["questions"]:
        questions_options_raw.append({
            "question_id": question["id"],
            "question": question["content"],
            "options_string": " ".join(["[{}]. {}".format(option["option_id"], option["title"]) for option in question["options"]])
        })
    
    submit_context = {
        "exam_instance_id": exam["exam_instance_id"],
        "is_submit":True,
        "questions": send_to_AI(questions_options_raw, exam["exam_instance_id"], token)
    }

    print("Đang nộp bài...")

    while True:
        try:
            res = requests.put("https://api.hocvalamtheobac.vn/v1/exams/submit", json=submit_context, headers={"Authorization": f"Bearer {token}"})
            if res.status_code == 200:
                input(f"Nộp bài thành công!\n\nKiểm tra điểm của bạn trên trang chủ!\nEnter để kết thúc chương trình.")
                break
        except:
            print("Không thể gửi, đang thử lại...")
            time.sleep(1)


def send_to_AI(questions_options_raw, exam_instance_id, token):
    sle = seleAI.SeleBardHelper()
    sle.init()

    ans = []
    for ask in questions_options_raw:
        while True:
            try:
                ans.append({
                    "question_id": ask["question_id"],
                    "selected_id": re.findall(r'\[[0-9]+\]', sle.prompt(f"Chọn câu trả lời cho câu hỏi sau về Việt Nam, bao gồm cả ID câu trả lời. Ví dụ: \"[ID]. Xin chào\": {ask['question']} {ask['options_string']}"))[0].split("[")[1].split("]")[0]
                })
                print(f"Cập nhật ({len(ans)} / 30): {ans}")
                if len(ans) == 20:
                    print("Đang yêu cầu bắt đầu chạy thời gian test...")
                    while True:
                        try:
                            if requests.post("https://api.hocvalamtheobac.vn/v1/exams/start", json={"exam_instance_id": exam_instance_id}, headers={"Authorization": f"Bearer {token}"}) .status_code == 200:
                                print("Tiếp tục...")
                                break
                        except:
                            print("Không thể gửi, đang thử lại...")
                            time.sleep(1)
            except Exception as e:
                print(e)
                print("Đã xảy ra lỗi! Đang thử lại sau 5 giây...")
                time.sleep(5)
            else:
                break
    
    sle.close()
    return ans