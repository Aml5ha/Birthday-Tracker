# Birthday Tracker

Birthday Tracker is a script to extract the birthdays of your Facebook friends and create a CSV file that you can then import to your calendar!

## Usage

This program requires two files: `names.txt` and `birthday.html`.

`param: names.txt` should be a newline separated list of Facebook Friends whose birthdays you want to export to your calendar. If you want to extract all of your friends' birthdays, type `All` when prompted for this input.

`param: birthday.html` should be the downloaded html page from 'https://m.facebook.com/events/calendar/birthdays'. **Note:** Be sure to scroll down at least to the end of the current month of next year (12+ months) so all birthdays are displayed.

The program takes these two files, scrapes the birthdays, and writes them to a CSV file, which can then be imported to Google Calendar.

Since Google Calendar doesn't support recurring events, the program asks for a third parameter for how many years to keep the birthday on your calendar.
The default value for this optional parameter is 3 years.

Any birthdays not found will not be added to the csv file.

## Running the file
Download the file in the repo named 'birthday_tracker.py'. After having the file on your machine, you can run it via command line using python. Be sure to have downloaded birthday html and the optional names.txt placed in the same directory as the file.

```bash
python3 birthday_tracker.py
```
#

```
Enter filename that contains friends' names or press enter for default (default is names.txt). Or type 'All' to get everyone's birthdays!:All
Enter filename that has Facebook Mobile Birthday html displaying 12+ months or press enter for default (default is birthday.html): birthday.html
Enter years to keep event reminders or press enter for default (default is 3 years): 10
```
