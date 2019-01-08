import time
import datetime
import mysql.connector
from bs4 import BeautifulSoup
from selenium import webdriver

if __name__ == '__main__':
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="121314",
	  database="news"
	)

	mycursor = mydb.cursor()

	# 查询数据库中所有的文章title
	sql1 = "SELECT title FROM news"
	mycursor.execute(sql1)
	result = mycursor.fetchall()

	driver = webdriver.Chrome()
	driver.get("https://www.infoq.cn")
	time.sleep(1)

	news_list = driver.find_element_by_class_name("list")
	infos = news_list.find_elements_by_class_name("info")
	length = len(infos)

	for i in range(0, length):
		news_list = driver.find_element_by_class_name("list")
		infos = news_list.find_elements_by_class_name("info")
		info = infos[i]
		title = info.find_element_by_class_name("com-article-title").text
		author = info.find_element_by_css_selector("a.com-author-name.author").text
		news_url = info.find_element_by_class_name("com-article-title").get_attribute("href")

		# 根据title构造一个元组，判断数据是否已经存在数据库中
		temp = (title,)
		if temp in result:
			continue

		# 进入文章链接
		driver.get(news_url)
		time.sleep(1)    

		# 解析HTML，获取文章内容
		soup = BeautifulSoup(driver.page_source, from_encoding='utf-8')
		children = soup.find('div', {'class': 'article-typo article-content'}).findAll('p')
		content = ""
		for child in children:
			content += str(child)

		module = "科技"
		preference = 1
		abst = title
		browse_time = 0
		t = datetime.datetime.now()

		# 插入数据到数据库
		sql2 = "INSERT INTO news (title, content, module, author, time, browse_time, preference, abst) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		val = (title, content, module, author, t, browse_time, preference, abst)
		mycursor.execute(sql2, val)
		mydb.commit()
		print("News added.")

		# 返回首页
		driver.back()
		time.sleep(2)  

	driver.quit()
		
