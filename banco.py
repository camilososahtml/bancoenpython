from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

#entrenamiento del chatbot
preguntas_entrenamiento = [
    "como se cuanto dinero tengo",
    "como veo mi saldo",
    "como deposito plata",
    "como hago un deposito",
    "quiero ingresar dinero",
    "como retiro dinero",
    "quiero sacar plata",
    "como veo mi historial",
    "donde estan mis transacciones",
    "como cierro sesion",
    "como salgo del banco",
    "como funciona este banco",
    "que opciones tiene el menu",
    "como accedo a preguntas frecuentes"
]

respuestas_entrenamiento = [
    "Puedes ver tu saldo con la opción 1 del menú.",
    "Tu saldo se consulta con la opción 1 del menú.",
    "Para depositar, usa la opción 2 del menú.",
    "Puedes depositar seleccionando la opción 2.",
    "El depósito se hace en la opción 2 del menú.",
    "Para retirar dinero, usa la opción 3.",
    "Selecciona la opción 3 para retirar dinero.",
    "El historial está en la opción 4 del menú.",
    "Tus transacciones se ven en la opción 4.",
    "Puedes cerrar sesión con la opción 5.",
    "Sales del sistema usando la opción 5.",
    "Este banco funciona con un menú de opciones: saldo, depósitos, retiros e historial.",
    "El menú tiene opciones: 1-Saldo, 2-Depositar, 3-Retirar, 4-Historial, 5-Salir, 6-Preguntas Frecuentes.",
    "Estás en la sección de Preguntas Frecuentes, donde puedes consultar dudas básicas."
]

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(preguntas_entrenamiento)
modelo = MultinomialNB()
modelo.fit(X_train, respuestas_entrenamiento)


def mostrar_saldo(saldo):
    print(f"Tu saldo actual es: {saldo:.2f} pesos Uruguayos.")

def depositar():
    try:
        monto = float(input("Introduce una cantidad para depositar: "))
        if monto <= 0:
            print("La cantidad introducida no es válida. Ingresá un monto positivo.")
            return 0
        return monto
    except ValueError:
        print("Error: Tenés que ingresar un número válido.")
        return 0

def retirar(saldo):
    try:
        monto = float(input("Introduce la cantidad a retirar: "))
        if monto > saldo:
            print("Fondos insuficientes.")
            return 0
        elif monto <= 0:
            print("La cantidad debe ser mayor a 0.")
            return 0
        return monto
    except ValueError:
        print("Error: Tenés que ingresar un número válido.")
        return 0

def faq_chat():
    print("\n--- Preguntas Frecuentes ---")
    print("Escribe tu duda (ej: '¿cómo deposito plata?'). Escribe 'salir' para volver al menú.\n")
    while True:
        entrada = input("Tú: ").lower()
        if entrada in ["salir", "chau", "adios"]:
            print("Chatbot: Volviendo al menú principal...")
            break
        entrada_vector = vectorizer.transform([entrada])
        respuesta = modelo.predict(entrada_vector)
        print("Chatbot:", respuesta[0])

def mostrar_historial(historial):
    if not historial:
        print("No tienes transacciones aún.")
    else:
        print("\nHistorial de Transacciones:")
        print(f"{'Fecha y Hora':<20} | {'Tipo':<10} | {'Monto':<10} | {'Saldo':<10}")
        print("-" * 60)
        for transaccion in historial:
            print(f"{transaccion['fecha']:<20} | {transaccion['tipo']:<10} | "
                f"{transaccion['monto']:<10.2f} | {transaccion['saldo']:<10.2f}")


def menu_principal():
    historial = []
    saldo = 0
    en_ejecucion = True

    nombre = input("\nIngrese su nombre y apellido: ")
    while True:
        pin = input("Cree un PIN de 4 dígitos para su cuenta: ")
        if pin.isdigit() and len(pin) == 4:
            break
        else:
            print("El PIN debe ser un número de 4 dígitos.")
    print(f"{nombre}, Bienvenido al Banco Uruguayo.")

    while en_ejecucion:
        print("\n----- MENÚ PRINCIPAL -----")
        print("1. Mostrar Saldo")
        print("2. Depositar")
        print("3. Retirar")
        print("4. Ver Historial de Transacciones")
        print("5. Salir")
        print("6. Preguntas Frecuentes (Chatbot)")
        opcion = input("Introduce tu elección (1-6): ")

        if opcion == '1':
            mostrar_saldo(saldo)

        elif opcion == '2':
            monto = depositar()
            if monto > 0:
                saldo += monto
                historial.append({
                    "tipo": "Depósito",
                    "monto": monto,
                    "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "saldo": saldo
                })
                print(f"Depósito exitoso. Nuevo saldo: {saldo:.2f}")

        elif opcion == '3':
            monto = retirar(saldo)
            if monto > 0:
                pin_ingresado = input("Ingresa tu PIN para confirmar el retiro: ")
                if pin_ingresado != pin:
                    print("PIN incorrecto. Retiro cancelado.")
                else:
                    saldo -= monto
                    historial.append({
                        "tipo": "Retiro",
                        "monto": monto,
                        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "saldo": saldo
                    })
                    print(f"Retiro exitoso. Nuevo saldo: {saldo:.2f}")

        elif opcion == '4':
            mostrar_historial(historial)

        elif opcion == '5':
            en_ejecucion = False
            print("Sesión en el banco finalizada. Que tengas un buen día.")

        elif opcion == '6':
            faq_chat()

        else:
            print("Esa opción no existe. Intenta con otra.")

if __name__ == '__main__':
    menu_principal()
