﻿# xml-product-scrapper

## Description

This project is a Python script that parses XML files containing product information and imports the data into a MongoDB database. It connects to a MongoDB instance, verifies the connection, and performs periodic updates of product data.

## Features

- Parse product data from XML files.
- Connect to MongoDB and handle data insertion and updates.
- Scheduled execution for periodic updates.
- Error handling for connection issues and XML parsing.

## Prerequisites

- Python 3.x
- MongoDB instance (local or remote)
- Required Python packages (schedule, pymongo)

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd xml-product-scrapper
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install required packages**:
    ```bash
    pip install pymongo schedule
    ```

## Usage

1. **Prepare your XML file** with product data. The XML structure should be as follows:
    ```xml
    <Products>
        <Product ProductId="example_id">
            <Name>Example Product</Name>
            <Images>
                <Image Path="image1.jpg" />
                <Image Path="image2.jpg" />
            </Images>
            <ProductDetails>
                <ProductDetail Name="Price" Value="100,00" />
                <ProductDetail Name="DiscountedPrice" Value="80,00" />
                <ProductDetail Name="ProductType" Value="Example Type" />
                <ProductDetail Name="Quantity" Value="10" />
                <ProductDetail Name="Color" Value="Red" />
                <ProductDetail Name="Series" Value="Example Series" />
                <ProductDetail Name="Season" Value="2024" />
            </ProductDetails>
            <Description>This is an example product description.</Description>
        </Product>
    </Products>
    ```

2. **Run the script** with the XML file path and MongoDB connection string as arguments:
    ```bash
    python scrapper.py "path/to/products.xml" "mongodb://username:password@host:port/database"
    ```

## Scheduling

The script is set to run the import process every hour. You can modify the scheduling interval by changing the `schedule.every(1).hour.do(process_products)` line in the code.

## Error Handling

- If the MongoDB connection string is invalid or the database is unreachable, the script will print an error message and exit.
- If the XML file isn't provided or cannot be parsed, the script will raise an exception, and you will need to check the XML structure.

## Author

Ahmet Burak Karhan

