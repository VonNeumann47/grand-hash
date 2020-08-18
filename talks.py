from config import Lang

import re
from string import punctuation


def normalize_text(string, specials="?"):
    string = string.lower().strip().replace('ё', 'е')
    for c in punctuation:
        if c not in specials:
            string = string.replace(c, "")
    while "  " in string:
        string = string.replace("  ", " ")
    return string


talks_dict = {
    Lang.RUS.value: {
        "start":            "Пожалуйста, введи свой ник из игры.",

        "start_again":      "Пользователь с таким именем не найден.\n"
                            "Пожалуйста, введи свой ник из игры.",
        
        "lang":             "Выбери язык: Eng / Rus",
        
        "lang_again":       "Прости, но я не могу распознать такой мусор!\n"
                            "Выбери язык: Eng / Rus",
        
        "fork":             "Привет, я @GrandHashBot!\n"
                            "Кажется, ты очень сообразительный игрок, раз добрался сюда!\n"
                            "Я распознаю некоторые команды, в роде /help, /exit, /quit, /runaway, /getout и др.\n"
                            "Пиши мне в любое время, когда захочешь, не стесняйся!",
        
        "thanks":           "О, не за что меня благодарить!\n"
                            "Вообще, по большому счёту, я довольно бесполезен. Наверное...",
        
        "offensive":        "А ты знаешь, что я тоже ругаться могу?\n"
                            "Только не буду. Потому что я мудрее тебя и знаю больше.\n"
                            "Да и вообще, я просто лучше.",
        
        "question":         "Это что, вопрос?\n"
                            "Жаль что мне лень над ним думать.\n"
                            "Может, загуглишь?",
        
        "greeting":         "Здравствуй! Скажи же, здорово быть приветливым? :)",
        
        "bye":              "Пока! Возвращайся, а то мне скучно :(",
        
        "secret_found":     "Ок, кажется, ты шаришь...\n"
                            "Пиши /info, /talk или /random, чтобы узнать забавные факты о разработке игры.",

        "strange_content":  "ОГО, кажется, ты шаришь в высоких технологиях!\n"
                            "Сколько времени требуется, чтобы научиться отправлять медиафайлы?\n"
                            "(Я в любом случае не буду парсить этот мусор...)",

        "trash":            "ПОЖАЛУЙСТА, не кидай мне больше этот спам!",
        },
    Lang.ENG.value: {
        "start":            "Enter your username, please.",

        "start_again":      "User with this name was not found.\n"
                            "Enter your username, please.",
        
        "lang":             "Choose language: Eng / Rus",
        
        "lang_again":       "Sorry, I can't parse this garbage!\n"
                            "Choose language: Eng / Rus",
        
        "fork":             "Hi, I'm @GrandHashBot!\n"
                            "You seem to be a smart player coz you're here!\n"
                            "I know some commands like /help, /exit, /quit, /runaway, /getout and others.\n"
                            "Don't hesitate to talk to me any time you want!",
        
        "thanks":           "Ah, no problem!\n"
                            "Well, actually I'm rather useless. Probably...",
        
        "offensive":        "Did you know I can swear too?\n"
                            "But I don't wanna to. Coz I'm wiser and smarter than you.\n"
                            "At last, I'm simply better.",
        
        "question":         "What? A question?\n"
                            "Well, it's a pity that I'm too lazy to think about it.\n"
                            "Maybe, google?",
        
        "greeting":         "Hello, nice to meet you! It's just so cool to be friendly, isn't it? :)",
        
        "bye":              "Bye! Please, come back coz I'm bored :(",
        
        "secret_found":     "Well, you got it...\n"
                            "Use /info, /talk or /random to get some facts about game development.",

        "strange_content":  "WOW, it seems you're in touch with high technologies!\n"
                            "How long it takes to get used to sending media?\n"
                            "(I won't parse this trash anyway...)",

        "trash":            "Oh, PLEASE, just avoid sending this trash to me anymore!",
        },
    }


