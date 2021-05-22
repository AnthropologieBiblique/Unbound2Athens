# Test Random Strings Python
import string
import random
import fileinput
import re



def bookNameParser():
	bookNames = open('asv/book_names.txt', 'r')
	bookList = []
	for line in bookNames:
		bookList.append(re.findall(r'(\d\d)[A-Z].(.*)',line)[0])
	return(bookList)

#print(re.findall(r'(\S+)',"01O	Genesis"))
#print(bookNameParser())

def bibleParser(dict):
	bible = open('asv/lightasv_utf8.txt','r')
	book = "00"
	chapter = "00"
	for line in bible:
		verse = re.findall(r'(\d\d)[A-Z].(\d+).(\d+)..(\d+).(.+)',line)
		if not verse:
			pass
		else:
			verse = verse[0]
			if verse[0]!=book:
				print("new book !")
				book = verse[0]
			if verse[1]!=chapter:
				print("new chapter !")
				chapter = verse[1]
			verseText = "^^"+dict[verse[0]]+" "+verse[1]+":"+verse[2]+"^^ "+verse[4]
			print(verseText)

bookList = bookNameParser()
bookDict = dict(bookList)

bibleParser(bookDict)

