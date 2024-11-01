import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

class CURPGenerator:
    meses = {
        "enero": "01", "febrero": "02", "marzo": "03", "abril": "04", "mayo": "05",
        "junio": "06", "julio": "07", "agosto": "08", "septiembre": "09", "octubre": "10",
        "noviembre": "11", "diciembre": "12"
    }
    
    estados = {
        "aguascalientes": "AS", "baja california": "BC", "baja california sur": "BS",
        "campeche": "CC", "coahuila": "CL", "colima": "CM", "chiapas": "CS", "chihuahua": "CH",
        "ciudad de méxico": "DF", "durango": "DG", "guanajuato": "GT", "guerrero": "GR",
        "hidalgo": "HG", "jalisco": "JC", "méxico": "MC", "michoacán": "MN", "morelos": "MS",
        "nayarit": "NT", "nuevo león": "NL", "oaxaca": "OC", "puebla": "PL", "querétaro": "QT",
        "quintana roo": "QR", "san luis potosí": "SP", "sinaloa": "SL", "sonora": "SR",
        "tabasco": "TC", "tamaulipas": "TS", "tlaxcala": "TL", "veracruz": "VZ",
        "yucatán": "YN", "zacatecas": "ZS"
    }

    def __init__(self, nombre, apellido_paterno, apellido_materno, anio, mes, dia, sexo, estado):
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.anio = anio
        self.mes = mes.lower()
        self.dia = dia
        self.sexo = sexo
        self.estado = estado.lower()

    def validar_fecha(self):
        if self.mes not in self.meses:
            return False, "Mes inválido. Introduce el nombre correcto del mes."
        try:
            mes_numero = self.meses[self.mes]
            datetime(int(self.anio), int(mes_numero), int(self.dia))
            return True, ""
        except ValueError:
            return False, "Fecha inválida. Por favor, ingresa una fecha correcta."

    def generar_curp(self):
        es_fecha_valida, mensaje_error = self.validar_fecha()
        if not es_fecha_valida:
            return False, mensaje_error

        apellido_paterno = self.apellido_paterno.upper()
        apellido_materno = self.apellido_materno.upper()
        nombre = self.nombre.upper()

        def obtener_primera_vocal(palabra):
            for letra in palabra[1:]:
                if letra in 'AEIOU':
                    return letra
            return 'X'

        estado_codigo = self.estados.get(self.estado, "NE")

        curp = (
            apellido_paterno[0] +
            obtener_primera_vocal(apellido_paterno) +
            (apellido_materno[0] if apellido_materno else 'X') +
            nombre[0] +
            self.anio[-2:] +
            self.meses[self.mes] +
            self.dia.zfill(2) +
            self.sexo.upper() +
            estado_codigo.upper()
        )

        def obtener_primera_consonante_interna(palabra):
            for letra in palabra[1:]:
                if letra not in 'AEIOU':
                    return letra
            return 'X'

        curp += (
            obtener_primera_consonante_interna(apellido_paterno) +
            obtener_primera_consonante_interna(apellido_materno) +
            obtener_primera_consonante_interna(nombre)
        )

        curp += f"{random.randint(0, 9)}{random.randint(0, 9)}"

        return True, curp

def generar_curp():
    nombre = entry_nombre.get()
    apellido_paterno = entry_apellido_paterno.get()
    apellido_materno = entry_apellido_materno.get()
    anio = entry_anio.get()
    mes = combo_mes.get()
    dia = combo_dia.get()
    sexo = combo_sexo.get()
    estado = combo_estado.get()

    if not all([nombre, apellido_paterno, anio, mes, dia, sexo, estado]):
        messagebox.showerror("Error", "Todos los campos excepto 'Apellido Materno' son obligatorios.")
        return

    curp_generator = CURPGenerator(nombre, apellido_paterno, apellido_materno, anio, mes, dia, sexo, estado)
    valid, curp = curp_generator.generar_curp()
    
    if valid:
        messagebox.showinfo("CURP Generada", f"CURP: {curp}")
    else:
        messagebox.showerror("Error", curp)

root = tk.Tk()
root.title("Generador de CURP")

tk.Label(root, text="Nombre(s):").grid(row=0, column=0, pady=5)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, pady=5)

tk.Label(root, text="Apellido Paterno:").grid(row=1, column=0, pady=5)
entry_apellido_paterno = tk.Entry(root)
entry_apellido_paterno.grid(row=1, column=1, pady=5)

tk.Label(root, text="Apellido Materno:").grid(row=2, column=0, pady=5)
entry_apellido_materno = tk.Entry(root)
entry_apellido_materno.grid(row=2, column=1, pady=5)

tk.Label(root, text="Año de Nacimiento (AAAA):").grid(row=3, column=0, pady=5)
entry_anio = tk.Entry(root)
entry_anio.grid(row=3, column=1, pady=5)

tk.Label(root, text="Mes de Nacimiento:").grid(row=4, column=0, pady=5)
combo_mes = ttk.Combobox(root, values=list(CURPGenerator.meses.keys()), state="readonly")
combo_mes.grid(row=4, column=1, pady=5)

tk.Label(root, text="Día de Nacimiento:").grid(row=5, column=0, pady=5)
combo_dia = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(1, 32)], state="readonly")
combo_dia.grid(row=5, column=1, pady=5)

tk.Label(root, text="Sexo (H/M):").grid(row=6, column=0, pady=5)
combo_sexo = ttk.Combobox(root, values=["H", "M"], state="readonly")
combo_sexo.grid(row=6, column=1, pady=5)

tk.Label(root, text="Estado de Nacimiento:").grid(row=7, column=0, pady=5)
combo_estado = ttk.Combobox(root, values=list(CURPGenerator.estados.keys()), state="readonly")
combo_estado.grid(row=7, column=1, pady=5)

tk.Button(root, text="Generar CURP", command=generar_curp).grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
