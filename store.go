package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"
)

type Record struct {
	Event
	ID      int
	TimeUTC time.Time
}

type State struct {
	Balance int64
	History []Record
}

type Store struct {
	path string
	mu   sync.Mutex
}

func (s *Store) load() (State, error) {
	data, err := os.ReadFile(s.path)
	if errors.Is(err, os.ErrNotExist) {
		return State{Balance: 23456}, nil
	}
	var st State
	if err != nil {
		return st, err
	}
	if err = json.Unmarshal(data, &st); err != nil {
		return st, err
	}

	balance := int64(23456)
	var previousTime time.Time
	for i, r := range st.History {
		_, offset := r.TimeUTC.Zone()
		invalidTime := r.TimeUTC.IsZero() || offset != 0 || (!previousTime.IsZero() && r.TimeUTC.Before(previousTime))
		if r.ID != i+1 || invalidTime || r.Event != apply(balance, r.Operation, r.Input) {
			return st, fmt.Errorf("historial inconsistente")
		}
		balance = r.After
		previousTime = r.TimeUTC
	}
	if st.Balance != balance {
		return st, fmt.Errorf("saldo inconsistente")
	}
	return st, nil
}

func (s *Store) view() (State, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.load()
}

func (s *Store) move(op, input string) (Event, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	st, err := s.load()
	if err != nil {
		return Event{}, err
	}
	e := apply(st.Balance, op, input)
	st.Balance = e.After
	st.History = append(st.History, Record{e, len(st.History) + 1, time.Now().UTC()})
	tmp, err := os.CreateTemp(filepath.Dir(s.path), ".cuenta-*")
	if err != nil {
		return Event{}, err
	}
	defer os.Remove(tmp.Name())
	enc := json.NewEncoder(tmp)
	enc.SetIndent("", "  ")
	err = enc.Encode(st)
	if err == nil {
		err = tmp.Sync()
	}
	closeErr := tmp.Close()
	if err == nil {
		err = closeErr
	}
	if err == nil {
		err = os.Rename(tmp.Name(), s.path)
	}
	return e, err
}
