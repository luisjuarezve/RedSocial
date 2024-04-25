class Publicacion:
    def __init__(self, contenido, fecha_publicacion, perfil_id, foto):
        self.__contenido = contenido
        self.__fecha_publicacion = fecha_publicacion
        self.__perfil_id = perfil_id
        self.__foto = foto

    # Getters
    def get_contenido(self):
        return self.__contenido

    def get_fecha_publicacion(self):
        return self.__fecha_publicacion

    def get_perfil_id(self):
        return self.__perfil_id

    def get_foto(self):
        return self.__foto

    # Setters
    def set_contenido(self, contenido):
        self.__contenido = contenido

    def set_fecha_publicacion(self, fecha_publicacion):
        self.__fecha_publicacion = fecha_publicacion

    def set_perfil_id(self, perfil_id):
        self.__perfil_id = perfil_id

    def set_foto(self, foto):
        self.__foto = foto
