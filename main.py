from datetime import date, timedelta, datetime
from pprint import pprint
import os, argparse, subprocess


the_cal = {"t": 0, "tm": 1, "y": -1}


def read_args():  # Read commandline arguments and finalize the date
    # TODO: Create some meaningful args and messages, for now continue with hardcoded
    # values and later revisit on how to decide args structure
    aparser = argparse.ArgumentParser(description="Journaling CLI")
    aparser.add_argument(
        "-d",
        "--date",
        type=valid_date,
        help="Date for the entry, t = today, y = yesterday, tm = tomorrow, or date in YYY/MM/DD format",
    )
    aparser.add_argument(
        "-td", "--todo", type=str,
    )
    aparser.add_argument(
        "-n", "--note", type=str,
    )
    arg_datestr = aparser.parse_args().date
    arg_tdstr = aparser.parse_args().todo
    arg_nstr = aparser.parse_args().note
    arg_tdstr = ["To-Do", arg_tdstr]
    arg_nstr = ["Notes", arg_nstr]
    return arg_datestr, arg_tdstr


def valid_date(s):  # Helper function used by argparser to do date validation
    if s in ["t", "y", "tm"]:
        time_delta = the_cal[s]
        return datetime.strftime(
            datetime.now() + timedelta(days=time_delta), "%Y/%m/%d"
        )

    try:
        datetime.strptime(s, "%Y/%m/%d")
        # Check if it's valid date or not by trying to convert into actual date
        return datetime.strftime(datetime.strptime(s, "%Y/%m/%d"), "%Y/%m/%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


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


def md_read(read_path):
    f = open(read_path, "r")
    read_dict = {}
    read_lastheader = "uncategorized"  # catch any text before a header
    read_dict[read_lastheader] = []
    read_dict["header_order"] = []
    for x in f:
        x = x.rstrip()
        if (
            x[:2] == "# "
        ):  # check if a line is the title, and set that as the "title" in the dict
            read_dict["title"] = x[2:]
        elif (
            x[:3] == "## "
        ):  # check if a line is an h2, and set that as the header, which is a list of lines under it
            read_dict[x[3:]] = []
            read_lastheader = x[3:]
            read_dict["header_order"].append(x[3:])
        elif x != "":  # append any non-blank, non header lines to the last header list
            read_dict[read_lastheader].append(x)
    f.close()
    return read_dict


def md_write(write_dict, write_path):
    f = open(write_path, "w+")
    f.write("# " + write_dict["title"] + "\n")  # add title to top of file
    f.write("\n")
    for x in write_dict[
        "uncategorized"
    ]:  # write any uncategorized lines, which don't fall under a header
        f.write(x + "\n")
    if (
        len(write_dict["uncategorized"]) != 0
    ):  # only add a blank line if there were uncategorized items
        f.write("\n")
    for x in write_dict["header_order"]:  # for each header, write it
        f.write("## " + x + "\n")
        if x != write_dict["header_order"][-1]:
            f.write("\n")
        for y in write_dict[x]:  # for each line in the header, write it
            f.write(y + "\n")
        if (
            x != write_dict["header_order"][-1] and len(write_dict[x]) != 0
        ):  # don't add an extra newline
            f.write("\n")
    f.close()


def md_open(open_md):  # Open md file using vim
    print("opening file")
    os.system("vi " + open_md)


# Main workflow

date = read_args()[0]  # Get date
input = ["To-Do", "Do some wrk"]
md_file = md_init(date)  # Get file
md_dict = md_read(md_file)
if input[0] == "To-Do":
    input[1] = "- [ ] " + input[1]
elif input[0] == "Notes":
    input[1] = "- " + input[1]
md_dict[input[0]].append(input[1])
md_write(md_dict, md_file)
# md_open(md_file)  # Open the file
