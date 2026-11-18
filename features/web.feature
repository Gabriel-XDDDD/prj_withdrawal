# language: es
Característica: Operaciones desde la interfaz web
  Escenario: Enviar un abono mediante HTTP
    Dado un servidor web con una cuenta nueva
    Cuando envío un abono de 10 mediante el formulario
    Entonces la página muestra un saldo de 244.56
