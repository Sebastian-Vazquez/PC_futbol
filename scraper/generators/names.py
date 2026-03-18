import random

# Nombres por país/región
NOMBRES = {
    "ESP": {
        "nombres": ["Alejandro", "Carlos", "David", "Diego", "Fernando", "Francisco", "Gonzalo",
                    "Hugo", "Iván", "Javier", "Jorge", "José", "Juan", "Luis", "Manuel", "Marco",
                    "Marcos", "Miguel", "Pablo", "Pedro", "Rafael", "Raúl", "Roberto", "Rodrigo",
                    "Rubén", "Sergio", "Víctor", "Álvaro", "Andrés", "Antonio", "Borja", "César",
                    "Daniel", "Eduardo", "Emilio", "Enrique", "Gabriel", "Guillermo", "Héctor",
                    "Ignacio", "Jaime", "Joel", "Jonathan", "Lucas", "Mario", "Mateo", "Nicolás",
                    "Óscar", "Pau", "Pepe", "Unai", "Yerlan", "Aitor", "Iker", "Mikel", "Oier"],
        "apellidos": ["García", "López", "Martínez", "Sánchez", "Pérez", "González", "Rodríguez",
                      "Fernández", "Jiménez", "Torres", "Domínguez", "Vázquez", "Álvarez", "Moreno",
                      "Alonso", "Romero", "Navarro", "Ruiz", "Díaz", "Herrero", "Molina", "Ortiz",
                      "Delgado", "Ramos", "Castro", "Suárez", "Blanco", "Morales", "Santos", "Gil",
                      "Herrera", "Iglesias", "Marco", "Mendez", "Peña", "Reyes", "Silva", "Soler",
                      "Varela", "Vidal", "Carvajal", "Barrios", "Cortés", "Fidalgo", "Merino",
                      "Pedri", "Gavi", "Yamal", "Joselu", "Asensio", "Ceballos", "Fabián"]
    },
    "ENG": {
        "nombres": ["Aaron", "Adam", "Ben", "Bradley", "Callum", "Charlie", "Connor", "Daniel",
                    "Declan", "Edward", "Ethan", "Freddie", "Harry", "Jack", "Jake", "James",
                    "Jamie", "Jordan", "Joshua", "Kieran", "Kyle", "Liam", "Luke", "Marcus",
                    "Mason", "Michael", "Nathan", "Oliver", "Owen", "Phil", "Reece", "Ryan",
                    "Sam", "Scott", "Sean", "Tom", "Tyler", "Will", "Xherdan", "Zack"],
        "apellidos": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Davis", "Miller", "Wilson",
                      "Moore", "Taylor", "Anderson", "Thomas", "White", "Harris", "Martin", "Walker",
                      "Young", "King", "Wright", "Scott", "Green", "Hall", "Allen", "Shaw", "Rice",
                      "Sterling", "Trippier", "Maguire", "Henderson", "Pickford", "Saka", "Bellingham",
                      "Grealish", "Mount", "Foden", "Alexander-Arnold", "Stones", "Gomez", "Pope"]
    },
    "GER": {
        "nombres": ["Andreas", "Bastian", "Christian", "Daniel", "Erik", "Florian", "Hans", "Jonas",
                    "Kai", "Klaus", "Leroy", "Lukas", "Marc", "Marco", "Markus", "Max", "Michael",
                    "Niklas", "Pascal", "Philip", "Robin", "Sebastian", "Simon", "Stefan", "Thomas",
                    "Tim", "Timo", "Tobias", "Tom", "Willi"],
        "apellidos": ["Müller", "Schmidt", "Koch", "Wagner", "Fischer", "Meyer", "Weber", "Schulz",
                      "Becker", "Braun", "Neuer", "Rüdiger", "Kimmich", "Goretzka", "Gnabry", "Sané",
                      "Havertz", "Brandt", "Süle", "Gündogan", "Werner", "Musiala", "Wirtz", "Kroos",
                      "Hummels", "Boateng", "Lahm", "Schweinsteiger", "Podolski", "Klose", "Reus",
                      "Götze", "Draxler", "Can", "Kehrer", "Tah", "Raum", "Bellingham"]
    },
    "FRA": {
        "nombres": ["Alexandre", "Alphonse", "Antoine", "Axel", "Benjamin", "Boubacar", "Christopher",
                    "Clément", "Corentin", "Dylan", "Florent", "Franck", "Hugo", "Jonathan", "Jules",
                    "Kylian", "Léo", "Lucas", "Maxime", "Mohamed", "Moussa", "Nicolas", "Nuno",
                    "Ousmane", "Paul", "Pierre", "Raphaël", "Romain", "Samuel", "Théo", "Thomas",
                    "Tiemoué", "Timothée", "Wissam", "Yann", "Youssef"],
        "apellidos": ["Dupont", "Durand", "Bernard", "Robert", "Petit", "Thomas", "Richard",
                      "Mbappé", "Benzema", "Griezmann", "Pogba", "Giroud", "Lloris", "Varane",
                      "Hernandez", "Pavard", "Koundé", "Upamecano", "Camavinga", "Tchouaméni",
                      "Rabiot", "Dembélé", "Coman", "Thuram", "Kanté", "Matuidi", "Sissoko",
                      "Mendy", "Saliba", "Guendouzi", "Clauss", "Konaté", "Fofana"]
    },
    "ITA": {
        "nombres": ["Alessandro", "Andrea", "Angelo", "Antonio", "Bruno", "Carlo", "Daniele",
                    "Davide", "Emanuele", "Federico", "Filippo", "Francesco", "Giacomo", "Giorgio",
                    "Giovanni", "Giuseppe", "Jorginho", "Lorenzo", "Luca", "Marco", "Matteo",
                    "Mattia", "Michele", "Nicolo", "Pietro", "Riccardo", "Roberto", "Simone",
                    "Stefano", "Tommaso"],
        "apellidos": ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Ricci",
                      "Donnarumma", "Barella", "Jorginho", "Verratti", "Insigne", "Immobile",
                      "Belotti", "Chiellini", "Bonucci", "Acerbi", "Di Lorenzo", "Spinazzola",
                      "Locatelli", "Pellegrini", "Zaniolo", "Frattesi", "Tonali", "Retegui",
                      "Scamacca", "Raspadori", "Gnonto", "Dimarco", "Bastoni", "Gatti"]
    },
    "ARG": {
        "nombres": ["Alejandro", "Brian", "Claudio", "Diego", "Eduardo", "Emiliano", "Ezequiel",
                    "Facundo", "Fernando", "Franco", "Gastón", "Guido", "Guillermo", "Hernán",
                    "Joaquín", "Jorge", "Juan", "Lautaro", "Leandro", "Leonel", "Lucas", "Marcos",
                    "Martín", "Mauro", "Maximiliano", "Nahuel", "Nicolás", "Pablo", "Paulo",
                    "Rodrigo", "Santiago", "Sergio", "Thiago"],
        "apellidos": ["González", "Rodríguez", "García", "López", "Martínez", "Fernández",
                      "Messi", "Di María", "Dybala", "Agüero", "Higuaín", "Lavezzi", "Tevez",
                      "Mascherano", "Otamendi", "Romero", "Molina", "Tagliafico", "Acuña",
                      "De Paul", "Lo Celso", "Mac Allister", "Enzo Fernández", "Almada",
                      "Lautaro", "Julián Álvarez", "Correa", "Papu Gómez", "Paredes", "Pezzella",
                      "Lisandro Martínez", "Nahuel Molina", "Thiago Almada"]
    },
    "BRA": {
        "nombres": ["Alisson", "Allan", "Bruno", "Carlos", "Casemiro", "Danilo", "Douglas",
                    "Ederson", "Felipe", "Firmino", "Fred", "Gabriel", "Guilherme", "Gustavo",
                    "João", "Leonardo", "Lucas", "Luiz", "Marquinhos", "Matheus", "Neymar",
                    "Pedro", "Philippe", "Rafael", "Raphinha", "Ricardo", "Richarlison",
                    "Rodrygo", "Thiago", "Vinicius", "Vinícius", "Weverton"],
        "apellidos": ["Silva", "Santos", "Oliveira", "Souza", "Costa", "Pereira", "Lima",
                      "Alves", "Neymar Jr", "Vinicius Junior", "Rodrygo", "Raphinha", "Richarlison",
                      "Gabriel Jesus", "Gabriel Martinelli", "Endrick", "Savinho", "Andrade",
                      "Militão", "Marquinhos", "Casemiro", "Bruno Guimarães", "Paquetá",
                      "Fred", "Alisson", "Ederson", "Bremer", "Danilo", "Renan Lodi"]
    },
    "POR": {
        "nombres": ["André", "Bruno", "Carlos", "Cristiano", "Diogo", "Francisco", "Gonçalo",
                    "Hélder", "João", "José", "Luís", "Manuel", "Nuno", "Pedro", "Rafael",
                    "Ricardo", "Rui", "Sérgio", "Vitinha"],
        "apellidos": ["Silva", "Santos", "Ferreira", "Costa", "Rodrigues", "Martins",
                      "Ronaldo", "Félix", "Jota", "Cancelo", "Dias", "Mendes", "Neves",
                      "Bernardo Silva", "Bruno Fernandes", "Vitinha", "Danilo Pereira",
                      "Rúben Neves", "Gonçalo Ramos", "Rafael Leão", "Beto", "Semedo"]
    },
    "NED": {
        "nombres": ["Arjen", "Daley", "Denzel", "Frenkie", "Georginio", "Jasper", "Jordy",
                    "Kevin", "Luuk", "Memphis", "Nathan", "Ryan", "Stefan", "Virgil", "Wout"],
        "apellidos": ["de Ligt", "de Jong", "van Dijk", "Depay", "Blind", "Wijnaldum",
                      "Cillessen", "Dumfries", "Gravenberch", "Gakpo", "Frimpong", "Timber",
                      "Simons", "Veerman", "Malen", "Zirkzee", "van den Berg"]
    },
    "MEX": {
        "nombres": ["Carlos", "César", "Diego", "Edson", "Guillermo", "Hirving", "Jorge",
                    "José Juan", "Raúl", "Roberto", "Rodrigo"],
        "apellidos": ["Jiménez", "Lozano", "Álvarez", "Corona", "Ochoa", "Moreno", "Araujo",
                      "Sánchez", "Herrera", "Gallardo", "Antuna", "Vega", "Guardado", "Layún"]
    },
    "TUR": {
        "nombres": ["Alpay", "Arda", "Burak", "Calhanoglu", "Cengiz", "Emre", "Furkan",
                    "Hakan", "Kerem", "Merih", "Mert", "Ozan", "Samet", "Serdar", "Yusuf"],
        "apellidos": ["Yilmaz", "Kaya", "Demir", "Sahin", "Celik", "Arslan", "Dogan",
                      "Yildiz", "Calhanoglu", "Demiral", "Kabak", "Soyuncu", "Under",
                      "Yazici", "Kokcu", "Guler", "Aktürkoğlu", "Karaman", "Bardakci"]
    },
    "BEL": {
        "nombres": ["Axel", "Charles", "Dries", "Eden", "Jeremy", "Kevin", "Leandro",
                    "Loïs", "Nacer", "Romelu", "Thomas", "Thorgan", "Timothy", "Yannick"],
        "apellidos": ["De Bruyne", "Hazard", "Lukaku", "Tielemans", "Vertonghen",
                      "Alderweireld", "Witsel", "Mertens", "Carrasco", "Origi",
                      "Mangala", "Boyata", "Casteels", "Theate", "Onana", "Nkunku"]
    },
    "AUT": {
        "nombres": ["David", "Florian", "Konrad", "Marcel", "Marko", "Martin", "Michael",
                    "Patrick", "Peter", "Philipp", "Raphael", "Stefan", "Thomas"],
        "apellidos": ["Alaba", "Grillitsch", "Sabitzer", "Lazaro", "Gregoritsch",
                      "Baumgartner", "Seiwald", "Kainz", "Weimann", "Trimmel",
                      "Posch", "Prassl", "Danso", "Wimmer", "Hedl", "Pentz"]
    },
    "SCO": {
        "nombres": ["Andrew", "Callum", "Craig", "Danny", "Grant", "James", "John",
                    "Kevin", "Kieran", "Liam", "Lewis", "Ryan", "Scott", "Stuart"],
        "apellidos": ["Robertson", "McGregor", "Tierney", "McGinn", "Armstrong",
                      "Gilmour", "Adams", "Cooper", "Turnbull", "McKenna",
                      "Hanley", "Patterson", "Taylor", "Forrest", "Christie"]
    },
    "UKR": {
        "nombres": ["Andriy", "Artem", "Dmytro", "Heorhiy", "Mykhailo", "Oleksandr",
                    "Roman", "Ruslan", "Serhiy", "Taras", "Viktor", "Vitaliy", "Vladyslav"],
        "apellidos": ["Shevchenko", "Mudryk", "Malinovskyi", "Zinchenko", "Mykolenko",
                      "Tsygankov", "Shaparenko", "Lunin", "Trubin", "Dovbyk",
                      "Bondar", "Matviyenko", "Stepanenko", "Sudakov", "Buyalsky"]
    },
    "CHE": {
        "nombres": ["Breel", "Denis", "Edimilson", "Fabian", "Granit", "Kevin",
                    "Manuel", "Michel", "Remo", "Ricardo", "Ruben", "Xherdan"],
        "apellidos": ["Xhaka", "Shaqiri", "Embolo", "Akanji", "Elvedi", "Zakaria",
                      "Rodriguez", "Zuber", "Freuler", "Okafor", "Vargas",
                      "Rieder", "Widmer", "Kobel", "Sommer", "Omlin"]
    },
    "CZE": {
        "nombres": ["Adam", "Jan", "Jakub", "Lukas", "Martin", "Michal", "Milan",
                    "Ondrej", "Pavel", "Petr", "Radek", "Tomas", "Vladimir"],
        "apellidos": ["Soucek", "Schick", "Coufal", "Kral", "Jankto", "Holes",
                      "Sadilek", "Hlozek", "Jurasek", "Barak", "Kuchta",
                      "Vaclik", "Mandous", "Provod", "Lingr", "Matejovsky"]
    },
    "SRB": {
        "nombres": ["Aleksandar", "Dusan", "Filip", "Ivan", "Luka", "Marko",
                    "Milos", "Nemanja", "Nikola", "Stefan", "Sergej", "Uros"],
        "apellidos": ["Jovic", "Tadic", "Milinkovic-Savic", "Vlahovic", "Kostic",
                      "Mitrovic", "Pavlovic", "Lazovic", "Lukic", "Samardzic",
                      "Gudelj", "Babic", "Radonjic", "Zivkovic", "Djuricic"]
    },
    "GRE": {
        "nombres": ["Christos", "Dimitris", "Giorgos", "Kostas", "Lazaros",
                    "Manolis", "Nikos", "Panagiotis", "Petros", "Stefanos", "Tasos"],
        "apellidos": ["Tzavellas", "Fortounis", "Manolas", "Bakasetas", "Masouras",
                      "Ioannidis", "Pelkas", "Tsimikas", "Giannoulis", "Mavropanos",
                      "Tzolis", "Koulierakis", "Siopis", "Galanopoulos", "Retsos"]
    },
    "DNK": {
        "nombres": ["Andreas", "Christian", "Daniel", "Emil", "Jannik", "Jonas",
                    "Kasper", "Lasse", "Mathias", "Mikkel", "Pierre", "Simon", "Victor"],
        "apellidos": ["Eriksen", "Schmeichel", "Hojberg", "Skov Olsen", "Wind",
                      "Norgaard", "Jensen", "Maehle", "Andersen", "Christensen",
                      "Boilesen", "Bah", "Lindstrom", "Hojlund", "Dreyer"]
    },
    "SWE": {
        "nombres": ["Alexander", "Dejan", "Emil", "Gustav", "Isak", "Jordan",
                    "Karl", "Ludwig", "Marcus", "Mattias", "Patrik", "Sebastian", "Viktor"],
        "apellidos": ["Ibrahimovic", "Isak", "Forsberg", "Ekdal", "Claesson",
                      "Olsson", "Danielson", "Lindelof", "Krafth", "Kulusevski",
                      "Elanga", "Gyokeres", "Almqvist", "Svensson", "Larsson"]
    },
    "SAU": {
        "nombres": ["Abdullah", "Ahmed", "Ali", "Firas", "Hassan", "Khalid",
                    "Mohammed", "Nasser", "Omar", "Saleh", "Sultan", "Turki", "Yasser"],
        "apellidos": ["Al-Dawsari", "Al-Buraikan", "Al-Shahrani", "Al-Ghannam",
                      "Al-Najei", "Al-Malki", "Al-Faraj", "Al-Abed", "Bahebri",
                      "Al-Tambakti", "Al-Yami", "Al-Khaibari", "Kanno", "Al-Hassan"]
    },
    "JPN": {
        "nombres": ["Daichi", "Gaku", "Hiroki", "Kaoru", "Keigo", "Ko",
                    "Ritsu", "Ryusei", "Shoya", "Takefusa", "Wataru", "Yuki"],
        "apellidos": ["Minamino", "Doan", "Kamada", "Ito", "Mitoma", "Tomiyasu",
                      "Ueda", "Machino", "Furuhashi", "Asano", "Daizen",
                      "Soma", "Shibasaki", "Morita", "Hashioka", "Suzuki"]
    },
    "KOR": {
        "nombres": ["Changhoon", "Euigyo", "Heechan", "Hwang", "Hyunwoo", "Inbeom",
                    "Jaesung", "Junho", "Minjae", "Seunggyu", "Sungryong", "Wooram"],
        "apellidos": ["Son", "Kim", "Lee", "Hwang", "Park", "Cho",
                      "Kwon", "Jung", "Oh", "Yoon", "Baek", "Na",
                      "Heechan", "Seungsoo", "Kibum", "Taehyun", "Bomsun"]
    },
    "AUS": {
        "nombres": ["Aaron", "Adam", "Andrew", "Ben", "Chris", "Craig", "Daniel",
                    "Dylan", "Harry", "Jackson", "James", "Josh", "Liam",
                    "Marcus", "Martin", "Mathew", "Mitchell", "Riley", "Ryan"],
        "apellidos": ["Rowles", "Leckie", "Irvine", "Mabil", "Maclaren",
                      "Devlin", "Atkinson", "Holland", "Wright", "Boyle",
                      "McGree", "Duke", "Nabbout", "Geria", "Neville", "Toure"]
    },
    "EGY": {
        "nombres": ["Ahmed", "Ali", "Amr", "Hamdi", "Hussein", "Kahraba",
                    "Mahmoud", "Mohamed", "Mostafa", "Omar", "Ramadan", "Tarek", "Trezeguet"],
        "apellidos": ["Salah", "El-Neny", "Hegazy", "Galal", "Kahraba",
                      "El Shenawy", "El Hadary", "Elneny", "Sobhi", "Said",
                      "Ramadan", "Trézéguet", "Mido", "Aboutrika", "Gedo"]
    },
    "RSA": {
        "nombres": ["Bongani", "Bradley", "Bafana", "Dino", "Elias", "Given",
                    "Luther", "Lyle", "Ndabayithethwa", "Percy", "Ronwen", "Thembinkosi"],
        "apellidos": ["Zwane", "Tau", "Lorch", "Foster", "Williams",
                      "Mudau", "Dolly", "Mokoena", "Kekana", "Shalulile",
                      "Vilakazi", "Letsholonyane", "Parker", "Zuma", "Mhango"]
    },
    "UAE": {
        "nombres": ["Abdullah", "Ahmad", "Ali", "Hamdan", "Khalid",
                    "Mohammed", "Omar", "Salem", "Walid", "Yahia", "Youssef"],
        "apellidos": ["Al-Ahbabi", "Mubarak", "Al-Ameri", "Khalil", "Al-Hammadi",
                      "Sana", "Al-Shanqiti", "Ismail", "Al-Junaibi", "Abdulrahman"]
    },
    "TUN": {
        "nombres": ["Anis", "Ellyes", "Ferjani", "Hannibal", "Issam",
                    "Msakni", "Naim", "Seifeddine", "Wahbi", "Wajdi", "Youssef"],
        "apellidos": ["Jebali", "Msakni", "Sliti", "Skhiri", "Khazri",
                      "Sassi", "Ben Romdhane", "Drager", "Ghandri", "Bronn",
                      "Talbi", "Kechrida", "Ben Slimane", "Abdi", "Jelassi"]
    },
    "NGA": {
        "nombres": ["Alex", "Brown", "Chidera", "Emmanuel", "Festus",
                    "John", "Kelechi", "Moses", "Odion", "Taiwo", "Victor", "Wilfried"],
        "apellidos": ["Osimhen", "Iheanacho", "Ighalo", "Moses", "Ndidi",
                      "Mikel", "Ekong", "Collins", "Chukwueze", "Lookman",
                      "Aribo", "Aina", "Balogun", "Awoniyi", "Adeniran"]
    },
    "NZL": {
        "nombres": ["Clayton", "Danny", "Hamish", "Jake", "Liam", "Matthew",
                    "Oliver", "Ryan", "Sam", "Tim", "Tom", "Will"],
        "apellidos": ["Lewis", "Thomas", "Jones", "Smith", "Brown",
                      "Williams", "White", "Taylor", "Davies", "Evans",
                      "Hudson", "Fisher", "Riley", "Wood", "Hall"]
    },
    "CAN": {
        "nombres": ["Alphonso", "Atiba", "Cyle", "Jonathan", "Jonathan", "Kamal",
                    "Lucas", "Liam", "Milan", "Scott", "Stephen", "Tajon"],
        "apellidos": ["Davies", "Hutchinson", "Larin", "David", "Osorio",
                      "Miller", "Borjan", "Buchanan", "Eustaquio", "Johnston",
                      "Waterman", "Henry", "Fraser", "Adekugbe", "Vitoria"]
    },
}

# Nombres internacionales / genéricos para países no especificados
NOMBRES_GENERICOS = {
    "nombres": ["Alex", "Alexis", "Carlos", "David", "Ivan", "Juan", "Kevin", "Leo",
                "Luis", "Marco", "Martin", "Miguel", "Nicolas", "Pablo", "Rafael",
                "Roberto", "Rodrigo", "Santiago", "Sebastian", "Victor"],
    "apellidos": ["Rodriguez", "Garcia", "Martinez", "Lopez", "Gonzalez", "Sanchez",
                  "Silva", "Santos", "Costa", "Ferreira", "Oliveira", "Pereira",
                  "Lima", "Alves", "Souza", "Smith", "Johnson", "Brown", "Davis",
                  "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas"]
}

def nombre_aleatorio(pais: str) -> tuple[str, str]:
    data = NOMBRES.get(pais, NOMBRES_GENERICOS)
    nombre = random.choice(data["nombres"])
    apellido = random.choice(data["apellidos"])
    return nombre, apellido

def nombre_corto(nombre: str, apellido: str) -> str:
    """Genera el nombre corto tipo 'Mbappé' o 'L. Martínez'"""
    if len(apellido) <= 10:
        return apellido
    return f"{nombre[0]}. {apellido}"
