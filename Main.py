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
    inside_quotes = False
    for line in f:
        stripped = line.strip()
        # Detectar apertura/cierre de comillas multilínea
        if '"' in stripped:
            if not inside_quotes:
                inside_quotes = True
                buffer = [stripped.replace('"', '')]
            else:
                buffer.append(stripped.replace('"', ''))
                combined = ' '.join(buffer).strip()
                processed_base_rules.append(combined)
                buffer = []
                inside_quotes = False
        elif inside_quotes:
            buffer.append(stripped)
        else:
            if stripped:
                processed_base_rules.append(stripped)

# Convertir a set limpio
base_rules = set(rule.strip() for rule in processed_base_rules if rule.strip())

# Buscar coincidencias "retiradas"
errores = []

for rule in entry_rules:
    rule_upper = rule.strip().upper()
    for base_rule in base_rules:
        base_rule_upper = base_rule.strip().upper()
        if (
            'RETIRED' in base_rule_upper
            and rule_upper in base_rule_upper
            and rule_upper != base_rule_upper
        ):
            errores.append((rule, base_rule))
            break  # No hace falta seguir buscando para esta regla

# Guardar resultados en Result/Resultado.txt
os.makedirs('Result', exist_ok=True)

with open(resultado_path, 'w', encoding='utf-8') as f:
    if errores:
        f.write("❌ Reglas encontradas como RETIRED en la base estándar:\n\n")
        for original, retired in errores:
            f.write(f"- {original} ➜ encontrado como {retired}\n")
        print("✅ Errores guardados correctamente en 'Result/Resultado.txt'.")
    else:
        f.write("✅ No se encontraron reglas marcadas como RETIRED.\n")
        print("✅ No se encontraron reglas marcadas como RETIRED.")
