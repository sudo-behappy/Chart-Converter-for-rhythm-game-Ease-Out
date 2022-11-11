from json import load
from math import ceil, floor
from os.path import splitext, exists, isdir
from tkinter import Tk

# the original color of the track
color_reference = [
    "\"red\"", "\"orange\"", "\"green\"", "\"blue\"", "\"purple\""
]

# predefined get_delta(BPM=meta[0], lenM=meta[3][0], lenS=meta[3][1], note_type=i['beat'][2]) scale to avoid the decimal error
DELTA_SCALE = 100000000

TEMPLATES = {
    "tap": "\tnote({track}, {color}, \"{type}\", SPEED * {multiplier}, {init_time})\n",
    "hold": "\tnote({track}, {color}, \"{type}\", SPEED * {multiplier}, {init_time})\n",
    "long": "\tlong_note({track}, {color}, SPEED * {multiplier}, {init_time}, {end_time})\n",
    "long_hold": "\tlong_hold({track}, {color}, SPEED * {multiplier}, {init_time}, {end_time})\n",
    "kill": "\tkill_track({track}, {init_time})\n"
}

# when the track vanish, used for note transfer
track_vanish_time = [114514.0, 114514.0, 114514.0, 114514.0, 114514.0]


# add to clipboard
def add_to_clipboard(text):
    temp = Tk()
    temp.withdraw()
    temp.clipboard_clear()
    temp.clipboard_append(text)
    temp.update()
    temp.destroy()


# check the file extension and process the file
def get_chart_dict(path:str):
    path = path.replace("\"", "")
    if not exists(path) or isdir(path):
        return "invalid path"
    elif splitext(path)[1] == ".mc" or splitext(path)[1] == ".json":
        chart = load(open(path))
        return chart


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
    return int(delta * DELTA_SCALE)


# transform the malody time to real time
def get_time(node, delta) -> float:
    return round_fixed(
        (node[0] * node[2] * delta + (node[1]) * delta) / DELTA_SCALE,
        3
    )


# better input of the time
def format_time(time: str) -> tuple:
    time = time.replace("：", ":")
    if ":" in time:
        if len(time.split(":")) > 2:
            return -1, -1
        return int(time.split(":")[0]), float(time.split(":")[1])
    try:
        return 0, float(time)
    except ValueError:
        return -1, -1


# avoid the malody bug(sometimes the number will go above 4 and 32)
def flatten_note(note):
    for i in range(1, 3):
        if note['beat'][i] > 32:
            note['beat'][i] = int(note['beat'][i] / 72)
    if "endbeat" in note.keys():
        for i in range(1, 3):
            if note["endbeat"][i] > 32:
                note["endbeat"][i] = int(note['endbeat'][i] / 72)
    return note


# check if the note is hold, pass in a dictionary note
def check_hold(note: dict, delta) -> bool:
    return get_time(note["endbeat"], delta) - get_time(note["beat"], delta) <= delta / DELTA_SCALE + 0.1


# format the note, return a formatted string
def format_note(note, track, multiplier = 1) -> str:
    template = TEMPLATES[note[3]]
    template = template.format(
        track=track,
        color=note[0],
        init_time=note[1],
        type=note[3],
        end_time=note[2],
        multiplier=multiplier
    )
    return template

def get_bpm_dict(chart, length):
    # get the metadata from the chart
    

def get_meta(chart, time) -> tuple:
    name = chart["meta"]["song"]["title"]
    artist = chart["meta"]["song"]["artist"]
    length = format_time(time)
    bpm = chart["time"][0]["bpm"]
    if length == (-1, -1):
        return -1, -1, -1, -1
    return bpm, name, artist, length


# pass in two list note
def check_consecutive_note(note1, note2, delta) -> bool:
    return delta / DELTA_SCALE - 0.001 < round_fixed(abs(note2[1] - note1[2]), 3) < delta / DELTA_SCALE + 0.001


