import streamlit as st
import pandas as pd
import datetime
from modules import inward_split, sku_creation, product_creation, pdf_extractor, image_to_excel

st.set_page_config(page_title='Technosport Internal Suite', layout='wide')
col1, col2 = st.columns([1,10])
with col1:
    st.image('assets/technosport_logo.png', width=60)
with col2:
    st.markdown('<h1 style="margin:0; padding:0;">TECHNOSPORTS INTERNAL SUITE</h1>', unsafe_allow_html=True)
    st.markdown('**AI-Powered Garment Data Automation**', unsafe_allow_html=True)

st.markdown("""
<style>
.stApp {
    background-image: url("assets/technosport_logo.png");
    background-size: 200px;
    background-repeat: no-repeat;
    background-position: center;
    opacity: 0.03;
}
</style>
""", unsafe_allow_html=True)

page = st.sidebar.selectbox('Navigate', ['Home','Inward Split','SKU Creation','Product Creation','PDF Extractor','Image -> Excel','Admin'])

def assistant():
    with st.sidebar.expander('TECHNOSPORTS AI Assistant 💬', expanded=False):
        query = st.text_input('Ask the assistant', key='assistant_input')
        if st.button('Ask', key='ask_btn'):
            if query.strip()=='':
                st.info('Ask something like: "Suggest category for style OR266"')
            else:
                st.success('TECHNOSPORTS AI: Got it boss ✅. Suggestion: Check "Category" as T-shirt for this style.')

assistant()

if page=='Home':
    st.write('Welcome to TECHNOSPORTS Internal Suite. Use the sidebar to choose a module.')
elif page=='Inward Split':
    st.header('Inward Split - Percentage Allocation')
    st.markdown('Upload an Excel with columns: SKU, Planned_Qty, Received_Qty, EBO_Qty, D2C_Qty, LFR_Qty')
    uploaded = st.file_uploader('Upload Excel', type=['xlsx','csv'])
    manual = st.checkbox('Or enter manual values', value=False)
    if manual:
        sku = st.text_input('SKU','SKU123')
        planned = st.number_input('Planned Qty', value=100)
        received = st.number_input('Received Qty', value=100)
        ebo = st.number_input('EBO Qty', value=50)
        d2c = st.number_input('D2C Qty', value=30)
        lfr = st.number_input('LFR Qty', value=20)
        if st.button('Process Manual'):
            df = pd.DataFrame([{'SKU':sku, 'Planned_Qty':planned, 'Received_Qty':received, 'EBO_Qty':ebo, 'D2C_Qty':d2c, 'LFR_Qty':lfr}])
            out = inward_split.process_df(df)
            st.download_button('Download Processed Excel', data=inward_split.to_excel_bytes(out), file_name=f'Processed_Percentage_{datetime.date.today()}.xlsx')
    if uploaded:
        try:
            if uploaded.type=='text/csv':
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            st.write('Preview:', df.head())
            if st.button('Process File'):
                out = inward_split.process_df(df)
                st.success('Processed. Download below.')
                st.download_button('Download Processed Excel', data=inward_split.to_excel_bytes(out), file_name=f'Processed_Percentage_{datetime.date.today()}.xlsx')
        except Exception as e:
            st.error('Failed to read file: ' + str(e))
elif page=='SKU Creation':
    st.header('SKU Creation - Generate SKUs and allocations')
    uploaded = st.file_uploader('Upload SKU input Excel', type=['xlsx','csv'])
    if uploaded:
        try:
            if uploaded.type=='text/csv':
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            st.write('Preview:', df.head())
            if st.button('Generate SKUs'):
                out = sku_creation.process_input(df)
                st.success('Generated. Download below.')
                st.download_button('Download SKU Allocations', data=sku_creation.to_excel_bytes(out), file_name=f'SKU_Allocations_{datetime.date.today()}.xlsx')
        except Exception as e:
            st.error('Error: ' + str(e))
elif page=='Product Creation':
    st.header('Product Creation - Generate final CSV template')
    col1, col2 = st.columns(2)
    with col1:
        sheet1 = st.file_uploader('Upload Sheet 1 (Product Variant)', key='s1', type=['xlsx','csv'])
        sheet2 = st.file_uploader('Upload Sheet 2 (SKU Master)', key='s2', type=['xlsx','csv'])
    with col2:
        keywords = st.text_input('Keywords (comma/semicolon/colon separated)', 'blk,ble,trn')
        styleid = st.text_input('Style ID (manual)', 'PM86')
    if st.button('Create Products'):
        if not sheet1 or not sheet2:
            st.error('Please upload both files')
        else:
            try:
                df1 = pd.read_excel(sheet1) if sheet1.type!='text/csv' else pd.read_csv(sheet1)
                df2 = pd.read_excel(sheet2) if sheet2.type!='text/csv' else pd.read_csv(sheet2)
                out = product_creation.process_sheets(df1, df2, keywords, styleid)
                st.download_button('Download Final CSV', data=product_creation.to_csv_bytes(out), file_name=f'Final_Product_Creation_{datetime.date.today()}.csv')
            except Exception as e:
                st.error('Error: ' + str(e))
elif page=='PDF Extractor':
    st.header('PDF Keyword Extractor')
    files = st.file_uploader('Upload PDFs', accept_multiple_files=True, type=['pdf'])
    if files and st.button('Extract Pages'):
        try:
            out_bytes = pdf_extractor.extract_pages(files)
            st.download_button('Download Extracted PDF', data=out_bytes, file_name=f'Extracted_Pages_{datetime.date.today()}.pdf', mime='application/pdf')
        except Exception as e:
            st.error('Error: ' + str(e))
elif page=='Image -> Excel':
    st.header('Image to Excel (OCR)')
    imgs = st.file_uploader('Upload images', accept_multiple_files=True, type=['png','jpg','jpeg'])
    if imgs and st.button('Convert Images'):
        try:
            out_bytes = image_to_excel.process_images_to_excel(imgs)
            st.download_button('Download Excel', data=out_bytes, file_name=f'Image_to_Excel_{datetime.date.today()}.xlsx')
        except Exception as e:
            st.error('Error: ' + str(e))
elif page=='Admin':
    st.header('Admin Panel (Protected)')
    username = st.text_input('Admin username')
    password = st.text_input('Admin password', type='password')
    if st.button('Login'):
        if username=='Dhinesh' and password=='Dhinesh@143':
            st.success('Authenticated as admin ✅')
            st.subheader('Color Mappings (sample)')
            st.write('You can extend this in future - currently stored in memory for demo')
            if st.button('Show system info'):
                st.write({'app':'Technosport Internal Suite','version':'1.0'})
        else:
            st.error('Invalid credentials')
