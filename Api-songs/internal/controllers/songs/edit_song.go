package songs

import (
	"encoding/json"
	"net/http"
	"songs/internal/models"
	"songs/internal/services/songs"

	"github.com/go-chi/chi/v5"
	"github.com/gofrs/uuid"

	"github.com/sirupsen/logrus"
)

// ModifierChanson modifie les détails d'une chanson existante.
func EditSong(w http.ResponseWriter, r *http.Request) {
	songID, _ := uuid.FromString(chi.URLParam(r, "id"))
	var updatedSong models.Song                         // Pas de pointeur ici, juste la structure Song
	err := json.NewDecoder(r.Body).Decode(&updatedSong) // Utilisation de "&" pour obtenir l'adresse de la structure
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		_, _ = w.Write([]byte("Requête invalide"))
		return
	}

	// Appeler la fonction de mise à jour de la chanson dans le service approprié
	_, err = songs.UpdateSong(songID, &updatedSong) // Passer la référence de la structure mise à jour
	if err != nil {
		logrus.Errorf("Erreur lors de la modification de la chanson : %s", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		_, _ = w.Write([]byte("Erreur interne du serveur"))
		return
	}

	// Répondre avec un statut 200 OK si tout s'est bien passé
	w.WriteHeader(http.StatusOK)
	response, _ := json.Marshal(updatedSong)
	_, _ = w.Write(response)
}
