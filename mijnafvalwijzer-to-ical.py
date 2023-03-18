#!/usr/bin/env python

import sys
import re
import requests
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
from icalendar import Calendar, Event, Alarm

months = {
  "januari":   1,
  "februari":  2,
  "maart":     3,
  "april":     4,
  "mei":       5,
  "juni":      6,
  "juli":      7,
  "augustus":  8,
  "september": 9,
  "oktober":   10,
  "november":  11,
  "december":  12
}

if len(sys.argv) < 2:
    print("Usage {0} <postal code> <house number>".format(sys.argv[0]))
    exit(1)

postal_code = sys.argv[1]
housenumber = sys.argv[2]
housenumber_suffix = ""
waste_types = []

if len(sys.argv) >= 4:
  waste_types = sys.argv[3].split(",")

housenumber_re = re.search(r"^(\d+)(\D*)$", housenumber)
if housenumber_re.group():
  housenumber = housenumber_re.group(1)
  housenumber_suffix = housenumber_re.group(2) or ""

url = "https://www.mijnafvalwijzer.nl/nl/{0}/{1}/{2}".format(postal_code, housenumber, housenumber_suffix)
aw_html = requests.get(url)

aw = BeautifulSoup(aw_html.text, "html.parser")

cal = Calendar()
cal.add("prodid", "-//{0}//NL".format(sys.argv[0]))
cal.add("version", "2.0")
cal.add("name", "Afvalkalender")
cal.add("x-wr-calname", "Afvalkalender")
cal.add("x-wr-timezone", "Europe/Amsterdam")
cal.add("description", aw.title.string)
cal.add("url", url)

alarm = Alarm()
alarm.add("action", "DISPLAY")
alarm.add("trigger", value=timedelta(-1))

for item in aw.find_all("a", "wasteInfoIcon textDecorationNone"):
    # Get the waste type from the fragment in the anchors href
    waste_type = item["href"].replace("#", "").replace("waste-", "")
    if waste_type == "" or waste_type == "javascript:void(0);":
      if item.p.has_attr("class"):
        waste_type = item.p["class"][0]

    if not waste_types or waste_type in waste_types:
      raw_d = re.search("(\w+) (\d+) (\w+)", item.p.text)
      item_date = date(datetime.date.today().year, months.get(raw_d.group(3), 0), int(raw_d.group(2)))
      item_descr = item.find("span", {"class": "afvaldescr"}).text

      event = Event()
      event.add("uid", "{0}-{1}-{2}".format(item_date.timetuple().tm_year, item_date.timetuple().tm_yday, waste_type))
      event.add("dtstamp", datetime.now())
      event.add("dtstart", item_date)
      event.add("dtend", item_date + timedelta(1))
      event.add("summary", "Afval - {0}".format(item_descr.replace("\,", ",")))
      event.add("description", item_descr.replace("\,", ","))
      event.add_component(alarm)

      cal.add_component(event)

print(cal.to_ical().decode("utf-8"))
