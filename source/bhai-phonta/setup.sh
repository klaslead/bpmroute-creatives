#!/bin/sh
# Fetch three.js r170 into vendor/ (kept out of git).
set -e
cd "$(dirname "$0")"
npm i --no-save --prefix .npm three@0.170.0
mkdir -p vendor && cp .npm/node_modules/three/build/three.module.js vendor/ && rm -rf vendor/addons && cp -r .npm/node_modules/three/examples/jsm vendor/addons
