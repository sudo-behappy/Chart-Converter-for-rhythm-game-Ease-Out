from json import load
from math import ceil, floor
from os.path import basename, splitext, exists, dirname, realpath
from os import mkdir, listdir
from zipfile import ZipFile

# the original color of the track
color_reference = [
    "\"red\"", "\"orange\"", "\"green\"", "\"blue\"", "\"purple\""
]

path = input("path for your chart .mc or .mcz file: ")

# check valid path
if not exists(path):
    exit("invalid path")

# check the file extension and process the file
if splitext(path)[1] == ".mc" or splitext(path)[1] == ".json":
    chart = load(open(path))
elif splitext(path)[1] == ".mcz":
    try:
        mkdir("./temp/")
    except FileExistsError:
        pass
    f = ZipFile(path, "r")
    name = None
    for file in f.namelist():
        if splitext(file)[1] == ".mc":
            name = file
            f.extract(file, "./temp")
            break
    for file in listdir("./temp"):
        if splitext(file)[1] == ".mc":
            chart = load(open("./temp/" + name))
            break
else:
    exit("invalid file type")

# predefined delta scale to avoid the decimal error
DELTA_SCALE = 100000000

TEMPLATES = {
    "tap": "\tnote({track}, {color}, \"{type}\", SPEED, {init_time})\n",
    "hold": "\tnote({track}, {color}, \"{type}\", SPEED, {init_time})\n",
    "long": "\tlong_note({track}, {color}, SPEED, {init_time}, {end_time})\n",
    "long_hold": "\tlong_hold({track}, {color}, SPEED, {init_time}, {end_time})\n",
    "kill": "\tkill_track({track}, {init_time})\n"
}


# fixed round function
def round_fixed(num: float, rnd: int) -> float:
    ans = num * (10 ** rnd)
    if ans - int(ans) >= 0.5:
        return ceil(ans) / (10 ** rnd)
    return floor(ans) / (10 ** rnd)


# get the time between each small beat
def get_delta(BPM, lenM, lenS, note_type=4) -> float:
    # declared to determine when to kill track
    global total_beat
    song_time_second = lenM * 60 + lenS
    song_time_minute = round_fixed(song_time_second / 60, 10)
    total_beat = round_fixed(BPM * song_time_minute, 5)
    delta = song_time_second / (total_beat * note_type)
    return delta


# transform the malody time to real time
def get_time(node, delta: float) -> float:
    return round_fixed(
        (node[0] * node[2] * delta + (node[1]) * delta) / DELTA_SCALE,
        3
    )


# better input of the time
def format_time(time: str) -> tuple:
    return (
        int(time.split(":")[0]),
        float(time.split(":")[1])
    )


# avoid the malody bug(sometimes the number will go above 4 and 32)
def flatten_note(note):
    for i in range(1, 3):
        if note['beat'][i] > 4:
            note['beat'][i] = int(note['beat'][i] / 72)
    if "endbeat" in note.keys():
        for i in range(1, 3):
            if note["endbeat"][i] > 32:
                note["endbeat"][i] = int(note['endbeat'][i] / 72)
    return note


# check if the note is hold, pass in a dictionary note
def check_hold(note: dict) -> bool:
    return get_time(note["endbeat"], delta) - get_time(note['beat'], delta) <= delta / DELTA_SCALE + 0.1


# format the note, return a formatted string
def format_note(note, track) -> str:
    template = TEMPLATES[note[3]]
    template = template.format(
        track=track,
        color=note[0],
        init_time=note[1],
        type=note[3],
        end_time=note[2])
    return template


# pass in two list note
def check_consecutive_note(note1, note2):
    return delta / DELTA_SCALE - 0.001 < round_fixed(abs(note2[1] - note1[2]), 3) < delta / DELTA_SCALE + 0.001


# pass in a track array, check if long hold was needed
def check_consecutive_hold(notes, start_idx, track) -> tuple:
    idx = start_idx
    init_time = notes[idx][1]
    end_time = notes[idx][2]
    is_consecutive_hold = False
    while True:
        try:
            if notes[idx][3] == "hold" and notes[idx + 1][3] == "hold" and check_consecutive_note(notes[idx],
                                                                                                  notes[idx + 1]):
                # ans[track].append([color, init_time, end_time, key_type])
                end_time = notes[idx + 1][2]
                # after the note was merged, clean the chart
                note_list[track].pop(idx + 1)
                is_consecutive_hold = True
                idx += 1
            else:
                break
        except IndexError:
            return (init_time, end_time + round_fixed(delta  * 2 / DELTA_SCALE, 3))
    if is_consecutive_hold:
        return (init_time, end_time + round_fixed(delta  * 2 / DELTA_SCALE, 3))
    return (-1, -1)


bpm = chart["time"][0]["bpm"]
length = format_time(input("the length of the song, as shown in the malody chart editor"))
delta = int(get_delta(bpm, length[0], length[1]) * DELTA_SCALE)

note_list = [[], [], [], [], []]

'''
use note_list to store note data.
each track was represented by an element of the array.
'''

# when the track vanish, used for note transfer
track_vanish_time = [-1.0, -1.0, -1.0, -1.0, -1.0]

# get all notes into the list
for i in chart["note"]:
    if "column" not in i.keys():
        break
    i = flatten_note(i)
    track = i["column"]
    color = color_reference[track]
    key_type = "tap"
    end_time = None
    init_time = get_time(i["beat"], delta)
    if "endbeat" in i.keys():
        temp = i["endbeat"]
        if i["endbeat"][2] == 32:
            key_type = "kill"
            track_vanish_time[track] = init_time
        elif check_hold(i):
            key_type = "hold"
            end_time = get_time(i["endbeat"], delta)
        else:
            key_type = "long"
            end_time = get_time(i["endbeat"], delta)
    # input(str([color, init_time, end_time, key_type]))
    note_list[track].append([color, init_time, end_time, key_type])

# adjusting the notes
for i in range(len(note_list)):
    idx = 0
    for notes in note_list[i]:
        if notes[3] == 'hold':
            time = check_consecutive_hold(note_list[i], idx, i)
            # delete all the notes covered by long note
            if time == (-1, -1):
                idx += 1
                continue
            else:
                note_list[i][idx][3] = "long_hold"
                note_list[i][idx][1] = time[0]
                note_list[i][idx][2] = time[1]

        # shift the note
        if notes[1] > track_vanish_time[i]:
            if i < 2:
                note_list[i + 1].append(notes)
                note_list[i].pop(idx)
                continue
            elif i > 2:
                note_list[i - 1].append(notes)
                note_list[i].pop(idx)
        idx += 1

# writing into file
try:
    mkdir("./out")
except FileExistsError:
    pass
with open("./out/{}.txt".format(splitext(basename(path))[0]), "w+") as f:

    # make sure the iterating one is the longest
    max_cnt = -114514
    for i in range(5):
        max_cnt = max(max_cnt, len(note_list[i]))
    for i in range(max_cnt):
        flag = 0
        for j in range(5):
            try:
                f.write(format_note(note_list[j][i], j))
            except IndexError:
                flag += 1
            finally:
                if flag >= 5:
                    break