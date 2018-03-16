from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance
from datetime import datetime
import csv
import shutil


class DayAttributes(object):

    def __init__(self, title, color, accent):
        self.title = title
        self.color = color
        self.accent = accent


class Slide(object):

    def __init__(self, day, week, calender):
        self.date = self.custom_strftime(day)
        attributes = calender.get(day)
        self.day_title = attributes.title
        self.day_color = attributes.color
        self.day_accent = attributes.accent
        self.weekday_titles = list(calender.get(day).title for day in week)
        self.weekday_days = list(self.custom_strftime(day) for day in week)

    @staticmethod
    def custom_strftime(dt):
        if 4 <= dt.day <= 20 or 24 <= dt.day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][dt.day % 10 - 1]
        return dt.strftime("%A, %B %d").lstrip("0").replace(" 0", " ")+suffix

    def make(self):
        # Create the base image
        canvas = Image.open("bg.jpg")
        canvas = canvas.resize((1920, 1080), Image.ANTIALIAS)
        canvas = canvas.filter(ImageFilter.GaussianBlur(1))
        red = Image.new("RGB", canvas.size, self.day_color)
        canvas = Image.blend(canvas, red, 0.2)
        canvas = ImageEnhance.Brightness(canvas).enhance(.3)
        canvas = ImageEnhance.Contrast(canvas).enhance(2)
        # Get ready to add elements on top
        draw = ImageDraw.Draw(canvas)
        # Draw the rectangle
        draw.rectangle([(0, 0), (1360, 1080)], self.day_color)
        # Initialize the needed fonts
        day_type_font = ImageFont.truetype("arialbd.ttf", 295)
        date_font = ImageFont.truetype("arialbd.ttf", 90)
        weekdays_type_font = ImageFont.truetype("arialbd.ttf", 40)
        weekdays_days_font = ImageFont.truetype("arial.ttf", 40)
        # Write the day type
        draw.text((30, 10), self.day_title, self.day_accent, font=day_type_font)
        # Write the date
        draw.text((45, day_type_font.size+35), self.date, self.day_accent, font=date_font)
        # Write the week days
        weekdays_titles = "\n".join(self.weekday_titles)
        weekdays_days = "\n".join(self.weekday_days)
        weekdays_type_size = draw.multiline_textsize(weekdays_titles,
                                                     font=weekdays_type_font, spacing=weekdays_type_font.size/2)
        draw.multiline_text((1340-weekdays_type_size[0], 1060-weekdays_type_size[1]), weekdays_titles, self.day_accent,
                            font=weekdays_type_font, align="right", spacing=weekdays_type_font.size/2)
        draw.multiline_text((1380, 1060 - weekdays_type_size[1]), weekdays_days, self.day_color,
                            font=weekdays_days_font, align="left", spacing=weekdays_days_font.size / 2)
        return canvas


def run(file):

    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        days = []
        calendar = {}
        for row in reader:
            days.append(datetime.strptime(row[0], "%Y-%m-%d"))
            calendar.update({datetime.strptime(row[0], "%Y-%m-%d"): DayAttributes(*row[1:4])})
        for i in range(0, len(days), 5):
            for j in range(0, 5):
                day = days[i+j]
                print(day.strftime("%A, %B %d").lstrip("0").replace(" 0", " "))
                slide = Slide(day, days[i:i+5], calendar)
                img = slide.make()
                img.save("output/{}.png".format(day.strftime("%Y-%m-%d")), "png")
    archive_name = "{} - {}".format(days[0].strftime("%Y-%m-%d"), days[-1].strftime("%Y-%m-%d"))
    shutil.make_archive(archive_name, "zip", "output")


run("input.csv")
