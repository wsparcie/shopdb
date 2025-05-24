# ShopDataMaster

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![BCrypt](https://img.shields.io/badge/BCrypt-4.1.2-red.svg)](https://pypi.org/project/bcrypt/)
[![Colorama](https://img.shields.io/badge/Colorama-0.4.6-green.svg)](https://pypi.org/project/colorama/)
[![Status](https://img.shields.io/badge/Status-Alpha-yellow.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A simple console-based shop management system with automated data generation and secure login capabilities.

## Features

- **Secure Authentication**: BCrypt-based login system
- **Data Management**: 
  - Users
  - Products
  - Orders
  - Reviews
- **Automated Generation**: Random data generation for testing
- **Interactive Console**: Colorful terminal interface
- **Data Persistence**: File-based storage system

## Features in Detail

### Data Management
- **User Management**:
  - Personal information storage
  - Address tracking
  - Contact details
- **Product Inventory**:
  - Stock tracking
  - Price management
  - Product descriptions
  - Brand and type categorization
- **Order Processing**:
  - Multi-product orders
  - Quantity tracking
  - Total price calculation
  - Stock updates
- **Review System**:
  - Rating system
  - User comments
  - Average rating calculation
  - Product feedback

### Technical Features
- **Error Handling**:
  - Robust exception management
  - File operation safety
  - Data validation
- **Data Generation**:
  - Random user data
  - Product inventory generation
  - Order simulation
  - Review creation
- **Security**:
  - BCrypt password hashing
  - Secure login system
  - Session management

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the program:
   ```bash
   python __shopdb__.py
   ```

3. First-time setup:
   - Create a login credential when prompted
   - System will generate sample data automatically

4. Available commands:
   - `us`: Manage users
   - `pd`: Manage products
   - `ord`: Manage orders
   - `rev`: Manage reviews
   - `sv`: Save changes
   - `ex`: Exit program

5. Data operations:
   - `ls`: List items
   - `sr`: Sort items
   - `fl`: Filter items
   - `add`: Add new item
   - `del`: Delete item
   - `mdf`: Modify item

## Prerequisites

- Python 3.12+
- Required Python packages:
  ```
  bcrypt>=4.1.2
  colorama>=0.4.6
  ```

## Screenshots

![Console Interface](https://github.com/user-attachments/assets/443b3ac7-b722-4bfe-af7f-f87bb2a054ec)
![Orders Management](https://github.com/user-attachments/assets/45330294-6e9a-41bb-bf08-19a39f578c9e)
![Products View](https://github.com/user-attachments/assets/6b9c4b23-e934-49b0-9555-e006e865bf40)
![Order Details](https://github.com/user-attachments/assets/eb4488cf-9d12-4b23-a019-5742f81587f2)

## License

MIT License - feel free to use and modify as needed.
