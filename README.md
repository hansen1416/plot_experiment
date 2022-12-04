> some quesitons &ideas: 
> 
> 1. 试一下，建立一个72*3的数组，绘制在figsize = 1*1的画布上，看看s值多大合适？

```
figsizes = np.array([[i*i] for i in range(1, 16)])
marksizes = [0.5, 2, 4.2, 8, 12, 18, 24, 32, 40, 50, 60, 72, 84, 96, 110]
```
https://github.com/hansen1416/plot_experiment/tree/master/regression_result

> 2. 如果不需要xlim和ylim，那是不是投影转换的那些都可以注释掉？

Yes

> 3. 我注释掉muidsgrid，就是不用行列号，还用原来的x, y, 也会出现上下间距; 

Yes

> 4. 关于行列号的计算，我刚开始提议int(([x]-x0)/5)不是说涉及投影转换的问题，后来为什么又可以了？

