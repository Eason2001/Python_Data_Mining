import urllib.request 
import bs4 
import re

fstPattern = re.compile(r'\"prodRating\":\"(\d+\.\d+)\".+\"prodID\":\[\"(\d+)\".+\"prodPrice\":\[\"(\d+\.?\d*)\"',re.M|re.I)
secPattern = re.compile(r'.+ProductTitle\">(.+)</span>.+Positive <span.+(/d+) Reviews.+Critical <span.+(/d+) Reviews',re.M|re.I)


htmlDoc = urllib.request.urlopen("http://www.bestbuy.ca/en-CA/product/acer-acer-aspire-es-15-6-laptop-black-amd-a4-7210-1tb-hdd-6gb-ram-windows-10-es1-523-44lu/10509308.aspx?path=d4a7656ac63c96718b1a8b426f859caben02")
jsStr = htmlDoc.read().decode('utf-8')

# print(jsStr)

#going to find the attributes: posReviews, NegaReviews, reviews, overRating, 
# bsObj = BeautifulSoup(htmlDoc,'html.parser')
# nameList = bsObj.findAll("div", {"class":"rating-score font-xs colour-dark-grey inline-block margin-right-one"})
# for name in nameList: 
# 	print(name.get_text())

#"prodRating":"4.3","numProdReviews":"9","prodID":["10509308","10509308"],"prodPrice":["579.99","579.99"]


fstMatch=fstPattern.search(jsStr)
secMatch=secPattern.search(jsStr)

if fstMatch:
    # print ("matchObj.group() : ", matchObj.group())#匹配整个
    print ("fstMatch.group(1) : ", fstMatch.group(1))#匹配的第一个括号，prodRating
    print ("fstMatch.group(2) : ", fstMatch.group(2))#匹配的第一个括号，prodRating
    print ("fstMatch.group(3) : ", fstMatch.group(3))#匹配的第一个括号，prodRating
    print ("secMatch.group(1) : ", secMatch.group(1))#匹配的第一个括号，prodRating
    print ("secMatch.group(2) : ", secMatch.group(2))#匹配的第一个括号，prodRating
    print ("secMatch.group(3) : ", secMatch.group(3))#匹配的第一个括号，prodRating


    # print ("matchObj.group(2) : ", matchObj.group(2))#匹配的第二个括号


else:
    print ("No match!!")


