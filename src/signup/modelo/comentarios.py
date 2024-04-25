class Comentario:
    def __init__(self, contenido, fecha, publicacion_id, perfil_id):
        self.__contenido = contenido
        self.__fecha = fecha
        self.__publicacion_id = publicacion_id
        self.__perfil_id = perfil_id

    # Getters
    def get_contenido(self):
        return self.__contenido

    def get_fecha(self):
        return self.__fecha

    def get_publicacion_id(self):
        return self.__publicacion_id

    def get_perfil_id(self):
        return self.__perfil_id

    # Setters
    def set_contenido(self, contenido):
        self.__contenido = contenido

    def set_fecha(self, fecha):
        self.__fecha = fecha

    def set_publicacion_id(self, publicacion_id):
        self.__publicacion_id = publicacion_id

    def set_perfil_id(self, perfil_id):
        self.__perfil_id = perfil_id
