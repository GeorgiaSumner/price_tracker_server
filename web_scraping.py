import requests
from bs4 import BeautifulSoup
import re
import sys
import json
from multiprocessing import Pool


headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

search_term = str(sys.argv[1]).lower()

#search_term = input("text here")

all_stores=[['fabarmory',f"https://fabarmory.com/search?q={search_term}&options%5Bprefix%5D=last","product-card product-card--list","money","product-card__title"],
       ['cardmerchant',f"https://cardmerchant.co.nz/search?page=1&q=%2A{search_term}+flesh+singles%2A", "productCard__lower", "productCard__price", "productCard__title"],
        ['shufflencut' ,f"https://www.shuffleandcutgames.co.nz/search?q=*{search_term}+flesh+singles*",'product Norm',"productPrice", "productTitle"],
         ['sushiknight',f"https://sushiknightgaming.com/search?filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=&sort_by=relevance&q={search_term}&options%5Bprefix%5D=last", "grid__item","price-item price-item--sale price-item--last", "full-unstyled-link"],
        ['tcgculture', f"https://tcgculture.com/search?page=1&q=%2A{search_term}+flesh%2A","productCard__lower","productCard__price","productCard__title"]]

def parse(url):
    response = requests.get(url[1], headers = headers).text
    soup = BeautifulSoup(response, 'lxml')

    store = url[0]
    product = url[2]
    price = url[3]
    keywords = url[4]

    out = []
    result=0

    product_card = soup.find_all(class_ = product)
    
    if product_card:
        for card in product_card:
            keyword_filter = card.find(class_ = keywords)
            if  keyword_filter:
                keyword_check = keyword_filter.text.split(':')[0].strip()
            elif not keyword_filter:   
                htmlStr = '<li></li>'
                html_soup = BeautifulSoup(htmlStr, 'html.parser')
                keyword_check = html_soup.text.split(':')[0].strip()
            
            if search_term in keyword_check.casefold():
                price_filter = card.find(class_ = price)
                price_check = re.sub("[^\d\.]", "",price_filter.text.split(':')[0].strip())
                if price_check == "":
                    price_check = 999999
                    out.append(price_check)
                else:
                    result = float(price_check)
                    out.append(result)
            else: 
                out.append(999999)             
    else: 
        out.append(999999)  
    
    for i in range(len(out)):
        if out[i] == "":
                out[i] = 999999
  
    
    final_list = {'store':store, 'price':min(out)}
    json_list = json.dumps(final_list, ensure_ascii=False)
    json_conversion = json.loads(json_list)
    print(json_conversion)




if __name__ == '__main__':
    p = Pool(2)
    p.map(parse, all_stores)                                   
                                               






"""
rookgaming_card_price = rookgaming_soup.find_all(True, {"class":["box-text box-text-products text-center grid-style-2", "product-main"]})


#rookgaming_pricelist=[]
for card in rookgaming_card_price:
    price = card.find_all(class_ = "woocommerce-Price-amount amount")
    keyword_filter = card.find_all(class_ = "title-wrapper")
    for card_names in keyword_filter:
         keywords = card_names.text.split(':')[0].strip()
    if search_term in keywords.casefold():  
        for card_value in price:
            card_value.text.split(':')[0].strip()
            rookgaming_pricelist.append((re.sub("[^\d\.]", "",card_value.text.split(':')[0].strip() )))
  """          



#print(f"Fab Armory:{min(fabarmory_pricelist)}", f"Card Merchant:${min(cardmerchant_pricelist)}", f"Shuffle n Cut:{min(shufflencut_pricelist)}",f"Sushi Knight:{min(sushiknight_pricelist)}",f"Rook Gaming:{min(rookgaming_pricelist)}",f"TCG Culture:${min(tcgculture_pricelist)}" )


