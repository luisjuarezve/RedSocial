class Like:
    def __init__(self, publicacion_id, perfil_id):
        self.__publicacion_id = publicacion_id
        self.__perfil_id = perfil_id

    # Getters

    def get_publicacion_id(self):
        return self.__publicacion_id

    def get_perfil_id(self):
        return self.__perfil_id

    # Setters

    def set_publicacion_id(self, publicacion_id):
        self.__publicacion_id = publicacion_id

    def set_perfil_id(self, perfil_id):
        self.__perfil_id = perfil_id
