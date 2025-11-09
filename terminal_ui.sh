#!/bin/sh
# Minimal terminal-focused CLI UI to manage build-and-push dispatch
# Alpine-compatible, uses only sh, git, curl and "$BROWSER"
set -eu

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$repo_root" ]; then
  echo "ERROR: not inside a git repository."
  exit 1
fi
cd "$repo_root" || exit 1

WORKFLOW_PATH=".github/workflows/build-and-push.yml"

draw_header() {
  clear
  printf '%s\n' "========================================"
  printf ' Repo: %s\n' "$(basename "$repo_root")"
  printf ' Branch: %s\n' "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"
  printf ' Workflow: %s\n' "$WORKFLOW_PATH"
  printf '%s\n' "========================================"
}

pause() {
  printf "\nPresiona Enter para continuar..."
  read _dummy
}

create_workflow() {
  mkdir -p .github/workflows
  cat > "$WORKFLOW_PATH" <<'EOF'
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
  git add "$WORKFLOW_PATH" >/dev/null 2>&1 || true
  git commit -m "ci: add build-and-push workflow (created by terminal_ui)" >/dev/null 2>&1 || true
  echo "Workflow creado y commiteado. Haz push para subirlo al remoto."
  pause
}

detect_owner_repo() {
  remote_url="$(git config --get remote.origin.url 2>/dev/null || true)"
  if [ -z "$remote_url" ]; then
    echo ""
    return
  fi
  if echo "$remote_url" | grep -qE '^git@'; then
    echo "$remote_url" | sed -E 's#git@[^:]+:([^/]+/[^/.]+)(.git)?#\1#'
  else
    echo "$remote_url" | sed -E 's#https?://[^/]+/([^/]+/[^/.]+)(.git)?#\1#'
  fi
}

dispatch_workflow() {
  owner_repo="$(detect_owner_repo)"
  if [ -z "$owner_repo" ]; then
    printf "No se pudo detectar owner/repo desde origin. Exporta GITHUB_REPOSITORY o configura remote origin.\n"
    pause
    return
  fi

  branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"
  printf "Enviar dispatch para %s en la rama %s\n" "$owner_repo" "$branch"

  printf "Introduce GitHub PAT (repo scope) [se ocultará]: "
  stty -echo || true
  read -r GH_TOKEN || true
  stty echo || true
  printf "\n"
  if [ -z "$GH_TOKEN" ]; then
    echo "No se proporcionó token. Cancelado."
    pause
    return
  fi

  printf "Despachando workflow...\n"
  http_code=$(curl -s -o /dev/stderr -w "%{http_code}" -X POST \
    -H "Authorization: token ${GH_TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/${owner_repo}/actions/workflows/build-and-push.yml/dispatches" \
    -d "{\"ref\":\"${branch}\"}" || true)

  if [ "$http_code" = "204" ] || [ "$http_code" = "201" ]; then
    echo "Workflow despachado correctamente."
    "$BROWSER" "https://github.com/${owner_repo}/actions/workflows/build-and-push.yml" || true
  else
    echo "Dispatch falló (HTTP $http_code). Revisa Actions UI."
  fi
  pause
}

open_actions() {
  owner_repo="$(detect_owner_repo)"
  if [ -z "$owner_repo" ]; then
    echo "No se pudo detectar owner/repo."
    pause
    return
  fi
  "$BROWSER" "https://github.com/${owner_repo}/actions" || true
}

menu() {
  while :; do
    draw_header
    printf "\nOpciones:\n"
    printf "  1) Comprobar existencia del workflow\n"
    printf "  2) Crear workflow por defecto (si falta)\n"
    printf "  3) Despachar workflow ahora (pedirá GitHub PAT)\n"
    printf "  4) Abrir Actions en el navegador del host\n"
    printf "  5) Hacer git pull --rebase, add, commit y push (sync local)\n"
    printf "  q) Salir\n"
    printf "\nSelecciona una opción: "
    read -r opt

    case "$opt" in
      1)
        if [ -f "$WORKFLOW_PATH" ]; then
          echo "OK: $WORKFLOW_PATH existe."
        else
          echo "NO: $WORKFLOW_PATH no encontrado."
        fi
        pause
        ;;
      2)
        if [ -f "$WORKFLOW_PATH" ]; then
          echo "El workflow ya existe. Nada que hacer."
        else
          create_workflow
        fi
        ;;
      3)
        if [ ! -f "$WORKFLOW_PATH" ]; then
          echo "Workflow no existe. ¿Crear primero? [y/N]: "
          read -r c; case "$c" in y|Y) create_workflow ;; *) echo "Cancelado"; pause; continue ;; esac
        fi
        dispatch_workflow
        ;;
      4)
        open_actions
        pause
        ;;
      5)
        echo "Haciendo fetch..."
        git fetch origin || true
        branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"
        echo "Pull --rebase origin/$branch ..."
        if git pull --rebase origin "$branch"; then
          echo "Pull completado."
        else
          echo "Pull falló. Resuelve conflictos manualmente."
          pause
          continue
        fi
        git add -A
        if git diff --cached --quiet; then
          echo "No hay cambios para commitear."
        else
          msg="sync: update workspace $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
          git commit -m "$msg" || true
          echo "Commit creado."
        fi
        git push origin "$branch" || echo "Push falló."
        pause
        ;;
      q|Q)
        clear
        exit 0
        ;;
      *)
        echo "Opción inválida."
        pause
        ;;
    esac
  done
}

menu