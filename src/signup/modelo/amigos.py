class Amigo:
    def __init__(self, perfil_id, perfil_amigo_id, fecha):
        self.__perfil_id = perfil_id
        self.__perfil_amigo_id = perfil_amigo_id
        self.__fecha = fecha

    # Getters
    def get_perfil_id(self):
        return self.__perfil_id

    def get_perfil_amigo_id(self):
        return self.__perfil_amigo_id

    def get_fecha(self):
        return self.__fecha

    # Setters
    def set_perfil_id(self, perfil_id):
        self.__perfil_id = perfil_id

    def set_perfil_amigo_id(self, perfil_amigo_id):
        self.__perfil_amigo_id = perfil_amigo_id

    def set_fecha(self, fecha):
        self.__fecha = fecha