# pass in a track array, check if long hold was needed
def check_consecutive_hold(notes, start_idx, track, delta, note_list) -> tuple:
    idx = start_idx
    init_time = notes[idx][1]
    end_time = notes[idx][2]
    is_consecutive_hold = False
    while True:
        try:
            if notes[idx][3] == "hold" \
                    and notes[idx + 1][3] == "hold" \
                    and check_consecutive_note(notes[idx], notes[idx + 1], delta):
                # ans[track].append([color, init_time, end_time, key_type])
                end_time = notes[idx + 1][2]
                # after the note was merged, clean the chart
                note_list[track].pop(idx + 1)
                is_consecutive_hold = True
                idx += 1
            else:
                break
        except IndexError:
            return init_time, end_time
    if is_consecutive_hold:
        return init_time, end_time
    return -1, -1




'''
use note_list to store note data.
each track was represented by an element of the array.
'''


# get all notes into the list
def get_note_list(chart, meta):
    note_list = [[], [], [], [], []]
    for i in chart["note"]:
        if "column" not in i.keys():
            break
        i = flatten_note(i)
        track = i["column"]
        color = color_reference[track]
        key_type = "tap"
        end_time = None
        init_time = get_time(i["beat"], get_delta(BPM=meta[0], lenM=meta[3][0], lenS=meta[3][1], note_type=i['beat'][2]))
        if "endbeat" in i.keys():
            if i["endbeat"][2] == 32:
                key_type = "kill"
                track_vanish_time[track] = init_time
            elif check_hold(i, get_delta(BPM=meta[0], lenM=meta[3][0], lenS=meta[3][1], note_type=i['beat'][2])):
                key_type = "hold"
                end_time = get_time(i["endbeat"], get_delta(BPM=meta[0], lenM=meta[3][0], lenS=meta[3][1], note_type=i['endbeat'][2]))
            else:
                key_type = "long"
                end_time = get_time(i["endbeat"], get_delta(BPM=meta[0], lenM=meta[3][0], lenS=meta[3][1], note_type=i['endbeat'][2]))

        note_list[track].append([color, init_time, end_time, key_type])
    return note_list


# adjusting the notes
def adjust_notes(note_list, meta, chart) -> list:
    # IDK why but must do more than one loop to make the chart configured correctly
    for j in range(2):
        for i in range(len(note_list)):
            idx = 0
            for notes in note_list[i]:
                if notes[3] == 'hold':
                    print(notes)
                    time = check_consecutive_hold(
                        note_list[i],
                        idx,
                        i,
                        get_delta(
                            BPM=meta[0],
                            lenM=meta[3][0],
                            lenS=meta[3][1],
                            note_type=chart['note'][i]['beat'][2]
                        ),
                        note_list
                    )
                    if time == (-1, -1):
                        idx += 1
                        continue
                    else:
                        note_list[i][idx][3] = "long_hold"
                        note_list[i][idx][1] = time[0]
                        note_list[i][idx][2] = time[1]
                idx += 1
            idx = 0
            while idx < len(note_list[i]):
                notes = note_list[i][idx]
                if notes[1] > track_vanish_time[i]:
                    if i < 2:
                        note_list[i + 1].append(notes)
                        note_list[i].remove(notes)
                        if notes[1] > track_vanish_time[i + 1]:
                            note_list[i + 2].append(notes)
                            note_list[i + 1].remove(notes)
                    elif i > 2:
                        note_list[i - 1].append(notes)
                        note_list[i].remove(notes)
                        if notes[1] > track_vanish_time[i - 1]:
                            note_list[i - 2].append(notes)
                            note_list[i - 1].remove(notes)
                    continue
                idx += 1

    return note_list

# generate the code string for the chart
def generate_code_string(note_list):
    ans = ''
    max_cnt = -114514
    for i in range(5):
        max_cnt = max(max_cnt, len(note_list[i]))
    for i in range(max_cnt):
        flag = 0
        for j in range(5):
            try:
                ans += (format_note(note_list[j][i], j))
            # if it reaches the end of the track, check
            except IndexError:
                flag += 1
            finally:
                # if all 5 tracks were checked, break the loop
                if flag >= 5:
                    break
    return ans

# for debugging
def get_chart(path, length):
    if exists(path) or not length == '':
        chart = get_chart_dict(path)
    if chart == "invalid path":
        exit("invalid path")
    else:
        meta = get_meta(chart, length)
        if meta == (-1, -1, -1, -1):
            exit("error: invalid time(please use English :, not：)")
        else:
            note_list = get_note_list(chart, meta)
            adjusted_note_list = adjust_notes(note_list, meta, chart)
            chart_string = generate_code_string(adjusted_note_list)
            return chart_string
