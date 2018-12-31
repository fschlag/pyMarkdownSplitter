# pyMarkdownSplitter (Version: 0.4)

## Latest changes
### 0.4
* More generic way to generate navigation links for previous and next section (see [Navigation template example](#navigation-template-example))
* Refactoring
### 0.3
* Removed leading `http://` in local to global link conversion
* Previous and next chapter Links on bottom of each page
* Inputfile and Outputdir are now required arguments (they were before, but I've never checked  ;-))
### 0.2
* Remove non valid filename characters (e.g. `',', ';', '/'`).

## CI Status
[![Build Status](https://travis-ci.org/fschlag/pyMarkdownSplitter.svg?branch=master)](https://travis-ci.org/fschlag/pyMarkdownSplitter)

## Usage
```
python pymarkdownsplitter.py -i <inputfile> -o <outputdir> [-nt NAVIGATION_TEMPLATE]
```

### Navigation template example
By default pyMarkdownSplitter generates a navigation like this:

```[&larr; Previous Section](find-and-query.html) | [Next Section &rarr;](entity-adapter-and-descriptor.html)```

Leads to: [&larr; Previous Section](previous.html) | [Next Section &rarr;](next.html)

If you want to use a custom template, you can create a template file using the following _markers_:

Marker | Description
--- | ---
`#pymarkdown-previous-start#` | Marks the start of the previous link part
`#pymarkdown-previous-end#` | Marks the end of the previous link part
`#pymarkdown-previous-link#` | Placeholder for the previous link. Will be replaced with the corresponding html file.
`#pymarkdown-next-start#` | Marks the start of the next link part
`#pymarkdown-next-end#` | Marks the end of the next link part
`#pymarkdown-next-link#`| Placeholder for the next link. Will be replaced with the corresponding html file.
`#pymarkdown-separator-start#` | Marks the start of the separator i.e. the part between next and previous. Is only created if next AND previous link are generated. 
`#pymarkdown-separator-end#` | Marks the end of the separator.

#### Default template
```
#pymarkdown-previous-start#[&larr; Previous Section](#pymarkdown-previous-link#)#pymarkdown-previous-end##pymarkdown-separator-start# | #pymarkdown-separator-end##pymarkdown-next-start#[Next Section &rarr;](#pymarkdown-next-link#)#pymarkdown-next-end#
```

#### Example HTML template (see [templates/html_navigation.template](templates/html_navigation.template))
```
<div class="subpage-navigation"><p>#pymarkdown-previous-start#<a id="prev" href="#pymarkdown-previous-link#"> Prev.</a>#pymarkdown-previous-end##pymarkdown-separator-start# | #pymarkdown-separator-end##pymarkdown-next-start#<a id="next" href="#pymarkdown-next-link#">Next </a>#pymarkdown-next-end#</p></div>
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
