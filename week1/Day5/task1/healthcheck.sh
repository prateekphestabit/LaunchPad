#!/bin/bash

URL="http://localhost:8000/ping"    
LOG_FILE="logs/health.log"

echo "Starting health check for: $URL"
echo "Logging failures to: $LOG_FILE"
echo "-----------------------------------------"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

    # Send request (silent, fail on HTTP errors)
    if curl -fs --max-time 5 "$URL" > /dev/null; then
        echo "[$TIMESTAMP] ✔ Healthy"
    else
        echo "[$TIMESTAMP] FAILED to reach $URL" | tee -a "$LOG_FILE"
    fi

    sleep 10
done
