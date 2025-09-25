"""
Desobfuscador HTML/JS - Técnica String.fromCharCode()
"""

import re
import sys
import os

def extraer_codigos_char(contenido):
    """Extrae códigos de caracteres de objetos JavaScript"""
    mapa_char = {}
    
    # Buscar patrones: dpsh["Iw"] = 48;
    patron = r'dpsh\["([^"]+)"\]\s*=\s*(\d+);'
    coincidencias = re.findall(patron, contenido, re.DOTALL)
    
    for clave, valor in coincidencias:
        mapa_char[clave] = int(valor)
    
    # También revisar comillas simples: dpsh['Iw'] = 48;
    patron_simple = r"dpsh\['([^']+)'\]\s*=\s*(\d+);"
    coincidencias_simple = re.findall(patron_simple, contenido, re.DOTALL)
    
    for clave, valor in coincidencias_simple:
        mapa_char[clave] = int(valor)
    
    return mapa_char

def desobfuscar_construccion_strings(contenido, mapa_char):
    """Desobfusca líneas que construyen strings con String.fromCharCode()"""
    contenido_desobfuscado = contenido
    
    # Buscar patrones: html += String.fromCharCode(dpsh["Me"]);
    patron = r'(\w+)\s*\+=\s*String\.fromCharCode\(dpsh\["([^"]+)"\]\);'
    coincidencias = re.findall(patron, contenido)
    
    # Agrupar por variable
    variables = {}
    for nombre_var, clave in coincidencias:
        if nombre_var not in variables:
            variables[nombre_var] = []
        if clave in mapa_char:
            variables[nombre_var].append(chr(mapa_char[clave]))
        else:
            variables[nombre_var].append(f"[DESCONOCIDO:{clave}]")
    
    # Reemplazar en contenido
    for nombre_var, chars in variables.items():
        if all(len(c) == 1 for c in chars):
            string_decodificado = ''.join(chars)
            patron_bloque = f'({nombre_var}\\s*\\+=\\s*String\\.fromCharCode\\(dpsh\\["[^"]+?"\\]\\);\\s*)+'
            reemplazo = f'{nombre_var} += "{string_decodificado}";'
            contenido_desobfuscado = re.sub(patron_bloque, reemplazo, contenido_desobfuscado)
    
    return contenido_desobfuscado

def desobfuscar_llamadas_directas(contenido, mapa_char):
    """Desobfusca llamadas directas como String.fromCharCode(dpsh["key"])"""
    def reemplazar_codigo_char(match):
        clave = match.group(1)
        if clave in mapa_char:
            codigo = mapa_char[clave]
            try:
                char = chr(codigo)
                # Escapar caracteres especiales para JavaScript
                if char == '"': return '"\""'
                elif char == "'": return '"\'"'
                elif char == '\\': return '"\\\\"'
                elif char == '\n': return '"\\n"'
                elif char == '\r': return '"\\r"'
                elif char == '\t': return '"\\t"'
                elif char == '<': return '"<"'
                elif char == '>': return '">"'
                elif char == '&': return '"&"'
                elif ord(char) > 255: return f'"\\u{ord(char):04x}"'
                else: return f'"{char}"'
            except ValueError:
                return match.group(0)
        else:
            return match.group(0)
    
    # Reemplazar String.fromCharCode(dpsh["key"]) con el carácter actual
    patron = r'String\.fromCharCode\(dpsh\["([^"]+)"\]\)'
    return re.sub(patron, reemplazar_codigo_char, contenido)

