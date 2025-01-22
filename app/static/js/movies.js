const movieForm = document.querySelector('#movieForm');
const editMovieForm = document.querySelector('#editMovieForm');

movieForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const movieData = {
        title: document.getElementById('title').value,
        genre: document.getElementById('genre').value,
        synopsis: document.getElementById('synopsis').value,
        duration: parseInt(document.getElementById('duration').value),
        age_rating: parseInt(document.getElementById('age_rating').value),
        director: document.getElementById('director').value,
        release_date: document.getElementById('release_date').value
    };

    try {
        const response = await fetch('/movie', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(movieData)
        });

        const result = await response.json();

        if (response.ok) {
            await loadMovies()
            movieForm.reset();
        } else {
            alert(`Erro: ${result.detail}`);
        }
    } catch (error) {
        console.error('Erro:', error);
    }
});


const loadMovies = async () => {
    try {
        const response = await fetch('/movie');
        const data = await response.json();
        const movies = data.movies;

        const movieContainer = document.querySelector('.movie-container');
        movieContainer.innerHTML = '';

        movies.forEach(movie => {
            const movieCard = document.createElement('div');
            movieCard.classList.add('card');
            const releaseDate = new Date(movie.release_date);
            const formattedReleaseDate = releaseDate.toISOString().split('T')[0];

            movieCard.innerHTML = `
                    <div class="card-header">
                        <h3>${movie.title}</h3>
                    </div>
                    <div class="card-body">
                        <p><strong>ID:</strong> ${movie.id}</p>
                        <p><strong>Gênero:</strong> ${movie.genre}</p>
                        <p><strong>Duração:</strong> ${movie.duration} min</p>
                        <p><strong>Diretor:</strong> ${movie.director}</p>
                        <p><strong>Lançamento:</strong> ${formattedReleaseDate}</p>
                        <p><strong>Sinopse:</strong> ${movie.synopsis}</p>
                    </div>
                    <div id="rowConfig">
                        <img class="delete-btn" src="../static/icons/ic-trash.png" alt="" data-id="${movie.id}" data-title="${movie.title}"/>
                        <img class="edit-btn" src="../static/icons/ic-edit.png" alt="" data-movie="${JSON.stringify(movie).replace(/"/g, '&quot;')}"/>
                    </div>        
            `;

            movieContainer.appendChild(movieCard);
        });
    } catch (error) {
        console.error('Erro ao carregar filmes:', error);
    }
}

document.querySelector('.movie-container').addEventListener('click', async (e) => {
    if (e.target && e.target.classList.contains('delete-btn')) {
        const movieId = e.target.dataset.id;
        const movieTitle = e.target.dataset.title;

        const overlay = document.getElementById('dialog-overlay');
        const dialogMessage = document.querySelector('#dialog-message');

        overlay.classList.remove('hidden');
        dialogMessage.innerHTML = `Você tem certeza que deseja excluir este filme? <strong>${movieTitle}</strong>`;

        document.getElementById('dialog-confirm').onclick = async () => {
            try {
                const response = await fetch(`/movie?id=${movieId}`, {method: 'DELETE'});

                if (response.ok) {
                    await loadMovies();
                } else {
                    alert("Erro ao excluir o filme.");
                }
            } catch (error) {
                console.error('Erro ao excluir o filme:', error);
            } finally {
                overlay.classList.add('hidden');
            }
        };

        document.getElementById('dialog-cancel').onclick = () => {
            overlay.classList.add('hidden');
        };
    }
});


document.querySelector('.movie-container').addEventListener('click', async (e) => {
    if (e.target && e.target.classList.contains('edit-btn')) {
        const movieData = JSON.parse(e.target.dataset.movie);

        const releaseDate = new Date(movieData.release_date);
        const formattedReleaseDate = releaseDate.toISOString().split('T')[0];


        document.getElementById('title_edited').value = movieData.title;
        document.getElementById('genre_edited').value = movieData.genre;
        document.getElementById('duration_edited').value = movieData.duration;
        document.getElementById('director_edited').value = movieData.director;
        document.getElementById('release_date_edited').value = formattedReleaseDate;
        document.getElementById('synopsis_edited').value = movieData.synopsis;
        document.getElementById('age_rating_edited').value = movieData.age_rating;

        document.getElementById('movie_id_edited').value = movieData.id;

        document.getElementById('edit-modal').classList.remove('hidden');
    }
});

editMovieForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const movieId = document.getElementById('movie_id_edited').value;

    const movieData = {
        title: document.getElementById('title_edited').value,
        genre: document.getElementById('genre_edited').value,
        synopsis: document.getElementById('synopsis_edited').value,
        duration: parseInt(document.getElementById('duration_edited').value),
        age_rating: parseInt(document.getElementById('age_rating_edited').value),
        director: document.getElementById('director_edited').value,
        release_date: document.getElementById('release_date_edited').value
    };

    try {
        const response = await fetch(`/movie?id=${movieId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(movieData)
        });

        const result = await response.json();

        if (response.ok) {
            await loadMovies();
            editMovieForm.reset();
            document.getElementById('edit-modal').classList.add('hidden');
        } else {
            alert(`Erro: ${result.detail}`);
        }
    } catch (error) {
        console.error('Erro:', error);
    }
});

document.getElementById('close-modal').addEventListener('click', () => {
    document.getElementById('edit-modal').classList.add('hidden');
});

document.addEventListener('DOMContentLoaded', loadMovies);