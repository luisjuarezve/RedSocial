from django.db import models
import mariadb
from .modelo.amigos import Amigo
from .modelo.comentarios import Comentario
from .modelo.credencial import Credencial
from .modelo.likes import Like
from .modelo.perfil import Perfil
from .modelo.publicacion import Publicacion


class DatabaseHandler:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = '123456'
        self.database = 'red_social'
        self.connection = None
        self._cur = None

    def connect(self):
        try:
            self.connection = mariadb.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self._cur = self.connection.cursor()
        except mariadb.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def close(self):
        if self.connection:
            self.connection.close()

    def insertCredencial(self, credencial: Credencial):
        self._cur.execute("INSERT INTO credencial (correo_electronico, contrasena) VALUES (%s,%s)", (
            credencial.get_correo_electronico(),
            credencial.get_contrasena()
        ))
        self.connection.commit()

    def insertPerfil(self, perfil: Perfil):
        self._cur.execute("INSERT INTO perfil (credencial_id, nombre, apellido, fecha_nac, genero, lugar_residencia, situacion_sentimental, foto_perfil, foto_portada) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
            perfil.get_credencial_id(),
            perfil.get_nombre(),
            perfil.get_apellido(),
            perfil.get_fecha_nac(),
            perfil.get_genero(),
            perfil.get_lugar_residencia(),
            perfil.get_situacion_sentimental(),
            perfil.get_foto_perfil(),
            perfil.get_foto_portada()
        ))
        self.connection.commit()

    def insertAmigo(self, amigo: Amigo):
        self._cur.execute("INSERT INTO amigos (perfil_id, perfil_amigo_id) VALUES (%s,%s),(%s,%s)", (
            amigo.get_perfil_id(),
            amigo.get_perfil_amigo_id(),
            amigo.get_perfil_amigo_id(),
            amigo.get_perfil_id()
        ))
        self.connection.commit()

    def insertPublicacion(self, publicacion: Publicacion):
        self._cur.execute("INSERT INTO publicacion (contenido, perfil_id, foto) VALUES (%s,%s,%s)", (
            publicacion.get_contenido(),
            publicacion.get_perfil_id(),
            publicacion.get_foto()
        ))
        self.connection.commit()

    def insertComentario(self, comentario: Comentario):
        self._cur.execute("INSERT INTO comentarios (contenido, publicacion_id, perfil_id) VALUES (%s,%s,%s)", (
            comentario.get_contenido(),
            comentario.get_publicacion_id(),
            comentario.get_perfil_id()
        ))
        self.connection.commit()

    def insertLike(self, like: Like):
        self._cur.execute("INSERT INTO likes (publicacion_id, perfil_id) VALUES (%s,%s)", (
            like.get_publicacion_id(),
            like.get_perfil_id()
        ))
        self.connection.commit()

    def get_credencial_id(self, email, password):
        self._cur.execute("select id from credencial where correo_electronico = %s and contrasena = %s", (
            email, password
        ))
        result = self._cur.fetchone()
        if result is not None:
            return result[0]
        else:
            return None
        self.connection.commit()

    def auth_email(self, email):
        self._cur.execute("select * from credencial where correo_electronico = %s", (
            email,
        ))
        result = self._cur.fetchone()
        if result is not None:
            return result[0]
        else:
            return None
        self.connection.commit()
