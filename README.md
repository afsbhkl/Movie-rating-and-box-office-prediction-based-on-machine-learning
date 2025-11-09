## 🎬 基于机器学习的电影评分与票房预测
## 🎬 Machine Learning-Based Movie Rating and Box Office Prediction
<br>
## 📘 项目简介 / Project Overview

本项目以 2019–2022 年电影市场数据为基础，运用多种机器学习模型（线性回归、随机森林、LightGBM、CatBoost）对电影的评分与票房进行预测分析。
通过从电影自身特征、制片与发行因素以及宏观经济变量三个维度出发，我们探索了哪些因素最能影响一部电影的商业表现与观众口碑，从而为制片方投资决策与文化产品优化提供参考。
<br>
This project analyzes the movie market between 2019 and 2022, employing multiple machine learning models — Linear Regression, Random Forest, LightGBM, and CatBoost — to predict both movie ratings and box office performance.
It integrates film features, production and distribution variables, and macroeconomic indicators to uncover key determinants behind a movie’s commercial success and audience reception, providing data-driven insights for investment and production decisions.
<br><br>
## 🧩 数据来源与预处理 / Data Sources & Preprocessing

原始数据来自猫眼电影数据库。

通过爬虫补充了豆瓣评分、评分人数与百度指数等变量。

结合《中国统计年鉴》，引入宏观指标（GDP、第三产业增加值、消费水平、影院与银幕数量等）。

对分类变量（地区、档期、类型）进行了整合与独热编码。

异常值、缺失值经清洗与顺序填充处理。

票房划分为六个等级（微薄、小型、中型、大型、超大型、巨型）以降低极端值影响。

<br><br>

Base data: Maoyan Movie Database.

Additional variables from web scraping: Douban ratings, number of reviews, Baidu search indices.

Added macroeconomic data (GDP, tertiary industry, consumption, number of cinemas/screens) from China Statistical Yearbook.

Merged and one-hot encoded categorical variables such as region, release season, and genre.

Cleaned missing and outlier values.

Transformed box office values into six categorical levels to reduce outlier sensitivity.

<br><br>

## 🔍 探索性分析 / Exploratory Analysis<br>

疫情冲击： 受疫情影响的影片占约 75%，其票房明显低于未受影响影片。<br>
档期差异： 普通档电影平均票房最高，贺岁档相对较低。<br>
类型偏好： 剧情类影片数量最多，也是最受欢迎的类型。<br>
地区差异： 中国本土影片占比 66.6%，主导市场。<br>
时长分布： 大部分影片时长在 90–120 分钟间，呈正态分布。<br>
演员指数： 明星百度指数与票房呈“先升—下降—再升”的非线性关系。<br>
宏观因素： 票房受人均GDP、第三产业增加值、消费水平、影院银幕数等影响显著。<br>

Pandemic effect: About 75% of films were affected by COVID-19, showing significantly lower box office results.<br>
Release schedule: Regular-season films achieved the highest average revenue; New Year releases were lower.<br>
Genre preference: Drama is the dominant and most popular film type.<br>
Regional distribution: Chinese domestic films account for 66.6% of the dataset.<br>
Duration: Most films last 90–120 minutes, showing a near-normal distribution.<br>
Star effect: Baidu actor indices show a nonlinear pattern with box office — rising, then falling, then rising again.<br>
Macroeconomics: GDP per capita, tertiary industry output, consumption, and screen count all correlate strongly with box office results.
<br><br>
## 🤖 模型构建与结果 / Model Building & Results <br>
模型 / Model	预测目标	R²	MSE / AUC	主要结论 <br>
Linear Regression	评分预测 / Rating	0.25	0.77	解释力弱，仅能捕捉总体趋势 <br>
Random Forest	评分预测 / Rating	0.44	0.58	略有提升，但仍存在偏差<br>
LightGBM	评分预测 / Rating	0.90	0.12	拟合效果极佳，预测最准确<br>
LightGBM	票房预测 / Box Office	0.57	0.84	拟合较好，分类后改善明显<br>
CatBoost	票房预测 / Box Office	0.59	0.86	表现最佳，适合含分类变量的数据<br>
<br><br>
LightGBM achieved outstanding performance for rating prediction with R² = 0.902, while CatBoost provided the most accurate box office classification (AUC = 0.585, ROC-AUC = 0.863). These results demonstrate the effectiveness of gradient boosting models in handling nonlinear, high-dimensional film data.

<br><br>
## 🎯 主要发现 / Key Findings
宏观经济繁荣直接促进电影消费，居民收入和第三产业发展均显著提升票房表现。<br>
明星效应与观众搜索热度对票房的边际影响逐渐减弱，影片质量和类型成为核心决定因素。<br>
高分电影往往伴随中高票房，但票房巨制不一定拥有高口碑。<br>
LightGBM与CatBoost在复杂特征交互的预测中具有最佳表现，可为电影投资风险控制与发行策略提供辅助决策。<br>
<br><br>
Macroeconomic prosperity — especially income and tertiary industry growth — significantly drives box office performance.<br>
The influence of star popularity is diminishing; content quality and genre fit now dominate audience preference.<br>
High ratings often correlate with moderate-to-high box office, but blockbusters are not always well-rated.<br>
LightGBM and CatBoost models show superior performance in capturing nonlinear interactions, offering actionable insights for investment and release strategy.<br>




