#!/usr/bin/env bash
# 用法：./make_zip.sh 学号 姓名  ->  生成 学号姓名.zip，内含 report.pdf 和 code/
set -e
[ $# -eq 2 ] || { echo "用法：$0 学号 姓名"; exit 1; }
cd "$(dirname "$0")"
name="$1$2"
tmp=$(mktemp -d)
mkdir -p "$tmp/$name"
cp report/report.pdf "$tmp/$name/"
cp -r code "$tmp/$name/code" && rm -rf "$tmp/$name/code/__pycache__"
(cd "$tmp" && zip -qr "$name.zip" "$name")
mv "$tmp/$name.zip" .
rm -rf "$tmp"
echo "已生成 $name.zip"
