import csv, sys, os, re
                                                                                   
#def list_files(dir):                                                                                                  
#    r = []
#    subdirs = [x[0] for x in os.walk(dir)]
#    for x in os.walk(dir):
#        print(x)
#    for subdir in subdirs:
#        temp = os.walk(subdir).next()
#        if temp:
#            files = temp[2]                                                                             
#            if (len(files) > 0):                                                                                          
#                for file in files:                                                                                        
#                    r.append(subdir + "/" + file)                                                                         
#    return r

def list_files(dir):
    r = []
    for f in os.listdir(dir):
        r.append(f)
    return r

def match_trec(file):
    to_pattern = r"To:.*<(.*)>"
    from_pattern = r"From:(.*)"
    date_pattern = r"Date: (.*)"
    with open(file, 'r') as text:
        string = text.read()
        to_string = re.search(to_pattern, string).group(1)
        from_string = re.search(from_pattern, string).group(1)
        date_string = re.search(date_pattern, string).group(1)
        print(to_string, from_string, date_string)
    
def match_csv(file):
    
def main():
    file_list = list_files('/Accounts/nachtm/Desktop/trecdata/text_000/')
    match('/Accounts/nachtm/Desktop/trecdata/text_000/' + file_list[0])
    #print(file_list)
    #with open('emails.csv', 'w') as f:
        
if __name__ == '__main__':
    main()