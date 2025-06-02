import os

# Rutas a los archivos
data_entry_path = os.path.join('DataEntry', 'DataEntry.txt')
data_base_path = os.path.join('DataBase', 'DataBase.txt')
resultado_path = os.path.join('Result', 'Resultado.txt')

# Leer y limpiar DataEntry.txt
with open(data_entry_path, 'r', encoding='utf-8') as f:
    entry_rules = set(line.strip() for line in f if line.strip())

# Preprocesar DataBase.txt
processed_base_rules = []

with open(data_base_path, 'r', encoding='utf-8') as f:
    buffer = []
    for line in f:
        stripped = line.strip().replace('"', '')
        if stripped:
            buffer.append(stripped)
        else:
            if buffer:
                combined = ' '.join(buffer).strip()
                processed_base_rules.append(combined)
                buffer = []
    if buffer:
        combined = ' '.join(buffer).strip()
        processed_base_rules.append(combined)

# Convertir a set limpio
base_rules = set(rule.strip() for rule in processed_base_rules if rule.strip())

# Buscar coincidencias "retiradas"
errores = []

for rule in entry_rules:
    for base_rule in base_rules:
        if rule in base_rule and 'RETIRED' in base_rule.upper() and rule != base_rule:
            errores.append((rule, base_rule))

# Guardar resultados en Result/Resultado.txt
os.makedirs('Result', exist_ok=True)

with open(resultado_path, 'w', encoding='utf-8') as f:
    if errores:
        f.write("❌ Reglas encontradas como RETIRED en la base estándar:\n\n")
        for original, retired in errores:
            f.write(f"- {original} ➜ encontrado como {retired}\n")
        print("✅ Errores guardados en 'Result/Resultado.txt'.")
    else:
        f.write("✅ No se encontraron reglas marcadas como RETIRED.\n")
        print("✅ No se encontraron reglas marcadas como RETIRED.")
