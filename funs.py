import colors
def find_comment(found_words):
    print(colors.color.green("found comment:"))
    colors.color.reset()
    for comment in found_words:
        print(comment)  
#find urls
def find_urls(found_urls):
    global unique_js_files
    for javascript_file in found_urls:
        for i in javascript_file:
            print(str(i),end="")
        print()
    
def usernames(usernames):
    for username in usernames:
        print(username)
    
def passwords(passwords):
    for password in passwords:
        print(password)


