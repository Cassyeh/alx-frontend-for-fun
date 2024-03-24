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

import argparse
import pathlib
import re
import sys


def md_to_html(file_input, file_output):
    '''
    Converts markdown file to HTML file
    '''
    with open(file_input, encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    for line in md_content:
        # Check if the line is a heading
        match = re.match(r'(#){1,6} (.*)', line)
        if match:
            # Get the level of the heading
            h_level = len(match.group(1))
            # Get the content of the heading
            h_content = match.group(2)
            # Append the HTML equivalent of the heading
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
        else:
            html_content.append(line)

    # Write the HTML content to the output file
    with open(file_output, 'w', encoding='utf-8') as f:
        f.writelines(html_content)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert markdown to HTML')
    parser.add_argument('file_input', help='path to input markdown file')
    parser.add_argument('file_output', help='path to output HTML file')
    args = parser.parse_args()

    # Check if the input file exists
    input_path = pathlib.Path(args.file_input)
    if not input_path.is_file():
        print(f'Missing {input_path}', file=sys.stderr)
        sys.exit(1)

    # Convert the markdown file to HTML
    md_to_html(args.file_input, args.file_output)
