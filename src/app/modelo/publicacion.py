class Publicacion:
    def __init__(self, contenido, perfil_id, foto):
        self.__contenido = contenido
        self.__perfil_id = perfil_id
        self.__foto = foto

    # Getters
    def get_contenido(self):
        return self.__contenido

    def get_perfil_id(self):
        return self.__perfil_id

    def get_foto(self):
        return self.__foto

    # Setters
    def set_contenido(self, contenido):
        self.__contenido = contenido

    def set_perfil_id(self, perfil_id):
        self.__perfil_id = perfil_id

    def set_foto(self, foto):
        self.__foto = foto
