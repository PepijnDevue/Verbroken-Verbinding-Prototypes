# Verbroken-Verbinding-Test — Hostvereisten en uitvoerinstructies

Deze repository draait een Streamlit-app in een GPU-geactiveerde Docker-container. Deze README beschrijft welke software op de host nodig is en geeft korte instructies om de host voor te bereiden zodat de container toegang heeft tot NVIDIA GPU's.

## Kort overzicht

- Host OS: Linux (aanbevolen: Ubuntu/Debian). Andere Linux-distributies werken vaak ook, maar pakketnamen en installatie-stappen kunnen verschillen.
- Docker Engine: recente Docker (>= 19.03) met ondersteuning voor `--gpus`; Compose-plugin v2 of `docker-compose` >= 1.28 wordt aanbevolen voor `device_requests` in compose-bestanden.
- NVIDIA-driver: een recente NVIDIA-driver die bij je GPU past (geïnstalleerd op de host, niet in de container).
- nvidia-container-toolkit (of nvidia-docker2): vereist zodat Docker GPU's aan containers kan blootstellen.

## Minimale hostvereisten

- GPU-geschikte hardware met een ondersteunde NVIDIA GPU.
- NVIDIA-driver geïnstalleerd op de host (drivers moeten compatibel zijn met de CUDA-versie in het containerimage).
- Docker Engine geïnstalleerd en werkend (docker-daemon draait). Test met `docker version`.
- Docker Compose v2 (de Docker CLI-plugin) of een `docker-compose`-binary die `device_requests` ondersteunt.

## Aanbevolen versies

- Docker Engine: >= 19.03 (bij voorkeur de laatste stabiele release)
- Docker Compose: Docker Compose V2 (gebruik `docker compose`) of `docker-compose` >= 1.28+ als je de legacy-binary gebruikt
- NVIDIA-driver: de laatste stabiele driver voor je GPU (of in ieder geval compatibel met CUDA 11.8 dat door het image wordt gebruikt)
- nvidia-container-toolkit: de laatste stabiele versie voor je distributie

## Installatiestappen (Ubuntu/Debian voorbeeld)

Hieronder voorbeeldcommando's voor Ubuntu/Debian om de NVIDIA container toolkit te installeren. Pas aan voor jouw distributie en gewenste versies.

1. Installeer Docker Engine (volg de officiële Docker-documentatie). Controleer daarna met:

```bash
docker --version
docker run --rm hello-world
```

2. Installeer de NVIDIA-drivers op de host (buiten Docker). Controleer met `nvidia-smi`.

3. Installeer de NVIDIA container toolkit (voorbeeld):

```bash
# Voeg de NVIDIA pakket-repo toe (voorbeeld, uitvoeren als root)
distribution=$(.
  /etc/os-release;
  echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list |
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

Opmerking: bovenstaande stappen zijn een voorbeeld. Volg altijd de officiële NVIDIA instructies voor jouw OS: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

## Controleren of Docker GPU-toegang heeft

Na installatie van de toolkit en het herstarten van Docker kun je GPU-toegang verifiëren door een CUDA-container te draaien:

```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 nvidia-smi
```

Je zou output van `nvidia-smi` moeten zien met de lijst van GPU's. Als dit faalt, is de container-engine niet correct geconfigureerd om GPU's bloot te stellen.

## De Streamlit-app draaien

Vanuit de projectmap (waar `docker-compose.yml` en `Dockerfile` staan):

Aangeraden (Compose V2):

```bash
docker compose up --build
```

Legacy `docker-compose` (als `device_requests` niet ondersteund wordt, bouw en draai dan met `--gpus`):

```bash
docker-compose up --build
# of
docker build -t my-streamlit-app .
docker run --gpus all -p 8501:8501 --rm my-streamlit-app
```

Open vervolgens http://localhost:8501 in je browser.

## Problemen oplossen

- `permission denied` bij docker: zorg dat je gebruiker in de `docker`-groep zit of gebruik `sudo`.
- `nvidia-smi` niet gevonden / geen GPU's in container: controleer of de NVIDIA-drivers op de host geïnstalleerd zijn en of `nvidia-container-toolkit` aanwezig is; herstart Docker en voer de verificatiestap opnieuw uit.
- `device_requests` niet herkend in Compose: update naar een nieuwere Docker Compose (plugin) of gebruik `docker run --gpus all`.
- Als de host GPU's ziet maar de container niet: controleer of je Docker-daemon herstart is na installatie van de toolkit.

## Opmerkingen en beveiliging

- Dit project mount de werkmap in de container (bind mount). Dat is handig voor ontwikkeling maar wees voorzichtig in productie.
- De `Dockerfile` gebruikt een NVIDIA CUDA base image; zorg dat de driver, container-CUDA-versie en je GPU compatibel zijn.

---
Gemaakt: automatisch — bevat host-prerequisites en verificatiestappen om GPU-toegang voor dit project werkend te krijgen.
