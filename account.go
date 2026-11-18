package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

var money = regexp.MustCompile(`^[0-9]{1,12}([.,][0-9]{1,2})?$`)

func cents(s string) (int64, error) {
	s = strings.ReplaceAll(strings.TrimSpace(s), ",", ".")
	if !money.MatchString(s) {
		return 0, fmt.Errorf("importe inválido")
	}
	parts := strings.Split(s+".00", ".")
	return strconv.ParseInt(parts[0]+(parts[1] + "00")[:2], 10, 64)
}
func soles(n int64) string { return fmt.Sprintf("%d.%02d", n/100, n%100) }

type Event struct {
	Operation       string
	Input           string
	Before, After   int64
	Status, Message string
}

func apply(balance int64, op, input string) Event {
	e := Event{Operation: op, Input: input, Before: balance, After: balance, Status: "error"}
	n, err := cents(input)
	switch {
	case err != nil || n == 0:
		e.Message = "Ingrese un monto positivo con hasta dos decimales."
	case op == "retiro" && n > balance:
		e.Status = "fallo"
		e.Message = "Saldo insuficiente. Intente con un monto menor."
	case op == "retiro" && n%1000 != 0:
		e.Message = "Use múltiplos de S/ 10 para el retiro."
	case op == "retiro":
		e.After -= n
		e.Status = "éxito"
		e.Message = "Retiro realizado."
	case op == "abono" && balance <= 9223372036854775807-n:
		e.After += n
		e.Status = "éxito"
		e.Message = "Abono realizado."
	default:
		e.Message = "Operación inválida o saldo fuera de rango."
	}
	return e
}
