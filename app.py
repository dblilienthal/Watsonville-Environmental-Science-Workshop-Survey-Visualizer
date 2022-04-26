import pandas as pd
import streamlit as st

 
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

    st.header("Watsonville Environmental Workshop Monthly Report Visualizer")

    helper = FileUpload()
    data = helper.run()
    # If the data has been populated
    if data.shape != (0,0):
        st.dataframe(data.head(10))

        ### Sidebar code
        st.sidebar.header('Features to graph')
        column = st.sidebar.selectbox("Target Column", data.columns.tolist())
        timeseries_column = st.sidebar.selectbox("Time Column", data.columns.tolist())
        print("Selected columns:", column)
        freq = st.sidebar.selectbox("Frequency", ['Week', 'Month', 'Year', 'All'])
        print("Selected Frequency:", freq)





