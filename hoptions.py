import random

def request_confirm() -> bool:
    code = random.randint(2141, 99999)
    print(f"Trước khi bắt đầu:\n\n1. Chương trình sử dụng Google Bard với mục đích trả lời những câu hỏi.\n2. Kết quả sẽ ngẫu nhiên tùy theo câu trả lời của AI vì tính chính xác chưa cao, trong khoảng từ 150 đến 250 điểm.\n3. Chịu trách nhiệm khi bị phát hiện :).\n4. Điền OK và thêm vào đó mã xác nhận. (VD: \"OK <Mã>\")\nMã: {code}")



    confirm = input("> ")

    if confirm == f"OK {code}":
        return True
    else:
        input("\nMã sai. Enter để thoát chương trình.")
        exit()