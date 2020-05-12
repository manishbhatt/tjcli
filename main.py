from datetime import date, timedelta, datetime
import os, argparse

the_cal = {"t": 0, "tm": 1, "y": -1}


def main():
    read_args()


def read_args():
    # TODO: Create some meaningful args and messages, for now continue with hardcoded
    # values and later revisit on how to decide args structure
    aparser = argparse.ArgumentParser(description="Journaling CLI")
    aparser.add_argument(
        "-d",
        type=valid_date,
        help="Date for the entry, t=today,y=yesterday,tm=tomorrow, or date in YYY/MM/DD format",
    )
    date_string = aparser.parse_args().d
    open_note(get_note_file(date_string))


def open_note(note_file):
    print("opening file")
    os.system("vi" + " " + note_file)


def get_note_file(date_label):
    the_file = date_label + ".md"
    the_path = date_label[:7]
    os.makedirs(the_path, exist_ok=True)
    return the_file


def valid_date(s):
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


if __name__ == "__main__":
    main()
