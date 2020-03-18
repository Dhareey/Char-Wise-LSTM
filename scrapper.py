

def getchap(book, chapter):
	import requests
	from bs4 import BeautifulSoup as soup

	"""
	This funtion scraps the yoruba version of the bible based on the book and chapter entered
	It also formats the text in the page as a normal bible passage text by
	a. Adding space after each verse number
	b. Removing the footer of the page
	c. Removing the reference verses
	d. Each verse to start on a new line
	Note:
	Format for bible books should be abbreviations, eg Genesis = Gen

	"""
	url = 'https://www.bible.com/bible/911/'
	point= '.'
	book = book.upper()
	# Request for page
	req = requests.get(url+book+point+chapter+point+'YCB')
	#Parse the page into HTML tree and extract passage from page
	page = soup(req.content, 'lxml')
	passages = page.find('div', class_='mw6 center pa3 pt4 pb7 mt6')
	# Extract each verse number
	numbers = [number.get_text() for number in passages.find_all('span', class_='label')]
	# Reference verses in page
	removetext = [verses.get_text() for verses in passages.find_all('span', class_= 'note x')]
	# Remove footer from passage
	passage = passages.get_text().split('Bíbélì Mímọ́ ní Èdè Yorùbá Òde-Òní')[0]
	# Replace reference text with empty string
	for each in removetext:
		passage = passage.replace(each, '')
	# Add space after each verse number
	# First split the passage into 2 using the chapter number 10
	# Add newline before each number and space after
	passage1, passage2 = passage.split('10')[0], passage.split('10')[1]
	
	for eachverse in numbers:
		try:
			if int(eachverse) < 10:
				passage1= passage1.replace(eachverse, '\n'+eachverse+ ' ')
			else:
				passage2= passage2.replace(eachverse, '\n' + eachverse + ' ')
		except:
			pass

	# Join both strings together, adding the chapter 10 back
	biblePassage = passage1.strip() + '\n10 ' + passage2.strip()

	return biblePassage.replace('  ',' ').replace('  ',' ')
