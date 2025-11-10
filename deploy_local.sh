#!/bin/bash
# Script para desplegar el sistema en local (backend + dashboard)

# Instala dependencias
pip install -r requirements.txt

# Arranca backend y dashboard automatizados
bash start_dashboard.sh
