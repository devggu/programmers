import re


class File:
    def __init__(self, string):
        self.string = string
        self.head = ""
        self.number = ""
        self.tail = ""
        self.parse(self.string)

    def parse(self, string):
        m = re.match(r"([^\d]*)([0-9]*)(.*)", string)
        if m:
            self.head = m.group(1)
            self.number = m.group(2)
            self.tail = m.group(3)


def solution(files):
    answer = []
    file_objects = []
    for file in files:
        file_objects.append(File(file))

    file_objects.sort(key=lambda x: (x.head.lower(), int(x.number)))

    for file_object in file_objects:
        answer.append(file_object.string)

    print(answer)
    return answer


if __name__ == "__main__":
    files = ["img12.png", "img10.png", "img02.png", "img1.png", "IMG01.GIF", "img2.JPG"]
    # answer = ["img1.png", "IMG01.GIF", "img02.png", "img2.JPG", "img10.png", "img12.png"]
    solution(files)
