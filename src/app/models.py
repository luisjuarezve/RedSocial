from django.db import models

from django.db import models
import mariadb
from .modelo.amigos import Amigo
from .modelo.comentarios import Comentario
from .modelo.credencial import Credencial
from .modelo.likes import Like
from .modelo.perfil import Perfil
from .modelo.publicacion import Publicacion
from .modelo.solicitudes import Solicitud

# Clase conector con mariadb


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
# [C] Funciones de insertar datos en bd

    def insertAmigo(self, amigo: Amigo):
        self._cur.execute("INSERT INTO amigos (perfil_id, perfil_amigo_id) VALUES (%s,%s),(%s,%s)", (
            amigo.get_perfil_id(),
            amigo.get_perfil_amigo_id(),
            amigo.get_perfil_amigo_id(),
            amigo.get_perfil_id()
        ))
        self._cur.execute("DELETE FROM solicitudes WHERE perfil_id_emisor = %s and perfil_amigo_id_receptor = %s",
                          (amigo.get_perfil_amigo_id(), amigo.get_perfil_id(),))
        self.connection.commit()

    def insertSolicitud(self, solicitud: Solicitud):
        self._cur.execute("INSERT INTO solicitudes (perfil_id_emisor, perfil_amigo_id_receptor) VALUES (%s,%s)", (
            solicitud.get_perfil_id_emisor(),
            solicitud.get_perfil_id_receptor(),
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
        self._cur.execute("UPDATE publicacion SET cant_comentarios = cant_comentarios+1 WHERE id = %s",
                          (comentario.get_publicacion_id(),))
        self.connection.commit()

    def insertLike(self, like: Like):
        self._cur.execute("INSERT INTO likes (publicacion_id, perfil_id) VALUES (%s,%s)", (
            like.get_publicacion_id(),
            like.get_perfil_id(),
        ))
        self._cur.execute("UPDATE publicacion SET cant_likes = cant_likes+1 WHERE id = %s",
                          (like.get_publicacion_id(),))
        self.connection.commit()
# [R] Funciones de leer Registros de BD

    def get_credencial_id(self, credencial: Credencial):
        self._cur.execute("select id from credencial where correo_electronico = %s and contrasena = %s", (
            credencial.get_correo_electronico(),
            credencial.get_contrasena()
        ))
        row = self._cur.fetchone()
        self.connection.commit()
        return row

    def get_perfil_by_credencial(self, credencial_id: int):
        try:
            self._cur.execute("""select p.id, p.nombre, p.apellido, fecha_nac, genero, situacion_sentimental, lugar_residencia, fecha_registro, p.foto_perfil, p.foto_portada
                from perfil as p where p.credencial_id = %s""",
                              (credencial_id,))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_perfil(self, perfil_id: int):
        try:
            self._cur.execute("""select id, nombre, apellido, fecha_nac, genero, situacion_sentimental, lugar_residencia, fecha_registro, foto_perfil, foto_portada
                from perfil where id = %s""",
                              (perfil_id,))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_perfil_by_name(self, name: str):
        try:
            self._cur.execute("""select p.id, p.nombre, p.apellido, fecha_nac, genero, situacion_sentimental, lugar_residencia, fecha_registro, p.foto_perfil, p.foto_portada
            from credencial as c
            inner join perfil as p 
            on c.id = p.credencial_id where p.nombre like %s or p.apellido like %s""",
                              ('%' + name + '%', '%' + name + '%'))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_amigo(self, perfil_id, perfil_amigo):
        try:
            self._cur.execute(""" select p.id, p.nombre, p.apellido, fecha_nac, genero, situacion_sentimental, lugar_residencia, fecha_registro, p.foto_perfil, p.foto_portada
            from amigos as a
            inner join perfil as p on a.perfil_amigo_id = p.id 
            where a.perfil_id = %s and perfil_amigo_id = %s
            """, (
                perfil_id, perfil_amigo,
            ))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_all_amigos(self, perfil_id):
        try:
            self._cur.execute(""" select p.id, p.nombre, p.apellido, fecha_nac, genero, situacion_sentimental, lugar_residencia, fecha_registro, p.foto_perfil, p.foto_portada
            from amigos as a
            inner join perfil as p on a.perfil_amigo_id = p.id 
            where a.perfil_id = %s order by p.nombre asc
            """, (
                perfil_id,
            ))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_all_amigos_order_by_fecha(self, perfil_id):
        try:
            self._cur.execute("""select p.id, p.nombre, p.apellido, fecha_nac, genero, situacion_sentimental, lugar_residencia, fecha_registro, p.foto_perfil, p.foto_portada
            from amigos as a
            inner join perfil as p on a.perfil_amigo_id = p.id 
            where perfil_id = %s order by a.fecha asc""",
                              (perfil_id,))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_all_amigos_gender(self, perfil_id, gender):
        try:
            self._cur.execute("""select p.id, p.nombre, p.apellido, fecha_nac, genero, situacion_sentimental, lugar_residencia, fecha_registro, p.foto_perfil, p.foto_portada 
            from amigos as a
            inner join perfil as p on a.perfil_amigo_id = p.id
            where p.id = %s and p.genero = %s """, (
                perfil_id, gender,
            ))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_solicitud(self, perfil_emisor_id, perfil_receptor_id):
        try:
            self._cur.execute("""select p.id, p.nombre, p.apellido, p.foto_perfil, s.fecha from solicitudes as s
                inner join perfil as p on s.perfil_id_emisor = p.id where s.perfil_id_emisor = %s and s.perfil_amigo_id_receptor = %s""",
                              (perfil_emisor_id, perfil_receptor_id,))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_all_solicitudes(self, perfil_id):
        try:
            self._cur.execute("""select p.id, p.nombre, p.apellido, p.foto_perfil, s.fecha from solicitudes as s
                inner join perfil as p on s.perfil_id_emisor = p.id where perfil_amigo_id_receptor = %s""",
                              (perfil_id,))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_like(self, like: Like):
        try:
            self._cur.execute(""" select l.publicacion_id, p.id, p.nombre, p.apellido, p.foto_perfil 
            from likes as l
            inner join perfil as p on l.perfil_id = p.id 
            where p.id = %s and l.publicacion_id = %s
            """, (
                like.get_perfil_id(),
                like.get_publicacion_id(),
            ))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_all_like(self, like: Like):
        try:
            self._cur.execute("""select p.id, p.nombre, p.apellido, p.foto_perfil 
            from likes as l
            inner join perfil as p on l.perfil_id = p.id 
            where l.publicacion_id = %s
            """, (
                like.get_perfil_id(),
                like.get_publicacion_id(),
            ))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_all_publicacion(self, perfil_id):
        try:
            self._cur.execute(""" select p.id, pf.nombre, pf.apellido, pf.foto_perfil, p.contenido, p.foto, p.fecha_publicacion, p.cant_likes, p.cant_comentarios, pf.id
                from publicacion as p
                inner join perfil as pf on p.perfil_id = pf.id
                where p.perfil_id = %s """, (
                perfil_id,
            ))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def get_all_comentarios(self, publicacion_id):
        try:
            self._cur.execute("""select c.publicacion_id, p.nombre, p.apellido, p.foto_perfil, c.contenido, c.fecha
            from comentarios as c
            inner join perfil as p on c.perfil_id = p.id
            where c.publicacion_id = %s
            """, (
                publicacion_id,
            ))
            self.connection.commit()
            return self._cur.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e
# [U] Funciones de actualizacion

    def update_foto_perfil(self, perfil_id, new_foto_path):
        try:
            sql = """
                UPDATE perfil
                SET foto_perfil = %s
                WHERE id = %s
            """
            self._cur.execute(sql, (new_foto_path, perfil_id))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

    def update_foto_portada(self, perfil_id, new_foto_path):
        try:
            sql = """
                UPDATE perfil
                SET foto_portada = %s
                WHERE id = %s
            """
            self._cur.execute(sql, (new_foto_path, perfil_id))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

    def update_perfil(self, perfil_id, nombre, apellido, fecha_nac, genero, situacion, lugar_residencia):
        try:
            sql = """
                UPDATE perfil SET nombre = %s, apellido = %s, fecha_nac = %s, genero = %s, 
                situacion_sentimental = %s, lugar_residencia = %s WHERE id = %s
            """
            self._cur.execute(sql, (nombre, apellido, fecha_nac,
                              genero, situacion, lugar_residencia, perfil_id))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
# [D] Funciones de borrar registros de la bd

    def drop_amigo(self, amigo: Amigo):
        self._cur.execute("DELETE FROM amigos WHERE perfil_id = %s and perfil_amigo_id = %s",
                          (amigo.get_perfil_id(), amigo.get_perfil_amigo_id()))
        self._cur.execute("DELETE FROM amigos WHERE perfil_id = %s and perfil_amigo_id = %s",
                          (amigo.get_perfil_amigo_id(), amigo.get_perfil_id()))
        self.connection.commit()

    def drop_solicitud(self, solicitud: Solicitud):
        self._cur.execute("DELETE FROM solicitudes WHERE perfil_id_emisor = %s and perfil_amigo_id_receptor = %s", (
            solicitud.get_perfil_id_emisor(),
            solicitud.get_perfil_id_receptor(),
        ))
        self.connection.commit()

    def drop_publicacion(self, perfil_id: int, publicacion_id: int):
        self._cur.execute("DELETE FROM publicacion WHERE perfil_id = %s and id = %s", (
            perfil_id, publicacion_id,
        ))
        self.connection.commit()

    def drop_like(self, like: Like):
        self._cur.execute("delete from likes where publicacion_id = %s and perfil_id = %s", (
            like.get_publicacion_id(),
            like.get_perfil_id(),
        ))
        self._cur.execute("UPDATE publicacion SET cant_likes = cant_likes-1 WHERE id = %s",
                          (like.get_publicacion_id(),))
        self.connection.commit()

    def drop_comentario(self, publicacion_id, perfil_id):
        self._cur.execute("delete from comentarios where publicacion_id = %s and perfil_id = %s", (
            publicacion_id, perfil_id,
        ))
        self._cur.execute("UPDATE publicacion SET cant_comentarios = cant_comentarios-1 WHERE id = %s",
                          (publicacion_id,))
        self.connection.commit()
