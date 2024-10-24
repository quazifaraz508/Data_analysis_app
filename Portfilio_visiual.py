import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from Portfolio_visiual_2 import Bar_Chart
from Portfolio_visiual_3 import HeatMap



class Data_visualization():
    def __init__(self, df):
        self.df = df

    def num_of_line_chart(self ,visual_data,index1, index2,selected_marker, color, label ,markersize_line1):
        if visual_data == "basic_line_chart":
            plt.plot(index1, index2 ,selected_marker, color=color, label=label, markersize = markersize_line1)
        elif visual_data == "area_line_chart":
            plt.fill_between(index1, index2, color = color,  alpha = self.alpha_)
            plt.plot(index1, index2 ,selected_marker, color = color , label = label,alpha = 0.4 )
        elif visual_data == "step_line_chart":
            plt.step(index1, index2,selected_marker, color = color, label = label, markersize = markersize_line1,where=self.where_step_opn )
        
            
    def chart_data(self, visual_data,maximum_lines, x_axis, maximum_num_heads, selected_marker, markersize_line1):
        self.grid_fun(visual_data)
        
        for i in range(maximum_lines):
            y_axis = st.selectbox(f"Select Y-axis for line {i + 1}:", self.df.columns.tolist())
            color = st.color_picker(f"Choose color for {y_axis}:", value='#FF0000',key=f"color_picker_{i}")

            if visual_data == "basic_line_chart" or "area_line_chart" or "step_line_chart":
                self.num_of_line_chart(visual_data,self.df[x_axis].head(maximum_num_heads), self.df[y_axis].head(maximum_num_heads), selected_marker, color, y_axis ,markersize_line1)
            else:
                st.warning(f"Column {y_axis} not found in the dataframe")

        
    def show_data(self, visual_data, chart_type):
        markers = ['o','-','o-','--','s-', 's', '^','^-', 'D','D-', 'x','x-', '*','*-', 'P','P-', 'H', '|', '1', '2', '3']
        self.maximum_lines = st.number_input("Enter the number of lines:", min_value=1, value=1, key=f"{chart_type}1_num_lines_unique")
        self.x_axis = st.selectbox("Select X-axis:", self.df.columns.tolist(), key=f"{chart_type}x_axis_unique_key")
        self.maximum_num_heads = st.number_input("Enter the number of entities to display:", min_value=1, value=50,  key=f"{chart_type}max_head_unique_key")
        fig_size = st.radio("Change figure size", ["No", "Yes"])
        if fig_size == "Yes":  
            self.fig_width = st.number_input("Enter the figure width:", min_value=4, value = 16)
            self.fig_height = st.number_input("Enter the figure height:", min_value=4, value = 7)
        else:
            self.fig_width = 16
            self.fig_height = 7
            
        marker_opn = st.radio("select marker:", ["No","Yes"],  key=f"{chart_type}marker_opn_unique_key")
        
        if marker_opn == "Yes":
            self.selected_marker = st.selectbox('Select Marker Style:', markers)
            markersize_line_decision = st.radio("want to change marker size", [ "No", "Yes"])
            self.markersize_line1 = st.number_input("Enter the marker size:", min_value=1, value=10) if markersize_line_decision == "Yes" else 10
        else:
            self.selected_marker = "-"
            self.markersize_line1 = 10
        

    def grid_fun(self, chart_type):
        grid_inp = st.radio("select grid:", ["Yes", "No"], key=f"{chart_type}gird_inp")
        if grid_inp == "Yes":
            plt.grid()
        else:
            pass  
    
    def download_chart(self, value_key):
        plt.xlabel(self.x_axis)
        
        plt.ylabel('Values')
        
        plt.legend()
        
        # Save the figure to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        st.pyplot(plt)

        st.download_button(
            label="Download Chart",
            data=buf,
            file_name="line_chart.png",
            mime="image/png",
            key= f"{value_key}"
        )
        
    def final_line_chart(self):
        visual_data = "basic_line_chart"
        
        st.title("Line Chart")
        self.show_data(visual_data, visual_data)
        plt.figure(figsize=(self.fig_width, self.fig_height))
        self.chart_data( visual_data,self.maximum_lines, self.x_axis, self.maximum_num_heads, self.selected_marker, self.markersize_line1)    
     
        self.download_chart(visual_data)
        
    
    def Final_area_chart(self):
        visual_data = "area_line_chart"
        
        st.title("Area Chart")
        
        self.show_data(visual_data,visual_data)
        plt.figure(figsize=(self.fig_width, self.fig_height))
        
        visiblity = st.radio("Visiblity of area:", ["default", "custom"])
        if visiblity == "default":
            self.alpha_ = 0.4
        else:
            self.alpha_ = st.number_input("Enter Alpha (0 to 1):", min_value=0.10, max_value=1.0, value=0.4, step=0.1)
        self.chart_data( visual_data,self.maximum_lines, self.x_axis, self.maximum_num_heads, self.selected_marker, self.markersize_line1)    
        
        self.download_chart(visual_data)
    
    def Final_step_chart(self):
        visual_data = "step_line_chart"
        st.title("Step Chart")
        self.show_data(visual_data, visual_data)
        plt.figure(figsize=(self.fig_width, self.fig_height))
        
        where_Step_list = ['mid', 'pre', 'post']
        where_step = st.radio("select where step", ["No", "Yes"])
        if where_step == "Yes":
            self.where_step_opn = st.selectbox("Enter",where_Step_list)
            
        else:
            self.where_step_opn = "mid"
        self.chart_data( visual_data,self.maximum_lines, self.x_axis, self.maximum_num_heads, self.selected_marker, self.markersize_line1)    
        plt.title("Step Chart")
        
        self.download_chart(visual_data)
    

    def main(self):
        
        data_visulization_op1 = st.selectbox("Line Chart:", ["None","Line Chart","Area Line Chart","Step Line Chart"])
        
        if data_visulization_op1 == "Line Chart":
            self.final_line_chart()
        
        elif data_visulization_op1 == "Area Line Chart":
            self.Final_area_chart()
        
        elif data_visulization_op1 == "Step Line Chart":
            self.Final_step_chart()
        
        data_visulization_op2= st.selectbox("Bar Chart", ["None","Bar Chart",])
        if data_visulization_op2 == "Bar Chart":
            data_bar_chart = Bar_Chart(self.df)
            data_bar_chart.main()
        
        data_visulization_op3 = st.selectbox("Heatmap", ["None","Heatmap""Heatmap with pivot","Clustered  Heatmap"])
        if data_visulization_op3:
            data_heatmap = HeatMap(self.df)
            data_heatmap.main(data_visulization_op3)
