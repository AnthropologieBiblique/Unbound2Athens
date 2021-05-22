# Test Random Strings Python
import string
import random
import fileinput


# random UID creator
def createUID():
	letters = string.ascii_letters
	return(''.join(random.choice(letters) for i in range(9)))

def createDatom(datomNumber, datomType, datomValue):
	return("[" + str(datomNumber) + " " + datomType + " " + str(datomValue) + " 536870912]")

def createChildrenDatom(datomNumber, childNumber):
	childNumber = datomNumber + childNumber
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


print(createChildrenDatom("52","23"))
print(createUIDDatom("52"))
print(createClosedDatom("52"))
print(createTitleDatom("52", "Bonjour comment allez-vous ?"))
print(createStringDatom("52", "Bonjour comment allez-vous ?"))

f = open('test.txt', 'w')
def createChapter(chapterNumber, chapterName, blockNumber):
	chapterNumber = f"{chapterNumber:02d}"
	for i in range(blockNumber):
		i = f"{i:02d}"
		f.write(createChildrenDatom(chapterNumber,i)+"\n")
	f.write(createOpenDatom(chapterNumber)+"\n")
	chapterName = chapterName + chapterNumber
	f.write(createStringDatom(chapterNumber,chapterName)+"\n")
	f.write(createUIDDatom(chapterNumber)+"\n")
	for i in range(blockNumber):
		datomNumber = chapterNumber + f"{i:02d}"
		f.write(createOpenDatom(datomNumber)+"\n")
		string = "This is the block number "+str(datomNumber)
		f.write(createStringDatom(datomNumber, string)+"\n")
		f.write(createUIDDatom(datomNumber)+"\n")

def createPage(pageNumber, pageTitle, childrenChapter):
	pageNumber = f"{pageNumber:02d}"
	childrenChapter = f"{childrenChapter:02d}"
	f.write(createChildrenDatom(pageNumber,childrenChapter)+"\n")
	f.write(createOpenDatom(pageNumber)+"\n")
	f.write(createUIDDatom(pageNumber)+"\n")
	f.write(createTitleDatom(pageNumber,pageTitle)+"\n")

createPage(0,"Page",1)
createChapter(1,"Chapitre",3)

testEDN = open('testEDN.edn','w')
f = open('test.txt', 'r')
prefix = open('edn/prefix.edn', 'r')
suffix = open('edn/suffix.edn', 'r')

for line in prefix:
	testEDN.write(line)

for line in f:
	testEDN.write(line)

for line in suffix:
	testEDN.write(line)