facts_dict = {
    Lang.RUS.value: ["3-ий уровень - самый толстый (1200+ строк кода!)",

                     "Как ни странно, 11-ый уровень создавался в последнюю очередь: свёртка гауссовым ядром - наше всё!",

                     "Проект с игрой компилируется больше минуты!",

                     "Перед релизом игра прошла двойное независимое альфа- и бета-тестирование.\n"
                     "Загляни в Credits, чтобы узнать, кто в этом виноват :)",

                     "Изначально игру планировалось писать на Haskell.\n"
                     "Если ты не шаришь, кто это, можешь купить себе тортик и отпраздновать это с друзьями.\n"
                     "(Они же тоже не знают?)",

                     "Игру на графах на 9-ом уровне авторы изобрели сами.\n"
                     "Её общее решение им неизвестно, и для реализации ИИ была написана многопоточная программа.\n"
                     "Она перебирает всю игру и работает за приемлемое время для деревьев на не более чем 16 вершинах.\n"
                     "Возможно, в общем случае эта задача NP-полна...",

                     "На самом деле Жора на 9-ом уровне уже просчитал всю игру заранее и лишь делает вид, что думает :)\n"
                     "Название уровня предупреждает: одна ошибка может стоить вам звезды!",

                     "Запустить игру удалось уже на второй день разработки! Хоть там и было очень пусто...\n"
                     "Чудеса инкрементного проектирования!",

                     "Самый неприятный (буквально!) баг возник при реализации паузы.\n"
                     "При возврате фокуса после его потери игра пыталась одновременно возобновить и приостановить музыку.\n"
                     "И ей это удавалось.",

                     "Самый длительный по исправлению баг был связан с dynamic_cast в C++.\n"
                     "В какой-то момент (спустя 2 дня поисков бага) вдруг показалось, что проблема заключается в операторе return...\n"
                     "Баг тут же исправился.",

                     "Сколько различных эффектов Paint.NET вы сможете найти во всей игре?",

                     "Внимательно изучите экран Credits: сколько реальных людей там упомянуто?",

                     "На этапе загрузки игры стоит специальный таймер, из-за которого вы наблюдаете этот процесс не менее 10 секунд.\n"
                     "Так вы сможете прочитать больше мемных фраз из тех, что мы для вас приготовили!",

                     "3, 10, 42 - самые главные числа в игре. Запомни!",

                     "А вы уже открыли все достижения?\n"
                     "Когда кажется, что цель игры достигнута, непременно возникает новая...",

                     "Вам лучше не знать, какими хаками игра растягивается в fullscreen! Ой...",

                     "Этой игре лишь не хватает монетизации, вебки и рекламы.\n"
                     "Но не торопитесь забрасывать игру - оставайтесь с нами!",

                     "Некоторые ачивки кажутся очевидными, некоторые - вдохновляют, когда открываются, но другие...\n"
                     "Если вы застряли и что-то оказывается для вас невозможным - просто напишите авторам игры!",
                     ],
    Lang.ENG.value: ["Level 3 is the most \"fat\" (1200+ code lines!)",

                     "Suddenly, level 11 was the last to be done: convolution with Gauss kernel - we love you!",

                     "It takes more than a minute to compile the game project!",

                     "The game passed through double independent alpha- and beta-testing before being released.\n"
                     "Visit Credits page to see whose fault it is :)",

                     "Initially it was decided to code the game on Haskell.\n"
                     "If you've never heard of it, just go and buy a cake for a party with friends.\n"
                     "(They don't know about it too, right?)",

                     "The game concept on level 9 was created by game authors.\n"
                     "They don't know the general solution for this problem, so they wrote a multithreaded program for AI.\n"
                     "It brute-forces all positions and works in satisfying time for trees on less than 16 vertices.\n"
                     "Probably, this problem is NP-complete in general case...",

                     "Actually, George on level 9 has already brute-forced all the positions and just acts like he's thinking :)\n"
                     "The level's title warns you: one miss may cost you a star!",

                     "We managed to run the game on the second day! Even though it was so empty...\n"
                     "The miracle of incremental design!",

                     "The most disagreeable (literally!) bug emerged while implementing the pause.\n"
                     "Every time the game got the focus back, it tried to resume and stop playing the music simultaneously.\n"
                     "And it always managed to.",

                     "The longest bug (in time to fix it) was caused by dynamic_cast in C++.\n"
                     "2 days of bug search later, it seemed to be the \"return\" operator to be the problem...\n"
                     "The bug fixed itself instantly.",

                     "How many different Paint.NET effects can you find in the game?",

                     "Explore the Credits page attentively: how many different real people are mentioned there?",

                     "There is a special timer on loading stage which makes you wait for at least 10 seconds.\n"
                     "Thus you can read more funny phrases we've prepared for you!",

                     "3, 10, 42 - these are the most important numbers in the game. Remember!",

                     "Have you unlocked all the achievements?\n"
                     "As you get to know you're done with the game, another target emerges...",

                     "You better not know by which hackes stretch the game in fullscreen mode! Oops...",

                     "The only missing things in the game are monetization, webcam and ads.\n"
                     "But don't drop the game - stay tuned!",

                     "Some achievements seem evident to get, some can inspire you when unlocked, but others...\n"
                     "If you're stuck and smth seems to be impossible for you, just contact the game authors!",
                     ],
    }


secret_pass = {
    Lang.RUS.value: "каждому хакеру очень нужна своя звезда",
    Lang.ENG.value: "every hacker needs his own star",
    }


