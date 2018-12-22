#!/usr/bin/env python

import argparse
import os
import re
import string
import sys

VERSION = "0.1"
HELP_TEXT = "pymarkdownsplitter.py -i <inputfile> -o <outputdir>"


class Section:
    def __init__(self):
        self.title = ''
        self.lines = []

    def get_cleaned_title(self):
        return self.title.rstrip('\n')

    def get_converted_title(self):
        return self.get_cleaned_title().lower().replace(' ', '-')


class ParsedFile:
    def __init__(self, header_section, sections):
        self.header_section = header_section
        self.sections = sections


def create_output_directory(dir):
    if os.path.isdir(dir):
        print("Output directory already exists.")
        if len(os.listdir(dir)) > 0:
            print("Error: Output directory exists but is not empty.")
            sys.exit(2)
        else:
            print("Using existing output directory")
    else:
        print("Creating directory " + dir)
        os.mkdir(dir)


def create_link_for_index_file(title, raw_filename):
    return "[" + title + "](http://" + raw_filename + ".html)\n"


def replace_local_link_with_global(line):
    """Currently only replaces 'first level links' e.g. "# Heading 1" with the corresponding html-file"""
    """ToDO: Find a way to replace different levels "##" and so on (need to collect all heading and map them in each section)"""
    pattern = re.compile('(?<=\]\(#)([\w,-]+)')
    for m in re.finditer(pattern, line):
        line = line.replace("](#" + m.group(0), "](http://" + m.group(0) + ".html")
    return line


def parse_file(inputfile):
    header_section = None
    sections = []
    with open(inputfile, 'r') as input:
        current_section = None
        for line in input:
            if line.startswith("# "):  # Creating new section
                current_section = Section()
                sections.append(current_section)
                current_section.title = line.replace("# ", "", 1)
                if header_section is not None:
                    header_section.lines.append(create_link_for_index_file(current_section.get_cleaned_title(),
                                                                           current_section.get_converted_title()))
            elif current_section is not None:  # Reading parts of section
                current_section.lines.append(replace_local_link_with_global(line))
            elif header_section is None and line.startswith("% "):  # Creating header
                header_section = Section()
                header_section.title = line.replace("% ", "", 1)
            else:  # Writing leading header section lines
                header_section.lines.append(line)

    return ParsedFile(header_section, sections)


def save_parsed_file_to_output_directory(parsed_file, outputdir):
    # Save header
    with open(outputdir + "/" + parsed_file.header_section.get_converted_title() + ".md", 'w') as f:
        f.write("% " + parsed_file.header_section.title)
        for line in parsed_file.header_section.lines:
            f.write(line)
    for sec in parsed_file.sections:
        with open(outputdir + "/" + sec.get_converted_title() + ".md", 'w') as f:
            f.write("% " + sec.title)
            for line in sec.lines:
                f.write(line)


def work(inputfile, outputdir):
    create_output_directory(outputdir)
    parsed_file = parse_file(inputfile)
    save_parsed_file_to_output_directory(parsed_file, outputdir)


if __name__ == '__main__':
    print("pyMarkdownSplitter (Version: " + VERSION + ")")
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", "--inputfile", help="Markdown input file to split")
    argument_parser.add_argument("-o", "--outputdir",
                                 help="Output directory for the splitted markdowns. Created if missing.")
    args = argument_parser.parse_args()
    work(args.inputfile, args.outputdir)
