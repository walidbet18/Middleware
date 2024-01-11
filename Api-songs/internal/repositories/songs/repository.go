package songs

import (
	"songs/internal/helpers"
	"songs/internal/models"

	"github.com/gofrs/uuid"
)

func GetAllSongs() ([]models.Song, error) {
	db, err := helpers.OpenDB()
	if err != nil {
		return nil, err
	}

	rows, err := db.Query("SELECT * FROM songs")
	defer helpers.CloseDB(db)
	if err != nil {
		return nil, err
	}
	defer func() {
		_ = rows.Close()
	}()

	songs := []models.Song{}
	for rows.Next() {
		var data models.Song
		err = rows.Scan(&data.ID, &data.Title, &data.Artist, &data.Filename, &data.Published)
		if err != nil {
			return nil, err
		}
		songs = append(songs, data)
	}

	return songs, nil
}

func GetSongByID(id uuid.UUID) (*models.Song, error) {
	db, err := helpers.OpenDB()
	if err != nil {
		return nil, err
	}

	row := db.QueryRow("SELECT * FROM songs WHERE id=?", id)

	defer helpers.CloseDB(db)
	var song models.Song
	err = row.Scan(&song.ID, &song.Title, &song.Artist, &song.Filename, &song.Published)
	if err != nil {
		return nil, err
	}
	return &song, nil
}

func AddSong(song *models.Song) error {
	db, err := helpers.OpenDB()
	if err != nil {
		return err
	}

	if err != nil {
		return err
	}
	id, err := uuid.NewV4() // Générer un nouvel UUID

	// Convertir UUID en chaîne avant de l'insérer dans la base de données
	_, err = db.Exec("INSERT INTO songs (id, title, artist, filename, published) VALUES (?, ?, ?, ?, ?)",
		id.String(), song.Title, song.Artist, song.Filename, song.Published)

	defer helpers.CloseDB(db)

	if err != nil {
		return err
	}

	return nil
}

func EditSong(songID uuid.UUID, song *models.Song) error {
	db, err := helpers.OpenDB()
	if err != nil {
		return err
	}

	_, err = db.Exec("UPDATE songs SET title = ?, artist = ?, filename = ?, published = ? WHERE id = ?",
		song.Title, song.Artist, song.Filename, song.Published, songID)

	defer helpers.CloseDB(db)
	if err != nil {
		return err
	}

	return nil
}

func DeleteSong(songID uuid.UUID) error {
	db, err := helpers.OpenDB()
	if err != nil {
		return err
	}

	_, err = db.Exec("DELETE FROM songs WHERE id = ?", songID)
	defer helpers.CloseDB(db)
	if err != nil {
		return err
	}

	return nil
}
