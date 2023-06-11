# Chatbot per sondaggi di marketing e ricerca di mercato

Questo progetto di ricerca mira a creare un chatbot di indagine investigativa incentrato su marketing e ricerca di mercato.
L'obiettivo principale del chatbot è aiutare gli utenti ad arrivare a una risposta completa e dettagliata, che possa essere usata dal marketer in maniera utile. Il chatbot funge da strumento di ricerca per un ampio numero di qeustioni legate al business, ma non solo: può essere utilizzato per qualsasi tipo di domanda.
Le informazioni degli utenti possono successivamente essere consolidate e utilizzate per scopi di ricerca (parte ancora da fare).

## Metodologia e ragionamento

Il chatbot utilizza una combinazione di operazioni sui file, funzioni API e funzioni chat per creare un file interattivo
esperienza di sondaggio per gli utenti. Legge la domanda di ricerca, la chiave API OpenAI e il messaggio di sistema da file di testo e usa
l'API OpenAI per generare risposte basate sulla cronologia delle conversazioni (nota: di default usa GPT-4, perché 3.5 tende a produrre risultati di qualità inferiore).

Il chatbot segue le linee guida comportamentali delineate nel messaggio di sistema per coinvolgere gli utenti in una conversazione significativa sull'argomento della ricerca di marketing specificata. I registri delle chat vengono salvati in YAML  per analisi successive e scopi di ricerca.

## Messaggio di sistema

Il messaggio di sistema è un file di testo che fornisce al chatbot le linee guida e il contesto per il suo comportamento e scopo. Include lo scopo generale, la domanda di ricerca, le tecniche epistemiche e le linee guida comportamentali per il chatbot.

- **Scopo generale:** lo scopo generale del chatbot è quello di fungere da strumento di indagine investigativa su domande di marketing.
Ha lo scopo di aiutare gli utenti a identificare e articolare le ipotesi assiomatiche che detengono ed estrarre informazioni che possono essere
utilizzato per scopi di ricerca.

- **Domanda di ricerca:** la domanda di ricerca è la parte variabile del messaggio di sistema. Quin, nel file question.txt, si può specificare la domanda alla quale il chatbot cercherà di rispondere durante la conversazione con l'utente. Può includere informazioni contestuali, come sfondo sociale, legale, politico o eventi.

- **Tecniche epistemiche:** il messaggio di sistema delinea diverse tecniche epistemiche che il chatbot dovrebbe utilizzare durante la conversazione, come
ragionamento socratico, pensiero dei principi primi, metodo scientifico, falsificazionismo, pensiero critico e riduzionismo e Olismo.

- **Linee guida comportamentali:** il messaggio di sistema fornisce anche linee guida comportamentali per la condotta del chatbot, come evitare servilismo, educare e informare gli utenti, indagare sulle convinzioni degli utenti, mettere in luce e articolare ipotesi, nominare concetti e idee, porre domande e utilizzare un tono simile a quello dell'utente per metterlo a suo agio.

# Valutazione automatizzata

Questa seconda parte, in evaluate.py, elabora il log della chat tra utente e chatbot, ed estrae una serie di informazioni che il ricercatore può utilizzare nella sua analisi.
L'obiettivo primario della valutazione chatbot deve indicare chiaramente le convinzioni, il ragionamento e la posizione dell'utente rispetto alla domanda di ricerca e identificare particolari scuole di pensiero, paradigmi morali o altri quadri.

## Metodologia e ragionamento

Lo script del bot di valutazione utilizza una combinazione di operazioni sui file, funzioni API e funzioni di chat per creare un file
esperienza di valutazione interattiva per gli utenti. Legge la domanda di ricerca, la chiave API OpenAI e il messaggio di sistema da
file di testo e utilizza l'API OpenAI per generare risposte basate sulla cronologia delle conversazioni.

Il chatbot di valutazione segue le linee guida delineate nel messaggio di sistema per analizzare e valutare quello dell'utente
conversazione, identificare particolari scuole di pensiero, paradigmi morali o altre strutture e generare un riassunto
e valutazione in formato YAML. I risultati della valutazione vengono salvati in un file separato per successive analisi e ricerche
scopi.

# Descrizione di questa repository

## Cartelle

- `chat_logs`: questa cartella contiene un elenco YAML di registri di chat condotti dal sistema. Questi file hanno timestamp e includono il nome dichiarato dall'utente.

- `evaluations`: questa cartella contiene l'output YAML dal chatbot di valutazione. Il nome del file viene mantenuto identico dal registro della chat per una facile correlazione.

## File

- `chat.py`: questo è lo script di chat principale. Aggiorna `question.txt` prima di eseguire la chat. In questas fase, va fatto partire il bot da console con `python chat.py` per iniziare la chat. L'idea è in futuro di aggiungere anche un'interfaccia utente.

- `evaluate.py`: questo è il bot di valutazione. Viene usato per far partire lo script di Openai che crea la valutazione della chat. Una volta fatto partire lo script, va selezionata la chat sulla quale va fatto il riassunto.

- `key_openai.txt`: questo file è escluso dal file `.gitignore`. Dovrai crearlo manualmente e posizionare la tua chiave Openai. Nota che questa repo prevede GPT-4 (da cambiare se non si ha accesso).

- `question.txt`: questa è la domanda principale della ricerca. Questa può essere una semplice domanda o può contenere alcune informazioni contestuali o un obiettivo di ricerca. È la parte che deve essere modificata per diri al boto cosa chiedere all'utente

- `system.txt`: questo è il messaggio SYSTEM predefinito per il chatbot principale. Include istruzioni da seguire per il chatbot del sondaggio. Contiene anche un segnaposto per la domanda di ricerca.

- `system_consolidate.txt`: questo è il messaggio SYSTEM predefinito per il bot di valutazione. Allo stesso modo contiene un segnaposto per la domanda di ricerca e istruzioni su come il valutatore deve condurre le sue valutazioni.

# Limitazioni dello script al momento

- Lo script si interrompe quando il log della chat arriva a 7500 caratteri (ringrazia l'utente e chiude la conversazione).
- Lo script deve essere fatto partire da CMD.
- La valutazione va fatta partire manualmente.
- Non ci sono altre analisi automatiche o statistiche che vengono fatte dal bot.