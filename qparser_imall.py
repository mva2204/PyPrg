from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class Parser(object):
    def __init__(self, driver, http_adress):
        self.driver = driver
        self.http_adress = http_adress

    def parse(self, html):
        self.http_adress = html
        return self.go_to_page()


    def go_to_page(self):
        self.driver.get(self.http_adress)
        res = self.driver.page_source
        print("page src = {}".format(res))
        return res

        div_row = self.driver.find_elements_by_class_name("artikul1")
        div_old = []
        print("div_old {} == {} div_row ".format(div_old, div_row))
        t = 0
        while len(div_old) != len(div_row):# and t < 1:
            div_old = div_row
            try:
                show_goods_res = self.driver.find_element_by_class_name("show_goods")
                show_goods = show_goods_res.click()
            except NoSuchElementException:
                pass

            div_row = self.driver.find_elements_by_class_name("artikul1")
            t += 1
            print("div_old {} == {} div_row {}".format(len(div_old), len(div_row), t))

        # print(self.driver.page_source)
        print(div_row)
        print("len = {}".format(len(div_row)))
        # print("page_source = {}".format(self.driver.page_source))
        res = self.driver.page_source
        return res
        # show_goods_link = show_goods.get_attribute("href")
        # self.driver.get(show_goods_link)




def main():
    driver = webdriver.Firefox()

    html = 'https://mall.industry.siemens.com/mall/ru/ru/Catalog/Products/10046385?tree=CatalogTree'
    parser = Parser(driver, html)
    parser.parse(html)

    # driver.find_elements_by_class_name()
    # btn_elem = driver.find_element_by_class_name("btn")
    # btn_elem.click()

if __name__ == "__main__":
    main()