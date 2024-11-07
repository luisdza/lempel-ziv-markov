from shiny import reactive
from shiny.express import input, render, ui

import lzma
import matplotlib.pyplot as plt
import time

ui.page_opts(title="LZMA Compression Visualiser", fillable=True)

with ui.sidebar(title="Filter controls"):
    ui.input_text_area("input_data", "Enter Data to Compress", rows=5, value="Hello, LZMA! This is a compression test.")
    ui.input_slider("level", "Compression Level", min=0, max=9, value=6)
    ui.input_slider("dictionary_size", "Dictionary Size (KB)", min=4, max=1536, value=32, step=4)
    ui.input_slider("lc", "Literal Context Bits (lc)", min=0, max=4, value=3)
    ui.input_slider("lp", "Literal Position Bits (lp)", min=0, max=4, value=0)
    ui.input_slider("pb", "Position Bits (pb)", min=0, max=4, value=2)
    ui.input_switch("show_details", "Show Compression Details", value=True)
    ui.input_switch("show_time", "Show Compression Time", value=True)

with ui.layout_columns():
    @render.plot
    def compression_plot():
        # Validate lc + lp <= 4
        if input.lc() + input.lp() > 4:
            raise ValueError("The sum of lc (Literal Context Bits) and lp (Literal Position Bits) must be at most 4.")
        # Get input data and compression parameters
        data = input.input_data().encode('utf-8')
        dict_size = input.dictionary_size() * 1024
        lc = input.lc()
        lp = input.lp()
        pb = input.pb()
        
        # Compress data with LZMA
        start_time = time.time()
        compressor = lzma.LZMACompressor(format=lzma.FORMAT_XZ, filters=[{
            'id': lzma.FILTER_LZMA2,
            'dict_size': dict_size,
            'lc': lc,
            'lp': lp,
            'pb': pb
        }])
        compressed_data = compressor.compress(data) + compressor.flush()
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
        ax.set_title(f"Compression Ratio: {compression_ratio:.2f}")
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
        dict_size = input.dictionary_size() * 1024
        lc = input.lc()
        lp = input.lp()
        pb = input.pb()
        
        # Compress data with LZMA
        start_time = time.time()
        compressor = lzma.LZMACompressor(format=lzma.FORMAT_XZ, filters=[{
            'id': lzma.FILTER_LZMA2,
            'dict_size': dict_size,
            'lc': lc,
            'lp': lp,
            'pb': pb
        }])
        compressed_data = compressor.compress(data) + compressor.flush()
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
            f"Dictionary Size: {dict_size // 1024} KB\n"
            f"Literal Context Bits (lc): {lc}\n"
            f"Literal Position Bits (lp): {lp}\n"
            f"Position Bits (pb): {pb}\n"
        )
        if input.show_details():
            details += f"\nCompression Time: {compression_time:.4f} seconds"
        
        return details