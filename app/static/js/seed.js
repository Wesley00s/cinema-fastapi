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

const roomList = [
    {"number": 1, "capacity": 150},
    {"number": 2, "capacity": 180},
    {"number": 3, "capacity": 250},
    {"number": 4, "capacity": 200},
    {"number": 5, "capacity": 220},
    {"number": 6, "capacity": 210},
    {"number": 7, "capacity": 190},
    {"number": 8, "capacity": 260},
    {"number": 9, "capacity": 150},
]

const movieList = [
    {
        title: "O Poderoso Chefão",
        genre: "Drama",
        synopsis: "Na Nova York dos anos 1940, a família Corleone reina sobre um império clandestino de apostas, proteção e influência política." +
            " Don Vito Corleone (Marlon Brando), o patriarca respeitado e temido, equilibra poder e família enquanto governa com códigos rígidos" +
            " de honra. Porém, quando se recusa a entrar no lucrativo negócio de narcóticos, um ousado atentado coloca seu legado em risco." +
            " Enquanto Vito luta pela vida, seu filho Michael (Al Pacino) – um herói de guerra que sempre rejeitou o mundo do crime – é arrastado" +
            " para uma teia de vingança, traições e guerras entre as Cinco Famílias. Sua transformação de jovem idealista a líder implacável revela" +
            " o custo humano do poder, enquanto a família se envolve em uma trama que vai de Las Vegas à Sicília, em uma jornada épica sobre lealdade," +
            " tradição e a corrupção da alma. Dirigido por Francis Ford Coppola, este clássico atemporal explora a dualidade entre família e negócios," +
            " com cenas icônicas como o batismo sangrento e diálogos imortais (\"Vou fazer uma oferta que ele não poderá recusar\"). Vencedor de 3 Oscars®" +
            " (incluindo Melhor Filme), é um estudo magistral sobre poder, ética e o preço da ambição.",
        duration: 175,
        age_rating: 16,
        director: "Francis Ford Coppola",
        release_date: "1972-03-24",
        posterUrl: "/static/image/god-p.png",
        backdropUrl: "/static/image/god-bd.png"
    },
    {
        title: "Interestelar",
        genre: "Ficção Científica",
        synopsis: "Em um futuro próximo, a Terra agoniza sob tempestades de poeira e colheitas fracassadas. Cooper (Matthew McConaughey), um ex-piloto da NASA" +
            " viúvo e pai dedicado, luta para sustentar seus filhos em uma sociedade agrícola decadente. Quando uma anomalia gravitacional leva sua família a coordenadas" +
            " secretas, ele descobre um projeto desesperado: uma equipe de cientistas, liderada pelo enigmático Dr. Brand (Michael Caine), planeja atravessar um buraco" +
            " de minhoca recém-descoberto perto de Saturno – uma ponte para galáxias distantes onde três planetas potencialmente habitáveis aguardam. A bordo da nave Endurance," +
            " Cooper e a astrofísica Amelia Brand (Anne Hathaway) enfrentam dilatação temporal, buracos negros colossais e paradoxos cósmicos enquanto exploram mundos" +
            " alienígenas extremos: desde um oceano plano sob ondas gigantes até um planeta congelado iluminado por uma estrela moribunda. Enquanto horas nesses mundos equivalem" +
            " a décadas na Terra, Cooper luta contra o tempo para salvar a humanidade – e reconcilia-se com a promessa feita à filha Murphy, cujo destino se entrelaça com segredos" +
            " de gravidade quântica e uma quinta dimensão. Dirigido por Christopher Nolan e com consultoria do físico Kip Thorne, o filme mescla ciência de ponta (como a representação" +
            " realista do buraco negro Gargântua) com uma narrativa emocional sobre amor, sacrifício e a sobrevivência da espécie. Vencedor do Oscar® de Melhores Efeitos Visuais, é uma" +
            " odisseia cósmica que questiona: \"Como salvar a humanidade quando o tempo é um inimigo relativo?\"",
        duration: 169,
        age_rating: 12,
        director: "Christopher Nolan",
        release_date: "2014-11-07",
        posterUrl: "/static/image/interstellar-p.png",
        backdropUrl: "/static/image/interstellar-bd.png"
    },
    {
        title: "Clube da Luta",
        genre: "Drama",
        synopsis: "Em uma sociedade corroída pelo consumismo e pela alienação, um narrador anônimo (Edward Norton) – um homem" +
            " branco-collar sufocado por sua vida burocrática e insônia crônica – encontra alívio em grupos de apoio para doenças" +
            " que não tem. Sua frágil rotina desmorona quando conhece Tyler Durden (Brad Pitt), um saboneteiro carismático e anarquista" +
            " que personifica tudo o que ele secretamente deseja ser: livre, imprevisível e desprendido das amarras do sistema. Juntos," +
            " fundam o Clube da Luta, um subterrâneo clandestino onde homens frustrados extravasam sua raiva em combates brutais." +
            " O que começa como uma terapia violenta evolui para um movimento anticapitalista radical, com células secretas espalhadas" +
            " pelo país. Enquanto o Clube da Luta ganha força, o narrador se vê preso em uma espiral de caos, incêndios criminosos e atos" +
            " de sabotagem industrial. A linha entre realidade e delírio se desfaz quando ele descobre que Tyler e a enigmática Marla Singer" +
            " (Helena Bonham Carter) – uma figura autodestrutiva que frequenta os mesmos grupos de apoio – guardam segredos que desafiam sua" +
            " própria sanidade. Dirigido por David Fincher e baseado no livro de Chuck Palahniuk, o filme é um soco no estômago da cultura" +
            " corporativa, explorando temas como masculinidade tóxica, identidade fragmentada e a busca por propósito em um mundo hipercapitalista." +
            " Com diálogos icônicos (\"A primeira regra do Clube da Luta é: você não fala sobre o Clube da Luta\") e uma reviravolta que redefiniu" +
            " o cinema dos anos 1990, é um retrato perturbador de como o vazio existencial pode alimentar monstros.",
        duration: 139,
        age_rating: 18,
        director: "David Fincher",
        release_date: "1999-10-15",
        posterUrl: "/static/image/punch-p.png",
        backdropUrl: "/static/image/punch-bd.png"
    },
    {
        title: "O Exterminador do Futuro",
        genre: "Ficção Científica",
        synopsis: "No ano de 2029, as máquinas governam um mundo pós-apocalíptico após a ascensão da inteligência artificial Skynet," +
            " que quase exterminou a humanidade. Em um último esforço para vencer a guerra, a resistência humana liderada por John Connor" +
            " envia um soldado leal, Kyle Reese (Michael Biehn), de volta a 1984 para proteger sua mãe, Sarah Connor (Linda Hamilton)," +
            " uma jovem garçonete comum. Porém, Skynet contra-ataca enviando um Exterminador T-800 (Arnold Schwarzenegger) – um cyborgue" +
            " assassino revestido de tecido humano e programado para matar Sarah antes que John nasça. Em Los Angeles, Sarah é arrastada" +
            " para um pesadelo tecnológico: perseguida por uma máquina indestrutível que não sente dor, medo ou remorso, ela descobre seu" +
            " próprio destino enquanto Reese a protege com armas improvisadas e conhecimento sobre um futuro sombrio. Entre tiroteios em" +
            " clubes noturnos, explosões e uma icônica perseguição de caminhão, a dupla enfrenta o implacável T-800, cujo esqueleto endoarmado" +
            " brilha sob a pele destruída. Cada minuto é uma corrida contra o tempo, onde a sobrevivência de Sarah não significa apenas salvar" +
            " sua vida, mas garantir o futuro da humanidade. Dirigido por James Cameron, este marco dos anos 1980 redefine o gênero sci-fi com" +
            " efeitos práticos revolucionários (como o crânio cromado do T-800) e uma narrativa que mistura ação implacável com dilemas éticos" +
            " sobre inteligência artificial. A frase \"I'll be back\" entrou para a cultura pop, assim como a performance icônica de Schwarzenegger," +
            " que transformou o Exterminador em um símbolo do cinema de ação.",
        duration: 107,
        age_rating: 16,
        director: "James Cameron",
        release_date: "1984-10-26",
        posterUrl: "/static/image/terminator-p.png",
        backdropUrl: "/static/image/terminator-bd.png"
    },
    {
        title: "Pulp Fiction",
        genre: "Crime",
        synopsis: "Em Los Angeles, histórias de criminosos, boxeadores e gângsters se entrelaçam de maneira violenta e absurdamente cômica." +
            " Vincent Vega (John Travolta) e Jules Winnfield (Samuel L. Jackson), dois assassinos de aluguel com filosofias próprias, recuperam" +
            " uma misteriosa maleta para seu chefe, Marsellus Wallace (Ving Rhames). Enquanto isso, Butch (Bruce Willis), um boxeador corrupto," +
            " trai Marsellus, e Mia Wallace (Uma Thurman), a esposa do chefão, envolve Vincent em uma noite de drogas e dança que beira o surreal." +
            " Com diálogos afiados (\"Você sabe o que eles chamam de Quarter Pounder com Queijo em Paris?\") e cenas antológicas" +
            " (como o revival de dança de Vincent e Mia), Quentin Tarantino tece uma colcha de retratos sobre redenção, acaso e violência ritualizada." +
            " Vencedor da Palma de Ouro e Oscar® de Melhor Roteiro, o filme revoluciona a narrativa não linear, transformando referências de cultura pop" +
            " em um mosaico cru e hipnótico sobre o submundo do crime.",
        duration: 154,
        age_rating: 18,
        director: "Quentin Tarantino",
        release_date: "1994-10-21",
        posterUrl: "/static/image/pulp-p.png",
        backdropUrl: "/static/image/pulp-bd.png"
    },
    {
        title: "O Senhor dos Anéis: O Retorno do Rei",
        genre: "Fantasia",
        synopsis: "Na conclusão épica da trilogia de J.R.R. Tolkien, Frodo (Elijah Wood) e Sam (Sean Astin) avançam pelas terras de Mordor para destruir" +
            " o Um Anel na Montanha da Perdição, enquanto Gollum (Andy Serkis) os segue, consumido pela obsessão de recuperar seu \"precioso\". Enquanto isso," +
            " Aragorn (Viggo Mortensen) lidera os exércitos de Gondor e Rohan em uma batalha desesperada contra as forças de Sauron nos Portões Negros, numa" +
            " tentativa de distrair o Olho que Tudo Vê. Entre campos de batalha repletos de trolls e olifantes, a coragem de personagens como Gandalf (Ian McKellen)," +
            " Legolas (Orlando Bloom) e Gimli (John Rhys-Davies) é testada até o limite. Com a destruição do Anel, a Terramédia testemunha o fim da Era dos Elfos" +
            " e o início do domínio dos Homens. Dirigido por Peter Jackson, o filme venceu 11 Oscars®, incluindo Melhor Filme, com cenas icônicas como a carga dos" +
            " Rohirrim sob a luz do amanhecer e o emocionante \"You bow to no one\". Uma jornada sobre sacrifício, amizade e a luz que persiste nas horas mais escuras.",
        duration: 201,
        age_rating: 12,
        director: "Peter Jackson",
        release_date: "2003-12-25",
        posterUrl: "/static/image/lord-p.png",
        backdropUrl: "/static/image/lord-bd.png"
    },
    {
        title: "Cidade de Deus",
        genre: "Crime",
        synopsis: "Nas favelas do Rio de Janeiro dos anos 1960-1980, Buscapé (Alexandre Rodrigues), um jovem aspirante a fotógrafo, narra a ascensão e queda de Zé Pequeno" +
            " (Leandro Firmino), um dos traficantes mais temidos da Cidade de Deus. Da infância em gangues de crianças (os \"Terninhos\") ao domínio do tráfico de drogas," +
            " Zé Pequeno (também chamado Li'l Zé) impõe seu reinado com crueldade, enquanto Buscapé busca escapar do ciclo de violência através da arte. O filme retrata" +
            " décadas de conflitos entre facções, assassinatos brutais e a corrupção policial, com personagens como Bené (Phellipe Haagensen) e Sandro Cenoura (Matheus Nachtergaele)" +
            " ilustrando as escolhas morais em um ambiente onde a sobrevivência dita as regras. Dirigido por Fernando Meirelles e Kátia Lund, o longa é um retrato visceral" +
            " da vida nas favelas, com fotografia dinâmica e atuações marcantes de um elenco majoritariamente amador. Indicado a 4 Oscars®, é um soco sociopolítico que questiona:" +
            " \"Até onde você iria para não virar bandido?\"",
        duration: 130,
        age_rating: 18,
        director: "Fernando Meirelles e Kátia Lund",
        release_date: "2002-08-30",
        posterUrl: "/static/image/cidade-p.png",
        backdropUrl: "/static/image/cidade-bd.png"
    },
    {
        title: "Toy Story",
        genre: "Animação",
        synopsis: "No quarto de Andy, os brinquedos ganham vida quando os humanos não estão olhando. Woody (voz de Tom Hanks), um cowboy de borracha e líder adorado," +
            " vê seu posto ameaçado pela chegada de Buzz Lightyear (Tim Allen), um astronauta de ação high-tech que acredita ser um verdadeiro herói espacial. Ciúmes" +
            " e rivalidade levam os dois a se perderem durante uma mudança da família, forçando-os a uma jornada caótica para voltar a Andy antes que ele se mude. Entre" +
            " encontros com brinquedos psicodélicos (como o Sr. Cabeça de Batata) e o sádico vizinho Sid – que tortura brinquedos em experimentos bizarros –, Woody e Buzz" +
            " descobrem a importância da lealdade e da amizade. O primeiro longa-metragem totalmente em CGI, dirigido por John Lasseter, revolucionou a animação e inaugurou " +
            "a era de ouro da Pixar. Com humor inteligente e temas universais sobre aceitação e propósito, tornou-se um clássico atemporal, com frases icônicas como" +
            " \"Ao infinito e além!\".",
        duration: 81,
        age_rating: 0,
        director: "John Lasseter",
        release_date: "1995-12-22",
        posterUrl: "/static/image/toy-p.png",
        backdropUrl: "/static/image/toy-bd.png"
    },
    {
        title: "Parasita",
        genre: "Terror",
        synopsis: "A família Kim, moradora de um semissubterrâneo em Seul, sobrevive com bicos de pizza e WiFi roubado. Quando o filho Ki-woo (Choi Woo-shik) consegue" +
            " um emprego como tutor da rica família Park, ele inicia um plano elaborado: infiltrar cada membro da família Kim na casa dos Parks como empregados (motorista," +
            " governanta, professora), expulsando os funcionários originais com manipulação sutil. A fachada perfeita começa a ruir quando os segredos da mansão dos Parks" +
            " – incluindo um bunker secreto – entram em choque com a ganância e a luta de classes. Entre reviravoltas chocantes e um banho de sangue simbólico durante uma festa" +
            " de aniversário, o filme explora a dialética entre opressores e oprimidos, questionando quem é o verdadeiro parasita. Dirigido por Bong Joon-ho, vencedor" +
            " de 4 Oscars® (incluindo Melhor Filme), é um thriller social afiado que mistura humor negro, suspense e crítica ao capitalismo moderno.",
        duration: 132,
        age_rating: 16,
        director: "Bong Joon-ho",
        release_date: "2019-11-07",
        posterUrl: "/static/image/parasite-p.png",
        backdropUrl: "/static/image/parasite-bd.png"
    },
];

