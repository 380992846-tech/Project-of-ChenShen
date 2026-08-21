# 其他工具（诗词 · 物理）

> 大模型/ 下暂不属于主线的两个独立工具。

## 古典诗词生成 API —— `poem_api.py`

基于 Flask 的 RESTful 服务，使用词库（名词/动词/意象/情感）+ 格律校验 + 风格调制生成古典诗词。

```bash
pip install flask flask-cors numpy scikit-learn
python 大模型/其他工具（诗词·物理）/poem_api.py   # 访问 http://localhost:5000
```

## 一维弹性碰撞模拟 —— `elastic_collision_sim.py`

事件驱动的物理引擎：碰撞时刻预测、完全弹性碰撞解析、球-球/球-墙碰撞、重叠修复；
备选 RK4 积分器，支持轨迹绘图、动画帧导出与质量比扫描实验。

```bash
pip install numpy matplotlib
python 大模型/其他工具（诗词·物理）/elastic_collision_sim.py --balls 5 --tmax 20 --animate
```
