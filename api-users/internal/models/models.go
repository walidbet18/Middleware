package models

import (
	"github.com/gofrs/uuid"
)

type User struct {
	ID       *uuid.UUID `json:"id"`
	Username string     `json:"username"`
	Password string     `json:"password"`
	Name     string     `json:"name"`
}
