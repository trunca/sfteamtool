import re, os, time, datetime, traceback, urllib, urllib2
import time

user_agent_default = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4';

def Sacarpelicula(ENLACE):
    URL = ENLACE
    
    req = urllib2.Request(URL)
    req.add_header('User-Agent', user_agent_default)
    Abrir = urllib2.urlopen(req)
    data = Abrir.read()
    Abrir.close()
    
    Busca0 = re.findall(r'<input type="hidden" name="op" value="([^"]*)"', data)
    Busca1 = re.findall(r'<input type="hidden" name="usr_login" value="([^"]*)"', data)
    Busca2 = re.findall(r'<input type="hidden" name="id" value="([^"]*)"', data)
    Busca3 = re.findall(r'<input type="hidden" name="fname" value="([^"]*)"', data)
    Busca4 = re.findall(r'<input type="hidden" name="referer" value="([^"]*)">', data)
    Busca5 = re.findall(r'<input type="hidden" name="hash" value="([^"]*)"', data)
    Busca6 = re.findall(r'<input type="submit" name="imhuman".+?value="([^"]*)"', data)
    
    OP0 = Busca0[0]
    OP1 = Busca1[0]
    OP2 = Busca2[0]
    OP3 = Busca3[0]
    OP4 = Busca4[0]
    OP5 = Busca5[0]
    OP6 = Busca6[0]

    time.sleep(12)
    
    POST = "op=" + OP0 + "&usr_login=" + OP1 + "&id=" + OP2 + "&fname=" + OP3 + "&referer=" + OP4 + "&hash=" + OP5 + "&imhumman=" +OP6
    
    req = urllib2.Request(URL, POST)
    req.add_header('User-Agent', user_agent_default)
    Abrir = urllib2.urlopen(req)
    data = Abrir.read()
    Abrir.close()
    
    BUSCAENLACE = re.findall(r'file:\s"(.+?)"', data)
    
    URLFINAL = BUSCAENLACE[0]
    
    return URLFINAL