def obtener_mapa_char_defecto():
    """Mapeo de caracteres por defecto basado en patrones de ofuscación comunes"""
    return {
        "Iw": 48, "ed": 108, "AT": 33, "Ax": 116, "aq": 90, "Hf": 100, "Bh": 43, "DZ": 224,
        "zT": 237, "FW": 80, "Nv": 305, "Sn": 109, "NV": 350, "bI": 112, "bG": 38, "Xv": 34,
        "kW": 99, "UG": 91, "da": 252, "TK": 74, "mK": 88, "Dn": 58, "lv": 61, "dW": 8226,
        "Ky": 117, "Zf": 59, "Rd": 118, "Me": 65279, "cp": 56, "pd": 243, "qH": 98, "SX": 95,
        "tN": 105, "Uu": 169, "US": 67, "FI": 123, "pC": 125, "Ov": 72, "RS": 97, "jz": 50,
        "cD": 77, "Lm": 47, "ZN": 78, "mu": 84, "Lk": 107, "NA": 71, "Xl": 231, "uZ": 120,
        "CC": 86, "MB": 41, "wS": 119, "cX": 85, "AC": 32, "zz": 35, "rD": 104, "Jo": 233,
        "rl": 69, "pO": 57, "LG": 103, "lR": 10, "Is": 40, "mB": 65, "pu": 79, "cY": 75,
        "dZ": 227, "If": 106, "XO": 60, "sv": 87, "bu": 46, "TL": 245, "MP": 73, "Pr": 64,
        "Wu": 55, "Go": 225, "VY": 51, "aI": 121, "UU": 250, "my": 110, "bC": 44, "Kf": 52,
        "Ig": 54, "fG": 102, "CK": 39, "Hp": 70, "GN": 93, "BV": 49, "fB": 113, "BN": 124,
        "KN": 89, "Uf": 81, "Db": 122, "QM": 246, "zS": 37, "Jw": 232, "AF": 101, "cy": 111,
        "cq": 76, "Qh": 68, "ls": 82, "GL": 83, "Yq": 114, "Nn": 115, "Yx": 53, "nE": 62,
        "zX": 66, "FC": 45
    }

def procesar_archivo(ruta_archivo):
    """Procesar y desobfuscar archivo HTML/JS"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except UnicodeDecodeError:
        # Probar diferentes codificaciones
        codificaciones = ['latin1', 'cp1252', 'iso-8859-1']
        for codificacion in codificaciones:
            try:
                with open(ruta_archivo, 'r', encoding=codificacion) as f:
                    contenido = f.read()
                break
            except UnicodeDecodeError:
                continue
        else:
            print("Error: No se pudo leer el archivo con ninguna codificación común")
            return
    
    # Intentar extraer mapeo del archivo primero
    mapa_char = extraer_codigos_char(contenido)
    
    # Si no se encuentra mapeo completo, usar el por defecto
    if len(mapa_char) < 50:
        mapa_char = obtener_mapa_char_defecto()
    
    if not mapa_char:
        print("Error: No se encontraron definiciones de códigos de caracteres.")
        return
    
    # Desobfuscar construcción de strings
    contenido_desobfuscado = desobfuscar_construccion_strings(contenido, mapa_char)
    
    # Desobfuscar llamadas directas
    contenido_desobfuscado = desobfuscar_llamadas_directas(contenido_desobfuscado, mapa_char)
    
    # Guardar archivo desobfuscado
    nombre_base = os.path.splitext(ruta_archivo)[0]
    archivo_salida = f"{nombre_base}_limpio.html"
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(contenido_desobfuscado)
    
    # Verificar claves faltantes
    claves_usadas = set()
    patron = r'dpsh\["([^"]+)"\]'
    coincidencias = re.findall(patron, contenido)
    claves_usadas.update(coincidencias)
    
    claves_faltantes = claves_usadas - set(mapa_char.keys())
    
    # Mostrar resultado final
    if claves_faltantes:
        print(f"Desobfuscación completada con {len(claves_faltantes)} claves faltantes")
    else:
        print(f"Desobfuscación completada exitosamente")
    
    print(f"Archivo guardado en: {archivo_salida}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python desobfuscador.py <archivo.html>")
        print("Ejemplo: python desobfuscador.py muestra.html")
        return
    
    ruta_archivo = sys.argv[1]
    
    if not os.path.exists(ruta_archivo):
        print(f"Error: Archivo '{ruta_archivo}' no encontrado.")
        return
    
    procesar_archivo(ruta_archivo)

if __name__ == "__main__":
    main()