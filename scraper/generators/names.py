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
