import logging
import time
import requests

# Logger configuration
logger = logging.getLogger(__name__)


def obtain_codprov(mi_provincia):
    """
    Extract the code of the provincia specified by the user.
    :param mi_provincia: provincia specified by the user
    :return: codprov
    """

    endpoint = "https://www.el-tiempo.net/api/json/v2/municipios"
    codprov = None
    
    try:
        response = requests.get(url=endpoint, timeout=2)
        data = response.json()
        for i in range(len(data)):
            if data[i]['NOMBRE_PROVINCIA'] == mi_provincia:
                codprov = data[i]['CODPROV']
                return codprov
        if codprov is None:
            logger.error("No se ha encontrado la provincia introducida")
            
    # except KeyError
    except requests.ReadTimeout as ex:
        logger.error(str(time.strftime("%H:%M:%S")) + "- requests.ReadTimeout - " + str(ex))
    except requests.ConnectionError as ex:
        logger.error(str(time.strftime("%H:%M:%S")) + "- requests.ConnectionError - " + str(ex))


def obtain_id(codprov, mi_municipio):
    """
    Extract the id of the municipio specified by the user.
    :param codprov: code of the provincia specified by the user
    :param mi_municipio: municipio specified by the user
    :return: id
    """

    endpoint = "https://www.el-tiempo.net/api/json/v2/provincias/" + codprov + "/municipios"
    id = None
    
    try:
        response = requests.get(url=endpoint, timeout=2)
        data = response.json()

        for i in range(len(data["municipios"])):
            if data["municipios"][i]['NOMBRE'] == mi_municipio:
                codigoine = data["municipios"][i]['CODIGOINE']
                id = codigoine[0:5]
                break
            
        if id is None:
            logger.error("No se ha encontrado el id del municipio introducido.")
        
        return id
            
    # except KeyError
    
    except requests.ReadTimeout as ex:
        logger.error(str(time.strftime("%H:%M:%S")) + "- requests.ReadTimeout - " + str(ex))
    except requests.ConnectionError as ex:
        logger.error(str(time.strftime("%H:%M:%S")) + "- requests.ConnectionError - " + str(ex))


def obtain_min_max_temperature(codprov, id):
    """
    Extract information about max temperature and min temperature of the municipio specified by the user.
    :param codprov: code of the provincia specified by the user
    :param id: id of the municipio specified by the user
    :return: max_temperature, min_temperature
    """

    endpoint = "https://www.el-tiempo.net/api/json/v2/provincias/" + codprov + "/municipios/" + id

    try:
        response = requests.get(url=endpoint, timeout=2)
        data = response.json()
        max_temperature = data["temperaturas"]["max"]
        min_temperature = data["temperaturas"]["min"]

        return max_temperature, min_temperature
    except requests.ReadTimeout as ex:
        logger.error(str(time.strftime("%H:%M:%S")) + "- requests.ReadTimeout - " + str(ex))
    except requests.ConnectionError as ex:
        logger.error(str(time.strftime("%H:%M:%S")) + "- requests.ConnectionError - " + str(ex))


if __name__ == '__main__':
    # User data input
    print(f"\n\033[94mPor favor, introduzca el nombre de la provincia que desea consultar:\033[0m")
    mi_provincia = input()
    print(f"\033[94mIntroduzca ahora el nombre del municipio (perteneciente a {mi_provincia}):\033[0m")
    mi_municipio = input()

    # FIRST: obtain [CODPROV] of the municipio
    codprov = obtain_codprov(mi_provincia)
    if codprov == None:
        logger.error("Fallo al obtener el código de provincia.")
    else:
        # SECOND: obtain [ID] of the municipio
        id = obtain_id(codprov, mi_municipio)
        if id == None:
            logger.error("Fallo al obtener el id.")
        else:
            # THIRD: obtain min and max temperature of the municipio
            max_temp, min_temp = obtain_min_max_temperature(codprov, id)

            # Output information
            print(f'\n\033[1mINFORMACIÓN RELATIVA A {mi_municipio} ({mi_provincia})')
            print(f'-> TEMPERATURA MAX DE HOY: {max_temp}º')
            print(f'-> TEMPERATURA MIN DE HOY: {min_temp}º')
