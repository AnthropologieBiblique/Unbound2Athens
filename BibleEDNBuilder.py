import string
import random
import fileinput
import re

### GENERAL FUNCTIONS FOR DATOM CREATION

# random UID creator
def createUID():
	letters = string.ascii_letters
	return(''.join(random.choice(letters) for i in range(9)))

# Datom creator. The base structure is [datomNumber datomType datomValue UserNumber]. I hardcode the user number for a random value.
def createDatom(datomNumber, datomType, datomValue):
	return("[" + str(datomNumber) + " " + datomType + " " + str(datomValue) + " 536870912]")

# Creates a children datom. Child of a page, or child of a block it's the same. Inputs are the datomNumber (address) of the parent, and the datomNumber (address) of the child.
def createChildrenDatom(datomNumber, childNumber):
	datomType = ":block/children"
	return createDatom(datomNumber, datomType, childNumber)

# Creates a random UID for a datom. Every datom MUST have a unique UID for Athens to import correctly. Input is the datomNumber (address)
def createUIDDatom(datomNumber):
	datomValue = "\"" + createUID() + "\""
	datomType = ":block/uid"
	return createDatom(datomNumber, datomType, datomValue)

# Creates a flag for the block to be opened. Input is datomNumber (address)
def createOpenDatom(datomNumber):
	datomType = ":block/open"
	datomValue = "true"
	return createDatom(datomNumber, datomType, datomValue)

# Creates a flag for the block to be closed. Input is datomNumber (address)
def createClosedDatom(datomNumber):
	datomType = ":block/open"
	datomValue = "false"
	return createDatom(datomNumber, datomType, datomValue)

# Creates a page title. The fact that a datom has a title property will flag it as a page for Athens. Inputs are datomNumber (address) and title
def createTitleDatom(datomNumber, title):
	datomType = ":node/title"
	datomValue = "\"" + title + "\""
	return createDatom(datomNumber, datomType, datomValue)

# Creates a block string. Every datom that doesn't have a title is considered as ablock and needs a string. Inputs are datomNumber (address) and string
def createStringDatom(datomNumber, string):
	datomType = ":block/string"
	datomValue = "\"" + string + "\""
	return createDatom(datomNumber, datomType, datomValue)

# Simple function to show datoms in columm by adding a newline at every file writing step. Much easier to review output files
def writeLine(f,line):
	f.write(line+"\n")

### BIBLE / UNBOUND SPECIFIC FUNCTIONS - ASSUMING A FIXED STRUCTURE
## The bible is a main [[Bible]] page with one block per [[Bible Book]]
## Each Bible book has its own page with title "Bible Book", with one closed block per chapter, and one opened sub-block per verse

# Create the main bible page. 999 address is used not to have any interferences with other datom numbers
def terminateBiblePage(title):
	page = open('output/'+title+'page.edn', 'a')
	writeLine(page,createOpenDatom(999))
	writeLine(page,createUIDDatom(999))
	writeLine(page,createTitleDatom(999,"📖 Bible "+title))

# This will create all the [[Bible Book]] children blocks from the 999 main bible page. 9555 is added before every datomNumber to be sure they are unique
def createBookBlock(bookTuple, title):
	page = open('output/'+title+'page.edn','a')
	writeLine(page,createChildrenDatom(999,"9555"+bookTuple[0]))
	bookBlock = open('output/'+title+'page.edn','a')
	writeLine(bookBlock,createOpenDatom("9555"+bookTuple[0]))
	bookTitle = "[[📖 " + title + " " + bookTuple[1] + "]]"
	writeLine(bookBlock,createStringDatom("9555"+bookTuple[0],bookTitle))
	writeLine(bookBlock,createUIDDatom("9555"+bookTuple[0]))

# This will create a unique page for each bible book, each page having a matching title with the address [[title]] that was added above
def terminateBookPage(bookTuple, title):
	page = open('output/'+title+'page.edn', 'a')
	writeLine(page,createOpenDatom("999"+bookTuple[0]))
	writeLine(page,createUIDDatom("999"+bookTuple[0]))
	writeLine(page,createTitleDatom("999"+bookTuple[0],"📖 "+title+" "+bookTuple[1]))

# Book list and dictionnary creator from the book names list
def bookNameParser(path):
	bookNames = open('input/'+path+'/book_names.txt', 'r')
	bookList = []
	for line in bookNames:
		bookList.append(re.findall(r'(\d\d)[A-Z].(.*)',line)[0])
	return(bookList)

# This is the main piece. 
# It will run through the unbound file, 
# detect each time it sees a new book, create the dedicated page, 
# detect each time it sees a new chapter, create the dedicated block,
# detect each time it sees a new verse, create the dedicated block
# the regex outputs a list including the book ID, chapter ID, verse ID
# by design, each verse already has a unique ID, which I simply use as the datomNumber for each verse
# The strange 888, 777 are meant not to have any conflicts and to be sure each datomNumber is very unique

