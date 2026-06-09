"""
Módulo para la normalización de expresiones horarias en textos.
Autor: Pau Lozano Danes
"""
import re

def normalizar_match(match):
    """
    Función auxiliar para normalizar el objeto match encontrado por la expresión regular.
    Ajusta los distintos formatos para devolver un string en formato HH:MM.
    """
    # Extraemos los grupos de la expresión regular
    hora_str = match.group('hora')
    min_str = match.group('min1') or match.group('min2')
    particula = match.group('particula')
    periodo = match.group('periodo')
    
    hora = int(hora_str)
    
    # Comprobación de errores de formato:
    # 1. Los minutos como "17:5" (un solo dígito tras los dos puntos) son inválidos en formato estándar
    if match.group('min1') and len(match.group('min1')) != 2:
        return match.group(0) # Retornamos la cadena original si es inválida
    
    # Parseo de minutos basados en partículas habladas
    if particula:
        particula = particula.strip().lower()
        if particula == 'en punto':
            minutos = 0
        elif particula == 'y cuarto':
            minutos = 15
        elif particula == 'y media':
            minutos = 30
        elif particula == 'menos cuarto':
            hora -= 1
            minutos = 45
    else:
        minutos = int(min_str) if min_str else 0

    # Ajustes basados en el periodo del día (reloj de 12 horas)
    if periodo:
        periodo = periodo.lower()
        if 'tarde' in periodo or 'noche' in periodo:
            # Validación: No se dice "17 de la tarde" o "13 de la tarde"
            if hora > 12:
                return match.group(0)
            if hora != 12:
                hora += 12
        elif 'mañana' in periodo or 'madrugada' in periodo or 'mediodía' in periodo:
            # Validación: No se dice "13 de la mañana"
            if hora > 12:
                return match.group(0)
            if hora == 12 and ('mañana' in periodo or 'madrugada' in periodo):
                hora = 0
                
    # Validación global de horas y minutos
    if not (0 <= hora <= 23) or not (0 <= minutos <= 59):
        return match.group(0)
        
    return f"{hora:02d}:{minutos:02d}"

def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero ficText, analiza las expresiones horarias y escribe ficNorm
    con las horas en formato estándar HH:MM.
    """
    
    # Expresión regular principal para capturar todas las variantes
    # Formatos contemplados:
    # - 18:30, 8:05, 17:5 (se validará dentro de la función) -> min1
    # - 8h, 8h30m, 10h30m -> min2
    # - 8 en punto, 4 y media, 5 menos cuarto -> particula
    # - de la mañana, de la tarde, etc. -> periodo
    
    patron = re.compile(
        r'\b'
        r'(?P<hora>\d{1,2})'                                       # Hora (1 o 2 dígitos)
        r'(?:'
            r':(?P<min1>\d{1,2})\b'                                # Formato estándar HH:MM
            r'|'
            r'h(?:(?P<min2>\d{1,2})m)?\b'                          # Formato HhMm o Hh
            r'|'
            r'\s+(?P<particula>en punto|y cuarto|y media|menos cuarto)' # Formato hablado
        r')?'
        r'(?:\s+de la\s+(?P<periodo>mañana|tarde|noche|madrugada|mediodía))?' # Periodo opcional
        r'\b',
        re.IGNORECASE
    )

    with open(ficText, 'r', encoding='utf-8') as f_in, \
         open(ficNorm, 'w', encoding='utf-8') as f_out:
        
        for linea in f_in:
            # re.sub permite pasar una función que procesa cada coincidencia
            linea_norm = patron.sub(normalizar_match, linea)
            f_out.write(linea_norm)