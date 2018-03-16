# day-slide-hero
For making day slides, like for a school.

[Example slide](https://imgur.com/xrXJIX1)

## How to use

*This was quickly thrown together and it works, not really intended to be robust or anything. Easier than making the 210 slides I had to by hand though.*

1. Make a file called input.csv with groups of 5 dates (1 week of weekdays) in the format `ISO8601 Date,Name of Day,Background Color,Accent Color`, for example:
```
2017-09-04,No School,red,black
2017-09-05,No School,red,black
2017-09-06,A Day,cornflowerblue,white
2017-09-07,B Day,yellow,black
2017-09-08,A Day,cornflowerblue,white
```

2. Include an image (mine was 628x400) called `bg.jpg` for the background.
3. Run the script.
4. Enjoy your zip file with all the generated slides.
