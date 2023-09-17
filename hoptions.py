import os

def request_option() -> int:
    print("Chọn loại test:\n\n1. Làm bài test chính thức.\n2. Làm bài test thử.")

    test_option = input("> ")

    if test_option == "1":
        return 0
        
    if test_option == "2":
        return 1
    
    os.system("cls")

    return request_option()