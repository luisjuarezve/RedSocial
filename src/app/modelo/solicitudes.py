class Solicitud:
    def __init__(self, perfil_id_emisor, perfil_id_receptor):
        self.__perfil_id_emisor = perfil_id_emisor
        self.__perfil_id_receptor = perfil_id_receptor

    def get_perfil_id_emisor(self):
        return self.__perfil_id_emisor

    def get_perfil_id_receptor(self):
        return self.__perfil_id_receptor

    def set_perfil_id_emisor(self, nuevo_perfil_id_emisor):
        self.__perfil_id_emisor = nuevo_perfil_id_emisor

    def set_perfil_id_receptor(self, nuevo_perfil_id_receptor):
        self.__perfil_id_receptor = nuevo_perfil_id_receptor
