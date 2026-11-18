# language: es
Característica: Operaciones en efectivo
  Esquema del escenario: Aplicar el movimiento sin alterar el saldo ante un rechazo
    Dado que <nombre> tiene <saldo> soles
    Cuando solicita un <operacion> de <monto>
    Entonces obtiene <estado> y un saldo de <final> soles

    Ejemplos:
      | nombre | saldo  | operacion | monto | estado | final  |
      | Alice  | 234.56 | retiro    | 200   | éxito  | 34.56  |
      | Hamza  | 198.76 | retiro    | 200   | fallo  | 198.76 |
      | Pedro  | 300.00 | retiro    | -20   | error  | 300.00 |
      | Alice  | 34.56  | abono     | 20.50 | éxito  | 55.06  |
      | Alice  | 34.56  | abono     | 0     | error  | 34.56  |
