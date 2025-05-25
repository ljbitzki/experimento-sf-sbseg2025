#!/bin/bash
iptables  -F
iptables  -X
iptables  -Z
iptables  -P INPUT DROP
iptables  -A INPUT -i lo -j ACCEPT
iptables  -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
############################################################################################################
iptables  -A INPUT -s 0.0.0.0/0 -j ACCEPT
