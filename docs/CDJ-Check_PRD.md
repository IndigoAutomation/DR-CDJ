# CDJ-Check — Product Requirements Document

**Audio Compatibility Checker & Converter per Pioneer CDJ-2000 Nexus**

| Campo | Dettaglio |
|---|---|
| **Versione documento** | 1.0 |
| **Data** | 28 Febbraio 2026 |
| **Stato** | Draft — In revisione |
| **Target hardware** | Pioneer CDJ-2000 Nexus (1ª generazione) |
| **Classificazione** | Confidenziale |

---

## 1. Panoramica Prodotto

### 1.1 Obiettivo

CDJ-Check è un tool desktop leggero che permette ai DJ di verificare istantaneamente se i propri file audio sono compatibili con il Pioneer CDJ-2000 Nexus e, in caso contrario, di convertirli automaticamente nel formato di massima qualità supportato dal player.

### 1.2 Problema

Il Pioneer CDJ-2000 Nexus è uno standard industriale nei club e nei festival, ma supporta un insieme limitato e specifico di formati audio. I DJ si trovano regolarmente ad affrontare:

- Tracce in formati non supportati (OGG, OPUS, FLAC, WMA) che non vengono lette dal CDJ.
- File WAV/AIFF con sample rate non standard (96 kHz, 192 kHz) che causano errori di lettura.
- Conversioni con tool generici che downsamplano inutilmente a 16-bit/44.1 kHz, perdendo qualità quando il CDJ supporta 24-bit/48 kHz.
- Nessun modo rapido per validare un'intera libreria musicale prima di una serata.

### 1.3 Proposta di Valore

CDJ-Check elimina completamente il rischio di incompatibilità con un workflow drag-and-drop: trascini, verifichi, converti. Zero configurazione, zero competenze tecniche richieste, zero perdita di qualità non necessaria.

> 🎯 **Vision:** il DJ non deve mai più chiedersi "questo file funzionerà sul CDJ?". CDJ-Check risponde in millisecondi e risolve in secondi.

### 1.4 Target Users

- **DJ professionisti** che suonano su impianti Pioneer in club e festival.
- **DJ resident** che gestiscono librerie musicali ampie e variegate.
- **Producer/DJ** che lavorano con formati ad alta risoluzione (FLAC 24-bit, WAV 96 kHz) e devono esportare versioni CDJ-ready.
- **Agenzie e service audio** che preparano chiavette USB per eventi.

---

## 2. Specifiche di Riferimento: CDJ-2000 Nexus

Formati audio supportati dal Pioneer CDJ-2000 Nexus (1ª generazione NXS, firmware più recente):

| Formato | Bit Depth | Sample Rate | Bitrate / Note |
|---|---|---|---|
| MP3 | N/A | 44.1 kHz | 32–320 kbps (CBR e VBR) |
| AAC (M4A) | N/A | 44.1 / 48 kHz | 16–320 kbps |
| WAV (PCM) | 16 / 24-bit | 44.1 / 48 kHz | Non compresso |
| AIFF (PCM) | 16 / 24-bit | 44.1 / 48 kHz | Non compresso |

> ⚠️ **ATTENZIONE:** il CDJ-2000 Nexus (1ª gen.) **NON supporta FLAC**. Il supporto FLAC è stato introdotto solo con il CDJ-2000 NXS2. Questo è un errore molto comune tra i DJ.

### 2.1 Formati NON Supportati (conversione necessaria)

| Formato | Motivo di Incompatibilità |
|---|---|
| FLAC | Non supportato dalla 1ª generazione NXS |
| OGG Vorbis | Codec non riconosciuto dal firmware |
| OPUS | Codec non riconosciuto dal firmware |
| WMA | Formato Microsoft, non supportato |
| ALAC (Apple Lossless) | Non supportato dal CDJ-2000 NXS |
| WAV/AIFF 32-bit float | Bit depth non supportata |
| WAV/AIFF > 48 kHz | Sample rate troppo alto (es. 96/192 kHz) |

---

## 3. User Stories

### US-01: Verifica rapida di un singolo file

