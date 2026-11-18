# language: es
Característica: Integridad de la transacción
  Escenario: Persistir tres intentos y recuperar el saldo al reiniciar
    Dado un archivo de cuenta nuevo
    Cuando retiro 200 dos veces e ingreso un abono negativo
    Entonces el archivo registra éxito, fallo y error y conserva 34.56 soles
