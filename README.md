# Unbound2Athens
Convert unbound format bible to Athens

### What it is
A quick and dirty python3 script to parse bibles from unbound format and create a fake Roam Research EDN export.
That fake Roam Research EDN export can then be imported into Athens software https://github.com/athensresearch/athens/

### What it can't do
Warning : the EDN file **can't be used** to import unbound bibles onto Roam Research
If that's your usecase you should have a look here : https://www.zsolt.blog/2020/12/importing-bible-to-roam-final-solution.html
The script hasn't been tested intensively and I currently use it only to create heavy Athens databases for stress tests
There may be some bugs or unexpected behaviours

### What is unbound format
Unbound project has sadly been stopped a few months ago. It meant to provide with plain text bibles in various languages from public domain editions
https://www.biola.edu/unbound
Fortunately I was able to download most of the existing unbound bibles, that you can find in my dedicated repository
