#!/usr/bin/python3
"""
A script markdown2html.py that takes an argument 2 strings:
- First argument is the name of the Markdown file
- Second argument is the output file name

If number of arguments < 2:
print in STDERR Usage: ./markdown2html.py README.md README.html and exit 1
If Markdown file doesn't exist:
print in STDER Missing <filename> and exit 1
Otherwise, print nothing and exit 0
"""


if __name__ == "__main__":
    import sys
    from os import path
    import re
    import hashlib

    hash_dict = {"#": "h1", "##": "h2", "###": "h3", "####": "h4",
                 "#####": "h5", "######": "h6", "-": "ul", "*": "ol"}

    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    if not path.exists(sys.argv[1]) or not str(sys.argv[1]).endswith(".md"):
        sys.stderr.write("Missing " + sys.argv[1] + '\n')
        exit(1)

    def funcHeadings(pattern):
        tag = hash_dict[lineSplit[0]]
        toWrite = line.replace("{} ".format(lineSplit[0]), "<{}>".format(tag))
        toWrite = toWrite[:-1] + ("</{}>\n".format(tag))
        fw.write(toWrite)

    def funcInline(line, pattern):
        flag = 0
        while pattern in line:
            if not flag:
                if pattern == "**":
                    line = line.replace(pattern, "<b>", 1)
                    flag = 1
                else:
                    line = line.replace(pattern, "<em>", 1)
                    flag = 1
            else:
                if pattern == "**":
                    line = line.replace(pattern, "</b>", 1)
                    flag = 0
                else:
                    line = line.replace(pattern, "</em>", 1)
                    flag = 0
        return line

    def md5Markdown(line):
        rep = []
        while "[[" in line and "]]" in line:
            rep = []
            for count in range(len(line)):
                if not count == len(line) - 1 and line[count] == '[' and line[count + 1] == '[':
                    rep.append(count)
                elif not count == len(line) - 1 and line[count] == "]" and line[count + 1] == ']':
                    rep.append(count)
            if rep:
                sliceObj = slice(rep[0], rep[1] + 2)

            toRep = line[sliceObj]
            toHash = toRep[2:-2]
            md = hashlib.md5(toHash.encode()).hexdigest()
            line = line.replace(toRep, md)
        return line

    def funcForCases(line):
        rep = []
        s = ''
        while '((' in line:
            rep = []
            for count in range(len(line)):
                if not count == len(line) - 1 and line[count] == '(' and line[count + 1] == '(':
                    rep.append(count)
                elif not count == len(line) - 1 and line[count] == ")" and line[count + 1] == ')':
                    rep.append(count)
            if rep:
                sliceObj = slice(rep[0], rep[1] + 2)
            toRep = line[sliceObj]
            s = toRep
            for char in toRep:
                if char == 'c':
                    toRep = toRep.replace('c', '')
                elif char == 'C':
                    toRep = toRep.replace('C', '')
            line = line.replace(s, toRep[2:-2])
        return line

    with open(sys.argv[1], mode='r') as fr, open(sys.argv[2], mode='w+') as fw:
        first = 0
        f = 0
        read = fr.readlines()
        for i, line in enumerate(read):
            # For inline markdown
            if "**" in line:
                line = funcInline(line, "**")
            if "__" in line:
                line = funcInline(line, "__")
            if "[[" in line and "]]" in line:
                line = md5Markdown(line)
            if "((" in line and "))" in line:
                line = funcForCases(line)

            # split by spaces
            lineSplit = line.split(' ')
            if lineSplit[0] in hash_dict:
                # Headings
                if lineSplit[0].startswith('#'):
                    funcHeadings(lineSplit[0])
                # Lists
                elif lineSplit[0].startswith("-") or lineSplit[0].startswith("*"):
                    tag = hash_dict[lineSplit[0]]
                    #if its the first item list
                    if not first:
                        toWrite = "<{}>\n".format(tag)
                        fw.write(toWrite)
                        first = lineSplit[0]
                    # do every time for '-' or '*'
                    toWrite = line.replace("{} ".format(lineSplit[0]), "<li>")
                    toWrite = toWrite[:-1] + ("</li>\n")
                    fw.write(toWrite)
                    # if its the last item list
                    if i is len(read) - 1 or not read[i + 1].startswith("{} ".format(first)):
                        toWrite = "</{}>\n".format(tag)
                        fw.write(toWrite)
                        first = 0
            else:
                # paragraphs
                if line[0] != "\n":
                    #first paragraph
                    if not f:
                        fw.write("<p>\n")
                        f = 1
                    fw.write(line)
                    # if next line is part of the paragraph
                    if i != len(read) - 1 and read[i + 1][0] != "\n" and read[i + 1][0] not in hash_dict:
                        fw.write("<br/>\n")
                    else:
                        fw.write("</p>\n")
                        f = 0
        exit(0)
