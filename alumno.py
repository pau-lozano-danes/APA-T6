"""
Módulo para el tratamiento de las notas de los alumnos.
Autor: Pau Lozano Danés
"""
import re

class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:
    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=None):
        if notas is None:
            notas = []
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlum):
    """
    Lee un fichero de texto con los datos de todos los alumnos y devuelve
    un diccionario en el que la clave sea el nombre de cada alumno y su
    contenido el objeto Alumno correspondiente.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171	Blanca Agirrebarrenetse	9.5
    23	Carles Balcells de Lara	4.9
    68	David Garcia Fuster	7.0
    """
    dic_alumnos = {}
    
    # Expresión regular:
    # Grupo 1: Opcional, captura dígitos iniciales (numIden)
    # Grupo 2: Captura el nombre completo de forma perezosa
    # Grupo 3: Captura el resto de la línea que contiene las notas (números y espacios)
    patron = re.compile(r'^\s*(?:(\d+)\s+)?([a-zA-ZÀ-ÿ\s]+?)\s+([\d\.\s]+)$')

    with open(ficAlum, 'r', encoding='utf-8') as f:
        for linea in f:
            # Limpiamos los espacios al final para evitar fallos con los saltos de línea
            match = patron.search(linea.rstrip())
            if match:
                num_iden_str = match.group(1)
                nombre = match.group(2).strip()
                notas_str = match.group(3).split()
                
                num_iden = int(num_iden_str) if num_iden_str else -1
                notas = [float(nota) for nota in notas_str]
                
                dic_alumnos[nombre] = Alumno(nombre, num_iden, notas)

    return dic_alumnos

if __name__ == '__main__':
    import doctest
    # Ejecutamos los tests en modo verboso y normalizando los espacios
    doctest.testmod(verbose=True, optionflags=doctest.NORMALIZE_WHITESPACE)