const populateMovies = async () => {
    try {

        const response = await fetch('/movie/all');
        const data = await response.json();
        const existingTitles = data.movies.map(movie => movie.title);

        for (const movie of movieList) {
            if (!existingTitles.includes(movie.title)) {

                const createResponse = await fetch('/movie', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        title: movie.title,
                        genre: movie.genre,
                        synopsis: movie.synopsis,
                        duration: movie.duration,
                        age_rating: movie.age_rating,
                        director: movie.director,
                        release_date: movie.release_date
                    })
                });

                const result = await createResponse.json();

                if (createResponse.ok) {
                    console.log(`Filme» "${movie.title}" criado com sucesso.`);

                    const posterBlob = await fetch(movie.posterUrl).then(res => res.blob());
                    const backdropBlob = await fetch(movie.backdropUrl).then(res => res.blob());

                    const posterFile = new File([posterBlob], "poster.png", {type: "image/jpeg"});
                    const backdropFile = new File([backdropBlob], "backdrop.png", {type: "image/jpeg"});
                    const uploadSuccess = await handleImageUpload(result.movie.id, posterFile, backdropFile);
                    if (!uploadSuccess) {
                        console.error(`Erro ao fazer upload das imagens para "${movie.title}"`);
                    }
                } else {
                    console.error(`Erro ao criar filme "${movie.title}": ${result.detail}`);
                }
            } else {
                console.log(`Filme "${movie.title}" já existe no banco de dados.`);
            }
        }
    } catch (error) {
        console.error('Erro ao popular filmes:', error);
    }
};

const populateRooms = async () => {

    try {
        const response = await fetch('/room/all');
        const data = await response.json();
        const existingRooms = data.rooms.map(room => room.number);

        for (const room of roomList) {
            if (!existingRooms.includes(room.number)) {

                const response = await fetch('/room', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(room)
                });

                const result = await response.json();

                if (response.ok) {
                    console.log(`Sala» "${room.number}" criada com sucesso.`)
                } else {
                    alert(`Erro: ${result.detail}`);
                }
            } else {
                console.log(`Sala "${room.number}" já existe no banco de dados.`);
            }
        }

    } catch (error) {
        console.error('Erro:', error);
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await populateMovies()
    await populateRooms()
});