def bibleParser(dict, title,path,name):
	bible = open('input/'+path+'/'+name+'_utf8.txt','r')
	parsedBible = open('output/'+title+'verses'+'.edn','a')
	book = "00"
	chapter = "00"
	for line in bible:
		verse = re.findall(r'(\d\d)[A-Z]\s(\d+)\s+(\d+)\s(|\S+)\s(\d+)\s(.+)',line)
		if not verse:
			pass
		else:
			verse = verse[0]
			if verse[0]!=book:
				writeLine(parsedBible,createOpenDatom("888"+verse[0]))
				writeLine(parsedBible,createUIDDatom("888"+verse[0]))
				writeLine(parsedBible,createTitleDatom("888"+verse[0],"📖 "+title+" "+dict[verse[0]]))
				book = verse[0]
			if verse[1]!=chapter:
				writeLine(parsedBible,createChildrenDatom("888"+verse[0],"777"+verse[0]+verse[1]))
				writeLine(parsedBible,createClosedDatom("777"+verse[0]+verse[1]))
				writeLine(parsedBible,createUIDDatom("777"+verse[0]+verse[1]))
				chapterTitle = "📜 "+dict[verse[0]]+" "+verse[1]
				writeLine(parsedBible,createStringDatom("777"+verse[0]+verse[1],chapterTitle))
				chapter = verse[1]
			verseText = "^^"+dict[verse[0]]+" "+verse[1]+":"+verse[2]+verse[3]+"^^ "+verse[5]
			writeLine(parsedBible,createChildrenDatom("777"+verse[0]+verse[1],verse[4]))
			writeLine(parsedBible,createOpenDatom(verse[4]))
			writeLine(parsedBible,createUIDDatom(verse[4]))
			writeLine(parsedBible,createStringDatom(verse[4],verseText))

# This collects the different pieces to create a title.edn file that (hopefully !) can directly be imported into Athens
def bibleBuilder(title,path,name):
	### PROGRAM ###
	open('output/'+title+'page.edn', 'w')
	open('output/'+title+'.edn','w')
	open('output/'+title+'verses.edn','w')

	### CREATION DICTIONNAIRE
	bookList = bookNameParser(path)
	bookDict = dict(bookList)

	### CREATION PAGE BIBLE AVEC BLOCKS LIVRES
	for book in bookList:
		createBookBlock(book, title)
		terminateBookPage(book, title)
	terminateBiblePage(title)

	### PARSING BIBLE
	bibleParser(bookDict, title,path,name)

	### CREATION EDN
	bible = open('output/'+title+'.edn','a')
	prefix = open('edn/prefix.edn','r')
	suffix = open('edn/suffix.edn','r')
	pageBible = open('output/'+title+'page.edn', 'r')
	versesBible = open('output/'+title+'verses.edn', 'r')
	for line in prefix:
		writeLine(bible,line)
	for line in pageBible:
		writeLine(bible,line)
	for line in versesBible:
		writeLine(bible,line)
	for line in suffix:
		writeLine(bible,line)

# /!\ Some bibles don't have a unique ID for each verse. In this case you should use the tests/bibleEDNBuilderNoNumber.py script, slightly different
# Most of them will work, though
# Some of them, despite the script running well, won't import into Athens, I still don't know why

bibleBuilder("ASV","asv","asv")
bibleBuilder("YLT","ylt","ylt")
bibleBuilder("LXX","lxx_a_unaccented","lxx_a_unaccented")
bibleBuilder("MYANMAR","myanmar_judson_1835","myanmar_judson_1835")
bibleBuilder("MRT","french_martin_1744","french_martin_1744")
bibleBuilder("WLC","wlc","wlc")
bibleBuilder("GB2000","greek_byzantine_2000","greek_byzantine_2000")
bibleBuilder("SWE","swedish_1917","swedish_1917")
bibleBuilder("NOR","norwegian","norwegian")
bibleBuilder("ROM","romanian_cornilescu","romanian_cornilescu")

# /!\ Caution, these need to be processed with the /tests/bibleEDNBuilderNoNumber.py instead
#bibleBuilder("SVD","arabic_svd","arabic_svd")

# /!\ Caution, these don't work for the moment (script runs, but Athens can't import)
#bibleBuilder("WEB","web","web")
#bibleBuilder("DRB","french_darby","french_darby")
#bibleBuilder("SRV","spanish_reina_valera_1909","spanish_reina_valera_1909")
#bibleBuilder("VUL","latin_nova_vulgata","latin_nova_vulgata")
#bibleBuilder("LSG","french_lsg","french_lsg")

# /!\ Caution, these need to be processed with the /tests/bibleEDNBuilderNoNumber.py instead AND they don't work (script runs, but Athens can't import)
#bibleBuilder("PST","peshitta","peshitta")


