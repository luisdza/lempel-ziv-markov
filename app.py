import lzma
import numpy as np
import matplotlib.pyplot as plt
from shiny import App, render, ui
import time

# LZMA documentation: https://docs.python.org/3/library/lzma.html

# Create UI for LZMA Compression Visualiser
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_text_area("input_data", "Enter Data to Compress", rows=5, value="Hello, LZMA! This is a compression test."),
        ui.input_slider("level", "Compression Level", min=0, max=9, value=6),
        ui.input_slider("dictionary_size", "Dictionary Size (KB)", min=4, max=1536, value=32, step=4),
        ui.input_slider("lc", "Literal Context Bits (lc)", min=0, max=4, value=3),
        ui.input_slider("lp", "Literal Position Bits (lp)", min=0, max=4, value=0),
        ui.input_slider("pb", "Position Bits (pb)", min=0, max=4, value=2),
        ui.input_select("mode", "Compression Mode", choices=["MODE_FAST", "MODE_NORMAL"], selected="MODE_NORMAL"),
        ui.input_slider("nice_len", "Nice Length", min=1, max=273, value=64),
        ui.input_select("mf", "Match Finder", choices=["MF_HC3", "MF_HC4", "MF_BT2", "MF_BT3", "MF_BT4"], selected="MF_BT4"),
        ui.input_slider("depth", "Maximum Search Depth", min=0, max=100, value=0),
        ui.input_switch("show_details", "Show Compression Details", value=True),
        ui.input_switch("show_time", "Show Compression Time", value=True),
    ),
    ui.output_plot("compression_plot"),
    ui.output_text("compression_summary"),
    title="LZMA Compression Visualiser"
)

# Define server logic for compression and visualisation
def server(input, output, session):
    @render.plot
    def compression_plot():
        # Validate lc + lp <= 4
        if input.lc() + input.lp() > 4:
            raise ValueError("The sum of lc (Literal Context Bits) and lp (Literal Position Bits) must be at most 4.")
        # Get input data and compression parameters
        data = input.input_data().encode('utf-8')
        level = input.level()
        dict_size = input.dictionary_size() * 1024
        lc = input.lc()
        lp = input.lp()
        pb = input.pb()
        mode = lzma.MODE_FAST if input.mode() == "MODE_FAST" else lzma.MODE_NORMAL
        nice_len = input.nice_len()
        mf = input.mf()
        depth = input.depth()
        
        # Compress data with LZMA
        start_time = time.time()
        compressor = lzma.LZMACompressor(format=lzma.FORMAT_XZ, filters=[{
            'id': lzma.FILTER_LZMA2,
            'dict_size': dict_size,
            'lc': lc,
            'lp': lp,
            'pb': pb
        }])
        compressed_parts = []
        chunk_size = 1024
        for i in range(0, len(data), chunk_size):
            compressed_parts.append(compressor.compress(data[i:i+chunk_size]))
        compressed_parts.append(compressor.flush())
        compressed_data = b"".join(compressed_parts)
        end_time = time.time()
        compression_time = end_time - start_time
        
        # Calculate compression ratio
        original_size = len(data)
        compressed_size = len(compressed_data)
        compression_ratio = compressed_size / original_size if original_size > 0 else 1
        
        # Visualise compression ratio
        fig, ax = plt.subplots()
        ax.bar(["Original Size", "Compressed Size"], [original_size, compressed_size], color=["blue", "red"])
        ax.set_ylabel("Size (bytes)")
        ax.set_title(f"Compression Level: {level}, Compression Ratio: {compression_ratio:.2f}")
        if input.show_time():
            ax.text(0.5, 0.9, f"Compression Time: {compression_time:.4f} seconds", transform=ax.transAxes, ha='center', fontsize=10, color='green')
        return fig
    
    @render.text
    def compression_summary():
        # Validate lc + lp <= 4
        if input.lc() + input.lp() > 4:
            return "Error: The sum of lc (Literal Context Bits) and lp (Literal Position Bits) must be at most 4."
        # Get input data and compression parameters
        data = input.input_data().encode('utf-8')
        level = input.level()
        dict_size = input.dictionary_size() * 1024
        lc = input.lc()
        lp = input.lp()
        pb = input.pb()
        mode = lzma.MODE_FAST if input.mode() == "MODE_FAST" else lzma.MODE_NORMAL
        nice_len = input.nice_len()
        mf = input.mf()
        depth = input.depth()
        
        # Compress data with LZMA
        start_time = time.time()
        compressor = lzma.LZMACompressor(format=lzma.FORMAT_XZ, filters=[{
            'id': lzma.FILTER_LZMA2,
            'dict_size': dict_size,
            'lc': lc,
            'lp': lp,
            'pb': pb
        }])
        compressed_parts = []
        chunk_size = 1024
        for i in range(0, len(data), chunk_size):
            compressed_parts.append(compressor.compress(data[i:i+chunk_size]))
        compressed_parts.append(compressor.flush())
        compressed_data = b"".join(compressed_parts)
        end_time = time.time()
        compression_time = end_time - start_time
        
        # Calculate sizes and ratio
        original_size = len(data)
        compressed_size = len(compressed_data)
        compression_ratio = compressed_size / original_size if original_size > 0 else 1
        
        details = (
            f"Original Size: {original_size} bytes\n"
            f"Compressed Size: {compressed_size} bytes\n"
            f"Compression Ratio: {compression_ratio:.2f}\n"
            f"Compression Level: {level}\n"
            f"Dictionary Size: {dict_size // 1024} KB\n"
            f"Literal Context Bits (lc): {lc}\n"
            f"Literal Position Bits (lp): {lp}\n"
            f"Position Bits (pb): {pb}\n"
            f"Mode: {input.mode()}\n"
            f"Nice Length: {nice_len}\n"
            f"Match Finder: {mf}\n"
            f"Depth: {depth}\n"
        )
        if input.show_details():
            details += "\nCompression Process Details:\n"
            details += f"Chunks Processed: {len(compressed_parts) - 1}\n"
            for idx, part in enumerate(compressed_parts[:-1]):
                details += f"Chunk {idx + 1} Size: {len(part)} bytes\n"
        if input.show_time():
            details += f"\nCompression Time: {compression_time:.4f} seconds"
        
        return details

# Create and run app
app = App(app_ui, server)
