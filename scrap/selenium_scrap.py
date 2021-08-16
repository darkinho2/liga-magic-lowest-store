from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

def get_driver(headless=False):
    options = Options()
    options.headless = headless
    options.add_argument('--no-sandbox')
    options.add_argument('--lang=en')
    options.add_argument('--disable-setuid-sandbox')
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    options.to_capabilities()
    chromedriver_path = "chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_path, options=options)
    return driver

def get_list(driver, url):
    driver.get(url)
    lista_card = driver.find_elements_by_class_name("deck-card")
    deck_list = []
    for element in lista_card:
        if element.text:
            deck_list.append(element.text)
    return deck_list

def get_lojas(driver, card):
    driver.get(f"https://www.ligamagic.com.br/?view=cards%2Fcard&card={card}")
    comprar = driver.find_elements_by_class_name("e-col7")
    scroll = 50
    for buy in comprar[:10]:
        buy.click()
        driver.execute_script(f"scroll(0, {scroll});")
        time.sleep(0.5)
        scroll += 40


    print("oi")

def cart_price(driver):
    driver.get("https://www.ligamagic.com.br/?view=mp/carrinho")
    price_dict = {}
    soup = BeautifulSoup(driver.page_source, "html.parser")
    carro = soup.find_all("div", "boxshadow conteudo box-interna box-margin-t")
    cart_loja = []
    cart ={}
    for loja in carro:
        try:
            cart[loja.find("span").text] = {"cards": [], "total": 0}
            print(loja.find("span").text)
            itens = loja.find(class_="itens")
            details = list(filter(None, itens.get_text().split("\n")))
            start = 0
            for item in range(1, (int(len(details)/7)+1)):
                print(start, item*7)
                cart[loja.find("span").text]['cards'].append(dict(zip(['Nome', "edicao", "lingua", "estado", "unidade", "valor unitario", "valor total"],
                                                                    details[start:item*7])))
                start += 7
        except Exception as ex:
            print(ex)
            continue
    for key, value in cart.items():
        total = 0
        for cards in value['cards']:
            total += float(cards['valor total'].replace(",", ".").lstrip("R$ "))
        cart[key]['total'] = total
    with open("cart.txt", "w") as cartf:
        for key, values in cart.items():
            cartf.write(f"{key} ----- total {cart[key]['total']}\n")
            for card in values['cards']:
                cartf.write(f"{card}\n")
    print("oi")

if __name__ == '__main__':
    driver = get_driver()
    # cards = get_list(driver, "https://www.ligamagic.com.br/?view=dks/deck&id=2470990")
    cards = ['Aves do Paraíso']
    for card in cards:
        get_lojas(driver, card)
    prices = cart_price(driver)
    driver.close()

