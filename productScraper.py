import urllib.request     # python urllib library for HTTP request
import bs4                # beautiful4 plus-in for extracting page and product url 
import re                 # python regular expression moudle
import pymysql            # an open source mysql interface plus-in
import time               # python time operation module
import sys                # python system module

# a function to check if a laptop has already existed in database
def ifExisted(PRODUCTURL):
    cur.execute("SELECT * FROM LAPTOP_PRODUCT_1 WHERE PRODUCTURL = \"%s\"", (PRODUCTURL.strip()))
    if cur.rowcount == 0:
        return 0
    else:
        return 1

# a function to store the laptop data into database
def storeData(PRODUCTID, NAME, PRICE, RATING, TOTAL_REVIEW, POSI_RATE, POSI_REVIEW, CRIT_REVIEW, PRODUCTURL):
    cur.execute("INSERT INTO LAPTOP_PRODUCT_1 (PRODUCTID, NAME, PRICE, RATING, TOTAL_REVIEW, POSI_RATE, POSI_REVIEW, CRIT_REVIEW, PRODUCTURL) VALUES (%s,\"%s\",%s,%s,%s,%s,%s,%s,\"%s\")", (PRODUCTID, NAME, PRICE, RATING, TOTAL_REVIEW, POSI_RATE, POSI_REVIEW, CRIT_REVIEW, PRODUCTURL))
    cur.connection.commit()
    print("Successfully adding a product: ", PRODUCTID)
    print ("************************************************************************************************************************")

# a function to extract the laptop data. it will call storeData() to store laptop data
# after cleaning and processing the data.
def extrData(productUrl):
    # check whether the laptop has existed in database
    checkExist=ifExisted(productUrl)
    if checkExist:
        print("Skipping a repeated product: ", productUrl)	
        return
    # generating the pattern object that can search the HTML code
    pidPattern = re.compile(r'\"prodID\":\[\"(\d+)\"',re.M|re.I)
    pnamePattern = re.compile(r'\"prodName\":\[\"(.+\\\".+)\",\".+\\\".+\"\]',re.M|re.I)
    pricPattern = re.compile(r'\"prodPrice\":\[\"(\d+\.?\d*)\"',re.M|re.I)
    ratPattern = re.compile(r'\"prodRating\":\"(\d+\.\d+)\"',re.M|re.I)
    posiPattern = re.compile(r'.+<p class=\"font-xxs colour-dark-grey margin-none\">(\d+) Reviews</p>',re.M|re.I)
    critPattern = re.compile(r'.+<p class=\"font-xxs colour-dark-grey\">(\d+) Reviews</p>',re.M|re.I)
    # loading HTML code from a specific laptop url
    htmlDoc = urllib.request.urlopen(productUrl)
    jsStr = htmlDoc.read().decode('utf-8')
    # extracting the laptop data by using pattern object search() function
    pidMatch=pidPattern.search(jsStr)
    pnameMatch=pnamePattern.search(jsStr)
    pricMatch=pricPattern.search(jsStr)
    ratMatch=ratPattern.search(jsStr)
    posiMatch=posiPattern.search(jsStr)
    crtiMatch=critPattern.search(jsStr)
    # cleaning laptop data: dropping the laptop that doesn't have the complete data
    if pidMatch and pnameMatch and productUrl!="":
        PRODUCTID=int(pidMatch.group(1))
        NAME=pnameMatch.group(1)
        PRODUCTURL=productUrl
    else:
        print ("Skipping one bad product: ", productUrl)
        return
    # processing and initiating the laptop data
    if pricMatch:
        PRICE=float(pricMatch.group(1))
    else:
        PRICE=0
    if ratMatch:
        RATING=float(ratMatch.group(1))
    else:
        RATING=0
    if posiMatch:
        POSI_REVIEW=int(posiMatch.group(1))
    else:
        POSI_REVIEW=0
    if crtiMatch:
        CRIT_REVIEW=int(crtiMatch.group(1))
    else:
        CRIT_REVIEW=0
    # calculating the TOTAL_REVIEW and POSI_RATE
    TOTAL_REVIEW=POSI_REVIEW+CRIT_REVIEW
    if TOTAL_REVIEW!=0:
    	POSI_RATE=POSI_REVIEW/TOTAL_REVIEW
    else:
    	POSI_RATE=0
    print ("************************************************************************************************************************")
    print ("PRODUCTID : ", PRODUCTID)
    print ("NAME : ", NAME)
    print ("PRICE : ", PRICE)
    print ("RATING : ", RATING)
    print ("TOTAL_REVIEW : ", TOTAL_REVIEW)
    print ("POSI_RATE : ", POSI_RATE)
    print ("POSI_REVIEW : ", POSI_REVIEW)
    print ("CRIT_REVIEW : ", CRIT_REVIEW)
    print ("URL : ", PRODUCTURL)
    # call storeData() function to store a laptop data
    storeData(PRODUCTID, NAME, PRICE, RATING, TOTAL_REVIEW, POSI_RATE, POSI_REVIEW, CRIT_REVIEW, PRODUCTURL)



