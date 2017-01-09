#pyÉcrire

**Simple Book Writing**

Written for Python3, with Gtk3 and an WebKit3 based editor.

pyÉcrire is a simple book writing program for organising scenes, plot descriptions, character profiles, etc in an
organised interface. It is mainly written for my own personal book writing projects, and therefore suited to my own
needs. That said, I try to avoid adding complex features. The core idea is to have a layout with available files in a
tree view with a large editor with the feel of a document editor.

The files are organised either as part of a book (plot and scene files), or part of a universe (history and character
files). A book belongs to a universe, but a universe can have several books. The files are stored as plain HTML in
timestamped files with a folder for each file. Meaning that it tracks changes to some extent. All meta data is stored
in text files in each folder.

A lot of features are not yet working, and there are probably a number of bugs.

**Current features are:**

* HTML based editor that allows for three heading styles, lists and preformatted text.
* Editor can either be formatted with indented lines for each paragraph, or with a space between thes. The format can
  be selected for each file type.
* Scene files can be organised into numbered chapters, prologue or epilogue chapters, and moved freely within and
  between these. The intention is to add export features to concatenate these files into whole documents.
* Files are by default not editable, but the first menu button enables editing. This also starts a timer that records
  the amount of time spent editing, as well as words and characters added. The timer pauses if no changes are made for
  a given amount of time (by default 60 seconds). The time spent is recorded in a csv file in each file folder, named
  timing.txt.

**Features currently missing:**

* Cannot yet actually add universe-related files
* Spell checker not yet functioning
* Cannot delete files
* Cannot manually order files
* Most of the menu items have not been attached to functions
* The GUI for settings have not been set up, but the config file is found in the OS default user config location.

The current code is only tested on Ubuntu 16.04, where it is developed. It is theoretically cross-platform, and I have
tried to avoid platform dependent code, but it hasn't been tested yet.

