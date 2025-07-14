import sys
from bot_config.train_engine import train_all
from bot_config.ask_bot import ask

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Please provide command: 'train' or 'ask \"your question\"'")
        sys.exit(1)

    command = sys.argv[1]

    if command == "train":
        train_all()

    elif command == "ask":
        if len(sys.argv) < 3:
            print("❗ Bạn cần nhập câu hỏi sau 'ask'. Ví dụ: python main.py ask \"What is GMV?\"")
            sys.exit(1)
        question = sys.argv[2]
        print(ask(question))

    else:
        print(f"❗ Không hiểu lệnh '{command}'. Dùng 'train' hoặc 'ask'")
