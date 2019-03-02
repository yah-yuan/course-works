import sys
if __name__ == '__main__':
    res = '<div>congratuations!</div><div>cgi excu successfully</div>'
    argv = sys.argv
    for item in range(len(argv)):
        if item:
            res += '<div>recieve %d arg = %s</div>' % (item,argv[item])
    print(res)