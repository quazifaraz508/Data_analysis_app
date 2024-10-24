import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Portfilio_visiual import Data_visualization

st.title("Upload CSV & Excel file.")

# File upload
uploaded_file = st.file_uploader("Upload file", type=['csv', 'xlsx'])

button_style = """
        <style>
        div.stButton > button {
            background-color: #239a9a;
            color: black;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
    """
st.markdown(button_style, unsafe_allow_html=True)

encoding_inp =st.radio('enter encoding:', ['No', 'Yes'])
# Check if file is uploaded
if uploaded_file is not None:
    # Handle CSV file
    if uploaded_file.name.endswith('.csv'):
        if encoding_inp == 'Yes':
            encoding_text_inp = st.text_input('enter :')
            try:
                df = pd.read_csv(uploaded_file,  encoding= encoding_text_inp)
            except (UnicodeDecodeError, LookupError):
                st.error('Enter correct encoding.')
                
        else:
            try:
                df = pd.read_csv(uploaded_file)
            except (UnicodeDecodeError, LookupError):
                st.error('Enter correct encoding.')
                
        st.write("CSV file uploaded successfully!")
            
    # Handle Excel file
    elif uploaded_file.name.endswith('.xlsx'):
        if encoding_inp == 'Yes':
            encoding_text_inp = st.text_input('enter :')
            try:
                df = pd.read_excel(uploaded_file , encoding = encoding_text_inp)
            except (UnicodeDecodeError, LookupError):
                st.error('Enter correct encoding.')
        else:
            try:
                df = pd.read_excel(uploaded_file)
            except (UnicodeDecodeError, LookupError):
                st.error('Enter correct encoding.')
                
        st.write("Excel file uploaded successfully!")
    if 'show_data' not in st.session_state:
        st.session_state.show_data = False

    display_btn = st.button("Show/Hide Data")
    if display_btn:
        st.session_state.show_data = not st.session_state.show_data

    if st.session_state.show_data:
        st.dataframe(df)
    # Initialize the session state for section display
    if 'active_section' not in st.session_state:
        st.session_state.active_section = ""

    # Button to toggle sections
    details = "Data Details"
    clean = "Data Cleaning"
    visualize = "Data Visualization"
    analysis = "Data Analysis"
    if st.button(details):
        st.session_state.active_section = details
        
    if st.session_state.active_section == details:
        decision = st.radio("Details:", ["Check null value", "Numbers of columns", "Numbers of rows", "Data type of columns","Summary statistics", "Full info"])
        btn_details = st.button("find")
        
        if btn_details:
            if decision == "Check null value":
                st.write(df.isnull().sum())
            if decision == "Numbers of columns":
                st.write(df.shape[1])
            if decision == "Numbers of rows":
                st.write(df.shape[0])
            if decision == "Data type of columns":
                st.write(df.dtypes)
            if decision == "Summary statistics":
                st.write(df.describe())
            if decision == "Full info":
                st.write("null value ",df.isnull().sum())
                st.write("There is ",df.shape[1],"Columns")
                st.write("There is ",df.shape[0],"Rows")
                st.write("Data types ",df.dtypes,)
                st.write("statistics",df.describe())
                st.write("Unique values",df.nunique())
                
            
    if st.button(clean):
        st.session_state.active_section = clean

    if st.button(visualize):
        st.session_state.active_section = visualize

    if st.button(analysis):
        st.session_state.active_section = analysis

    # Display selected section
    if st.session_state.active_section == clean:
        st.title(clean)
    
        option1 = st.selectbox("Handling Missing Values",["None","Remove missing data","Fill missing data with 0", "Fill missing data with forward", "Fill missing data with mean", "Fill missing data with median", "Fill missing data with backward"])
         
        if option1 == "Remove missing data":
            df_clean = df.dropna()
            st.dataframe(df_clean)
        
        elif option1 == "Fill missing data with 0":
            df_clean = df.fillna(0)
            st.dataframe(df_clean)
            
        elif option1 == "Fill missing data with forward":
            df_clean = df.fillna(method= 'ffill')
            st.dataframe(df_clean)
        
        elif option1 == "Fill missing data with mean":
            df_numeric = df.select_dtypes(include=['number'])
            df_clean = df.fillna(df_numeric.mean())
            st.dataframe(df_clean)
            
        
        elif option1 == "Fill missing data with median":
            df_numeric = df.select_dtypes(include=['number'])
            df_clean = df.fillna(df_numeric.median())
            st.dataframe(df_clean)
            
        elif option1 == "Fill missing data with backward":
            df_clean = df.fillna(method = "bfill")
            st.dataframe(df_clean)
        
        option2 = st.selectbox("Removing Duplicates",["None","Removing Duplicates"])
        
        if option2 == "Removing Duplicates":
            df_clean = df.drop_duplicates()
            st.dataframe(df_clean)
        
        option4 = st.selectbox("Handling Inconsistent Formatting",["None","Uppercase all alphabets", "Lowercase all aplhabets", "Uppercase only fisrt alpabet" ])
          
        if option4 == "Uppercase all alphabets":
            df_clean = df.apply(lambda x: x.astype(str).str.upper())
            st.dataframe(df_clean)
            
        # if option3 == "Correcting Data Types":
        elif option4 == "Lowercase all aplhabets":
            df_clean = df.apply(lambda x : x.astype(str).str.lower())
            st.dataframe(df_clean)
        
        elif option4 == "Uppercase only fisrt alpabet":
            df_clean = df.apply(lambda x: x.astype(str).str.title())
            st.dataframe(df_clean)
        
        option5 = st.multiselect("Removing Unnecessary Columns",options=list(df.columns.tolist()))
        
        if option5:
            df_clean = df.drop(columns=option5)
            st.dataframe(df_clean)
          
            
    elif st.session_state.active_section == visualize:
        st.title(visualize)
        # Add your data visualization logic here
        data_vis = Data_visualization(df)
        data_vis.main()
    elif st.session_state.active_section == analysis:
        st.title(analysis)
        # Add your data analysis logic here
        st.header("Under Construction.....!")
st.write("**Developed by Faraz**")
