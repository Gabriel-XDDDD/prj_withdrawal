package main

import "testing"

func TestMovimientos(t *testing.T) {
	for _, c := range []struct {
		saldo             int64
		op, monto, estado string
		final             int64
	}{
		{23456, "retiro", "200", "éxito", 3456}, {19876, "retiro", "200", "fallo", 19876}, {1000, "retiro", "10", "éxito", 0}, {1000, "retiro", "5", "error", 1000}, {100, "abono", "0,25", "éxito", 125}, {100, "abono", "0", "error", 100}, {100, "abono", "-2", "error", 100}, {100, "abono", "1.005", "error", 100},
	} {
		e := apply(c.saldo, c.op, c.monto)
		if e.Status != c.estado || e.After != c.final {
			t.Errorf("%+v: %+v", c, e)
		}
	}
}