*Come DJ che ha scaricato una nuova traccia, voglio **trascinarla nella finestra del tool** per **sapere immediatamente se è compatibile** con il mio CDJ-2000 NXS.*

**Criterio di accettazione:** il verdetto appare in meno di 300 ms dal drop, con indicatore colorato e dettagli del formato.

---

### US-02: Conversione senza perdita di qualità

*Come producer che lavora in FLAC 24-bit/96 kHz, voglio **convertire le mie tracce per il CDJ** senza che vengano **downsamplate a 16-bit/44.1 kHz** quando il CDJ supporta 24-bit/48 kHz.*

**Criterio di accettazione:** il file FLAC 24-bit/96 kHz viene convertito in 16-bit/44.1 kHz 

---

### US-03: Preparazione batch per una serata

*Come DJ che sta preparando una USB per una serata, voglio **trascinare un'intera cartella** e **convertire automaticamente tutte le tracce non compatibili** in un colpo solo.*

**Criterio di accettazione:** il batch processing analizza e converte tutti i file con progress bar, salvando i risultati in una cartella `CDJ_Ready`.

---

### US-04: Avviso per sorgenti lossy

*Come DJ che ha ricevuto tracce in formato OGG, voglio **essere avvisato che la conversione a WAV non migliora la qualità effettiva** ma garantisce solo la compatibilità.*

**Criterio di accettazione:** per file sorgente lossy, il tool mostra un avviso inline (non modale) spiegando che la qualità originale non può essere recuperata.

---

### US-05: Nessun impatto sulle performance del PC

*Come DJ che lavora con Rekordbox/Ableton aperti, voglio che **CDJ-Check non rallenti il mio sistema** durante l'analisi e la conversione.*

**Criterio di accettazione:** RAM idle < 50 MB, CPU durante conversione configurabile (1–4 thread), nessun freeze dell'interfaccia.

---

## 4. Requisiti Funzionali

### 4.1 Analisi Audio (FR-100)

| ID | Requisito | Priorità |
|---|---|---|
| FR-101 | Il sistema deve estrarre codec, sample rate, bit depth, bitrate e durata da qualsiasi file audio tramite ffprobe | Must |
| FR-102 | Il tempo di analisi per singolo file deve essere inferiore a 200 ms | Must |
| FR-103 | Il sistema deve gestire file corrotti o troncati senza crash, mostrando un errore chiaro | Must |
| FR-104 | Il sistema deve riconoscere almeno: MP3, AAC, WAV, AIFF, FLAC, OGG, OPUS, WMA, ALAC | Must |
| FR-105 | Il sistema deve identificare WAV/AIFF con bit depth float (32-bit float) come non compatibili | Should |

### 4.2 Motore di Compatibilità (FR-200)

| ID | Requisito | Priorità |
|---|---|---|
| FR-201 | Il sistema deve confrontare i metadati di ogni file con la tabella di compatibilità CDJ-2000 NXS | Must |
| FR-202 | Il verdetto deve essere uno tra: ✅ Compatibile, ⚠️ Convertibile (lossless), 🟡 Convertibile (con perdita) | Must |
| FR-203 | Per ogni file non compatibile, il sistema deve proporre il formato target ottimale (massima qualità supportata) | Must |
| FR-204 | La tabella di compatibilità deve essere definita in un file JSON esterno, modificabile senza ricompilare | Should |
| FR-205 | Il sistema deve supportare profili multipli (CDJ-2000 NXS, NXS2, CDJ-3000, ecc.) selezionabili dall'utente | Could |

### 4.3 Conversione Audio (FR-300)

| ID | Requisito | Priorità |
|---|---|---|
| FR-301 | La conversione deve preservare la massima qualità compatibile (es. 24-bit se il CDJ lo supporta, non downsample a 16-bit) | Must |
| FR-302 | La conversione deve essere eseguita tramite FFmpeg via subprocess, senza processare il flusso audio in Python | Must |
| FR-303 | Il sistema deve supportare conversione batch con parallelismo configurabile (1–4 thread) | Must |
| FR-304 | I file convertiti devono essere salvati in una sottocartella `CDJ_Ready` nella directory originale | Must |
| FR-305 | Il sistema deve mostrare una progress bar con stima del tempo rimanente durante la conversione | Should |
| FR-306 | Il sistema deve preservare i tag ID3/metadata durante la conversione quando possibile | Should |

