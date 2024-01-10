package main

import (
	"net/http"
	"users/internal/controllers/users"
	"users/internal/helpers"
	_ "users/internal/models"

	"github.com/go-chi/chi/v5"
	"github.com/sirupsen/logrus"
)

func main() {
	r := chi.NewRouter()

	r.Route("/users", func(r chi.Router) {
		r.Get("/", users.GetUsers)
		r.Post("/", users.AddUser)

		r.Route("/{id}", func(r chi.Router) {
			r.Use(users.Ctx)
			r.Get("/", users.GetUser)
			r.Put("/", users.EditUser)
			r.Delete("/", users.DeleteUser)

		})
	})

	logrus.Info("[INFO] Web server started. Now listening on *:4010")
	logrus.Fatalln(http.ListenAndServe(":4010", r))

}

func init() {
	db, err := helpers.OpenDB()
	if err != nil {
		logrus.Fatalf("error while opening database : %s", err.Error())
	}
	schemes := []string{
		`CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
	username VARCHAR(100) NOT NULL
)`,
	}
	for _, scheme := range schemes {
		if _, err := db.Exec(scheme); err != nil {
			logrus.Fatalln("Could not generate table ! Error was : " + err.Error())
		}
	}
	helpers.CloseDB(db)
}
