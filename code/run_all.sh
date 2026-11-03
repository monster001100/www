#!/usr/bin/env bash
# 运行全部实验：2 个数据集 × 3 种算法 × 3 种剪枝方式
# 图片保存在 results/*.png，日志保存在 results/logs/*.log，汇总表保存在 results/summary.txt
set -e
cd "$(dirname "$0")"
mkdir -p results/logs
: > results/summary.txt
for ds in melon celeba; do
  for algo in 1 2 3; do
    case $algo in 1) name=ID3;; 2) name=C45;; 3) name=CART;; esac
    for prune in none pre post; do
      python3 tree.py "$ds" "$algo" "$prune" > "results/logs/${ds}_${name}_${prune}.log" 2>&1
      grep SUMMARY "results/logs/${ds}_${name}_${prune}.log" | tee -a results/summary.txt
    done
  done
done