### 4.4 Logica di Conversione Ottimale (FR-300 — Dettaglio)

| Formato Sorgente | Azione | Formato Target |
|---|---|---|
| WAV 24-bit / 48 kHz | Nessuna conversione | Già compatibile |
| WAV 24-bit / 96 kHz | Resample a 48 kHz | WAV 24-bit / 48 kHz |
| WAV 32-bit float | Converti bit depth + resample | WAV 24-bit / 48 kHz |
| FLAC 24-bit / 48 kHz | Decode e re-wrap | WAV 24-bit / 48 kHz |
| FLAC 16-bit / 44.1 kHz | Decode e re-wrap | WAV 16-bit / 44.1 kHz |
| OGG / OPUS / WMA | Transcode (lossy) | WAV 16-bit / 44.1 kHz* |
| MP3 320 kbps / 44.1 kHz | Nessuna conversione | Già compatibile |
| AIFF 24-bit / 96 kHz | Resample a 48 kHz | AIFF 24-bit / 48 kHz |
| ALAC 24-bit / 48 kHz | Decode e re-wrap | WAV 24-bit / 48 kHz |

*\* Per formati lossy sorgente, il tool avvisa che la conversione a WAV non migliora la qualità effettiva ma garantisce la compatibilità.*

### 4.5 Interfaccia Utente (FR-400)

| ID | Requisito | Priorità |
|---|---|---|
| FR-401 | La finestra principale deve supportare drag-and-drop di file e cartelle | Must |
| FR-402 | La drop zone deve dare feedback visivo (highlight) al passaggio del mouse con file | Must |
| FR-403 | La lista file deve mostrare: nome, formato, sample rate, bit depth, stato (icona colorata), azione proposta | Must |
| FR-404 | Il pulsante "Converti Non Compatibili" deve attivarsi solo quando ci sono file da convertire | Must |
| FR-405 | Gli avvisi (es. lossy source) devono essere inline nella lista, non popup modali | Should |
| FR-406 | L'interfaccia deve usare dark mode come default, coerente con l'estetica dei software DJ | Should |
| FR-407 | Deve essere disponibile anche un file picker classico come alternativa al drag-and-drop | Should |

---

## 5. Requisiti Non Funzionali

| Requisito | Target | Metrica |
|---|---|---|
| Tempo di analisi per file | < 200 ms | Misurato con ffprobe su file da 10 min |
| Tempo di conversione | < 1.5x durata traccia | WAV 24-bit/48 kHz, file da 5 min |
| Utilizzo RAM (idle) | < 50 MB | App aperta senza file caricati |
| Utilizzo RAM (batch 50 file) | < 150 MB | 50 tracce in coda di conversione |
| Utilizzo CPU durante conversione | Configurabile | 1–4 thread FFmpeg (impostabile) |
| Dimensione installer | < 60 MB | Bundle con FFmpeg incluso |
| Avvio applicazione | < 2 secondi | Cold start su HDD meccanico |
| Piattaforme | Windows 10+, macOS 12+, Linux | Test su tutte e tre |

---

## 6. Architettura Tecnica

### 6.1 Raccomandazione: Python + FFmpeg + CustomTkinter

> ✅ **La combinazione Python + FFmpeg + CustomTkinter offre il miglior rapporto tra velocità di sviluppo, leggerezza, qualità della GUI e prestazioni audio.**

Motivazioni:

- **FFmpeg fa il lavoro pesante:** tutto il processing audio (analisi, conversione, resampling) è delegato a FFmpeg via subprocess. Python non processa mai il flusso audio, quindi non grava sulla CPU. FFmpeg è scritto in C ed è il tool più veloce e ottimizzato per queste operazioni.
- **Python è solo l'orchestratore:** il codice Python si limita a leggere i metadati tramite ffprobe (millisecondi), applicare la logica di compatibilità (dict lookup), e lanciare ffmpeg per le conversioni. L'overhead di Python è trascurabile.
- **CustomTkinter per la GUI:** libreria basata su Tkinter con aspetto moderno (dark mode, widget arrotondati, look nativo). Leggerissima rispetto a PyQt/Electron. Supporta drag-and-drop tramite `tkinterdnd2`.
- **Cross-platform:** funziona su Windows, macOS e Linux senza modifiche. Bundle creato con PyInstaller (singolo eseguibile) o Nuitka per performance migliori.

