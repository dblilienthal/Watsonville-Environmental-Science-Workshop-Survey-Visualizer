from re import S
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

 
STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""
 
 
class FileUpload(object):
 
    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.markdown(STYLE, unsafe_allow_html=True)
        file = st.file_uploader("Upload file", type=['csv'])
        show_file = st.empty()
        if not file:
            show_file.info("Please upload a file of type: csv")
            return pd.DataFrame() # Returns a blank dataframe to avoid error. Might want to fix later 
        else:
            data = pd.read_csv(file)
            file.close()

            return data


 
if __name__ ==  "__main__":
    # Logo
    st.image('./WESW Logo.png')
    
    # Title
    st.header("Watsonville Environmental Workshop Monthly Report Visualizer")

    helper = FileUpload()
    data = helper.run()
    # If the data has been populated
    if data.shape != (0,0):
        st.dataframe(data.head(10))

        ### Sidebar code
        st.sidebar.header('Features to graph')
        st.sidebar.subheader('Timestamp column')
        timeseries_column = st.sidebar.selectbox("Time Column (The column that has the time the survey was taken)", data.columns.tolist())
        st.sidebar.subheader('Target Column')
        column = st.sidebar.selectbox("The column you want to graph", data.columns.tolist())
        st.sidebar.subheader('Frequency')
        freq = st.sidebar.radio("Frequency", ['Week', 'Month', 'Year', 'All'])
        #st.sidebar.subheader(f'Number of {freq}\'s')
        num_freq = ''
        top_num_freq = data.shape[1]
        if freq != 'All':
            num_freq = st.sidebar.slider(f'Number of {freq}\'s', 1, 12)

            top_num_freq = st.sidebar.slider(f'Top number of results', 1, 30)


        # Click for button
        clicked = st.sidebar.button('Make Graph')
        if clicked:
            print("Selected columns:", column)
            print('Time column:', timeseries_column)
            print("Selected Frequency:", freq)
            print("Number of freqs:",num_freq)

            # Convert the timecolumn to datetime
            data[timeseries_column] = pd.to_datetime(data[timeseries_column])
            data.set_index(timeseries_column)

            # Getting the data
            val_count_df = data[column].value_counts()[:top_num_freq]  # Geting value counts by selected column
            val_count_df.sort_values(ascending=True, inplace=True)
            st.dataframe(val_count_df)

            fig, ax = plt.subplots()
            ax.barh(val_count_df.index, val_count_df.values)

            st.pyplot(fig)







