from datetime import date, timedelta, datetime
import os, argparse, subprocess


the_cal = {"t": 0, "tm": 1, "y": -1}


def read_args():  # Read commandline arguments and finalize the date
    # TODO: Create some meaningful args and messages, for now continue with hardcoded
    # values and later revisit on how to decide args structure
    aparser = argparse.ArgumentParser(description="Journaling CLI")
    aparser.add_argument(
        "-d",
        type=valid_date,
        help="Date for the entry, t = today, y = yesterday, tm = tomorrow, or date in YYY/MM/DD format",
    )
    arg_datestr = aparser.parse_args().d
    return arg_datestr


def md_open(open_md):  # Open md file using vim
    print("opening file")
    os.system("vi" + " " + open_md)


def md_init(init_date):
    md_datehf = (
        datetime.strftime(
            datetime.strptime(init_date, "%Y/%m/%d"), "%B %d, %Y"
        )  # converts YYYY/MM/DD to Month DD, YYYY
        .lstrip("0")  # strips zero-padding from the day
        .replace(" 0", " ")
    )
    init_rootdir = "journal/"
    init_datedir = init_rootdir + init_date[:7]
    init_datefile = init_rootdir + init_date + ".md"
    os.makedirs(init_datedir, exist_ok=True)
    f = open(init_datefile, "w+")
    f.write("# " + md_datehf + "\n")
    f.write("\n")
    f.write("## To-Do\n")
    f.write("\n")
    f.write("## Notes\n")
    f.write("\n")
    f.write("## Journal\n")
    f.close()
    return init_datefile


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
md_open(md_file)  # Open the file