### 6.2 Confronto Architetture Valutate

| Architettura | Pro | Contro | Peso stimato |
|---|---|---|---|
| **Python + FFmpeg + CustomTkinter** ✅ | Sviluppo rapido, FFmpeg gestisce tutto, cross-platform, comunità enorme | GUI Tkinter meno ricca di Qt, richiede bundling Python | ~30–50 MB |
| Python + FFmpeg + PyQt6 | GUI moderna e professionale, ottimo cross-platform | PyQt6 aggiunge peso, licenza GPL/commercial | ~80–120 MB |
| Rust + FFmpeg CLI | Performance nativa, binario singolo, risorse minime | Curva di apprendimento ripida, sviluppo lento, GUI complessa | ~10–20 MB |
| Electron + FFmpeg | UI web moderna, facile da sviluppare | Pesante (Chromium embedded), RAM elevata, antitesi del requisito | ~150–250 MB |
| Go + FFmpeg CLI | Binario singolo, buone performance, cross-compile facile | Ecosistema GUI limitato, meno librerie audio | ~15–25 MB |
| Tauri (Rust + Web) | UI web + backend leggero, binario piccolo | Ecosistema giovane, debugging complesso | ~8–15 MB |

### 6.3 Architettura a Componenti

| Modulo | Responsabilità | Tecnologia |
|---|---|---|
| **AudioAnalyzer** | Estrae metadati dal file audio (codec, sample rate, bit depth, bitrate, durata) tramite ffprobe in formato JSON | `ffprobe` (subprocess) |
| **CompatibilityEngine** | Confronta i metadati con la tabella di compatibilità CDJ-2000 NXS. Restituisce verdetto + piano di conversione ottimale | Python puro (dict lookup) |
| **AudioConverter** | Esegue la conversione con i parametri ottimali. Gestisce la progress bar leggendo stderr di ffmpeg | `ffmpeg` (subprocess) |
| **GUI / Frontend** | Finestra drag-and-drop, lista file con indicatori colorati, pulsante converti, progress bar, report finale | CustomTkinter + tkinterdnd2 |

### 6.4 Flusso Operativo

1. L'utente trascina i file nella finestra (o usa il file picker).
2. `AudioAnalyzer` esegue ffprobe su ciascun file (tempo medio: 50–100 ms per file).
3. `CompatibilityEngine` valuta ogni file e assegna il verdetto con il piano di conversione.
4. La GUI mostra i risultati: verde (compatibile), giallo (convertibile lossless), arancione (convertibile con perdita).
5. L'utente clicca "Converti tutti". `AudioConverter` lancia ffmpeg in parallelo (thread pool) per i file non compatibili.
6. I file convertiti vengono salvati in una sottocartella `CDJ_Ready` nella stessa directory dei file originali.

---

## 7. User Experience e Interfaccia

### 7.1 Principi di Design

- **Zero configurazione iniziale:** il tool deve funzionare out-of-the-box.
- **Feedback visivo immediato:** ogni file mostra il suo stato con un colore e un'icona.
- **Azione in un click:** dopo il drag-and-drop, un solo pulsante per convertire tutto.
- **Dark mode come default:** coerente con l'estetica dei software DJ (Rekordbox, Traktor).
- **Nessun popup invasivo:** gli avvisi (es. lossy source) sono inline, mai modali.

### 7.2 Layout della Finestra

- **Drop Zone (alto):** area grande con bordo tratteggiato e icona. Testo: "Trascina qui le tue tracce". Si illumina al passaggio del mouse con file.
- **File List (centro):** tabella scrollabile con colonne — Nome File, Formato, Sample Rate, Bit Depth, Stato (colore), Azione proposta.
- **Action Bar (basso):** pulsante "Converti Non Compatibili" (attivo solo se ci sono file da convertire), progress bar generale, contatore file processati.

