import time
from timer_decorator import timer
import re

def string_to_cord_list(string):
    cord_list = re.findall(r"[A-G]#?", string)
    return cord_list

# class Music:
#     def __init__(self, string):
#         self.start, self.end, self.title, self.cord = string.split(",")
#         self.duration = self.get_duration()
#         self.cord_list = string_to_cord_list(self.cord)
#         self.totalcord = self.get_total_cord()
        
#     def get_duration(self):
#         start = self.start.split(":")
#         end = self.end.split(":")
#         return (int(end[0]) - int(start[0])) * 60 + (int(end[1]) - int(start[1]))
    
#     def get_total_cord(self):
#         totalcord = []
#         for i in range(self.duration):
#             totalcord.append(self.cord_list[i % len(self.cord_list)])
#         totalcord = "".join(totalcord)
        
#         print(f"{self.title} totalcord:  {totalcord}")
#         return totalcord
        
class Music:
    def __init__(self, string):
        self.start, self.end, self.title, self.cord = string.split(",")
        self.cord = re.sub(r"([A-G])#", lambda x: x.group(0).lower(), self.cord)
        self.cord = self.cord.replace("#", "")
        self.duration = self.get_duration()
        self.cord_list = string_to_cord_list(self.cord)
        self.totalcord = self.get_total_cord()
        
    def get_duration(self):
        start = self.start.split(":")
        end = self.end.split(":")
        return (int(end[0]) - int(start[0])) * 60 + (int(end[1]) - int(start[1]))
    
    def get_total_cord(self):
        totalcord = []
        for i in range(self.duration):
            totalcord.append(self.cord_list[i % len(self.cord_list)])
        totalcord = "".join(totalcord)
        
        print(f"{self.title} totalcord:  {totalcord}")
        return totalcord


@timer
def solution(m, musicinfos):
    answer = ""
    music_objs = []
    for musicinfo in musicinfos:
        music_objs.append(Music(musicinfo))
    
    for music in music_objs:
        print(music.title, music.totalcord)
    
    for music in music_objs:
        if m in music.totalcord:
            if answer == "":
                answer = music.title
            return music.title
        else:
            continue
    
    answer = "(None)"
    return answer


if __name__ == "__main__":
    test_cases = [
        [
            "CC#BCC#BCC#BCC#B",
            ["03:00,03:30,FOO,CC#B", "04:00,04:08,BAR,CC#BCC#BCC#B"],
            "FOO",
        ],
        [
            "ABCDEFG",
            ["12:00,12:14,HELLO,CDEFGAB", "13:00,13:05,WORLD,ABCDEF"],
            "HELLO",
        ],
        [
            "ABC",
            ["12:00,12:14,HELLO,C#DEFGAB", "13:00,13:05,WORLD,ABCDEF"],
            "WORLD",
        ],
    ]

    # answer = 	"FOO"
    for case in test_cases:
        m, musicinfos, answer = case
        result = solution(m, musicinfos)
        if answer == result:
            print("PASS")
        else:
            print("FAIL")
            print(f"Answer: {answer}, Result: {result}")

    print('c' == 'c')
