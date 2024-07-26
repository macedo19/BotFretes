from selenium import webdriver
import concurrent.futures
from selenium.webdriver.common.by import By
from time import sleep

class  Filtro:

    FILTRO = {
        "PR+PR": "https://www.fretebras.com.br/fretes/carga-de-pr/carga-para-pr/veiculo-truck/carroceria-grade+baixa/sem-rastreamento/frete-cheio",
        "PR+SC": "https://www.fretebras.com.br/fretes/carga-de-pr/carga-para-sc/veiculo-truck/carroceria-grade+baixa/sem-rastreamento/frete-cheio",
        "SC+PR": "https://www.fretebras.com.br/fretes/carga-de-sc/carga-para-pr/veiculo-truck/carroceria-grade+baixa/sem-rastreamento/frete-cheio",
        "SC+SC": "https://www.fretebras.com.br/fretes/carga-de-sc/carga-para-sc/veiculo-truck/carroceria-grade+baixa/sem-rastreamento/frete-cheio",
        "PR+SP": "https://www.fretebras.com.br/fretes/carga-de-pr/carga-para-sp/veiculo-truck/carroceria-grade+baixa/sem-rastreamento/frete-cheio",
        "SC+SP": "https://www.fretebras.com.br/fretes/carga-de-sc/carga-para-sp/veiculo-truck/carroceria-grade+baixa/sem-rastreamento/frete-cheio",
        "SP+PR": "https://www.fretebras.com.br/fretes/carga-de-sp/carga-para-pr/veiculo-truck/carroceria-grade+baixa/sem-rastreamento/frete-cheio",
        "SP+SC": "https://www.fretebras.com.br/fretes/carga-de-sp/carga-para-sc/veiculo-truck/carroceria-grade+baixa/sem-rastreamento/frete-cheio",
        "GO+PR": "https://www.fretebras.com.br/fretes/carga-de-go/carga-para-pr/veiculo-truck/carroceria-grade+baixa/sem-rastreamento/frete-cheio",
        "PR+GO": "https://www.fretebras.com.br/fretes/carga-de-pr/carga-para-go/veiculo-truck/carroceria-grade+baixa/sem-rastreamento/frete-cheio"
    }  

    



