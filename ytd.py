from datetime import date, timedelta, datetime
from pprint import pprint
import os, argparse, subprocess, configparser
from os import path
from pathlib import Path


the_cal = {"t": 0, "tm": 1, "y": -1}
all_args = {"d": "", "t": "", "n": "", "j": ""}
todo_tag = "## To-do"
notes_tag = "## Notes"
journal_tag = "## Journal"
check_box = "- [ ] "
nl="\n""
the_md_file = {
    "file_name": "",
    "header_order": ["Title", "t", "n", "j"],
    "Title": "",
    "t": [],
    "n": [],
    "j": [],
}

config = configparser.ConfigParser()
config.read(str(Path.home()) + "/ytodorc")
root_folder = config["config"]["root_folder"]


def main():
    # Main workflow
    read_args()  # Read all args and prepare all_args dict
    md_init()  # Based on all the args, process the file\
    pprint(the_md_file)
    md_write1()
    #md_open()  # Open the file
#

def read_args():  # Read commandline arguments and finalize the date
    # TODO: Create some meaningful args and messages, for now continue with hardcoded
    # values and later revisit on how to decide args structure
    aparser = argparse.ArgumentParser(description="Journaling CLI")
    aparser.add_argument(
        "-d",
        type=valid_date,
        help="Date for the entry, t = today, y = yesterday, tm = tomorrow, or date in YYY/MM/DD format",
    )
    aparser.add_argument("-t", help="Add entry in todo")
    aparser.add_argument("-j", help="Add entry in journal")
    aparser.add_argument("-n", help="Add entry in notes")
    arg_space = aparser.parse_args()
    all_args["d"] = arg_space.d
    all_args["t"] = arg_space.t
    all_args["n"] = arg_space.n
    all_args["j"] = arg_space.j


def md_init():
    init_date = all_args["d"]
    init_datedir = root_folder + init_date[:7]
    md_file_name = root_folder + init_date + ".md"
    the_md_file["file_name"] = md_file_name
    os.makedirs(init_datedir, exist_ok=True)
    if not path.exists(md_file_name):
        the_md_file["Title"] = "Date:" + init_date 
        the_md_file["t"].extend([todo_tag])
        the_md_file["n"].extend([notes_tag])
        the_md_file["j"].extend([journal_tag])
    else:
        f = open(md_file_name, "r")
        ar = []
        file_content = f.readlines()
        the_md_file["Title"] = file_content[0]
        for ln in file_content[1:]:
            if ln.strip() == todo_tag:
                the_md_file["t"].extend([todo_tag])
                ar = the_md_file["t"]
                continue
            if ln.strip() == notes_tag:
                the_md_file["n"].extend([notes_tag])
                ar = the_md_file["n"]
                continue
            if ln.strip() == journal_tag:
                the_md_file["j"].extend([journal_tag])
                ar = the_md_file["j"]
                continue
            ar.append(ln)
        f.close()
    for v in ["t", "n", "j"]:
        if all_args[v] is not None:
            the_md_file[v].append(all_args[v])


def md_write1():
    md_file_name=the_md_file["file_name"] 
    f = open(md_file_name, "w+")
    f.writelines(the_md_file["t"])
    f.writelines(the_md_file["n"])
    f.writelines(the_md_file["j"])




def md_write():
    md_file_name=the_md_file["file_name"] 
    f = open(md_file_name, "w+")
    for file_header in the_md_file["header_order"]:
        for header_contents in the_md_file[file_header]:
            for each_line in header_contents:
                f.write(each_line)

    f.close()


def md_open():  # Open md file using vim
    md_file_name=the_md_file["file_name"] 
    print("opening file")
    os.system("vi " + md_file_name)


def valid_date(s):  # Helper function used by argparser to do date validation
    if s in ["t", "y", "tm"]:
        time_delta = the_cal[s]
        return datetime.strftime(
            datetime.now() + timedelta(days=time_delta), "%Y/%m/%d"
        )

    try:
        # Check if it's valid date or not by trying to convert into actual date
        return datetime.strftime(datetime.strptime(s, "%Y/%m/%d"), "%Y/%m/%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
    raise argparse.ArgumentTypeError(msg)


if __name__ == "__main__":
    main()
