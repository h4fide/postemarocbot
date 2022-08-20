import os


def main():
    try:
        os.system("python src/bot.py & python src/patrol.py")
    except:
        pass


if __name__ == "__main__":
    fileslist = os.listdir('src/')
    requires_files = ["bot.py", "patrol.py"]
    print(requires_files)
    for file in requires_files:
        if file not in fileslist:
            print(f"{file} is missing")
            exit()
    main() 