
from Credencial import Credenciais  as cr 
from WebScrapping import Scrapping as scrap
from Arquivo import ArquivoExcell as ae
# 
#  Executa um bot ao qual realiza uma coleta dos dados da página do Frete Bras 
#  Aplicando conceitos de web scrapping, utiliza-se algumas bibliotecas para a extração das informações
#  Instale as bibliotecas utilizadas como selenium e openpyxl
# 

credencial = cr.Credenciais()
credencial.getCredenciais()

#Realiza a extração dos dados da página
scrapping = scrap.Scrapping()
scrapping.autenticaSite(credencial.getLogin(), credencial.getPassword())

excell = ae.Excell()
wb = excell.getWb()

#Inicia a extracao
scrapping.setWbArquivo(wb)
scrapping.iniciaThreads()

excell.salvaArquivoMaquina(scrapping.getWb())

scrapping.finalizaScrapping()