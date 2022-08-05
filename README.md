# Chart Converter for rhythm game Ease Out

[简体中文](#如何使用)

a tool to convert 5k malody chart to chart script inside Ease Out

It currently does not support multiple BPM or notes other than 1/4 notes

## how to use:

you first need to create a **5k** malody chart, with specified requirements and note references.

then, create a terminal window inside the repo folder, run the program with:

```bash
python main.py
```

or run the main.exe file in the release folder

Then, input the path of .mc, .mcz, or .json file corresponding to your chart

Then, input the length of the music **inside the malody editor**(with the format **M:S**, keep all the decimals).

The program will guide you while you are doing so.

The program will generate a \[songName\].txt file in the `./out` folder with the chart gdscript code in it. Copy and paste that to the `chart_\[corresponding difficulty(EZ, HD, IN, AT)\]()` method in the godot editor

don't forget to check the indentation.

## note references

### tap and long key

tap and hold were the same in malody and Ease Out

### hold

hold is the same as the drag note in the game *Phigros*.

use the long note that has the exact same length of a 1/4 beat in malody to make hold note.

### long hold

to create long hold, just put consecutive holds together, separated by a 1/4 beat in malody.

Program will do the interpolation between notes.

### kill track

to kill a track, write a long note that begin with a 1/4 beat and end with a 1/32 beat on the corresponding track.

The long note can be any length, the program will correct it.

You can put notes on that track as usual. The note on it will automatically be shifted to the adjacent left/right track, with the original color, increasing the difficulty of your chart.

## requirement for the malody chart

1. the chart must be 5k and all the tracks must be destroyed at the end of the song.
2. the track must be destroyed from left to right, or right to left. You must not delete a track between two tracks.
3. right now the chart converting tool does not support multiple BPM chart, so no change of speed or multiple BPM among the malody chart.
4. keep in mind that the notes above the deleted chart will be shifted to the other track while players are playing the chart.
5. No overlapping notes with different color, or long note inside a long note(same or different color).
6. NO SHIT CHART, NO SHIT CHART, NO SHIT CHART!

## 如何使用

首先, 在malody中, 按照[音符映射表](#音符映射表)和给定的[要求](#要求)创作一个**5key**谱面.

然后, 在repo目录打开一个终端, 运行

```commandline

python main_chs.py

```

或运行release文件夹中的main.exe

然后, 根据程序指示, 填入谱面文件(.mc, .mcz 或.json文件)路径和**malody编辑器内部**的谱面时长(分钟:秒, 秒填入所有的小数位).

程序提供了充分的指引

程序会在`./out`目录下生成一个\[歌名\].txt文件, 包含着谱面对应的gdscript代码. 将代码复制到godot编辑器中的`chart_\[对应难度(EZ, HD, IN, AT)\]()`方法下

不要忘记检查缩进

## 音符映射表

### tap和长键

malody的长键和tap与Ease Out一模一样

### hold

hold是*Phigros*中的黄键

在malody中, 使用拥有刚好1/4个beat的长键来构造hold

### 长hold

通过把连续的hold, 中间间隔1/4个beat, 写在一个track上来构造长hold.

程序会自动在note之间进行插值

### 轨道消失

在指定的轨道上写一个以1/4 beat开始, 1/32 beat结束的长键来消除轨道

长键可以是任意长度

你可以在那个轨道上接着写note, 程序会自动将其移动到下一个/上一个轨道上

## 要求

1. 谱面必须是5key谱面, 所有的track在歌曲的最后必须被销毁
2. 轨道必须以从左到右/从右到左的顺序被销毁, 当一个轨道的两侧轨道没有被销毁之前, 你不能销毁那个轨道
3. 现在这个铺面转换器暂时不支持多BPM的谱面, 所以说在malody中不要使用多BPM或变速谱面.
4. 注意, 当你在轨道被销毁之后在上面写note, 在玩家游玩的时候note会自动传递给相邻的轨道, 来增加游戏难度. 注意不要让玩家过于受苦.
5. 不要写重叠的不同颜色note, 或者同色和异色的重叠note
6. 不要写大粪谱! 不要写大粪谱! 不要写大粪谱!
