from urllib.request import urlopen
html = urlopen("http://www.bestbuy.ca/en-CA/product/acer-acer-aspire-es-15-6-laptop-black-amd-a4-7210-1tb-hdd-6gb-ram-windows-10-es1-523-44lu/10509308.aspx?path=d4a7656ac63c96718b1a8b426f859caben02") 
print(html.read())
