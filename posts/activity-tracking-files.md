---
layout: post
date: 2018-06-14
title: Editing and analyzing activity tracking files
---
A month ago I started running with a GPS watch and a footpod, but kept the GPS feature off. A
footpod is a small device that sits on top of my foot and tracks movements. For the particular watch model I own,
turning the GPS off means that it will record my speed and distance from the foodpod data instead of using my
position. GPS watches work by regularly finding where you are and then calculate the speed and distance by "connecting
the dots" between each position. It will often cut corners and the position is not always precise if you approach tall
buildings or pass under bridges. Footpods on the other hand will accurately monitor the movement of the foot and
knows exactly how long your step was and how much time it took. The recording of the distance and speed is
[far more accurate](http://fellrnr.com/wiki/GPS_Accuracy).

Some runners like myself love to see the result of a run on the computer and even share it with friends and colleagues
on social sites like Strava. Unfortunately, if I turn off the GPS during a run I don't get the nice map displays and,
in the case of Strava, many core features of the site like segments are lost. That's really unfortunate, so I started
looking for a way to add back maps to my footpod runs.


## What an activity track file looks like

Sport trackers will store activity data in the form of FIT, TCX, or GPX files. There's usually a way to copy those files
to a computer with an USB cable or by downloading them from an service such as Garmin Connect. Those files follow one
of the formats defined by Garmin and other manufacturers and Web services try to maintain compatibility with them.

The FIT format is the most recent design and handles a greater number of types of information. However, the file
content is not readable and requires decoding software. There are code libraries that do that for us if necessary.
The TCX format is very similar but is actually readable. If you have access to a TCX file, you can open it in a text
editor of your choice and you'll see information presented in a quirky format, called XML:

```xml 
<?xml version="1.0" encoding="UTF-8"?>
<TrainingCenterDatabase xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd" xmlns:ns5="http://www.garmin.com/xmlschemas/ActivityGoals/v1" xmlns:ns3="http://www.garmin.com/xmlschemas/ActivityExtension/v2" xmlns:ns2="http://www.garmin.com/xmlschemas/UserProfile/v2" xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
 <Activities>
  <Activity Sport="Running">
   <Id>2018-06-10T12:48:07Z</Id>
   <Lap StartTime="2018-06-10T12:48:07Z">
    <TotalTimeSeconds>289</TotalTimeSeconds>
    <DistanceMeters>923.63</DistanceMeters>
    <MaximumSpeed>12600.0</MaximumSpeed>
    <Calories>0</Calories>
    <AverageHeartRateBpm>
     <Value>145</Value>
    </AverageHeartRateBpm>
    <MaximumHeartRateBpm>
     <Value>157</Value>
    </MaximumHeartRateBpm>
   </Lap>
  </Activity>
 </Activities>
</TrainingCenterDatabase>
```

In an XML file, content is organized in a series of _elements_. Elements have a name and they're written as a start
_tag_, some content, and an end tag. Elements can contain either text or other elements. Start tags look like `<Name>`,
and end tags are similarly `</Name>`. Some tags have extra information about them called _attributes_. Those attributes
are included between the start tag brackets and have a name and a value. In the example above, on the fourth line you
will find an `Activity` start tag. It has a `Sport` attribute that is `Running`. What it means in the case of a TCX file
is that all the content between this tag and the end tag `</Activity>` at the bottom will be about an activity, and in
particular a _running_ activity. In the middle of the example, you'll find heart rate information that is given in the
context of that activity.


## Reading files with a computer program

Editing long sequence of XML tags by hand would be terribly tedious, so we should rely on computer programs to automate
the task. I'm typically using the Python language to quickly write such tools and it happens that there are useful code
libraries available. For FIT files, the package `fitparse` can be used. There are multiple ways to load packages, still
I recommend using a virtualenv if you know how to create them, otherwise it's probably safe to install the package for
yourself by using a command line such as `pip install --user fitparse`. TCX files can be read with only the standard
packages that come with the language.


### Reading the FIT file

The FIT files are made of many records and each record may have field data. It can be viewed by enumerating each record
and then enumerating each field:

```python
import fitparse
import sys


# Execute this program files with the path to the FIT file as the last
# argument.
fit_file = fitparse.FitFile(
    sys.argv[1], data_processor=fitparse.StandardUnitsDataProcessor())

for record in fitfile.get_messages():
    print(record.name)
    if record.type == 'data':
        for field_data in record:
            print(' * {}: {}'.format(field_data.name, field_data.value))
```

### Reading the TCX file

The tools to read XML files are already available with Python. Those tools are much more sophisticated as they allow
programmers not only to enumerate elements, but also to search for specific tags and attributes. The top element that
contains all the other elements in the file is called the _root_ element and the structure is called a _tree_ (imagine
something closer to a genealogical tree than something you would see outside the window.)

A tag that contains most of the interesting data is the `Trackpoint` tag. We can get a list of all of those and print
their time element like this:

```python
import sys
import xml.etree.ElementTree as ET

# Execute this program files with the path to the TCX file as the last
# argument.
tcx_file = ET.parse(sys.argv[1])

root = tcx_file.getroot()

# For the computers, the actual tag names are really long so we have to use this trick to avoid typing those
# ridiculous names each time we want to refer to a tag. We'll just use `tcx:` and the short name instead.
ns = {
    'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
}

# The syntax to get elements is called XPath.
track = root.find('./tcx:Activities/tcx:Activity/tcx:Lap/tcx:Track', ns)
for trackpoint_time in track.iterfind('./tcx:Trackpoint/tcx:Time', ns):
    print(trackpoint_time.text)
```

### Writing a TCX file

Creating new FIT files is a bit too complicated and is not a feature of the `fitparse` package. To be able to create
new activity files, we can rely on the relative simplicity of the XML format used by TCX files. Creating an almost
empty, but still probably valid file looks a bit like this:

```python
import datetime
import random
import xml.etree.ElementTree as ET

root = ET.Element('TrainingCenterDatabase')

# Tell the library to set up the long element names.
root.set(
    'xsi:schemaLocation',
    ' '.join([
        'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
        'http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd',
    ])
)
root.set('xmlns', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

now = datetime.datetime.utcnow().isoformat() + 'Z'

activities = ET.SubElement(root, 'Activities')
activity = ET.SubElement(activities, 'Activity')
activity.set('Sport', 'Running')
activity_id = ET.SubElement(activity, 'Id')
activity_id.text = now

lap = ET.SubElement(activity, 'Lap')
lap.set('StartTime', now)
total_time = ET.SubElement(lap, 'TotalTimeSeconds')
total_time.text = '1'
intensity = ET.SubElement(lap, 'Intensity')
intensity.text = 'Active'

track = ET.SubElement(lap, 'Track')
trackpoint = ET.SubElement(track, 'Trackpoint')
time = ET.SubElement(trackpoint, 'Time')
time.text = now
position = ET.SubElement(trackpoint, 'Position')
latitude = ET.SubElement(position, 'LatitudeDegrees')
latitude.text = '{:.1f}'.format(random.uniform(-90.0, 90.0))
longitude = ET.SubElement(position, 'LongitudeDegrees')
longitude.text = '{:.1f}'.format(random.uniform(-180.0, 180.0))
altitude = ET.SubElement(trackpoint, 'AltitudeMeters')
altitude.text = '{}'.format(random.randrange(0, 4000))
distance = ET.SubElement(trackpoint, 'DistanceMeters')
distance.text = '0'
heart_rate = ET.SubElement(trackpoint, 'HeartRateBpm')
heart_rate.text = '{}'.format(random.randrange(60, 180))

print('<?xml version="1.0" encoding="UTF-8"?>')
ET.dump(root)
```

You can probably run this program, copy the printed output into a new TCX file and upload that to your favorite
activity tracking site. It will show yourself having just finished an 1-second activity where you were probably
standing up in the air, in the middle of an ocean. What a workout!


## Putting it all together

Now comes the long and experimental part where we reverse engineer a FIT file containing a real run (the one recorded
with the footpod) and a TCX file exported from a Strava route that was just created manually and exported. The plan is
to read each record of the FIT file, convert that into the closest equivalent we can find in the TCX format, and walk
through the Strava route file to find the equivalent position for the elapsed time.

Hopefully there's a trick. From either Garmin Connect or Strava, there's the option to export not only the original
FIT file, but also an equivalent TCX file. This way we can basically try to reproduce that TCX file as closely as
possible, with only the addition of the `Position` tags.


### Interpolating positions

Once the mechanics of reading and writing activity tracking files was well understood, the challenge was to find a way to
correcly determine the runner position for any specific distance in the original activity. The distance markers in each
file don't match. For example, the route may have the position for every meter and the activities are recorded every second,
so the distance will probably fall between two exact meter values. We need to figure out a technique that gives us the
closest value from the route file as we go through the activity records.

  1. Pick the first position in the route. Call this position "behind".
  2. Pick the next position in the route. Call this position "ahead". It doesn't matter if it's ahead of anything for now.
  3. Compare the current distance with the "ahead" position.
     - If "ahead" is not ahead of that distance, make "ahead" the new "behind" and pick the next position from the
        route. Repeat until this isn't true anymore.
     - If "ahead" is really ahead of that distance, we found two consecutive positions on the route that are just
       around the current runner's position.
  4. Calculate the fraction of the distance between the "behind" and the "ahead" positions. Zero would mean that the
     runner is exactly at the same distance as "behind". One would mean that they're exactly where "ahead" is. One
     half falls right in the middle of the two positions.
  5. Assume the Earth is flat for a second.
  6. Take each coordinate of the "behind" point and add to it a fraction of the difference between the coordinates of
     the "ahead" and "behind" positions, using the fraction calculated before. For example, if the fraction is one
     half, calculate "longitude behind + ½ (longitude ahead − longitude behind)". Do the same for the latitude and
     you've got the approximate position of the runner.
  7. Repeat all steps from 3 with the next record.
