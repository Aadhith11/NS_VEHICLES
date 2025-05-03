import pandas as pd
import re
from datetime import datetime

def parse_vehicle_posts(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split content into individual posts
    posts = content.split('\n\n')
    
    data = []
    for post in posts:
        if not post.strip():
            continue
            
        lines = post.strip().split('\n')
        post_data = {}
        
        # Extract date (assuming it's in the first line)
        date_match = re.search(r'Posted (.*)', lines[0])
        if date_match:
            post_data['Date posted'] = date_match.group(1)
        
        # Extract seller information
        for line in lines:
            if 'Seller:' in line:
                parts = line.split('Seller:')
                if len(parts) > 1:
                    post_data['Seller name'] = parts[1].strip()
            elif 'Location:' in line:
                parts = line.split('Location:')
                if len(parts) > 1:
                    post_data['Seller location'] = parts[1].strip()
            
            # Extract vehicle details and price
            car_info = re.search(r'(\d{4})\s+(\w+)\s+(\w+)', line)
            if car_info:
                post_data['Year'] = car_info.group(1)
                post_data['Make'] = car_info.group(2)
                post_data['Model'] = car_info.group(3)
            
            price_match = re.search(r'\$?([\d,]+)', line)
            if price_match and 'Price (CAD)' not in post_data:
                price = price_match.group(1).replace(',', '')
                post_data['Price (CAD)'] = float(price)
        
        if post_data:
            data.append(post_data)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Reorder columns
    columns = ['Date posted', 'Seller name', 'Seller location', 'Year', 'Make', 'Model', 'Price (CAD)']
    df = df.reindex(columns=columns)
    
    return df

def main():
    input_file = 'vehicle_data.txt'  # Update this with your input file name
    output_file = 'ns_vehicles.xlsx'
    
    df = parse_vehicle_posts(input_file)
    df.to_excel(output_file, index=False)
    print(f"Data has been exported to {output_file}")

if __name__ == "__main__":
    main()
