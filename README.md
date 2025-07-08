# mr Classes Visualization

A comprehensive Python tool for visualizing Collatz sequences and their m-transforms with automated mr-pair detection and dual-panel analysis charts. Most interesting results are obtained while using values for n within the same class. These values can be taken from [here](https://github.com/hhvvjj/collatz-mr-classes-extractor/tree/main/values)

## Features

This program generates detailed visualizations of Collatz sequences, applying the m-transform `m = (c - p) / 2` where `p = 2` if `c` is even, `p = 1` if `c` is odd, and provides comprehensive analysis of sequence patterns and mr-pair occurrences.

- **Dual-Panel Visualization**: Side-by-side Collatz sequences and m-transform analysis
- **mr-Pair Detection**: Automatic identification of first repeated values in m-sequences
- **Interactive Analysis**: Real-time matplotlib visualization with detailed annotations
- **High-Quality Output**: Professional PDF generation with 600 DPI resolution
- **Multiple Sequences**: Simultaneous analysis of multiple starting values
- **Detailed Console Output**: Comprehensive numerical analysis and sequence breakdowns
- **Adaptive Scaling**: Intelligent axis configuration based on value ranges
- **Pattern Recognition**: Visual highlighting of critical sequence regions

## Dependencies

### Required Python Packages
```bash
pip install matplotlib numpy argparse
```

### System Requirements
- Python 3.6 or higher
- At least 1GB RAM for large sequences
- Display support for matplotlib (X11/Wayland on Linux, native on macOS)

## Installation

```bash
# Clone the repository
git clone https://github.com/hhvvjj/collatz-sequence-visualizer.git
cd collatz-sequence-visualizer
```

## Usage

```bash
python mr_classes_visualization.py "<numbers>"
```

### Arguments
- `numbers`: Comma-separated list of positive integers (required)

### Input Formats
```bash
# Both formats accepted
python mr_classes_visualization.py "27,31"    # No spaces
python mr_classes_visualization.py "27, 31"   # With spaces
```

### Example

```bash
# Analyze classic Collatz starting points
python mr_classes_visualization.py "27,31"
```

## Output

### Console Analysis
```
Generating Collatz analysis for: [27, 41]

=== Analysis for n=27 ===
Collatz sequence: [27, 82, 41, 124, 62, 31, 94, 47, 142, 71, 214, 107, 322, 161, 484, 242, 121, 364, 182, 91, 274, 137, 412, 206, 103, 310, 155, 466, 233, 700, 350, 175, 526, 263, 790, 395, 1186, 593, 1780, 890, 445, 1336, 668, 334, 167, 502, 251, 754, 377, 1132, 566, 283, 850, 425, 1276, 638, 319, 958, 479, 1438, 719, 2158, 1079, 3238, 1619, 4858, 2429, 7288, 3644, 1822, 911, 2734, 1367, 4102, 2051, 6154, 3077, 9232, 4616, 2308, 1154, 577, 1732, 866, 433, 1300, 650, 325, 976, 488, 244, 122, 61, 184, 92, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1, 4, 2, 1]
Collatz sequence reversed: [1, 2, 4, 1, 2, 4, 8, 16, 5, 10, 20, 40, 80, 160, 53, 106, 35, 70, 23, 46, 92, 184, 61, 122, 244, 488, 976, 325, 650, 1300, 433, 866, 1732, 577, 1154, 2308, 4616, 9232, 3077, 6154, 2051, 4102, 1367, 2734, 911, 1822, 3644, 7288, 2429, 4858, 1619, 3238, 1079, 2158, 719, 1438, 479, 958, 319, 638, 1276, 425, 850, 283, 566, 1132, 377, 754, 251, 502, 167, 334, 668, 1336, 445, 890, 1780, 593, 1186, 395, 790, 263, 526, 175, 350, 700, 233, 466, 155, 310, 103, 206, 412, 137, 274, 91, 182, 364, 121, 242, 484, 161, 322, 107, 214, 71, 142, 47, 94, 31, 62, 124, 41, 82, 27]
m sequence: 13, 40, 20, 61, 30, 15, 46, 23, 70, 35, 106, 53, 160, 80, 241, 120, [60], 181, 90, 45, 136, 68, 205, 102, 51, 154, 77, 232, 116, 349, 174, 87, 262, 131, 394, 197, 592, 296, 889, 444, 222, 667, 333, 166, 83, 250, 125, 376, 188, 565, 282, 141, 424, 212, 637, 318, 159, 478, 239, 718, 359, 1078, 539, 1618, 809, 2428, 1214, 3643, 1821, 910, 455, 1366, 683, 2050, 1025, 3076, 1538, 4615, 2307, 1153, 576, 288, 865, 432, 216, 649, 324, 162, 487, 243, 121, [60], 30, 91, 45, 22, 11, 34, 17, 52, 26, 79, 39, 19, 9, 4, 2, 7, 3, 1, 0, 0, 1, 0
m inverted: 0, 1, 0, 0, 1, 3, 7, 2, 4, 9, 19, 39, 79, 26, 52, 17, 34, 11, 22, 45, 91, 30, [60], 121, 243, 487, 162, 324, 649, 216, 432, 865, 288, 576, 1153, 2307, 4615, 1538, 3076, 1025, 2050, 683, 1366, 455, 910, 1821, 3643, 1214, 2428, 809, 1618, 539, 1078, 359, 718, 239, 478, 159, 318, 637, 212, 424, 141, 282, 565, 188, 376, 125, 250, 83, 166, 333, 667, 222, 444, 889, 296, 592, 197, 394, 131, 262, 87, 174, 349, 116, 232, 77, 154, 51, 102, 205, 68, 136, 45, 90, 181, [60], 120, 241, 80, 160, 53, 106, 35, 70, 23, 46, 15, 30, 61, 20, 40, 13
First mr value: 60
mr positions in original m sequence: 16, 91
mr positions in inverted m sequence: 22, 97

=== Analysis for n=41 ===
Collatz sequence: [41, 124, 62, 31, 94, 47, 142, 71, 214, 107, 322, 161, 484, 242, 121, 364, 182, 91, 274, 137, 412, 206, 103, 310, 155, 466, 233, 700, 350, 175, 526, 263, 790, 395, 1186, 593, 1780, 890, 445, 1336, 668, 334, 167, 502, 251, 754, 377, 1132, 566, 283, 850, 425, 1276, 638, 319, 958, 479, 1438, 719, 2158, 1079, 3238, 1619, 4858, 2429, 7288, 3644, 1822, 911, 2734, 1367, 4102, 2051, 6154, 3077, 9232, 4616, 2308, 1154, 577, 1732, 866, 433, 1300, 650, 325, 976, 488, 244, 122, 61, 184, 92, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1, 4, 2, 1]
Collatz sequence reversed: [1, 2, 4, 1, 2, 4, 8, 16, 5, 10, 20, 40, 80, 160, 53, 106, 35, 70, 23, 46, 92, 184, 61, 122, 244, 488, 976, 325, 650, 1300, 433, 866, 1732, 577, 1154, 2308, 4616, 9232, 3077, 6154, 2051, 4102, 1367, 2734, 911, 1822, 3644, 7288, 2429, 4858, 1619, 3238, 1079, 2158, 719, 1438, 479, 958, 319, 638, 1276, 425, 850, 283, 566, 1132, 377, 754, 251, 502, 167, 334, 668, 1336, 445, 890, 1780, 593, 1186, 395, 790, 263, 526, 175, 350, 700, 233, 466, 155, 310, 103, 206, 412, 137, 274, 91, 182, 364, 121, 242, 484, 161, 322, 107, 214, 71, 142, 47, 94, 31, 62, 124, 41]
m sequence: 20, 61, 30, 15, 46, 23, 70, 35, 106, 53, 160, 80, 241, 120, [60], 181, 90, 45, 136, 68, 205, 102, 51, 154, 77, 232, 116, 349, 174, 87, 262, 131, 394, 197, 592, 296, 889, 444, 222, 667, 333, 166, 83, 250, 125, 376, 188, 565, 282, 141, 424, 212, 637, 318, 159, 478, 239, 718, 359, 1078, 539, 1618, 809, 2428, 1214, 3643, 1821, 910, 455, 1366, 683, 2050, 1025, 3076, 1538, 4615, 2307, 1153, 576, 288, 865, 432, 216, 649, 324, 162, 487, 243, 121, [60], 30, 91, 45, 22, 11, 34, 17, 52, 26, 79, 39, 19, 9, 4, 2, 7, 3, 1, 0, 0, 1, 0
m inverted: 0, 1, 0, 0, 1, 3, 7, 2, 4, 9, 19, 39, 79, 26, 52, 17, 34, 11, 22, 45, 91, 30, [60], 121, 243, 487, 162, 324, 649, 216, 432, 865, 288, 576, 1153, 2307, 4615, 1538, 3076, 1025, 2050, 683, 1366, 455, 910, 1821, 3643, 1214, 2428, 809, 1618, 539, 1078, 359, 718, 239, 478, 159, 318, 637, 212, 424, 141, 282, 565, 188, 376, 125, 250, 83, 166, 333, 667, 222, 444, 889, 296, 592, 197, 394, 131, 262, 87, 174, 349, 116, 232, 77, 154, 51, 102, 205, 68, 136, 45, 90, 181, [60], 120, 241, 80, 160, 53, 106, 35, 70, 23, 46, 15, 30, 61, 20
First mr value: 60
mr positions in original m sequence: 14, 89
mr positions in inverted m sequence: 22, 97
High-resolution PDF saved as: class_mr_60_visualization.pdf
```

## Visualization Features

### Left Panel: Collatz Sequences
- **Reversed sequences**: Shows how sequences grow from 1 to starting value
- **Multiple overlays**: Represents different starting points simultaneously

### Right Panel: m-Transform Sequences
- **Reversed sequences**: Shows how sequences grow from o to starting value
- **Multiple overlays**: Represents different starting points simultaneously
- **Pattern detection**: Automatic mr-pair identification and highlighting
- **Critical point marking**: Visual indicators for maximum values
- **Position labeling**: Precise index annotations for analysis
- **Region analysis**: Highlighted zones between repetition points

## Research Applications

This tool is designed for researchers and educators studying:

- **Collatz Sequence Dynamics**: Visual understanding of sequence evolution
- **Transform Analysis**: Behavior of m-transforms and repetition patterns
- **Educational Visualization**: Clear, annotated charts for teaching
- **Pattern Recognition**: Identification of sequence structures and regularities
- **Comparative Analysis**: Side-by-side comparison of multiple sequences

Best application of this tool is obtaned representing values from the diffrerent 42 mr classes. For instance, for mr=1821, some values for n are:
```bash
python mr_classes_visualization.py "3643,7286,14572,19429,25905,29144"
```

## Algorithm Details

### Core Visualization
1. **Sequence Generation**: Standard 3n+1 Collatz sequence with trivial cycle
2. **m-Transform**: Apply `m = (c-p)/2` transformation
3. **Reversal Analysis**: Invert sequences to show growth patterns
4. **mr-Pair Detection**: Identify first repeated m-values
5. **Critical Point Analysis**: Find maximum values in key regions
6. **Annotation System**: Intelligent label positioning to avoid overlaps

### Visualization Strategy
- **Color Coding**: Powers-of-2 based color assignment for distinctiveness
- **Adaptive Layout**: Dynamic axis scaling based on data ranges
- **Anti-Overlap**: Smart label positioning to prevent visual clutter
- **High-Quality Output**: Professional PDF generation with vector graphics

## Research Background

This implementation provides visual analysis of the Collatz conjecture and related transforms:

- **Collatz Sequence**: The classic 3n+1 problem visualization
- **m-Transform**: Reveals predefined and standardized paths based on 42 mr classes
- **mr-Pair Analysis**: Studies repetition patterns in transformed sequences
- **Growth Visualization**: Shows sequence evolution in reverse chronological order

The visualization approach enables pattern recognition that may not be apparent in numerical analysis alone.

**Reference:** The complete theoretical framework is detailed in the research paper: http://dx.doi.org/10.5281/zenodo.15546925

## Contributing

Contributions are welcome! Areas of interest:

- Additional visualization modes and analysis features
- Performance optimizations for very large sequences
- Enhanced annotation and labeling systems

## Academic Citation

For academic use, please cite both the original theoretical work and this implementation.

## License

CC-BY-NC-SA 4 License - see LICENSE file for details.

## Contact

For questions about the algorithm implementation or mathematical details drop me an email.