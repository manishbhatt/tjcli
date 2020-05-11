#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

from datetime import date,timedelta,datetime
import os,argparse

the_cal = {'TODAY': 0 , 'TOMORROW' : 1, 'YESTERDAY' : -1 } 

def main():
    read_args()
    #md_file=get_note_file("Yesterday")
    #open_note(md_file)

def read_args():
    # TODO: Create some meaningful args and messages, for now continue with hardcoded 
	# values and later revisit on how to decide args structure
    aparser=argparse.ArgumentParser(description="Journaling CLI")
    aparser.add_argument('-t','--today',action='store_true',help='Open journal entry for today')
    aparser.add_argument('-y','--yesterday',action='store_true',help='Open journal entry for yesterday')
    aparser.add_argument('-tm','--tomorrow',action='store_true',help='Open journal entry form tomorrow')
    args=aparser.parse_args()

    print(args)
    
def open_note(note_file):
    print("opening file")
    os.system('vi' + ' ' + note_file)

def get_note_file(day_label):
    time_delta=the_cal[day_label.upper()]
    the_file=datetime.strftime(datetime.now() + timedelta(days=time_delta),'%Y/%m/%d')+'.md'
    the_path=datetime.strftime(datetime.now() + timedelta(days=time_delta),'%Y/%m')
    os.makedirs(the_path,exist_ok=True)
    return the_file 



if __name__ == "__main__":
       main()

