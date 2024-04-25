class Credencial:
    def __init__(self, correo_electronico: str, contrasena: str):
        self.__correo_electronico = correo_electronico
        self.__contrasena = contrasena

    def __str__(self):
        return f"Correo electronico: {self.__correo_electronico}, Contraseña: {self.__contrasena}"

    def get_correo_electronico(self):
        return self.__correo_electronico

    def set_correo_electronico(self, nuevo_correo_electronico):
        self.__correo_electronico = nuevo_correo_electronico

    def get_contrasena(self):
        return self.__contrasena

    def set_contrasena(self, nueva_contrasena):
        self.__contrasena = nueva_contrasena
