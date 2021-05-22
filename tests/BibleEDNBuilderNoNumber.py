# Test Random Strings Python
import string
import random
import fileinput
import re

# random UID creator
def createUID():
	letters = string.ascii_letters
	return(''.join(random.choice(letters) for i in range(9)))

def createDatom(datomNumber, datomType, datomValue):
	return("[" + str(datomNumber) + " " + datomType + " " + str(datomValue) + " 536870912]")

def createChildrenDatom(datomNumber, childNumber):
	datomType = ":block/children"
	return createDatom(datomNumber, datomType, childNumber)

def createUIDDatom(datomNumber):
	datomValue = "\"" + createUID() + "\""
	datomType = ":block/uid"
	return createDatom(datomNumber, datomType, datomValue)

def createOpenDatom(datomNumber):
	datomType = ":block/open"
	datomValue = "true"
	return createDatom(datomNumber, datomType, datomValue)

def createClosedDatom(datomNumber):
	datomType = ":block/open"
	datomValue = "false"
	return createDatom(datomNumber, datomType, datomValue)

def createTitleDatom(datomNumber, title):
	datomType = ":node/title"
	datomValue = "\"" + title + "\""
	return createDatom(datomNumber, datomType, datomValue)

def createStringDatom(datomNumber, string):
	datomType = ":block/string"
	datomValue = "\"" + string + "\""
	return createDatom(datomNumber, datomType, datomValue)

def writeLine(f,line):
	f.write(line+"\n")

def terminateBiblePage(title):
	page = open(title+'page.edn', 'a')
	writeLine(page,createOpenDatom(999))
	writeLine(page,createUIDDatom(999))
	writeLine(page,createTitleDatom(999,"📖 Bible "+title))

def createBookBlock(bookTuple, title):
	page = open(title+'page.edn','a')
	writeLine(page,createChildrenDatom(999,"9555"+bookTuple[0]))
	bookBlock = open(title+'page.edn','a')
	writeLine(bookBlock,createOpenDatom("9555"+bookTuple[0]))
	bookTitle = "[[📖 " + title + " " + bookTuple[1] + "]]"
	writeLine(bookBlock,createStringDatom("9555"+bookTuple[0],bookTitle))
	writeLine(bookBlock,createUIDDatom("9555"+bookTuple[0]))

def terminateBookPage(bookTuple, title):
	page = open(title+'page.edn', 'a')
	writeLine(page,createOpenDatom("999"+bookTuple[0]))
	writeLine(page,createUIDDatom("999"+bookTuple[0]))
	writeLine(page,createTitleDatom("999"+bookTuple[0],"📖 "+title+" "+bookTuple[1]))

def bookNameParser(path):
	bookNames = open(path+'/book_names.txt', 'r')
	bookList = []
	for line in bookNames:
		bookList.append(re.findall(r'(\d\d)[A-Z].(.*)',line)[0])
	return(bookList)

def bibleParser(dict, title,path,name):
	bible = open(path+'/'+name+'_utf8.txt','r')
	parsedBible = open(title+'verses'+'.edn','a')
	book = "00"
	chapter = "00"
	indent = 10
	for line in bible:
		verse = re.findall(r'(\d\d)[A-Z]\s(\d+)\s+(\d+)\s(.+)',line)
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
			verseText = "^^"+dict[verse[0]]+" "+verse[1]+":"+verse[2]+"^^ "+verse[3]
			writeLine(parsedBible,createChildrenDatom("777"+verse[0]+verse[1],indent))
			writeLine(parsedBible,createOpenDatom(indent))
			writeLine(parsedBible,createUIDDatom(indent))
			writeLine(parsedBible,createStringDatom(indent,verseText))
			indent+=10

def bibleBuilder(title,path,name):
	### PROGRAM ###
	open(title+'page.edn', 'w')
	open(title+'.edn','w')
	open(title+'verses.edn','w')

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
	bible = open(title+'.edn','a')
	prefix = open('edn/prefix.edn','r')
	suffix = open('edn/suffix.edn','r')
	pageBible = open(title+'page.edn', 'r')
	versesBible = open(title+'verses.edn', 'r')
	for line in prefix:
		writeLine(bible,line)
	for line in pageBible:
		writeLine(bible,line)
	for line in versesBible:
		writeLine(bible,line)
	for line in suffix:
		writeLine(bible,line)

#bibleBuilder("WLC","wlc","wlc")
#bibleBuilder("ASV","asv","asv")
#bibleBuilder("WEB","web","web")
#bibleBuilder("MYANMAR","myanmar_judson_1835","myanmar_judson_1835")
#bibleBuilder("LXX","lxx_a_unaccented","lxx_a_unaccented")
#bibleBuilder("VUL","latin_nova_vulgata","latin_nova_vulgata")
#bibleBuilder("LSG","french_lsg","french_lsg")

#bibleBuilder("DRB","french_darby","french_darby")
#bibleBuilder("MRT","french_martin_1744","french_martin_1744")

#bibleBuilder("PST","peshitta","peshitta")
#bibleBuilder("SRV","spanish_reina_valera_1909","spanish_reina_valera_1909")
#bibleBuilder("SVD","arabic_svd","arabic_svd")

