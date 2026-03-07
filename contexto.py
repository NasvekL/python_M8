import os
import json
import pathspec

# Configuración
ARCHIVO_SALIDA = 'resultado_codigo.txt'
LIMITE_LINEAS = 500

def obtener_reglas_gitignore(ruta_raiz):
    ruta_gitignore = os.path.join(ruta_raiz, '.gitignore')
    lineas_ignoradas = []
    
    if os.path.exists(ruta_gitignore):
        with open(ruta_gitignore, 'r', encoding='utf-8') as f:
            lineas_ignoradas = f.readlines()
    
    # Detectar dinámicamente el nombre de este script
    nombre_script = os.path.basename(__file__)
    
    # Ignorar siempre la carpeta .git, el archivo de salida y el propio script
    lineas_ignoradas.extend(['.git/', ARCHIVO_SALIDA, nombre_script])
    
    # Compilar las reglas usando el estándar de git
    return pathspec.PathSpec.from_lines('gitwildmatch', lineas_ignoradas)

def construir_arbol_json(rutas):
    arbol = {}
    for ruta in rutas:
        partes = ruta.split('/')
        actual = arbol
        for parte in partes[:-1]:
            actual = actual.setdefault(parte, {})
        actual[partes[-1]] = "archivo"
    return arbol

def generar_archivo_contexto(ruta_raiz):
    spec = obtener_reglas_gitignore(ruta_raiz)
    archivos_validos = []
    
    # 1. Recorrer el directorio filtrando según .gitignore
    for root, directorios, archivos in os.walk(ruta_raiz):
        ruta_relativa_dir = os.path.relpath(root, ruta_raiz)
        if ruta_relativa_dir == '.':
            ruta_relativa_dir = ''
            
        # Modificar 'directorios' in situ para evitar que os.walk entre en carpetas ignoradas
        directorios[:] = [d for d in directorios if not spec.match_file(os.path.join(ruta_relativa_dir, d) + '/')]
        
        for archivo in archivos:
            ruta_relativa_archivo = os.path.join(ruta_relativa_dir, archivo).replace('\\', '/')
            if not spec.match_file(ruta_relativa_archivo):
                archivos_validos.append(ruta_relativa_archivo)
                
    archivos_validos.sort()
    
    # Generar la estructura en JSON (muy legible para las IAs)
    estructura_json = json.dumps(construir_arbol_json(archivos_validos), indent=2, ensure_ascii=False)
    
    with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as salida:
        # Escribir la estructura de directorios
        salida.write("ESTRUCTURA DEL PROYECTO (JSON):\n")
        salida.write(estructura_json)
        salida.write("\n")
        
        # 2, 3 y 4. Escribir el contenido de cada archivo
        for ruta_archivo in archivos_validos:
            ruta_absoluta = os.path.join(ruta_raiz, ruta_archivo)
            
            # Control de errores para evitar archivos binarios (ej: .png, .pdf, .pyc)
            try:
                with open(ruta_absoluta, 'r', encoding='utf-8') as f:
                    lineas = f.readlines()
            except UnicodeDecodeError:
                # Si no se puede leer como texto, lo saltamos silenciosamente
                continue
            except Exception as e:
                print(f"Aviso: No se pudo leer {ruta_archivo} - {e}")
                continue
                
            # Insertar los 3 saltos de línea requeridos
            salida.write("\n\n\n")
            salida.write(f"Archivo {ruta_archivo}:\n")
            
            # Comprobar límite de líneas
            if len(lineas) > LIMITE_LINEAS:
                salida.writelines(lineas[:LIMITE_LINEAS])
                
                # Asegurar que haya un salto de línea antes de imprimir el mensaje de recorte
                if not lineas[LIMITE_LINEAS - 1].endswith('\n'):
                    salida.write('\n')
                    
                lineas_restantes = len(lineas) - LIMITE_LINEAS
                salida.write(f"\n... ({lineas_restantes} lineas mas)\n")
            else:
                salida.writelines(lineas)

if __name__ == "__main__":
    directorio_actual = os.getcwd()
    print(f"Analizando directorio: {directorio_actual}")
    generar_archivo_contexto(directorio_actual)
    print(f"¡Listo! Archivo '{ARCHIVO_SALIDA}' generado con éxito.")