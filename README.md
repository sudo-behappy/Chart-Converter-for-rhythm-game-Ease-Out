# Chart Converter for rhythm game Ease Out

a tool to convert 5k malody chart to chart script inside Ease Out

It currently doesn't support multiple BPM or notes other than 1/4 notes

## how to use:

you first need to create a **5k** malody chart, with specified requirements and note references.

then, run the program with:

```bash
python main.py
```

or run the chartConverter.exe file in the release folder

Then, input the path of .mc or .mcz file corresponding to your chart.

The program will generate a .txt file with the chart code in it, copy and paste that to the *chart()* method in the godot editor

don't forget to check the indentation

## note references

### tap and long key

tap and hold were the same in malody and Ease Out

### hold

hold is the same as the drag note in the game *Phigros*

use the drag note that has the exact same length of a 1/4 beat in malody to make hold note

### long hold

to create long hold, just put consecutive holds together, separated by a 1/4 beat in malody

The program will identify them automatically and convert them into long hold
