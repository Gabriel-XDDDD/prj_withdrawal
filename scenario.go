package main

import (
	"flag"
	"fmt"
	"os"
)

func scenario() bool {
	name := flag.String("nombre", "Alice", "titular")
	start := flag.String("saldo", "234.56", "saldo inicial")
	amount := flag.String("retiro", "", "importe de retiro")
	deposit := flag.String("abono", "", "importe de abono")
	expected := flag.String("test", "", "exito, fallo o error")
	flag.Parse()
	if *amount == "" && *deposit == "" {
		return false
	}
	b, err := cents(*start)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	op, input := "retiro", *amount
	if *deposit != "" {
		op, input = "abono", *deposit
	}
	e := apply(b, op, input)
	fmt.Printf("%s | %s | %s | %s\n", *name, e.Status, soles(e.After), e.Message)
	want := *expected
	if want == "exito" {
		want = "éxito"
	}
	if want != "" && want != e.Status {
		os.Exit(1)
	}
	return true
}
