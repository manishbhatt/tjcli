from datetime import date, timedelta, datetime
import os, argparse


the_cal = {"t": 0, "tm": 1, "y": -1}


def read_args():  # Read commandline arguments and finalize the date
    # TODO: Create some meaningful args and messages, for now continue with hardcoded
    # values and later revisit on how to decide args structure
    aparser = argparse.ArgumentParser(description="Journaling CLI")
    aparser.add_argument(
        "-d",
        type=valid_date,
        help="Date for the entry, t=today,y=yesterday,tm=tomorrow, or date in YYY/MM/DD format",
    )
    date_string = aparser.parse_args().d
    return date_string


def open_note(note_file):  # Open md file using vim
    print("opening file")
    os.system("vi" + " " + note_file)


def md_init(date_label):  # Initialize md file with template and original content
    the_file = date_label + ".md"
    the_path = date_label[:7]
    os.makedirs(the_path, exist_ok=True)
    return the_file


def valid_date(s):  # Helper function used by argparser to do date validation
    if s in ["t", "y", "tm"]:
        time_delta = the_cal[s]
        return datetime.strftime(
            datetime.now() + timedelta(days=time_delta), "%Y/%m/%d"
        )

    try:
        print(datetime.strptime(s, "%Y/%m/%d"))
        # Check if it's valid date or not by trying to convert into actual date
        return datetime.strftime(datetime.strptime(s, "%Y/%m/%d"), "%Y/%m/%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


# Main workflow

date_label = read_args()  # Get date
md_file = md_init(date_label)  # Get file
open_note(md_file)  # Open the file
