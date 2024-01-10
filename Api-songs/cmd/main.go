package main

import (
	"net/http"
	"songs/internal/controllers/songs"
	"songs/internal/helpers"

	"github.com/go-chi/chi/v5"
	"github.com/sirupsen/logrus"
)

func main() {
	r := chi.NewRouter()

	r.Route("/songs", func(r chi.Router) {
		r.Get("/", songs.GetSongs)
		r.Post("/", songs.AddSong)
		r.Route("/{id}", func(r chi.Router) {
			r.Use(songs.Ctx)
			r.Put("/", songs.EditSong)
			r.Get("/", songs.GetSong)
			r.Delete("/", songs.DeleteSong)

		})
	})

	logrus.Info("[INFO] Web server started. Now listening on *:4010")
	logrus.Fatalln(http.ListenAndServe(":4010", r))

}

func init() {
	db, err := helpers.OpenDB()
	if err != nil {
		logrus.Fatalf("error while opening database: %s", err.Error())
	}
	defer helpers.CloseDB(db)

	schemes := []string{
		`CREATE TABLE IF NOT EXISTS songs (
            id UUID PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            artist VARCHAR(100) NOT NULL,
            filename VARCHAR(50) NOT NULL,
            published VARCHAR(20) NOT NULL
        )`,
	}

	for _, scheme := range schemes {
		if _, err := db.Exec(scheme); err != nil {
			logrus.Fatalln("Could not generate table! Error was: " + err.Error())
		}
	}
}
