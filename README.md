> some quesitons &ideas: 
> 
> 1. 试一下，建立一个72*3的数组，绘制在figsize = 1*1的画布上，看看s值多大合适？

笨人用笨办法，下面这些数据是没有完全对齐，刚好留了一点点缝隙的情况，做了一个polynomial regression。S也就是marker size 和 figsize 之间的关系还是比较明显的。另外当degree=3的时候，预测出来的值相对比较准确

```
figsizes = np.array([[i*i] for i in range(1, 16)])
marksizes = [0.5, 2, 4.2, 8, 12, 18, 24, 32, 40, 50, 60, 72, 84, 96, 110]
```
https://github.com/hansen1416/plot_experiment/tree/master/regression_result

> 2. 如果不需要xlim和ylim，那是不是投影转换的那些都可以注释掉？

是的

> 3. 我注释掉muidsgrid，就是不用行列号，还用原来的x, y, 也会出现上下间距; 

是的，很奇怪。我后来用heatmap尝试了一下，X，Y全部转成了INT。我感觉是scatter 不太能处理好float的X，Y坐标，而且精度比较低。

> 4. 关于行列号的计算，我刚开始提议int(([x]-x0)/5)不是说涉及投影转换的问题，后来为什么又可以了？

你给的公式没错，只是我需要先从3857转成 NZGD2000 之后再应用你的公式就可以了

