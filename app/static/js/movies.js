const movieForm = document.querySelector('#movieForm');
const editMovieForm = document.querySelector('#editMovieForm');

const handleImageUpload = async (movieId, posterFile, backdropFile) => {
    try {
        const payload = {
            movie_id: movieId,
            poster_image_data: null,
            backdrop_image_data: null
        };

        const readFileAsBase64 = (file) => {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const base64 = e.target.result.split(',')[1];
                    resolve(base64);
                };
                reader.onerror = reject;
                reader.readAsDataURL(file);
            });
        };
        if (posterFile) {
            payload.poster_image_data = await readFileAsBase64(posterFile);
        }
        if (backdropFile) {
            payload.backdrop_image_data = await readFileAsBase64(backdropFile);
        }

        const response = await fetch('/movie/images', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        return response.ok;
    } catch (error) {
        console.error('Erro no upload de imagens:', error);
        return false;
    }
};

movieForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(movieForm);
    const posterFile = formData.get('poster');
    const backdropFile = formData.get('backdrop');

    const movieData = {
        title: formData.get('title'),
        genre: formData.get('genre'),
        synopsis: formData.get('synopsis'),
        duration: parseInt(formData.get('duration')),
        age_rating: parseInt(formData.get('age_rating')),
        director: formData.get('director'),
        release_date: formData.get('release_date')
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
            if (posterFile.size > 0 || backdropFile.size > 0) {
                const uploadSuccess = await handleImageUpload(result.movie.id, posterFile, backdropFile);
                if (!uploadSuccess) {
                    alert('Filme criado, mas houve um erro no upload das imagens');
                }
            }
            await loadMovies();
            movieForm.reset();
            clearImage('poster');
            clearImage('backdrop');
        } else {
            alert(`Erro: ${result.detail}`);
        }
    } catch (error) {
        console.error('Erro:', error);
    }
});

const loadMovies = async () => {
    try {
        const response = await fetch('/movie/all');
        const data = await response.json();
        const movies = data.movies;

        const movieContainer = document.querySelector('#movieList');
        movieContainer.innerHTML = '';

        movies.forEach(movie => {
            const movieCard = document.createElement('div');
            movieCard.className = 'flex flex-col p-1 m-4 max-w-70 min-h-140 bg-stone-800 shadow-2xl border-2 border-stone-800 rounded-xl hover:scale-102 hover:border-orange-400 transition duration-200';

            movieCard.innerHTML = `
                <img src="/movie/${movie.id}/image/poster" alt="Movie poster" class="h-60 object-cover object-top rounded-xl">
                <h2 class="text-orange-300 text-2xl font-bold p-2 uppercase">${movie.id} - ${movie.title}</h2>
                <div class="p-3">
                    <p class="text-white"><strong>Gênero:</strong> ${movie.genre}</p>
                    <p class="text-white"><strong>Duração:</strong> ${movie.duration} min</p>
                    <p class="text-white"><strong>Classificação:</strong> ${movie.age_rating}+</p>
                    <p class="text-white line-clamp-3 mt-2">${movie.synopsis}</p>
                </div>
                <div class="flex justify-between gap-2 p-2 mt-auto">
                    <button class="delete-btn text-red-100 hover:text-orange-400 cursor-pointer hover:scale-150 transition duration-300" 
                        data-id="${movie.id}" data-title="${movie.title}">🗑️</button>
                    <button class="edit-btn text-red-100 hover:text-orange-400 cursor-pointer hover:scale-150 transition duration-300" 
                        data-movie="${JSON.stringify(movie).replace(/"/g, '&quot;')}">✏️</button>
                </div>
            `;

            movieContainer.appendChild(movieCard);
        });
    } catch (error) {
        console.error('Erro ao carregar filmes:', error);
    }
};

document.querySelector('#movieList').addEventListener('click', async (e) => {
    if (e.target.classList.contains('edit-btn')) {
        try {
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

            document.getElementById('movie_id').value = movieData.id;
            document.getElementById('edit-modal').classList.remove('hidden');

        } catch (error) {
            console.error('Erro ao parsear dados do filme:', error);
            alert('Erro ao carregar dados para edição');
        }
    }
});

document.querySelector('#movieList').addEventListener('click', async (e) => {
    if (e.target.classList.contains('delete-btn')) {
        const movieId = e.target.dataset.id;
        const movieTitle = e.target.dataset.title;

        const overlay = document.getElementById('dialog-overlay');
        const dialogMessage = document.querySelector('#dialog-message');

        overlay.classList.remove('hidden');
        dialogMessage.innerHTML = `Você tem certeza que deseja excluir este filme? <strong>${movieTitle}</strong>`;

        document.getElementById('dialog-confirm').onclick = async () => {
            try {
                const response = await fetch(`/movie/${movieId}`, {method: 'DELETE'});

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

editMovieForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const movieId = document.getElementById('movie_id').value;
    const formData = new FormData(editMovieForm);

    const movieData = {
        title: formData.get('title_edited'),
        genre: formData.get('genre_edited'),
        synopsis: formData.get('synopsis_edited'),
        duration: parseInt(formData.get('duration_edited')),
        age_rating: parseInt(formData.get('age_rating_edited')),
        director: formData.get('director_edited'),
        release_date: formData.get('release_date_edited')
    };

    try {
        const response = await fetch(`/movie/${movieId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(movieData)
        });

        if (response.ok) {
            await loadMovies();
            editMovieForm.reset();
            document.getElementById('edit-modal').classList.add('hidden');
        } else {
            const result = await response.json();
            alert(`Erro: ${result.detail}`);
        }
    } catch (error) {
        console.error('Erro:', error);
    }
});

document.querySelector('#btnCancelEdit').addEventListener('click', async function (event) {
    document.getElementById('edit-modal').classList.add('hidden');
})

const setupImagePreview = (inputId, previewId, previewImageId) => {
    const input = document.getElementById(inputId);
    const previewContainer = document.getElementById(previewId);
    const previewImage = document.getElementById(previewImageId);

    input.addEventListener('change', function () {
        const file = this.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                previewContainer.classList.remove('hidden');
            };
            reader.readAsDataURL(file);
        }
    });
};

const clearImage = (type) => {
    const input = document.getElementById(`${type}`);
    const previewContainer = document.getElementById(`${type}-preview`);
    const previewImage = document.getElementById(`${type}-preview-image`);

    if (input) input.value = '';
    if (previewImage) previewImage.src = '';
    if (previewContainer) previewContainer.classList.add('hidden');
};

document.addEventListener('DOMContentLoaded', () => {
    setupImagePreview('poster', 'poster-preview', 'poster-preview-image');
    setupImagePreview('backdrop', 'backdrop-preview', 'backdrop-preview-image');
    loadMovies();
});