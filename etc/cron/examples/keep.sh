#!/bin/sh
wall "Cronmanager called keep internet alive script !"
ping -c 5 www.google.com
exit 0
