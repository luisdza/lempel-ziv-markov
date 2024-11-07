# LZMA Compression Visualiser

This project is a ShinyLive application for visualizing the LZMA compression algorithm. It allows users to input data, adjust compression parameters, and observe how the LZMA compression works in real-time.

## Features
- Input data to compress
- Adjust various compression parameters
- Visualize compression ratio and time
- Display detailed compression process information

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/luisdza/lempel-ziv-markov.git
    cd lempel-ziv-markov
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Run the application:
    ```sh
    python app.py
    ```

2. Open your web browser and navigate to `http://localhost:8000` to access the application.

## Usage

- Enter the data you want to compress in the "Enter Data to Compress" text area.
- Adjust the compression parameters using the provided sliders and dropdowns.
- The application will display a plot showing the original and compressed sizes, along with the compression ratio and time.
- Detailed compression information will be displayed below the plot if the corresponding switches are enabled.

## Dependencies

- Python 3.x
- `shinylive`
- `matplotlib`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.