class Scrapping:

    # PATH onde esta intalado seu driver do chrome
    PATH_FOR_DRIVER = "C:/chromedriver/chromedriver-win64/chromedriv.exe"

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


    def setWbArquivo(self, wb):
        self.wb =  wb

    def getWb(self):
        return self.wb
    

    #Meotod que realiza a extração dos dados do site
    def executaPorThread(self, driver,  ws, url, pagina):

        caminho = url + "/" + str(pagina)
        driver.get(caminho)

        sleep(2)

        div_dos_itens = driver.find_element(By.CSS_SELECTOR, ".sc-9769d6f0-0.ktWhJT")
        itens = div_dos_itens.find_elements(By.TAG_NAME, "a")

        guia_original = driver.current_window_handle

        for item in itens:
            link = item.get_attribute('href')
            script = "window.open('" + link + "', '_blank');"
            driver.execute_script(script)
            sleep(2)
            abas = driver.window_handles
            driver.switch_to.window(abas[-1])
            sleep(6)

            try:
                div_data = driver.find_element(By.CSS_SELECTOR, ".info-carga.frt-details .data-carga")
                data = div_data.find_element(By.TAG_NAME, "span").text
                div_produto = driver.find_element(By.CSS_SELECTOR, ".carga-preco.barra-vert.triangulo")

                #Info do produto
                produto = driver.find_element(By.CSS_SELECTOR, ".frete-dados.frete-carga").text
                preco = driver.find_element(By.CSS_SELECTOR, ".frete-dados.frete-preco").text

                #Info da origem 
                div_origem_destino = driver.find_element(By.CSS_SELECTOR, ".orig-dest")
                div_origem = div_origem_destino.find_element(By.CSS_SELECTOR, ".origem")
                a_origem = div_origem.find_elements(By.TAG_NAME, "a")
                cidade_origem, estado_origem = [origem.text for origem in a_origem]
                
                #Info do destino 
                div_destino = div_origem_destino.find_element(By.CSS_SELECTOR, ".destino")
                a_destino = div_destino.find_elements(By.TAG_NAME, "a")
                cidade_destino, estado_destino = [destino.text for destino in a_destino]

                #Info do veiculo 
                div_veiculo = driver.find_element(By.CSS_SELECTOR, ".detalhe-frete.frt-details .detalhe.barra-vert .detalhe_item .frete-dados.frete-veiculos")
                a_veiculo = div_veiculo.find_elements(By.TAG_NAME, "a")
                veiculo = " | ".join([veiculo_nome.text for veiculo_nome in a_veiculo])

                #Info do carroceria 
                div_carroceria = driver.find_element(By.CSS_SELECTOR, ".detalhe-frete.frt-details .detalhe.barra-vert .detalhe_item .frete-dados.frete-carrocerias")
                a_carroceria = div_carroceria.find_elements(By.TAG_NAME, "a")
                carroceria = " | ".join([carroceria_nome.text for carroceria_nome in a_carroceria])

                #Info da carga 
                tipo_de_carga = driver.find_element(By.CSS_SELECTOR, ".detalhe-frete.frt-details .detalhe.barra-vert .detalhe_item .frete-dados.frete-complemento").text
                rastreamento = driver.find_element(By.CSS_SELECTOR, ".detalhe-frete.frt-details .detalhe.barra-vert .detalhe_item .frete-dados.frete-rastreamento").text
                observacao = driver.find_element(By.CSS_SELECTOR, ".detalhe-frete.frt-details .detalhe.barra-vert .detalhe_item_obs .frete-dados.frete-obs").text
                empresa = driver.find_element(By.CSS_SELECTOR, ".titulo-geral-topo .total .cor-vermelho").text
                


                #Salva no arquivo
                ws.append([data, produto, empresa ,preco, cidade_origem, estado_origem, cidade_destino, estado_destino, veiculo,
                        carroceria, tipo_de_carga, rastreamento, observacao, link])
                

            except Exception as e:
                print(f"Erro ao extrair detalhes do frete: {e}")
                sleep(1)

            driver.close()
            driver.switch_to.window(guia_original)
            sleep(2)


    def extrairFretes(self, driver, ws, url):
      
        #Total de páginas por filtro
        total_paginas = driver.find_element(By.CSS_SELECTOR, ".sc-f24de481-0 .sc-f24de481-3 .sc-8b546cbe-0 fuel-typography[color='neutral-default']").find_element(By.TAG_NAME, 'p').text
        total_itens_pagina = int(total_paginas.split()[1])

        for  pagina in range(1, total_itens_pagina + 1):
            self.executaPorThread(driver ,ws, url, pagina) 

    def processaFrete(self, name, url,  cookies):
        ws = self.wb.create_sheet(title=name)
        # ws.append(["DATA", "PRODUTO", "EMPRESA" ,"PREÇO", "CIDADE ORIGEM", "ESTADO ORIGEM", "CIDADE DESTINO", "ESTADO DESTINO", "VEICULO", "CARROCERIA", "TIPO DE CARGA", "RASTREAMENTO", "OBSERVACAO", "LINK", "DISTANCIA", "GASTO COMBUSTIVEL"])
        ws.append(["DATA", "PRODUTO", "EMPRESA" ,"PREÇO", "CIDADE ORIGEM", "ESTADO ORIGEM", "CIDADE DESTINO", "ESTADO DESTINO", "VEICULO", "CARROCERIA", "TIPO DE CARGA", "RASTREAMENTO", "OBSERVACAO", "LINK"])

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()

        try:
            self.extrairFretes(driver, ws, url)
        finally:
            driver.quit()


    #Executa a extração em Threads, para cada filtro sera uma thread
    def iniciaThreads(self):

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(Filtro.FILTRO.items())) as executor:
            futures = [executor.submit(self.processaFrete, name, url, self.cookies) for name, url in Filtro.FILTRO.items()]
            concurrent.futures.wait(futures)

    def finalizaScrapping(self):
        self.driver.quit()