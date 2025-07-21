import streamlit as st
import pandas as pd
import base64
from io import StringIO

def get_csv_download_link(df, filename="tohands_inventory.csv"):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    return href

def main():
    """
    The main function to run the Streamlit app.
    """
    st.title("Tohands Inventory CSV Creator")

    st.write("""
    This app helps you create a CSV file with your product inventory data in the format required by the Tohands smart calculator.
    Fill in the details for each product below and click 'Add Product'. Once you have added all your products, you can download the complete CSV file.
    """)

    # Initialize session state to store the dataframe
    if 'product_df' not in st.session_state:
        st.session_state.product_df = pd.DataFrame(columns=[
            'SKU_ID', 'PRODUCT_NAME', 'PRODUCT_MRP', 'PRODUCT_SELLING_PRICE',
            'PRODUCT_CATEGORY_ID', 'PRODUCT_UNIT_ID', 'PRODUCT_QUANTITY'
        ])

    st.header("Enter Product Details")

    # Create a form for user input
    with st.form("product_form", clear_on_submit=True):
        sku_id = st.text_input("SKU ID")
        product_name = st.text_input("Product Name")
        product_mrp = st.number_input("Product MRP", min_value=0.0, format="%.2f")
        product_selling_price = st.number_input("Product Selling Price", min_value=0.0, format="%.2f")
        product_category_id = st.text_input("Product Category ID")
        product_unit_id = st.text_input("Product Unit ID")
        product_quantity = st.number_input("Product Quantity", min_value=0, step=1)

        # Submit button for the form
        submitted = st.form_submit_button("Add Product")

        if submitted:
            new_product = {
                'SKU_ID': sku_id,
                'PRODUCT_NAME': product_name,
                'PRODUCT_MRP': product_mrp,
                'PRODUCT_SELLING_PRICE': product_selling_price,
                'PRODUCT_CATEGORY_ID': product_category_id,
                'PRODUCT_UNIT_ID': product_unit_id,
                'PRODUCT_QUANTITY': product_quantity
            }
            new_df = pd.DataFrame([new_product])
            st.session_state.product_df = pd.concat([st.session_state.product_df, new_df], ignore_index=True)
            st.success("Product added successfully!")

    st.header("Current Inventory Data")

    # Display the dataframe
    if not st.session_state.product_df.empty:
        st.dataframe(st.session_state.product_df)

        # Add a download button
        st.markdown(get_csv_download_link(st.session_state.product_df), unsafe_allow_html=True)
    else:
        st.info("No products added yet. Fill the form above to add products.")


if __name__ == "__main__":
    main()