# Connect to the database
conn = pymysql.connect(host='localhost',
                        user='root',
                        password='5278520',
                        db='webData',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

# setting the domain URL from where the programm will extract data
domainURL="http://www.bestbuy.ca"
categoryURL="/en-ca/category/laptops/36711.aspx?"    
connectSTR="type=product&page="

##extracting the page link from categoryURL
startPage=1;    # starting page number
endPage=1;      # default ending page number, it will be replaced with MAXIMUM page number
html = urllib.request.urlopen(domainURL+categoryURL)
bsObj = bs4.BeautifulSoup(html,"html.parser")
for link in bsObj.find("div", {"class":"pagination-control-wrapper text-center"}).find_all("a",href=re.compile(".+(page).+")):
    # updating endPage with the MAXIMUM page number
    if link.get('data-page') and int(link.get('data-page')) > endPage:
        endPage=int(link.get('data-page'))

##extracting the product link from page link
try:
    with conn.cursor() as cur:
        for x in range(startPage, endPage+1):
            urlStr=domainURL+categoryURL+connectSTR+str(x)
            html = urllib.request.urlopen(urlStr)
            bsObj = bs4.BeautifulSoup(html,"html.parser")
            print ("====================================================== the "+str(x)+ " pages =====================================================")
            ## extracting the laptop product link from a "div" tag
            for link in bsObj.find("div", {"id":"ctl00_CP_ctl00_ctl01_ProductSearchResultListing_SearchProductListing"}).find_all("a",href=re.compile("^(/en-ca/product/)")):
                ## generating a specific laptop product link
                if link.get('href'):
                    productUrl=domainURL+link.get('href')
                    ## after obtaining the product url, call the function to extract the product data from this url
                    ## and if the product data is suitable for storing, it will be sotred into database
                    extrData(productUrl.strip())
                    # time.sleep(0.1)
        cur.execute("SELECT PRODUCTID, NAME, RATING, TOTAL_REVIEW, POSI_RATE  FROM LAPTOP_PRODUCT ORDER BY TOTAL_REVIEW DESC, POSI_RATE DESC, RATING DESC  LIMIT 0,10")
        data=cur.fetchall()
        # data is dictionary type
        print ("********************************************************************************************************************************")
        print ("**********************************************TOP 10 HOTTEST LAPTOPS RECOMMENDATION:********************************************")
        for recomItem in data:
            # print("PRODUCTID=%d   NAME=%s   TOTAL_REVIEW=%d   POSI_RATE=%.2f    RATING=%.1f "%(recomItem['PRODUCTID'],recomItem['NAME'].split('(')[0], recomItem['TOTAL_REVIEW'], recomItem['POSI_RATE']*100, recomItem['RATING']));  
            print("  PRODUCTID={0:d}   NAME={1:<48}   TOTAL_REVIEW={2:d}   POSI_RATE={3:0.2f}    RATING={4:0.1f} ".format(recomItem['PRODUCTID'],recomItem['NAME'].split('(')[0], recomItem['TOTAL_REVIEW'], recomItem['POSI_RATE']*100, recomItem['RATING']));  
        print ("********************************************************************************************************************************")
        print ("********************************************************************************************************************************")


finally:
    cur.close()
    conn.close()
    sys.exit()




# for links in bsObj.find("div", {"id":"ctl00_CP_ctl00_ctl01_ProductSearchResultListing_SearchProductListing"}).findAll("a",href=re.compile("^(/en-ca/product/)(\.aspx\?)*$")):
# print (link.attrs['href'])