key_phrases = {
    Lang.RUS.value: {
        "каждому":  "Я всего лишь бот, и КАЖДОМУ из нас можно позавидовать :)",
        "хакеру":   "Я всего лишь бот, но такому ХАКЕРУ, как ты, я бы даже две звезды отдал!",
        "очень":    "Я всего лишь бот, но если ОЧЕНЬ захотеть, то я могу и другом стать :)",
        "нужна":    "Я всего лишь бот, но даже мне иногда НУЖНА моральная поддержка друзей...",
        "своя":     "Я всего лишь бот, но даже я очень хочу, чтобы у меня была СВОЯ звезда...",
        "звезда":   "Я всего лишь бот, но я верю, что и моя ЗВЕЗДА взойдёт однажды.",
        },
    Lang.ENG.value: {
        "every":    "I'm just a bot, but I'd like to repeat EVERY moment from my past.",
        "hacker":   "I'm just a bot, but you're such a phenomenal HACKER so that I'd give you even 2 stars if I had any :)",
        "needs":    "I'm just a bot, but even such a piece of metal NEEDS friends sometimes...",
        "his":      "I'm just a bot, and every bot knows HIS weak places, you know :)",
        "own":      "I'm just a bot, but I'd like to have my OWN star...",
        "star":     "I'm just a bot, but I believe in my STAR to arise one day!",
        },
    }


def reEscapeString(string):
    specials = r"&*!.)_($+-'/"
    return ''.join(("\\" if c in specials else "") + c for c in string)

swearMatch = ""
with open("Swears.txt", 'r', encoding='utf-8') as fin:
    for line in fin:
        line = reEscapeString(line.strip())
        swearMatch += rf"^(.* )?{line}( .*)?$|"
    swearMatch = swearMatch[:-1]

regexps = {
    Lang.RUS.value: {
        "lang_rus":     r"^(рус?(ский)?)( язык?)?$|"
                        r"^на русс?(ком|кий)( языке?)?$|"
                        r"^п(о|а)-?русс?ки$",

        "lang_eng":     r"^(англ(ийский)?)( язык?)?$"
                        r"^на англ(е|ий?ском|ий?сккий)( языке?)?$|"
                        r"^п(о|а)-?англий?ски$",

        "offensive":    swearMatch,

        "question":     r"^.*\?$|"
                        r"^((а|но|и|или) )?((о(бо?)?|во?|со?|над?|под?|перед|за|через|про|у|мимо|рядом с|около|внутр(ь|и)|ко?|для|близ) )?(что|кто|чего|кого|чему|кому|чем|кем|чем|зачем|почем|как|котор|где|когда|можно).*?$",

        "thanks":       r"^спс|сяп(ки)?|с?пасибо( тебе| вам)?|сенк(с| ю)|благодар(ю|ствую)|дякую( тоби| вам)?$",

        "greeting":     r"^прив(ет(ики?)?|ки)?|здорово|здрав?ствуй(те)?|дороу|дратути|добр(ый день|ое утро|ый вечер(ок|очек)?)|хай|хелл?оу?|салют$",

        "bye":          r"^(доброй|спокойной) ночи|пока|поке(да|дов(а|о))|прощай(те)?|(сладких|добрых) снов|до ?(свид(ания|анн?я|ос|ули)|встречи?|связи|завтра)$",
        },
    Lang.ENG.value: {
        "lang_rus":     r"^(rus?(sian)?)( lang(uage)?)?$",

        "lang_eng":     r"^(eng?(lish)?)( lang(uage)?)?$",

        "offensive":    swearMatch,

        "question":     r"^.*\?$|"
                        r"^(what|when|who|why|where|whom|which|whose|how|is|are|am|have|has|do|does|can|could|shall|should|will|would)\b.*?$",

        "thanks":       r"^thx|thank (you|u)|thanks$",

        "greeting":     r"^hi|hey|hello|greetin(gs?)?|good (evening|morning|day|night|afternoon|noon)|salut|nice to meet (u|you)$",

        "bye":          r"^(good ?)?bye$",
        },
    }


def is_lang_rus(text):
    for lang in Lang:
        if re.match(re.compile(regexps[lang.value]["lang_rus"], re.I), text) is not None:
            return True
    return False

def is_lang_eng(text):
    for lang in Lang:
        if re.match(re.compile(regexps[lang.value]["lang_eng"], re.I), text) is not None:
            return True
    return False

def is_offensive(text):
    for lang in Lang:
        if re.match(re.compile(regexps[lang.value]["offensive"], re.I), text) is not None:
            return True
    return False

def is_question(text):
    for lang in Lang:
        if re.match(re.compile(regexps[lang.value]["question"], re.I), text) is not None:
            return True
    return False

def is_thanks(text):
    for lang in Lang:
        if re.match(re.compile(regexps[lang.value]["thanks"], re.I), text) is not None:
            return True
    return False

def is_greeting(text):
    for lang in Lang:
        if re.match(re.compile(regexps[lang.value]["greeting"], re.I), text) is not None:
            return True
    return False

def is_bye(text):
    for lang in Lang:
        if re.match(re.compile(regexps[lang.value]["bye"], re.I), text) is not None:
            return True
    return False

def is_word_in(text, word):
    return re.match(re.compile(fr"^(.* )?{word}( .*)?$", re.I), text) is not None

