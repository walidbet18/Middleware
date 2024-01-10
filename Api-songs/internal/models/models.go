package models

import (
	"github.com/gofrs/uuid"
)

type Song struct {
	ID        *uuid.UUID `json:"id"`
	Title     string     `json:"title"`
	Artist    string     `json:"artist"`
	Filename  string     `json:"filename"` // Type peut être un genre musical par exemple
	Published string     `json:"published"`
}
