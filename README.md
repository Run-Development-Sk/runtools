# runtools

Pomocné Python skripty pre projekty RunDevelopment. Po inštalácii sú
k dispozícii ako konzolové príkazy:

- `dockerinfo` – prehľad Docker images, kontajnerov, volumes a build cache
- `gitexport` – export zmien z Git repozitára
- `gitmirror` – zrkadlenie Git repozitára do iného repozitára

## Inštalácia

> **Poznámka:** Python 3.12+ na Debian/Ubuntu systémoch blokuje inštaláciu
> balíkov priamo do systémového Pythonu (PEP 668). Pre CLI nástroje odporúčame
> `pipx`, ktorý to rieši automaticky.

### Cez `pipx` (odporúčané)

`pipx` nainštaluje balík do izolovaného virtuálneho prostredia a konzolové
príkazy (`dockerinfo`, `gitexport`, `gitmirror`) sprístupní globálne v `PATH`.

**Inštalácia `pipx`** (ak ho ešte nemáš):

```bash
sudo apt install pipx
pipx ensurepath
```

Po `ensurepath` reštartuj terminál (alebo spusti `source ~/.bashrc`), aby sa
cesta prejavila.

**Inštalácia `runtools`:**

```bash
pipx install "runtools @ git+https://git@github.com/RunDevelopmentSk/runtools.git@main"
```

### Cez `requirements.txt` (devcontainer / venv)

Pridaj do `requirements.txt`:

```text
runtools @ git+https://git@github.com/RunDevelopmentSk/runtools.git@main
```

a nainštaluj s `--break-system-packages` (vhodné v devcontaineri alebo venv):

```bash
pip install -r requirements.txt --break-system-packages
```

### Ručne (núdzovo)

Ak inštalácia nie je možná, tak je úplne postačujúce stiahnúť požadovaný skript z priečinka [https://github.com/RunDevelopmentSk/runtools  > `/src/runtools/`](https://github.com/RunDevelopmentSk/runtools/tree/main/src/runtools) a spúšťať ho ako iné Python skripty, napr.:

```
python3 dockerinfo.py
```

## Aktualizácia

Keďže inštalácia ide vždy z vetvy `main` (bez verzovania), pip/pipx pri
opätovnom spustení nemusí zaznamenať zmenu commit hashu.

### Cez `pipx`

```bash
pipx install --force "runtools @ git+https://git@github.com/RunDevelopmentSk/runtools.git@main"
```

(`pipx upgrade runtools` nie je spoľahlivé pri inštalácii z gitu bez tagov —
preto `--force`.)

### Cez `requirements.txt`

```bash
pip install --upgrade --force-reinstall -r requirements.txt --break-system-packages
```