---

## 8. Dipendenze e Distribuzione

| Dipendenza | Versione | Licenza | Ruolo |
|---|---|---|---|
| Python | 3.11+ | PSF | Runtime |
| FFmpeg / ffprobe | 6.x+ | LGPL/GPL | Analisi e conversione audio |
| CustomTkinter | 5.x | MIT | GUI moderna |
| tkinterdnd2 | 0.3+ | MIT | Supporto drag-and-drop nativo |
| PyInstaller / Nuitka | Latest | GPL / Apache | Bundling in eseguibile singolo |

FFmpeg verrà incluso nel bundle dell'applicazione (binario statico). L'utente non dovrà installare nulla separatamente. Il bundle finale sarà un singolo file eseguibile per piattaforma.

---

## 9. Rischi e Mitigazioni

| Rischio | Impatto | Probabilità | Mitigazione |
|---|---|---|---|
| Pioneer aggiorna il firmware e cambia i formati supportati | Medio | Bassa | File di configurazione JSON esterno, aggiornabile senza rilasciare nuova versione |
| File audio corrotti causano crash di FFmpeg | Basso | Media | Timeout su subprocess + gestione errori con fallback e messaggio utente chiaro |
| Performance degradata su librerie molto grandi (1000+ file) | Medio | Media | Analisi parallelizzata con ThreadPool, conversione con coda a priorità |
| Licenza FFmpeg GPL potrebbe complicare distribuzione commerciale | Alto | Bassa | Usare build LGPL di FFmpeg (senza codec GPL) oppure distribuire FFmpeg separatamente |
| Differenze di comportamento tra OS (path, drag-and-drop) | Medio | Media | Test CI/CD su tutte e tre le piattaforme, astrazione del filesystem con pathlib |

---

## 10. Roadmap e Fasi di Sviluppo

| Fase | Durata stimata | Deliverable |
|---|---|---|
| **Fase 1** — Core Engine | 1–2 settimane | AudioAnalyzer + CompatibilityEngine funzionanti da CLI, test suite completa |
| **Fase 2** — Conversione | 1 settimana | AudioConverter con logica di conversione ottimale, test su tutti i formati |
| **Fase 3** — GUI | 1–2 settimane | Interfaccia CustomTkinter completa con drag-and-drop e progress bar |
| **Fase 4** — Bundling & Test | 1 settimana | Eseguibili per Win/Mac/Linux, test end-to-end, fix bug |
| **Fase 5** — Espansioni (opzionale) | Ongoing | Supporto CDJ-3000, CDJ-2000 NXS2, Denon SC6000, profili custom |

---

## 11. Criteri di Successo

| Metrica | Target | Metodo di Misurazione |
|---|---|---|
| Accuratezza del verdetto di compatibilità | 100% | Test su corpus di 50+ file in formati diversi |
| Qualità della conversione | Nessun degrado non necessario | Confronto spettrogramma sorgente/output |
| Soddisfazione utente (dogfooding) | Nessun file rifiutato dal CDJ dopo conversione | Test in condizioni reali su CDJ-2000 NXS |
| Tempo medio analisi (singolo file) | < 200 ms | Benchmark automatizzato |
| Crash rate | 0% su file validi | Test suite + fuzzing con file corrotti |

---

## 12. Espansioni Future

- **Profili per altri player:** CDJ-3000, CDJ-2000 NXS2 (aggiunge FLAC), Denon SC6000 (aggiunge FLAC + ALAC).
- **Integrazione con Rekordbox:** lettura del database XML per analisi automatica della libreria.
- **Analisi audio avanzata:** clipping detection, loudness LUFS, true peak, verifica integrità file.
- **Modalità watch folder:** monitoraggio continuo di una cartella, conversione automatica di nuovi file.
- **Plugin per Rekordbox/Traktor:** integrazione diretta nel workflow del DJ.
- **Cloud sync:** sincronizzazione profili di compatibilità tra più postazioni.

---

*Fine del documento*
