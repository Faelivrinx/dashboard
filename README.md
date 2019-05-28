# dashboard

Projekt do analizy znaków di i tri gramów. Umożliwia obejrzenie statystyk z wczytanych plików, wprowadzenie własnego tekstu oraz wczytanie pliku txt.

## Wymagania:
- Python 3.6!

## Instalacja (docker):
Wymagany jest oczywiście zainstalowany Docker.

### Linux/MacOs
```bash
bash < restart.sh
bash < start.sh
```
### Windows (git bash)
```bash
sh restart.sh
sh start.sh
```
Po uruchomieniu powyższych skryptów uruchomiony zostanie kontener dockera lokalnie na porcie 8050. Ważne, aby był on dostępny :)
W razie problemów można zmienić w pliku _start.sh_

## Instalacja (basic python)

Jeśli nie mamy zainstalowanego dockera, ale mamy wersję Pythona 3.6 możemy bez problemowo uruchomić za jego pomocą aplikację.
Zostanie uruchomiona także lokalnie na porcie 8050.

```bash
pip install -r requirements.txt
python app.py
```

## Uwagi
Gdy wersja Pythona jest różna od 3.6 mogą wystąpić problemy z instalacją zależności, prośba o upewnienie się że używana jest wersja 3.6. 

## Autorzy

- Baczyński Konrad
- Bigaj Adam
- Jurasz Dominik
