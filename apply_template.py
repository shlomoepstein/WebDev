'''apply_template.py
This script applies an HTML template to all HTML files in a directory. It keeps
everything between the <nav> and <footer>, and replaces the rest with the template.

Rename files to anything other than *.html to exclude them.

Command line arguments:
    arg 1: The directory to run in
        default: The current directory
    arg 2: The template file
        default: File named 'template.html' in the working directory

There are no command line switches. If you want to set the template file, call
the script with arg 1 as '.'.

Author: Shlomo Epstein
Date: 2024-04-09
'''


from sys import argv as args
import os, re
from os.path import (isdir,
                     isfile,
                     exists,
                     dirname,
                     normpath,
                     realpath,
                     join as joinpath)


# Get the file extension from the last component of a path

def ext(path):
    return os.path.splitext(path)[1]


# Main

def main():

    # Get the directory from arg 1, if it's set. Default is current directory

    html_dir = os.curdir

    if len(args) > 1:
        html_dir = normpath(args[1])

    # Abort if html_dir doesn't exist or is not a directory

    if not exists(html_dir):
        print(f'{html_dir} does not exist')
        return
    if not isdir(html_dir):
        print(f'{html_dir} is not a directory')
        return

    # Get the template file from arg 2, if it's set. Default is 'template.html'
    # in the working directory

    template_path = normpath(joinpath(html_dir, 'template.html'))

    if len(args) > 2:
        template_path = normpath(args[2])

    # Abort if template_path doesn't exist or is not a file

    if not exists(template_path):
        print(f'{template_path} does not exist')
        return
    if not isfile(template_path):
        print(f'{template_path} is not a file')
        return

    # Get all html files besides for the template

    html_files = []

    for entry in os.scandir(html_dir):
        if (ext(entry) == '.html' and realpath(entry) != realpath(template_path)):
            html_files.append({'path': normpath(entry.path)})

    # Get the main content from each file

    for html in html_files:
        main = ''

        with open(html['path']) as file:
            in_main = False

            for line in file:

                # nasty hack, need to rewrite script to allow granular
                # control, probably going to need a separate config file
                if re.search(r'Author:', line):
                    html['author'] = line
                if re.search(r'Filename:', line):
                    html['filename'] = line
                if re.search(r'Date:', line):
                    html['date'] = line
                if re.search(r'<title>', line):
                    html['title'] = line

                if line.strip() == '</nav>':
                    in_main = True
                    continue

                if line.strip() == '</main>':
                    main += line
                    break

                if in_main:
                    main += line

        html['main'] = main

    # Get the contents of the template file

    template = ['', '']

    with open(template_path) as template_file:
        before_main = True
        after_main = False

        for line in template_file:

            # big bandaid (also they should stop killing ducks to make duck tape)
            if re.search(r'Author:', line):
                template[0] += html['author']
                continue
            if re.search(r'Filename:', line):
                template[0] += html['filename']
                continue
            if re.search(r'Date:', line):
                template[0] += html['date']
                continue
            if re.search(r'<title>', line):
                template[0] += html['title']
                continue

            if line.strip() == '</nav>':
                template[0] += line
                before_main = False

            if line.strip() == '</main>':
                after_main = True
                continue

            if before_main:
                template[0] += line

            if after_main:
                template[1] += line

    # Warn user before modifying files

    if html_dir != '.':
        print(f'Working directory:\n  {html_dir}\n')

    print(f'Template:\n  {template_path}')

    # Extra warning in case this was unintended
    if realpath(dirname(template_path)) != realpath(html_dir):
        print('\nTemplate file is not from the working directory')

    print('\nThe following file(s) will be modified:')
    for html in html_files:
        print(f'  {html["path"]}')

    match input('\nWould you like to continue? (y, n): ').lower():
        case 'y':
            pass
        case 'yes':
            pass
        case _:
            print('\nNo files have been modified')
            return

    # Apply the template

    for html in html_files:
        with open(html['path'], 'w') as file:
            file.write(template[0])
            file.write(html['main'])
            file.write(template[1])

    # Let the user know that the thing did the thing

    print('\nTemplate applied')


if __name__ == '__main__':
    main()
