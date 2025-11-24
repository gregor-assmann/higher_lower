# Otto Higher Lower Game

### Spielen

Spielen mit VPN auf: 
[higherlower.ov.otto.de](https://higherlower.ov.otto.de)


#### Aktuelles Docker Image:

```console
docker pull gregyr7/higherlower:latest
```

Oder in einer `docker-compose.yaml`
```yaml
# /higherlower/docker-compose.yaml

services:
    higherlower:
        mem_limit: 3221225472
        image: gregyr7/higherlower:latest
        ports:
          - "8000:8000"
```
Und dann einfach `docker compose up` um zu starten


#### Datenbank
Benötigt Link und Passwort
