import requests
import argparse

def geTgt(origen,user,password):
    data = {'username': user, 'password': password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    urlTicket = origen+'/SASLogon/v1/tickets'
    response = requests.post(urlTicket, headers=headers, params=data, verify = False)    
    if(response.status_code == 201 or response.status_code == 200 ):
        tgt = response.headers['Location'].split('/')[len(response.headers['Location'].split('/'))-1]
        return tgt , response.status_code 
    else:
        return 'error' , response.status_code 

def getTkt(origen, tgt , statuscode):
    if(statuscode== 201 or statuscode == 200 ):
        data = {'service': origen+'/SASStoredProcess/do'}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        urlTicket = origen+'/SASLogon/v1/tickets/'+tgt
        response = requests.post(urlTicket, headers=headers, params=data, verify = False)
        if (response.status_code == 200 or response.status_code == 201):
            ticket = response.text
            return ticket , response.status_code
        else:
           return 'error' , statuscode
    else:
        return 'error' , statuscode

def executeProgram(origen, ticket, statuscode , program):
    if(statuscode== 201 or statuscode == 200 ):
        data = {'_program': program}
        headers = {"Content-Type": "application/json"}
        urlTicket = origen+'/SASStoredProcess/do?ticket='+ticket
        response = requests.post(urlTicket, headers=headers, params=data, verify = False)
        if (response.status_code == 200 or response.status_code == 201):
            ticket = response.text
            return ticket , response.status_code
        else:
            return 'error' , response.status_code
    else:
        return 'error' , statuscode

def checker(args):
    if(args.origen == None):
        return 'debe ingresar una URL valida' , False
    elif(args.user == None):
        return 'debe ingresar un usuario' , False
    elif(args.user == None):
        return 'debe ingresar la password' , False
    elif(args.program == None):
        return 'debe ingresar  un programa' , False
    else:
        return '',True        




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual para la API ejecuta programas SAS')
    parser.add_argument('--origen', type=str, default=None)
    parser.add_argument('--user', type=str, default=None)
    parser.add_argument('--password', type=str, default=None)
    parser.add_argument('--program', type=str, default=None)
    args = parser.parse_args()
    mensaje , estado = checker(args)
    if(estado):
        tgt , statuscode = geTgt(args.origen,args.user, args.password)
        ticket , statuscode  = getTkt(args.origen,tgt , statuscode)
        respuesta , statuscode  = executeProgram(args.origen,ticket , statuscode, args.program)
        print(tgt)
        print(ticket)
        print(statuscode)
        print(respuesta)
    else:
        print(mensaje)


