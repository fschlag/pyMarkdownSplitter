#!/usr/bin/env python

import argparse
import os
import re
import sys

VERSION = "0.5"
HELP_TEXT = "pymarkdownsplitter.py -i <inputfile> -o <outputdir>"

EMPTY_LINE = '\n'

TEMPLATE_PREVIOUS_START = "#pymarkdown-previous-start#"
TEMPLATE_PREVIOUS_END = "#pymarkdown-previous-end#"
TEMPLATE_PREVIOUS_LINK = "#pymarkdown-previous-link#"

TEMPLATE_NEXT_START = "#pymarkdown-next-start#"
TEMPLATE_NEXT_END = "#pymarkdown-next-end#"
TEMPLATE_NEXT_LINK = "#pymarkdown-next-link#"

TEMPLATE_SEPARATOR_START = "#pymarkdown-separator-start#"
TEMPLATE_SEPARATOR_END = "#pymarkdown-separator-end#"

DEFAULT_NAVIGATION_TEMPLATE = "#pymarkdown-previous-start#[&larr; Previous Section](#pymarkdown-previous-link#)#pymarkdown-previous-end##pymarkdown-separator-start# | #pymarkdown-separator-end##pymarkdown-next-start#[Next Section &rarr;](#pymarkdown-next-link#)#pymarkdown-next-end#"

MD_CODEBLOCK = "```"
MD_H1 = "# "
NEW_HEADER = "% "

class Section:
    def __init__(self):
        self.title = ''
        self.lines = []
        self.next_section = None
        self.previous_section = None

    @classmethod
    def build_with_linked_sections(cls, previous_section, header_section):
        section = cls()
        if previous_section is not None:
            previous_section.next_section = section
            section.previous_section = previous_section
        else:
            section.previous_section = header_section
            header_section.next_section = section
        return section

    def get_cleaned_title(self):
        return self.title.rstrip('\n')

    def _get_converted_title(self):
        # to lower
        converted_title = self.get_cleaned_title().lower()
        # replace whitespace with underscore
        converted_title = converted_title.replace(' ', '-')
        # remove non valid filename characters
        converted_title = re.sub('[^0-9a-zA-Z-]+', '', converted_title)
        return converted_title

    def get_html_link(self):
        return self._get_converted_title() + ".html"

    def get_markdown_link(self):
        return self._get_converted_title() + ".md"

    def has_next_section(self):
        return self.next_section is not None

    def has_previous_section(self):
        return self.previous_section is not None


class ParsedFile:
    def __init__(self, header_section, sections):
        self.header_section = header_section
        self.sections = sections

    def getAllSections(self):
        outsections = self.sections
        outsections.insert(0, self.header_section)
        return outsections


class NavigationTemplate:
    def __init__(self, template_text):
        self.prefix = template_text[:template_text.find(TEMPLATE_PREVIOUS_START)]
        self.postfix = template_text[template_text.find(TEMPLATE_NEXT_END) + len(TEMPLATE_NEXT_END):]
        match = re.search(TEMPLATE_PREVIOUS_START + '(.+?)' + TEMPLATE_PREVIOUS_END, template_text)
        if match:
            self.previous = match.group(1)
        match = re.search(TEMPLATE_NEXT_START + '(.+?)' + TEMPLATE_NEXT_END, template_text)
        if match:
            self.next = match.group(1)
        match = re.search(TEMPLATE_SEPARATOR_START + '(.+?)' + TEMPLATE_SEPARATOR_END, template_text)
        if match:
            self.separator = match.group(1)
        self.valid_template = self.previous is not None and self.next is not None and TEMPLATE_PREVIOUS_LINK in self.previous and TEMPLATE_NEXT_LINK in self.next

    def generate_navigation_text(self, section):
        line = self.prefix
        if section.has_previous_section():
            previous_navigation = self.previous.replace(TEMPLATE_PREVIOUS_LINK,
                                                        section.previous_section.get_html_link())
            line = line + previous_navigation
        if section.has_previous_section() and section.has_next_section():
            line = line + self.separator
        if section.has_next_section():
            next_navigation = self.next.replace(TEMPLATE_NEXT_LINK, section.next_section.get_html_link())
            line = line + next_navigation

        line = line + self.postfix
        return line


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


def create_link_for_index_file(title, html_link):
    return "[" + title + "](" + html_link + ")\n"


def replace_local_link_with_global(line):
    """Currently only replaces 'first level links' e.g. "# Heading 1" with the corresponding html-file"""
    """ToDO: Find a way to replace different levels "##" and so on (need to collect all heading and map them in each section)"""
    pattern = re.compile('(?<=\]\(#)([\w,-]+)')
    for m in re.finditer(pattern, line):
        line = line.replace("](#" + m.group(0), "](" + m.group(0) + ".html")
    return line


def parse_file(inputfile):
    header_section = None
    sections = []
    in_codeblock = False
    with open(inputfile, 'r') as input:
        current_section = None
        for line in input:
            if line.startswith(MD_CODEBLOCK):
                in_codeblock = not in_codeblock
            if line.startswith(MD_H1) and not in_codeblock:  # Creating new section
                new_section = Section.build_with_linked_sections(current_section, header_section)
                current_section = new_section
                sections.append(current_section)
                current_section.title = line.replace(MD_H1, "", 1)
                if header_section is not None:
                    header_section.lines.append(create_link_for_index_file(current_section.get_cleaned_title(),
                                                                           current_section.get_html_link()))
                    header_section.lines.append(EMPTY_LINE) # to not have the links all in one line
            elif current_section is not None:  # Reading parts of section
                current_section.lines.append(replace_local_link_with_global(line))
            elif header_section is None and line.startswith(NEW_HEADER):  # Creating header
                header_section = Section()
                header_section.title = line.replace(NEW_HEADER, "", 1)
            else:  # Writing leading header section lines
                header_section.lines.append(line)

    return ParsedFile(header_section, sections)


def save_new_file_with_title(filename, title, lines):
    with open(filename, 'w') as f:
        f.write("% " + title)
        for line in lines:
            f.write(line)


def save_parsed_file_to_output_directory(parsed_file, outputdir, navigation_template):
    # Save each section
    for section in parsed_file.getAllSections():
        output_lines = section.lines
        if not navigation_template.valid_template:
            print("Navigation template is invalid. Will NOT generate any navigation links.")
        else:
            output_lines.append(navigation_template.generate_navigation_text(section))

        save_new_file_with_title(outputdir + "/" + section.get_markdown_link(),
                                 section.title,
                                 output_lines)


def work(arg_inputfile, arg_outputdir, arg_navigation_template):
    create_output_directory(arg_outputdir)
    parsed_file = parse_file(arg_inputfile)
    save_parsed_file_to_output_directory(parsed_file, arg_outputdir, NavigationTemplate(arg_navigation_template))


if __name__ == '__main__':
    print("pyMarkdownSplitter (Version: " + VERSION + ")")
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", "--inputfile", help="Markdown input file to split", required=True)
    argument_parser.add_argument("-o", "--outputdir",
                                 help="Output directory for the splitted markdowns. Created if missing.", required=True)
    argument_parser.add_argument("-nt", "--navigation-template",
                                 help="Template file for generating navigation links.", default="DEFAULT")
    args = argument_parser.parse_args()

    if args.navigation_template != "DEFAULT":
        try:
            with open(args.navigation_template, 'r') as template_file:
                navigation_template = template_file.read()
        except FileNotFoundError:
            print("Template file %s not found" % args.navigation_template)
    else:
        navigation_template = DEFAULT_NAVIGATION_TEMPLATE

    work(args.inputfile, args.outputdir, navigation_template)
