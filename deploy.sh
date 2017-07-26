#!/usr/bin/env bash


rsync --exclude='*.git/*' --exclude='*.json' --exclude='.idea' --exclude='_gitblog/' --exclude='logs/' -arvp '/Users/ganxiangle/Library/Mobile Documents/com~apple~CloudDocs/ftwo.me/' 'root@ftwo.me:/root/ftwo.me/'