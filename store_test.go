package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"sync"
	"testing"
	"time"
)

func TestHistorial(t *testing.T) {
	s := Store{path: filepath.Join(t.TempDir(), "cuenta.json")}
	for _, p := range [][2]string{{"retiro", "200"}, {"retiro", "200"}, {"abono", "-1"}} {
		if _, err := s.move(p[0], p[1]); err != nil {
			t.Fatal(err)
		}
	}
	reopened := Store{path: s.path}
	st, err := reopened.view()
	if err != nil || st.Balance != 3456 || len(st.History) != 3 {
		t.Fatal(st, err)
	}
	for i, want := range []string{"éxito", "fallo", "error"} {
		if st.History[i].Status != want {
			t.Fatal(st.History[i])
		}
	}
}

func TestDatosCorruptos(t *testing.T) {
	s := Store{path: filepath.Join(t.TempDir(), "cuenta.json")}
	if err := os.WriteFile(s.path, []byte("{"), 0600); err != nil {
		t.Fatal(err)
	}
	if _, err := s.move("abono", "10"); err == nil {
		t.Fatal("se aceptó un archivo corrupto")
	}
	b, err := os.ReadFile(s.path)
	if err != nil {
		t.Fatal(err)
	}
	if string(b) != "{" {
		t.Fatal("archivo sobrescrito")
	}
}

func TestHistorialSinFechaUTC(t *testing.T) {
	s := Store{path: filepath.Join(t.TempDir(), "cuenta.json")}
	e := apply(23456, "abono", "10")
	data, err := json.Marshal(State{Balance: e.After, History: []Record{{Event: e, ID: 1}}})
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(s.path, data, 0600); err != nil {
		t.Fatal(err)
	}
	if _, err := s.view(); err == nil {
		t.Fatal("se aceptó un registro sin fecha UTC")
	}
}

func TestHistorialFueraDeOrden(t *testing.T) {
	s := Store{path: filepath.Join(t.TempDir(), "cuenta.json")}
	first := apply(23456, "abono", "10")
	second := apply(first.After, "abono", "1")
	now := time.Now().UTC()
	st := State{Balance: second.After, History: []Record{
		{Event: first, ID: 1, TimeUTC: now},
		{Event: second, ID: 2, TimeUTC: now.Add(-time.Second)},
	}}
	data, err := json.Marshal(st)
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(s.path, data, 0600); err != nil {
		t.Fatal(err)
	}
	if _, err := s.view(); err == nil {
		t.Fatal("se aceptó un historial fuera de orden cronológico")
	}
}

func TestConcurrente(t *testing.T) {
	s := Store{path: filepath.Join(t.TempDir(), "cuenta.json")}
	var wg sync.WaitGroup
	for i := 0; i < 8; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if _, err := s.move("abono", "1"); err != nil {
				t.Error(err)
			}
		}()
	}
	wg.Wait()
	st, err := s.view()
	if err != nil || st.Balance != 24256 || len(st.History) != 8 {
		t.Fatal(st, err)
	}
}
