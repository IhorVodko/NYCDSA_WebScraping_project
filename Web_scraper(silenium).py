from selenium import webdriver
import csv

driver = webdriver.Chrome(r'C:\Users\ihorf\chromedriver.exe')
driver.get("https://www.cnn.com/search?size=10&q=opioid%7Cpurdue%7Cbankruptcy")

'''links pattern
https://www.cnn.com/search?size=10&q=opioid%7Cpurdue%7Cbankruptcy&page=1
https://www.cnn.com/search?size=10&q=opioid%7Cpurdue%7Cbankruptcy&from=10&page=20
https://www.cnn.com/search?size=10&q=opioid%7Cpurdue%7Cbankruptcy&from=20&page=30
https://www.cnn.com/search?size=10&q=opioid%7Cpurdue%7Cbankruptcy&from=30&page=40

https://edition.cnn.com/search?size=10&q=opioid%7Cpurdue%7Cbankruptcy&from=4100&page=4110
'''

csv_file = open('news.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
writer.writerow(['Date', 'Header', 'Article'])

#url pattern loop
urls = []
for i in range(0,410):
    x = i*10 
    y = (i+1)*10    
    urls.append(f'https://www.cnn.com/search?size=10&q=opioid%7Cpurdue%7Cbankruptcy&from={x}&page={y}')

#search loop
i = 1
for url in urls:
    try:
        print('PAGE ' + str(i) + '+'*30 )
        driver.get(url)
        articles = driver.find_elements_by_xpath('//div[@class="cnn-search__result cnn-search__result--article"]')
    
        for article in articles:
            news_dict = {}
            try:
                date = article.find_element_by_xpath('.//div[@class="cnn-search__result-publish-date"]//span[2]').text
                header = article.find_element_by_xpath('.//h3[@class="cnn-search__result-headline"]/a').text
                text = article.find_element_by_xpath('.//div[@class="cnn-search__result-body"]').text
                print('='*30)
            except:
                continue
            news_dict['date'] = date
            news_dict['header'] = header
            news_dict['text'] = text

            writer.writerow(news_dict.values())
        i += 1
    except Exception as e:
        print(e)
        csv_file.close()
        driver.close()
        break
    
csv_file.close()    
driver.close()