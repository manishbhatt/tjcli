from datetime import date, timedelta, datetime
from pprint import pprint
import os, argparse, subprocess
from os import path


the_cal = {"t": 0, "tm": 1, "y": -1}
todo_tag="## To-do"
notes_tag="## Notes"
journal_tag="## Journal"
the_md_file = {
    "uncategorized": [],
    "header_order": ["Title",todo_tag,notes_tag,journal_tag],
    "Title": "",
    todo_tag: [todo_tag+"\n\n"],
    notes_tag: [notes_tag+"\n\n"],
    journal_tag: [journal_tag+"\n\n"]
}


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
    if not path.exists(init_datefile):
        the_md_file["Title"] = md_datehf+"\n"*2
        md_write(init_datefile)
    return init_datefile


def md_read(read_path):
    f = open(read_path, "r")
    ar=[]
    file_content=f.readlines()
    the_md_file["Title"]=file_content[0]
    for ln in file_content[1:]:
        if ln.strip() == todo_tag:
            ar=the_md_file[todo_tag]
            continue
        if ln.strip() == notes_tag:
            ar=the_md_file[notes_tag]
            continue
        if ln.strip() == journal_tag:
            ar=the_md_file[journal_tag]
            continue
        ar.append(ln)
    pprint(the_md_file)
    f.close()

def md_write(write_path):
    f = open(write_path, "w+")
    for file_header in the_md_file["header_order"]:
        for header_contents in the_md_file[file_header]:
            for each_line in header_contents:
                f.write(each_line)


    f.close()


def md_open(open_md):  # Open md file using vim
    print("opening file")
    os.system("vi " + open_md)


# Main workflow

date = read_args()[0]  # Get date
md_file = md_init(date)  # Get file
md_read(md_file)  # Read the file, this function will be useful when we want to inject and update todos , notes etc..
md_open(md_file)  # Open the file
