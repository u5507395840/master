#!/bin/sh
# Interactive CLI to build & push Docker image to Docker Hub or dispatch GH Actions
# Works in Alpine devcontainer. Uses $BROWSER to open pages on host.
set -eu
trap 'stty echo' EXIT

cd "$(git rev-parse --show-toplevel 2>/dev/null || echo /workspaces/master)"

info() { printf "\n==> %s\n" "$1"; }
err() { printf "ERROR: %s\n" "$1" >&2; exit 1; }

info "Repo: $(basename "$(pwd)")"
printf "Rama actual: %s\n" "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"

printf "\nElige opción:\n  1) Build & push local (requiere docker/dockerd)\n  2) Dispatch GitHub Actions workflow (build+push on CI)\n  3) Salir\n\nElige [1/2/3]: "
read opt
case "$opt" in
  1)
    # Local path
    if ! command -v docker >/dev/null 2>&1; then
      printf "docker no encontrado en PATH.\n¿Deseas intentar instalar docker (apk) y arrancar dockerd aquí? [y/N]: "
      read yn
      if [ "$yn" != "y" ] && [ "$yn" != "Y" ]; then
        info "Abortando camino local. Elige la opción 2 para usar Actions."
        exit 0
      fi
      if [ "$(id -u)" != "0" ]; then
        err "Se requiere root para instalar/arrancar docker. Ejecuta 'sudo sh cli_deploy.sh' o cambia a root."
      fi
      info "Instalando docker..."
      apk update
      apk add --no-cache docker docker-cli || err "apk install falló"
    fi

    # Start dockerd if needed
    if ! docker info >/dev/null 2>&1; then
      info "Iniciando dockerd en background..."
      dockerd > /tmp/dockerd.log 2>&1 &
      DOCKERD_PID=$!
      i=0
      until docker info >/dev/null 2>&1 || [ $i -ge 30 ]; do
        i=$((i+1)); sleep 1
      done
      if ! docker info >/dev/null 2>&1; then
        printf "dockerd no arrancó. Revisa /tmp/dockerd.log\n"
        tail -n 80 /tmp/dockerd.log || true
        err "No se pudo iniciar dockerd aquí."
      fi
      CREATED_DOCKERD=1
    else
      CREATED_DOCKERD=0
    fi

    # Credentials
    printf "Docker Hub username: "
    read -r DH_USER
    printf "Docker Hub token (se ocultará): "
    stty -echo
    read -r DH_TOKEN
    stty echo
    printf "\n"

    printf "Haciendo login seguro...\n"
    printf '%s' "$DH_TOKEN" | docker login --username "$DH_USER" --password-stdin || err "docker login falló"

    # Build
    GIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo local)
    IMAGE="${DH_USER}/dogma-app:latest"
    IMAGE_SHA="${DH_USER}/dogma-app:${GIT_SHA}"

    info "Construyendo imagen ${IMAGE} desde Dockerfile..."
    docker build -t "$IMAGE" -f Dockerfile . || err "docker build falló"

    info "Etiquetando ${IMAGE_SHA}..."
    docker tag "$IMAGE" "$IMAGE_SHA" || true

    info "Pusheando ${IMAGE}..."
    docker push "$IMAGE" || err "push $IMAGE falló"
    info "Pusheando ${IMAGE_SHA}..."
    docker push "$IMAGE_SHA" || err "push $IMAGE_SHA falló"

    info "Imagenes subidas a Docker Hub."
    printf "Abriendo página de Docker Hub...\n"
    "$BROWSER" "https://hub.docker.com/repository/docker/${DH_USER}/dogma-app" || true

    if [ "${CREATED_DOCKERD:-0}" -eq 1 ]; then
      info "Deteniendo dockerd (PID $DOCKERD_PID)..."
      kill "$DOCKERD_PID" || true
    fi
    ;;

  2)
    # GitHub Actions dispatch
    WORKFLOW=".github/workflows/build-and-push.yml"
    if [ ! -f "$WORKFLOW" ]; then
      printf "%s no existe. ¿Quieres crear el workflow ahora? [y/N]: " "$WORKFLOW"
      read createwf
      if [ "$createwf" = "y" ] || [ "$createwf" = "Y" ]; then
        mkdir -p .github/workflows
        cat > "$WORKFLOW" <<'EOF'
name: Build and Push to Docker Hub
on:
  workflow_dispatch:
  push:
    branches: [ "main" ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: |
            ${{ secrets.DOCKERHUB_USERNAME }}/dogma-app:latest
            ${{ secrets.DOCKERHUB_USERNAME }}/dogma-app:${{ github.sha }}
EOF
        git add "$WORKFLOW"
        git commit -m "ci: add build-and-push workflow" || true
        git push origin "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)" || true
        info "Workflow creado y push realizado (revisa en GitHub)."
      else
        err "Necesitas el workflow en el repo para usar Actions."
      fi
    fi

    printf "Recuerda: DOCKERHUB_USERNAME y DOCKERHUB_TOKEN deben existir en Settings → Secrets.\n"
    printf "¿Deseas despachar el workflow ahora? (requiere GitHub PAT con 'repo' scope) [y/N]: "
    read dispatch
    if [ "$dispatch" != "y" ] && [ "$dispatch" != "Y" ]; then
      info "Dispatch cancelado. Puedes ejecutar desde Actions UI más tarde."
      exit 0
    fi

    printf "Introduce tu GitHub PAT (se ocultará): "
    stty -echo
    read -r GH_TOKEN
    stty echo
    printf "\n"

    REMOTE_URL=$(git config --get remote.origin.url || true)
    if [ -z "$REMOTE_URL" ]; then
      err "No se detectó remote.origin.url. Exporta GITHUB_REPOSITORY=owner/repo o configura origin."
    fi
    if echo "$REMOTE_URL" | grep -qE "^git@"; then
      OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's#git@[^:]+:([^/]+/[^/.]+)(.git)?#\1#')
    else
      OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's#https?://[^/]+/([^/]+/[^/.]+)(.git)?#\1#')
    fi
    if [ -z "$OWNER_REPO" ]; then err "No se pudo parsear OWNER/REPO"; fi

    info "Despachando workflow para ${OWNER_REPO} en la rama $(git rev-parse --abbrev-ref HEAD)..."
    http_code=$(curl -s -o /dev/stderr -w "%{http_code}" -X POST \
      -H "Authorization: token ${GH_TOKEN}" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/repos/${OWNER_REPO}/actions/workflows/build-and-push.yml/dispatches" \
      -d "{\"ref\":\"$(git rev-parse --abbrev-ref HEAD)\"}")

    if [ "$http_code" = "204" ] || [ "$http_code" = "201" ]; then
      info "Workflow despachado. Abriendo Actions page..."
      "$BROWSER" "https://github.com/${OWNER_REPO}/actions/workflows/build-and-push.yml" || true
    else
      err "Dispatch falló (HTTP $http_code). Revisa Actions UI."
    fi
    ;;

  *)
    info "Cancelado."
    exit 0
    ;;
esac

info "Proceso finalizado."