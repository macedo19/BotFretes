from Arquivo import ArquivoTexto as arquivoTxt

class Credenciais:

    def getCredenciais(self):
        txt = arquivoTxt.ArquivoTexto()
        credenciais = txt.ler()
        info = credenciais.split(';')
        self.login , self.password  = info[0], info[1]
        return True
    
    def getLogin(self):
        return self.login 
    
    def getPassword(self):
        return self.password 

    

