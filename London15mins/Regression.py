import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
from shapely.geometry import Point

# 读取房价数据
def load_data():
    # 读取房价数据（更新为实际路径）
    house_data = pd.read_csv("updated_london_house_price.csv")  # 更新为实际文件路径
    house_data['geometry'] = house_data.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
    house_data = gpd.GeoDataFrame(house_data, geometry='geometry')

    return house_data

# 运行OLS回归模型
def run_ols(house_data):
    print("Running OLS regression...")

    # 选择自变量和因变量
    X = house_data[['transit_access', 'park_access', 'school_access', 'commer_access', 'hospital_access']]
    X = sm.add_constant(X)  # 加上截距项
    y = house_data['price']
    
    # 运行OLS回归
    ols_model = sm.OLS(y, X).fit()

    # 输出OLS回归的详细统计结果
    print("\nOLS Regression Results:")
    print(ols_model.summary())  # 输出OLS回归的统计结果
    return ols_model

# 运行岭回归模型
def run_ridge(house_data, alpha=5.0):
    print(f"\nRunning Ridge regression with alpha={alpha}...")

    # 选择自变量和因变量
    X = house_data[['transit_access', 'park_access', 'school_access', 'commer_access', 'hospital_access']]
    y = house_data['price']
    
    # 数据集拆分：70%训练，30%测试
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 运行岭回归
    ridge_model = Ridge(alpha=alpha)
    ridge_model.fit(X_train, y_train)

    # 预测和评估模型
    y_pred = ridge_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    print(f"\nRidge Regression Mean Squared Error: {mse}")
    print(f"Ridge Model Coefficients: {ridge_model.coef_}")

    # 输出回归系数的详细信息，类似OLS回归的summary()输出
    print("\nRidge Regression Detailed Output:")
    print(f"Intercept: {ridge_model.intercept_}")
    for idx, col in enumerate(X.columns):
        print(f"Coefficient for {col}: {ridge_model.coef_[idx]}")

    return ridge_model


# 结果可视化
def plot_results(ols_model, ridge_model, house_data):
    # OLS残差图
    plt.figure(figsize=(15, 10))
    plt.subplot(211)
    plt.scatter(ols_model.fittedvalues, ols_model.resid)
    plt.xlabel("Fitted Values")
    plt.ylabel("Residuals")
    plt.title("OLS Residual Plot")

    # 岭回归残差图
    plt.subplot(212)
    plt.scatter(ridge_model.predict(house_data[['transit_access', 'park_access', 'school_access', 'commer_access', 'hospital_access']]), 
                house_data['price'] - ridge_model.predict(house_data[['transit_access', 'park_access', 'school_access', 'commer_access', 'hospital_access']]))
    plt.xlabel("Fitted Values")
    plt.ylabel("Residuals")
    plt.title("Ridge Regression Residual Plot")

    plt.tight_layout()
    plt.show()


# 主函数
def main():
    # 读取房价数据
    house_data = load_data()

    # 运行OLS回归
    ols_model = run_ols(house_data)

    # 运行岭回归
    ridge_model = run_ridge(house_data, alpha=1.0)

    # 绘制回归结果图
    plot_results(ols_model, ridge_model, house_data)

if __name__ == "__main__":
    main()
