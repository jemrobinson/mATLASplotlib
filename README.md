mATLASplotlib
=============

Matplotlib wrappers to allow plots compatible with the ATLAS style guidelines.

To allow matplotlib to use Helvetica (required for ATLAS style) follow the guidelines from here http://blog.olgabotvinnik.com/blog/2012/11/15/2012-11-15-how-to-set-helvetica-as-the-default-sans-serif-font-in/ (reproduced below). For Linux users, adding the .ttf fonts to ~/.fonts and removing ~/.matplotlib/fontList.cache ~/.matplotlib/fontManager.cache ~/.matplotlib/ttffont.cache should be enough.


1. Download and install Fondu to convert Mac-Helvetica to ttf-Helvetica
`brew install fondu`

2. Find Helvetica on your system
Probably somewhere like: `/System/Library/Fonts/Helvetica.dfont`

3. Find where matplotlib stores its data

`$ python
>>>import matplotlib; matplotlib.matplotlib_fname()
u'/Users/james/.matplotlib/matplotlibrc'`

We need to put the `.ttf` in this path in `fonts/ttf`

4. Create the `.ttf`
`sudo fondu -show /System/Library/Fonts/Helvetica.dfont`

5. Edit your `.matplotlibrc` file
Edit `~/.matplotlib/matplotlibrc`, find the line `font.sans-serif : Bitstream Vera Sans, ...` and put `Helvetica` at the beginning of this list

6. Force matplotlib to re-scan the font lists
Now we need to force matplotlib to re-create the font lists by removing the files.
`rm ~/.matplotlib/fontList.cache ~/.matplotlib/fontManager.cache ~/.matplotlib/ttffont.cache`


Examples
========

Examples which reproduce the plots on this page (https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/PubComPlotStyle) are included in the `examples` folder.
