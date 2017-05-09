import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

Target_URL='http://movie.douban.com/top250'

def download_page(URL):
	return requests.get(URL).content

def parse_html(html):
	movie_name_list=[]
	soup=BeautifulSoup(html,'html.parser')
	movie_list_soup=soup.find('ol',attrs={'class':'grid_view'})
	
	for movie_li in movie_list_soup.find_all('li'):
		detail=movie_li.find('div',attrs={'class':'hd'})
		movie_name=movie_li.find('span',attrs={'class':'title'}).text
		movie_name_list.append(movie_name)
	nextpage=soup.find('span',{'class':'next'}).find('a')
	#print(Target_URL+nextpage['href'])
	if nextpage:
		return(movie_name_list,Target_URL+nextpage['href'])
	return(movie_name_list,None)

def main():
	url=Target_URL
	name_list=[]
	while url:
		myURL=download_page(url)
		name,url=parse_html(myURL)
		name_list+=name
	
	TopMovies=pd.DataFrame(name_list,index=np.arange(1,251),columns=['Title'])
	TopMovies.to_excel('douban.xlsx',sheet_name='Sheet1')
if __name__=='__main__':
	main()