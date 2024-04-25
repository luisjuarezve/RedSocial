class Perfil:
    def __init__(self, credencial_id: int, nombre: str, apellido: str, fecha_nac: str, genero: str, lugar_residencia: str, situacion_sentimental: str, foto_perfil: str, foto_portada: str):
        self.__credencial_id = credencial_id
        self.__nombre = nombre
        self.__apellido = apellido
        self.__fecha_nac = fecha_nac
        self.__genero = genero
        self.__lugar_residencia = lugar_residencia
        self.__situacion_sentimental = situacion_sentimental
        self.__foto_perfil = foto_perfil
        self.__foto_portada = foto_portada

    # Getters
    def get_credencial_id(self):
        return self.__credencial_id

    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido

    def get_fecha_nac(self):
        return self.__fecha_nac

    def get_genero(self):
        return self.__genero

    def get_lugar_residencia(self):
        return self.__lugar_residencia

    def get_situacion_sentimental(self):
        return self.__situacion_sentimental

    def get_foto_perfil(self):
        return self.__foto_perfil

    def get_foto_portada(self):
        return self.__foto_portada

    # Setters
    def set_credencial_id(self, credencial_id):
        self.__credencial_id = credencial_id

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_apellido(self, apellido):
        self.__apellido = apellido

    def set_fecha_nac(self, fecha_nac):
        self.__fecha_nac = fecha_nac

    def set_genero(self, genero):
        self.__genero = genero

    def set_lugar_residencia(self, lugar_residencia):
        self.__lugar_residencia = lugar_residencia

    def set_situacion_sentimental(self, situacion_sentimental):
        self.__situacion_sentimental = situacion_sentimental

    def set_foto_perfil(self, foto_perfil):
        self.__foto_perfil = foto_perfil

    def set_foto_portada(self, foto_portada):
        self.__foto_portada = foto_portada
