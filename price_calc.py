#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
from datetime import datetime
import os 






# Function to calculate weight and price
def calculate_weight_and_price(inner_diameter, outer_diameter, height, price_per_kg,
                                                    edge_inner, edge_outer, edge_height):
    # Assuming copper density is 8.96 g/cm^3 (you can adjust as needed)

                                                      
    density = 8960 # kg/m3  
    volume = 3.1416 * (height/1000) * ((outer_diameter/(2*1000))**2 - (inner_diameter/(2*1000))**2)
    weight = density * volume  # Convert to kg 
    price = weight * price_per_kg * 2 


                                                      
    # 沿

    edge_volume = 3.1416 * (edge_height/1000) * ((edge_outer/(2*1000))**2 - (edge_inner/(2*1000))**2)
    edge_weight = density * edge_volume  # Convert to kg 
    edge_price = edge_weight * price_per_kg * 2 


    return weight + edge_weight, price + edge_price




# Main application
def main():
    st.title("铜套价格计算器")

    # 使用列来组织输入框
    col1, col2 = st.columns(2)

    with col1:
    # 左侧的输入框
        # Input fields
        inner_diameter = st.number_input("内径 (mm)", min_value=0.0, format="%.2f")
        outer_diameter = st.number_input("外径 (mm)", min_value=inner_diameter, format="%.2f")
        height = st.number_input("高 (mm)", min_value=0.0, format="%.2f")
        # price 
        price_per_kg = st.number_input("价格(元/斤)", value=35.0, format="%.2f")


  
  
    # edge
    with col2:
        edge_inner = st.number_input("沿-内径 (mm)", min_value=0.0, value=0.00, format="%.2f") 
        edge_outer = st.number_input("沿-外径 (mm)", min_value=0.0, value=0.00, format="%.2f") 
        edge_height = st.number_input("沿-高 (mm)", min_value=0.0, value=0.00, format="%.2f") 
        # 备注
        mark = st.text_input('备注', value='')



  

    # Button to perform calculation
    if st.button("计算"):
        weight, price = calculate_weight_and_price(inner_diameter, outer_diameter, 
            height, price_per_kg, edge_inner, edge_outer, edge_height)

        # 保存状态
        st.session_state['calculated_weight'] = weight * 2
        st.session_state['calculated_price'] = price
        # 显示计算结果
        if 'calculated_weight' in st.session_state and 'calculated_price' in st.session_state:
            st.write(f"重量:  {st.session_state['calculated_weight']:.2f} 斤")
            st.write(f"价格:  {st.session_state['calculated_price']:.2f} 元")


      

        # 时间戳 
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 计算结果保存
        curPage_df = pd.DataFrame([[inner_diameter, 
                                    outer_diameter, 
                                    height, 
                                    edge_inner, edge_outer, edge_height, 
                                    price_per_kg, 
                                    round(weight * 2, 2), 
                                    round(price, 2), 
                                    current_time, 
                                    mark]], 
                                    columns=["内径(mm)", "外径(mm)", "高(mm)", 
                                             "沿-内径(mm)", "沿-外径(mm)", "沿-高(mm)", 
                                             "单价(元/斤)", "重量(斤)", 
                                             "价格(元/个)", '时间', '备注'])



      
        if os.path.exists('./history_record.csv'):
            history = pd.read_csv('./history_record.csv')
        else:
            history = pd.DataFrame(columns=["内径(mm)", "外径(mm)", "高(mm)", "沿-内径(mm)", "沿-外径(mm)", "沿-高(mm)", 
                                             "单价(元/斤)", "重量(斤)", 
                                             "价格(元/个)", '时间', '备注'])

        history = pd.concat((history, curPage_df), axis=0) 
        history = history.drop_duplicates(keep='first').reset_index(drop=True)
        history.to_csv('./history_record.csv', index=False) 


  


    # Display history
    if st.button("历史记录"):

        # 显示计算结果
        if 'calculated_weight' in st.session_state and 'calculated_price' in st.session_state:
            st.write(f"重量:  {st.session_state['calculated_weight']:.2f} 斤")
            st.write(f"价格:  {st.session_state['calculated_price']:.2f} 元")



      
        if os.path.exists('./history_record.csv'):
            history = pd.read_csv('./history_record.csv')
        else:
            history = pd.DataFrame(columns=["内径(mm)", "外径(mm)", "高(mm)", "沿-内径(mm)", "沿-外径(mm)", "沿-高(mm)", 
                                             "单价(元/斤)", "重量(斤)", 
                                             "价格(元/个)", '时间', '备注'])
                


      
        history = history.T 
        history = history[sorted(history.columns, reverse=True)]
        history.columns = [str(i) for i in history.columns]


      
        # 宽度设置 
        column_config = {}
        for c in history.columns:
            column_config[c] = st.column_config.Column(label=c, width='large')
        st.dataframe(history, 
                    # width=2000, 
                    height=430, 
                    # use_container_width=True, 
                    column_config=column_config 
                    )  # 调整 width 和 height 以适应您的需求






















if __name__ == "__main__":
    main() 




















