# pyMarkdownSplitter (Version: 0.1)

## CI Status
[![Build Status](https://travis-ci.org/pyMarkdownSplitter/pyMarkdownSplitter.svg)](https://travis-ci.org/fschlag/pyMarkdownSplitter)

## Usage
```
python pymarkdownsplitter.py -i <inputfile> -o <outputdir>
```

## How it works
pyMarkdownSplitter reads the `inputfile` and searches for top-level headers (`#` aka H1).
For every top-level header a separate section file is created, using the header title as a filename.
(The header is converted to lowercase and whitespaces are replaced by dashes (-).

If a `[link description](link reference)` to a top-level heading is found, it is replaced by link pointing to the new md file, ending with `.html`.

## Example
Using the following Markdown file as an input 
```
% Manual

# Find and Query

Here is a [first link](#insert-and-update) and another link [second link](#blub-and-update)

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam

## Query
Some text in a subsection

# Insert and Update

Usually refers to a single entity. 

## Insert

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
```
creates three new files:
### manual.md - Index file
```
% Manual

[Find and Query](http://find-and-query.html)
[Insert and Update](http://insert-and-update.html)
```

### find-and-query.md - for the first section
```
% Find and Query

Here is a [first link](http://insert-and-update.html) and another link [second link](http://blub-and-update.html)

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam

## Query
Some text in a subsection
```

### insert-and-update.md - for the second section
```
% Insert and Update

Usually refers to a single entity. 

## Insert

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
```
