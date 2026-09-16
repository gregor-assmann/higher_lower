#!/bin/sh
set -eu

cd /app/scraper

cat > /etc/cron.d/higher-lower-scraper <<EOF
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
CRON_TZ=${TZ:-UTC}
0 6 * * * root cd /app/scraper && /usr/local/bin/python scraper.py >> /proc/1/fd/1 2>> /proc/1/fd/2
EOF

chmod 0644 /etc/cron.d/higher-lower-scraper

if ! /usr/local/bin/python scraper.py; then
	echo "Initial scrape failed; the next scheduled run will retry." >&2
fi

exec cron -f
