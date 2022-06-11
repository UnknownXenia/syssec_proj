# syssec_proj

运行示例：

`in_disk` 控制是否在磁盘IO
`build_tree` 建树
`target` 目标文件的名字
`acc` 准确度， 1/2/4/8 值越大，准确度越高，但是速度越慢
```
python3 ./detector.py --in_disk=0 --build_tree 1 --target glibc-2.9 --acc 4
```

