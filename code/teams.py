import json 

teams_data = [
    {
        "name": "Dinamo Moscow",
        "budget": 1200,
        "players": [
            {"name": "Nick Gusev", "position": "Forward", "skill": 92, "price": 118},
            {"name": "Semen Der-Arguchincev", "position": "Forward", "skill": 88, "price": 106},
            {"name": "Maxim Comtois", "position": "Forward", "skill": 90, "price": 110},
            {"name": "Sedrik Packett", "position": "Forward", "skill": 90, "price": 110},
            {"name": "Igor Ozhiganov", "position": "Defender", "skill": 87, "price": 82},
            {"name": "Artem Sergeev", "position": "Defender", "skill": 88, "price": 84},
            {"name": "Daniil Pylenkov", "position": "Defender", "skill": 85, "price": 79},
            {"name": "Vladislav Podyapolskiy", "position": "Goalkeeper", "skill": 90, "price": 106}
        ]
    },
    {
        "name": "Spartak",
        "budget": 1050,
        "players": [
            {"name": "Pavel Poryadin", "position": "Forward", "skill": 91, "price": 112},
            {"name": "Egor Filin", "position": "Forward", "skill": 87, "price": 104},
            {"name": "Ignat Korotkih", "position": "Forward", "skill": 85, "price": 100},
            {"name": "Daniil Gutik", "position": "Forward", "skill": 88, "price": 106},
            {"name": "Dmitriy Vishnevskiy", "position": "Defender", "skill": 87, "price": 82},
            {"name": "Daniil Ivanov", "position": "Defender", "skill": 86, "price": 80},
            {"name": "Andrey Mironov", "position": "Defender", "skill": 88, "price": 84},
            {"name": "Evgeniy Volokhin", "position": "Goalkeeper", "skill": 84, "price": 94}
        ]
    },
    {
        "name": "SKA",
        "budget": 1170,
        "players": [
            {"name": "Nikolay Goldobin", "position": "Forward", "skill": 91, "price": 112},
            {"name": "Matvey Korotkiy", "position": "Forward", "skill": 88, "price": 106},
            {"name": "Marat Hairulin", "position": "Forward", "skill": 89, "price": 108},
            {"name": "Sergey Plotnikov", "position": "Forward", "skill": 86, "price": 102},
            {"name": "Trevor Murphy", "position": "Defender", "skill": 88, "price": 84},
            {"name": "Sergey Sapego", "position": "Defender", "skill": 88, "price": 84},
            {"name": "Andrey Pedan", "position": "Defender", "skill": 89, "price": 86},
            {"name": "Sergey Ivanov", "position": "Goalkeeper", "skill": 85, "price": 96}
        ]
    },
    {
        "name": "Torpedo",
        "budget": 950,
        "players": [
            {"name": "Egor Vinogradov", "position": "Forward", "skill": 85, "price": 104},
            {"name": "Vladimir Tkachyov", "position": "Forward", "skill": 86, "price": 108},
            {"name": "Vasiliy Atanasov", "position": "Forward", "skill": 88, "price": 112},
            {"name": "Maxim Letunov", "position": "Forward", "skill": 87, "price": 110},
            {"name": "Mihail Naumenkov", "position": "Defender", "skill": 84, "price": 82},
            {"name": "Denis Aleksandrov", "position": "Defender", "skill": 83, "price": 80},
            {"name": "Bogdan Konyushkov", "position": "Defender", "skill": 86, "price": 86},
            {"name": "Dmitriy Shugayev", "position": "Goalkeeper", "skill": 83, "price": 98}
        ]
    },
    {
        "name": "CSKA",
        "budget": 1180,
        "players": [
            {"name": "Denis Zernov", "position": "Forward", "skill": 90, "price": 110},
            {"name": "Prokhor Poltapov", "position": "Forward", "skill": 89, "price": 108},
            {"name": "Klim Kostin", "position": "Forward", "skill": 89, "price": 108},
            {"name": "Ivan Drozdov", "position": "Forward", "skill": 88, "price": 106},
            {"name": "Jeremy Roy", "position": "Defender", "skill": 88, "price": 84},
            {"name": "Nick Nesterov", "position": "Defender", "skill": 88, "price": 84},
            {"name": "Nick Ebert", "position": "Defender", "skill": 90, "price": 88},
            {"name": "Alex Privalov", "position": "Goalkeeper", "skill": 88, "price": 102}
        ]
    },
    {
        "name": "Severstal",
        "budget": 1000,
        "players": [
            {"name": "Danil Aimurzin", "position": "Forward", "skill": 85, "price": 108},
            {"name": "Adam Lishka", "position": "Forward", "skill": 84, "price": 106},
            {"name": "Ivan Abrosimov", "position": "Forward", "skill": 85, "price": 108},
            {"name": "Ilya Ivanzov", "position": "Forward", "skill": 83, "price": 104},
            {"name": "Vladimir Grudinin", "position": "Defender", "skill": 84, "price": 84},
            {"name": "Ivan Ershov", "position": "Defender", "skill": 84, "price": 84},
            {"name": "Nick Kamalov", "position": "Defender", "skill": 83, "price": 82},
            {"name": "Konstantin Shostak", "position": "Goalkeeper", "skill": 86, "price": 106}
        ]
    },
    {
        "name": "Dinamo Minsk",
        "budget": 1150,
        "players": [
            {"name": "Sam Anas", "position": "Forward", "skill": 93, "price": 118},
            {"name": "Alex Limozh", "position": "Forward", "skill": 90, "price": 110},
            {"name": "Rayan Spuner", "position": "Forward", "skill": 90, "price": 110},
            {"name": "Vitaliy Pinchuk", "position": "Forward", "skill": 90, "price": 110},
            {"name": "Kristian Henkel", "position": "Defender", "skill": 89, "price": 86},
            {"name": "Pavel Denisov", "position": "Defender", "skill": 87, "price": 82},
            {"name": "Darren Diz", "position": "Defender", "skill": 89, "price": 80},
            {"name": "Zack Fukale", "position": "Goalkeeper", "skill": 89, "price": 104}
        ]
    },
    {
        "name": "Lokomotiv",
        "budget": 1300,
        "players": [
            {"name": "Alex Radulov", "position": "Forward", "skill": 96, "price": 110},
            {"name": "Egor Surin", "position": "Forward", "skill": 98, "price": 114},
            {"name": "Artur Kayumov", "position": "Forward", "skill": 97, "price": 112},
            {"name": "Pavel Kraskovskiy", "position": "Forward", "skill": 95, "price": 110},
            {"name": "Martin Gernat", "position": "Defender", "skill": 96, "price": 88},
            {"name": "Aleksey Bereglazov", "position": "Defender", "skill": 97, "price": 88},
            {"name": "Alex Yelesin", "position": "Defender", "skill": 97, "price": 88},
            {"name": "Daniil Isaev", "position": "Goalkeeper", "skill": 98, "price": 108}
        ]
    },
    {
        "name": "Dragons",
        "budget": 420,
        "players": [
            {"name": "Nick Mercly", "position": "Forward", "skill": 69, "price": 58},
            {"name": "Kevin Labank", "position": "Forward", "skill": 67, "price": 54},
            {"name": "Spencer Fu", "position": "Forward", "skill": 62, "price": 44},
            {"name": "Pavel Akolzin", "position": "Forward", "skill": 64, "price": 48},
            {"name": "Jake Bischoff", "position": "Defender", "skill": 64, "price": 41},
            {"name": "Riley Wil", "position": "Defender", "skill": 65, "price": 42},
            {"name": "Vladislav Leontyev", "position": "Defender", "skill": 66, "price": 44},
            {"name": "Patrick Rybar", "position": "Goalkeeper", "skill": 67, "price": 54}
        ]
    },
    {
        "name": "lada",
        "budget": 430,
        "players": [
            {"name": "Vladislav Chervonenko", "position": "Forward", "skill": 72, "price": 52},
            {"name": "Riley Savchuk", "position": "Forward", "skill": 72, "price": 52},
            {"name": "Andrey Chivilyov", "position": "Forward", "skill": 73, "price": 54},
            {"name": "Andrey Altybarmakyan", "position": "Forward", "skill": 71, "price": 50},
            {"name": "Willams Colbi", "position": "Defender", "skill": 72, "price": 44},
            {"name": "Daniil Bokun", "position": "Defender", "skill": 72, "price": 42},
            {"name": "Artem Zemchonok", "position": "Defender", "skill": 74, "price": 46},
            {"name": "Alex Trushkov", "position": "Goalkeeper", "skill": 73, "price": 54}
        ]
    },
    {
        "name": "Sochi",
        "budget": 440,
        "players": [
            {"name": "Willam Bitten", "position": "Forward", "skill": 70, "price": 54},
            {"name": "Timur Hafizov", "position": "Forward", "skill": 68, "price": 50},
            {"name": "Pavel Dedunov", "position": "Forward", "skill": 72, "price": 56},
            {"name": "Matvey Babenko", "position": "Forward", "skill": 71, "price": 54},
            {"name": "Danil Mokrushev", "position": "Defender", "skill": 67, "price": 42},
            {"name": "Cameron Li", "position": "Defender", "skill": 72, "price": 46},
            {"name": "Artem Volkov", "position": "Defender", "skill": 71, "price": 42},
            {"name": "Maxim Tretyak", "position": "Goalkeeper", "skill": 72, "price": 56}
        ]
    },
    {
        "name": "Amur",
        "budget": 430, 
        "players": [
            {"name": "Evgeniy Svechnikov", "position": "Forward", "skill": 75, "price": 50},
            {"name": "Danil Yurtaikin", "position": "Forward", "skill": 72, "price": 56},
            {"name": "Ivan Vorobyov", "position": "Forward", "skill": 70, "price": 50},
            {"name": "Alex Broadherst", "position": "Forward", "skill": 72, "price": 54},
            {"name": "Yaroslav Dyblenko", "position": "Defender", "skill": 70, "price":42},
            {"name": "Victor Antipin", "position": "Defender", "skill": 71, "price": 42},
            {"name": "Roman Abrosimov", "position": "Defender", "skill": 72, "price": 44},
            {"name": "Maxim Dorozhko", "position": "Goalkeeper", "skill": 73, "price": 56}
        ]
    },
    {
        "name": "Barys",
        "budget": 430,
        "players": [
            {"name": "Emil Galimov", "position": "Forward", "skill": 70, "price": 50},
            {"name": "Maxim Mukhametov", "position": "Forward", "skill": 70, "price": 50},
            {"name": "Max Willman", "position": "Forward", "skill": 71, "price": 52},
            {"name": "Maison Morelly", "position": "Forward", "skill": 72, "price": 54},
            {"name": "Adil Beketaev", "position": "Defender", "skill": 71, "price": 42},
            {"name": "Dmitriy Breus", "position": "Defender", "skill": 73, "price": 46},
            {"name": "Jake Massi", "position": "Defender", "skill": 72, "price": 44},
            {"name": "Nick Boyarkin", "position": "Goalkeeper", "skill": 72, "price": 54}
        ]
    },
    {
        "name": "Admiral",
        "budget": 480,
        "players": [
            {"name": "Stepan Starkov", "position": "Forward", "skill": 71, "price": 56},
            {"name": "Pavel Shen", "position": "Forward", "skill": 71, "price": 56},
            {"name": "Nick Soshnikov", "position": "Forward", "skill": 72, "price": 58},
            {"name": "Vladislav Kara", "position": "Forward", "skill": 74, "price": 62},
            {"name": "Dmitriy Deryabin", "position": "Defender", "skill": 72, "price": 48},
            {"name": "Alex Shepelev", "position": "Defender", "skill": 73, "price": 50},
            {"name": "Semen Ibragimov", "position": "Defender", "skill": 71, "price": 46},
            {"name": "Arseniy Ziba", "position": "Goalkeeper", "skill": 71, "price": 56}
        ]
    },
    {
        "name": "Sibir",
        "budget": 680,
        "players": [
            {"name": "Arkhip Nekolenko", "position": "Forward", "skill": 78, "price": 68},
            {"name": "Ivan Klimovich", "position": "Forward", "skill": 79, "price": 70},
            {"name": "Sergey Shirokov", "position": "Forward", "skill": 81, "price": 74},
            {"name": "Teilor Beck", "position": "Forward", "skill": 82, "price": 76},
            {"name": "Egor Alanov", "position": "Defender", "skill": 80, "price": 58},
            {"name": "Mihail Orlov", "position": "Defender", "skill": 79, "price": 56},
            {"name": "Egor Zaizev", "position": "Defender", "skill": 79, "price": 56},
            {"name": "Anton Krasotkin", "position": "Goalkeeper", "skill": 80, "price": 68}
        ]
    },
    {
        "name": "Nephtehimik",
        "budget": 600,
        "players": [
            {"name": "Nick Artamonov", "position": "Forward", "skill": 80, "price": 68},
            {"name": "Nick Horuzhev", "position": "Forward", "skill": 81, "price": 70},
            {"name": "Alex Dergachyov", "position": "Forward", "skill": 81, "price": 70},
            {"name": "Nick Popugayev", "position": "Forward", "skill": 81, "price": 70},
            {"name": "Dinar Hafizulin", "position": "Defender", "skill": 80, "price": 54},
            {"name": "Luka Profaka", "position": "Defender", "skill": 80, "price": 52},
            {"name": "Nick Hlystov", "position": "Defender", "skill": 79, "price": 52},
            {"name": "Yaroslav Ozolin", "position": "Goalkeeper", "skill": 80, "price": 64}
        ]
    },
    {
        "name": "Traktor",
        "budget": 700,
        "players": [
            {"name": "Joshua Livo", "position": "Forward", "skill": 88, "price": 76},
            {"name": "Mihail Grigorenko", "position": "Forward", "skill": 87, "price": 74},
            {"name": "Vasiliy Glotov", "position": "Forward", "skill": 88, "price": 76},
            {"name": "Alex Kadeykin", "position": "Forward", "skill": 88, "price": 76},
            {"name": "Sergey Telegin", "position": "Defender", "skill": 87, "price": 60},
            {"name": "Jordan Gross", "position": "Defender", "skill": 85, "price": 56},
            {"name": "Gregor Dronov", "position": "Defender", "skill": 86, "price": 58},
            {"name": "Sergey Mylnikov", "position": "Goalkeeper", "skill": 85, "price": 66}
        ]
    },
    {
        "name": "Salavat Yulaev",
        "budget": 700,
        "players": [
            {"name": "Sheldon Rempal", "position": "Forward", "skill": 89, "price": 78},
            {"name": "Evgeniy Kuznetsov", "position": "Forward", "skill": 86, "price": 72},
            {"name": "Alex Zharovskiy", "position": "Forward", "skill": 88, "price": 76},
            {"name": "Artem Gorshkov", "position": "Forward", "skill": 89, "price": 78},
            {"name": "Evgeniy Kulik", "position": "Defender", "skill": 86, "price": 58},
            {"name": "Ildan Gazimov", "position": "Defender", "skill": 86, "price": 58},
            {"name": "Alexey Vasilevskiy", "position": "Defender", "skill": 87, "price": 60},
            {"name": "Semen Vyazovoy", "position": "Goalkeeper", "skill": 87, "price": 70}
        ]
    },
    {
        "name": "Avtomobilist",
        "budget": 1000,
        "players": [
            {"name": "Daniel Sprong", "position": "Forward", "skill": 93, "price": 108},
            {"name": "Anatoliy Golyshev", "position": "Forward", "skill": 89, "price": 105},
            {"name": "Stephan Da Costa", "position": "Forward", "skill": 90, "price": 106},
            {"name": "Alex Sharov", "position": "Forward", "skill": 87, "price": 100},
            {"name": "Nick Tryamkin", "position": "Defender", "skill": 89, "price": 89},
            {"name": "Kirill Vorobyov", "position": "Defender", "skill": 87, "price": 85},
            {"name": "Sergey Zborovskiy", "position": "Defender", "skill": 88, "price":87},
            {"name": "Evgeniy Alikin", "position": "Goalkeeper", "skill": 92, "price": 110}
        ]
    },
    {
        "name": "Ak Bars",
        "budget": 950,
        "players": [
            {"name": "Dmitriy Yashkin", "position": "Forward", "skill": 90, "price": 106},
            {"name": "Ilya Saphonov", "position": "Forward", "skill": 91, "price": 108},
            {"name": "Nick Dynyak", "position": "Forward", "skill": 90, "price": 106},
            {"name": "Artem Galimov", "position": "Forward", "skill": 89, "price": 102},
            {"name": "Alexey Marchenko", "position": "Defender", "skill": 88, "price": 86},
            {"name": "Stepan Falkovskiy", "position": "Defender", "skill": 89, "price": 90},
            {"name": "Nick Lyamkin", "position": "Defender", "skill": 91, "price": 98},
            {"name": "Timur Bilyalov", "position": "Goalkeeper", "skill": 89, "price": 104}
        ]
    },
    {
        "name": "Avangard",
        "budget": 900,
        "players": [
            {"name": "Andrew Poturalski", "position": "Forward", "skill": 91, "price": 100},
            {"name": "Okulov Konstantin", "position": "Forward", "skill": 93, "price": 102},
            {"name": "Nail Yakupov", "position": "Forward", "skill": 92, "price": 100},
            {"name": "Michael Mcleod", "position": "Forward", "skill": 95, "price": 108},
            {"name": "Marsel Ibragimov", "position": "Defender", "skill": 91, "price": 88},
            {"name": "Damir Sharipzyanov", "position": "Defender", "skill": 94, "price": 94},
            {"name": "Vyacheslav Voinov", "position": "Defender", "skill": 92, "price": 90},
            {"name": "Nick Serebryakov", "position": "Goalkeeper", "skill": 93, "price": 107}
        ]
    },
    {
        "name": "Metalurg",
        "budget": 1100,
        "players": [
            {"name": "Roman Kanzerov", "position": "Forward", "skill": 98, "price": 120},
            {"name": "Dmitriy Silantiev", "position": "Forward", "skill": 95, "price": 106},
            {"name": "Alex Petunin", "position": "Forward", "skill": 96, "price": 108},
            {"name": "Daniil Vovchenko", "position": "Forward", "skill": 95, "price": 106},
            {"name": "Egor Yakovlev", "position": "Defender", "skill": 94, "price": 88},
            {"name": "Valeriy Orekhov", "position": "Defender", "skill": 94, "price": 92},
            {"name": "Robin Press", "position": "Defender", "skill": 94, "price": 92},
            {"name": "Ilya Nabokov", "position": "Goalkeeper", "skill": 96, "price": 110}
        ]
    }
]


with open("teams.json", "w", encoding="utf-8") as f:
    json.dump(teams_data, f, ensure_ascii=False, indent=4)
