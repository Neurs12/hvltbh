import requests, json, seleAI, re, time, random

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"

def test_riel(exam_data: dict):
    return run_test(exam_data["token"], f"https://api.hocvalamtheobac.vn/v1/exams/prepare?exam_user_id={exam_data['exam_user_id']}")
    

def run_test(token, url):
    print("Đang thiết lập...")
    exam = json.loads(requests.get(url, headers={"User-Agent": USER_AGENT, "Authorization": f"Bearer {token}"}).text)
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
            res = json.loads(requests.put("https://api.hocvalamtheobac.vn/v1/exams/submit", json=submit_context, headers={"User-Agent": USER_AGENT, "Authorization": f"Bearer {token}"}).text)
            if res["result"]:
                input(f"Điểm: {res['data']['score']} (Có thể không chính xác)\nNộp bài thành công!\n\nKiểm tra điểm của bạn trên trang chủ!\nEnter để kết thúc chương trình.")
                break
        except Exception as e:
            print(f"{e}\nKhông thể gửi, đang thử lại...")
            time.sleep(1)


def send_to_AI(questions_options_raw, exam_instance_id, token):
    sle = seleAI.SeleBardHelper()
    sle.init()

    ans = []
    for ask in questions_options_raw:
        prefix = ""
        while True:
            try:
                print(f"\nQuery: {ask['question']}\n{ask['options_string']}\nĐang chờ trả lời...")
                ans.append({
                    "question_id": ask["question_id"],
                    "selected_id": re.findall(r'\[[0-9]+\]', sle.prompt(f"{prefix} Tôi sẽ gõ một câu hỏi trắc nghiệm về Việt Nam, có số ID đứng trước câu trả lời và bạn sẽ trả lời lựa chọn đúng nhất. Tôi muốn bạn chỉ trả lời và không có gì khác. không viết lời giải thích, hoặc hỏi bất cứ điều gì, cũng không phải giải thích lí do cho câu trả lời đó. Khi trả lời, hãy bao gồm cả ID của câu trả lời. Ví dụ: \"[ID]. Như vậy\".\nCâu hỏi: {ask['question']}\n{ask['options_string']}"))[0].split("[")[1].split("]")[0]
                })
                print(f"Cập nhật ({len(ans)} / 30): Đã cập nhật (Đáp án :{ans[-1:]})\nĐang tạm dừng 5 giây...")
                time.sleep(5)
                if len(ans) == 10:
                    print("Đang yêu cầu bắt đầu chạy thời gian test...")
                    while True:
                        try:
                            if requests.post("https://api.hocvalamtheobac.vn/v1/exams/start", json={"exam_instance_id": exam_instance_id}, headers={"User-Agent": USER_AGENT, "Authorization": f"Bearer {token}"}) .status_code == 200:
                                print("Tiếp tục...")
                                break
                        except Exception as e:
                            print(f"{e}\nKhông thể gửi, đang thử lại...")
                            time.sleep(1)
            except Exception as e:
                prefix += random.choice("QWERTYUIOPASDFGHJKLZXCVBNM1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*()")
                print(f"{e}\nĐã xảy ra lỗi! Đang thử lại sau 5 giây...")
                time.sleep(5)
            else:
                break
    return ans