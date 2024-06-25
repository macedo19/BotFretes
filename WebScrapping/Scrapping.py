from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
class Scrapping:

    # PATH onde esta intalado seu driver do chrome
    PATH_FOR_DRIVER = "C:/chromedriver/chromedriver-win64/chromedriv"

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)


    #Metodo de autenticacao do site.
    #Informar login e senha salvo nas credencias
    def autenticaSite(self, login, password):

        #Acessa aba de autenticacao do site
        self.driver.get('https://www.fretebras.com.br/entrar')

        #autentica com as credenciais
        self.driver.find_element(By.NAME, "cpf").send_keys(login)
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.TAG_NAME, "button").click()

        sleep(10)

        self.setCookiesSite(self.driver.get_cookies())

    #Salva os cookies da pagina
    #Importante pois sera usado nas threads para nao ocorrer o caso de acessar um filtro e nao estar 'autenticado'
    def setCookiesSite(self, cookies):
        self.cookies = cookies