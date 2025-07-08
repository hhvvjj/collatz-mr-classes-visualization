#########################################################################################################
# mr_classes_visualization.py
#
# Implementation to represent graphically the 42 mr classes, their static positions and limits
#
# The complete article can be found on https://doi.org/10.5281/zenodo.15546925
#
#########################################################################################################

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import argparse
import sys

def collatz_sequence(n):
    """
    Generate the Collatz sequence for a given number.
    
    The Collatz conjecture states that for any positive integer n:
    - If n is even: n = n/2
    - If n is odd: n = 3n + 1
    - Continue until reaching 1, then add one iteration of the trivial cycle (1→4→2→1)
    
    Args:
        n (int): Initial number to generate the sequence (must be positive)
        
    Returns:
        list: Complete Collatz sequence including one iteration of trivial cycle
        
    Raises:
        ValueError: If n is not a positive integer
    """
    if n <= 0:
        raise ValueError("Number must be positive")
    
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    
    # Add one iteration of the trivial cycle: 1 -> 4 -> 2 -> 1
    sequence.extend([4, 2, 1])
    
    return sequence

def simple_m_sequence(n):
    """
    Calculate the m-transform sequence from a Collatz sequence.
    
    For each consecutive pair (ci, ci+1) in the Collatz sequence, the m-transform
    calculates: m = (ci - p) // 2, where p is the parity factor:
    - p = 1 if ci is odd (since next step will be 3*ci + 1)
    - p = 2 if ci is even (since next step will be ci // 2)
    
    This transform reveals hidden patterns in Collatz sequences.
    
    Args:
        n (int): Initial number for Collatz sequence
        
    Returns:
        tuple: (collatz_sequence, m_sequence) where m_sequence has one less element
    """
    try:
        collatz_seq = collatz_sequence(n)
        m_sequence = []
        
        for i in range(len(collatz_seq) - 1):
            ci = collatz_seq[i]
            p = 1 if ci % 2 == 1 else 2
            m = (ci - p) // 2
            m_sequence.append(m)
        
        return collatz_seq, m_sequence
    except Exception as e:
        print(f"Error in simple_m_sequence for n={n}: {e}")
        return collatz_sequence(n), []

def find_first_mr_pair(n):
    """
    Find the first repeated value (mr pair) in the m-transform sequence.
    
    The "mr" (m-repeat) value is the first value that appears twice in the m-sequence.
    This repetition often indicates the beginning of cyclic behavior in the transform.
    
    Args:
        n (int): Initial number for analysis
        
    Returns:
        tuple: (mr_value, first_position, second_position) if pair found, None otherwise
               Positions are 0-indexed within the m-sequence
    """
    try:
        collatz_seq, m_sequence = simple_m_sequence(n)
        
        seen = {}  # value -> first position where it appears
        for i, m_val in enumerate(m_sequence):
            if m_val in seen:
                # Found the second occurrence = first mr pair
                return m_val, seen[m_val], i
            seen[m_val] = i
        
        return None  # No pair found
    except Exception:
        return None

def plot_collatz_sequences(numbers):
    """
    Create a dual-panel visualization of Collatz sequences and their m-transforms.
    
    Generates a landscape-oriented PDF with two subplots:
    - Left panel: Reversed Collatz sequences (starting from 1, growing outward)
    - Right panel: Reversed m-transform sequences with mr-pair analysis
    
    The right panel includes special annotations:
    - Black dashed vertical lines at mr-pair positions
    - Yellow shaded region between mr-pair occurrences
    - Blue dot marking maximum value before first mr occurrence
    - Red dot marking maximum value between mr occurrences
    - Labels showing mr value and key positions
    
    Args:
        numbers (list): List of positive integers to analyze and visualize
    """
    # Find the highest mr value from all sequences for filename generation
    highest_mr = 0
    for num in numbers:
        mr_pair = find_first_mr_pair(num)
        if mr_pair is not None:
            mr_value = mr_pair[0]
            if mr_value > highest_mr:
                highest_mr = mr_value
    
    # Generate descriptive filename based on highest mr value found
    pdf_file = f"class_mr_{highest_mr}_visualization.pdf"

    # Create dual-panel figure in landscape orientation for better readability
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Generate distinct colors using powers of 2 pattern for visual clarity
    max_colors = min(len(numbers), 8)
    color_indices = [2**i % 10 for i in range(max_colors)]
    colors = [plt.cm.tab10(i) for i in color_indices]
    colors = colors * ((len(numbers) // max_colors) + 1)
    
    # LEFT PANEL: Reversed Collatz sequences (growth pattern from 1 outward)
    for i, num in enumerate(numbers):
        try:
            sequence = collatz_sequence(num)
            # Reverse to show growth pattern starting from 1
            reversed_sequence = sequence[::-1]
            steps = list(range(1, len(reversed_sequence) + 1))

            ax1.plot(steps, reversed_sequence, '-', 
                    color=colors[i], 
                    linewidth=1)
            
        except ValueError as e:
            print(f"Error with n={num}: {e}")
            continue
    
    ax1.set_xlabel('Number of steps (from 1)')
    ax1.set_ylabel('n Values')
    ax1.set_title('Collatz Sequences Reversed (Growth from 1)')
    ax1.grid(True, alpha=0.3)
    
    # Configure Y-axis scaling and ticks for left panel
    all_values = []
    for i, num in enumerate(numbers):
        try:
            sequence = collatz_sequence(num)
            reversed_sequence = sequence[::-1]
            all_values.extend(reversed_sequence)
        except Exception:
            continue
    
    if all_values:
        y_min = min(all_values)
        y_max = max(all_values)
        
        # Adaptive tick spacing based on value range
        import numpy as np
        range_size = y_max - y_min
        
        if range_size <= 20:
            ticks = list(range(y_min, y_max + 1))
        elif range_size <= 100:
            step = 5 if range_size <= 50 else 10
            ticks = list(range(y_min, y_max + step, step))
        else:
            ticks = np.linspace(y_min, y_max, 10, dtype=int)
            ticks = list(set(ticks))
            ticks.sort()
        
        ax1.set_yticks(ticks)
        margin = range_size * 0.02
        ax1.set_ylim(y_min - margin, y_max + margin)
    
    # Prevent scientific notation on Y-axis
    ax1.ticklabel_format(style='plain', axis='y')
    
    # RIGHT PANEL: m-transform sequences with mr-pair analysis
    mr_labels_info = []  # Store annotation data for the highest mr value
    
    for i, num in enumerate(numbers):
        try:
            # Generate both Collatz and m-transform sequences
            collatz_seq, m_sequence = simple_m_sequence(num)
            
            if not m_sequence:
                continue
            
            # Reverse sequences to show pattern evolution from the end
            reversed_collatz = collatz_seq[::-1]
            reversed_m_sequence = m_sequence[::-1]
            
            # Analyze mr-pair for this number
            mr_pair = find_first_mr_pair(num)
            
            # Print detailed analysis to console
            print(f"\n=== Analysis for n={num} ===")
            print(f"Collatz sequence: {collatz_seq}")
            print(f"Collatz sequence reversed: {reversed_collatz}")
            
            if mr_pair is not None:
                mr_value, first_pos_orig, second_pos_orig = mr_pair
                
                # Create visual markers for mr positions in original sequence
                m_seq_display = []
                for idx, val in enumerate(m_sequence):
                    if idx == first_pos_orig or idx == second_pos_orig:
                        m_seq_display.append(f"[{val}]")  # Bracket mr occurrences
                    else:
                        m_seq_display.append(str(val))
                
                # Calculate mr positions in reversed sequence
                seq_len = len(m_sequence)
                first_pos_inv = seq_len - 1 - second_pos_orig   # Second becomes first
                second_pos_inv = seq_len - 1 - first_pos_orig   # First becomes second
                
                # Create visual markers for mr positions in reversed sequence
                m_inv_display = []
                for idx, val in enumerate(reversed_m_sequence):
                    if idx == first_pos_inv or idx == second_pos_inv:
                        m_inv_display.append(f"[{val}]")
                    else:
                        m_inv_display.append(str(val))
                
                print(f"m sequence: {', '.join(m_seq_display)}")
                print(f"m inverted: {', '.join(m_inv_display)}")
                print(f"First mr value: {mr_value}")
                print(f"mr positions in original m sequence: {first_pos_orig}, {second_pos_orig}")
                print(f"mr positions in inverted m sequence: {first_pos_inv}, {second_pos_inv}")
            else:
                print(f"m sequence: {m_sequence}")
                print(f"m inverted: {reversed_m_sequence}")
                print("No mr pair found")
            
            # Plot m-transform sequence starting from step 0
            steps = list(range(len(reversed_m_sequence)))
            
            # Draw the main sequence line
            ax2.plot(steps, reversed_m_sequence, '-', 
                    color=colors[i], 
                    linewidth=1)
            
            # Add mr-pair analysis annotations if pair exists
            mr_pair = find_first_mr_pair(num)
            if mr_pair is not None:
                mr_value, first_pos_orig, second_pos_orig = mr_pair
                
                # Convert original positions to reversed sequence positions
                seq_len = len(m_sequence)
                first_pos_inv = seq_len - 1 - second_pos_orig
                second_pos_inv = seq_len - 1 - first_pos_orig
                
                # Validate positions are within bounds
                if first_pos_inv < len(reversed_m_sequence) and second_pos_inv < len(reversed_m_sequence):
                    # Mark mr-pair positions with vertical dashed lines
                    ax2.axvline(x=first_pos_inv, color='black', linestyle='--', alpha=0.8, linewidth=2)
                    ax2.axvline(x=second_pos_inv, color='black', linestyle='--', alpha=0.8, linewidth=2)
                    
                    # Highlight the mr-pair region with subtle background
                    ax2.axvspan(first_pos_inv, second_pos_inv, alpha=0.05, color='yellow')
                    
                    # Find maximum values in key regions for analysis
                    # Region 1: From start to first mr occurrence
                    max_before_first_mr = 0
                    max_pos_before = 0
                    for pos in range(0, first_pos_inv + 1):
                        if reversed_m_sequence[pos] > max_before_first_mr:
                            max_before_first_mr = reversed_m_sequence[pos]
                            max_pos_before = pos
                    
                    # Region 2: Between the two mr occurrences
                    max_between_mr = 0
                    max_pos_between = first_pos_inv
                    for pos in range(first_pos_inv, second_pos_inv + 1):
                        if reversed_m_sequence[pos] > max_between_mr:
                            max_between_mr = reversed_m_sequence[pos]
                            max_pos_between = pos
                    
                    # Mark critical points with colored dots
                    ax2.plot(max_pos_before, max_before_first_mr, 'bo', markersize=8, 
                            markerfacecolor='blue', markeredgecolor='darkblue', markeredgewidth=2)
                    ax2.plot(max_pos_between, max_between_mr, 'ro', markersize=8, 
                            markerfacecolor='red', markeredgecolor='darkred', markeredgewidth=2)
                    
                    # Store annotation data for later rendering (only highest mr shown)
                    center_x = (first_pos_inv + second_pos_inv) / 2
                    y_max_fill = ax2.get_ylim()[1]
                    text_y = y_max_fill * 0.85
                    
                    mr_labels_info.append({
                        'x': center_x,
                        'y': text_y,
                        'mr_value': mr_value,
                        'line1_x': first_pos_inv,
                        'line2_x': second_pos_inv,
                        'max_before_first': max_before_first_mr,
                        'max_pos_before': max_pos_before,
                        'max_between': max_between_mr,
                        'max_pos_between': max_pos_between,
                        'max_y_in_area': max(reversed_m_sequence[int(first_pos_inv):int(second_pos_inv)+1]) if int(first_pos_inv) < len(reversed_m_sequence) and int(second_pos_inv) < len(reversed_m_sequence) else 0
                    })
            
        except Exception as e:
            print(f"Error for n={num}: {e}")
            continue
    
    # Render annotations for the sequence with highest mr value only
    if mr_labels_info:
        highest_label = max(mr_labels_info, key=lambda x: x['max_y_in_area'])
        
        # Get current axis boundaries for label positioning
        y_limits = ax2.get_ylim()
        
        # Position main mr label at 5% from top edge
        y_range = y_limits[1] - y_limits[0]
        y_label_pos = y_limits[1] - (y_range * 0.05)
        
        ax2.text(highest_label['x'], y_label_pos, f'mr={highest_label["mr_value"]}', 
                horizontalalignment='center', verticalalignment='center',
                fontsize=8, fontweight='bold', color='black',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9, edgecolor='gray'))
        
        # Position line index labels at 15% from top edge
        line1_x = highest_label['line1_x']
        line2_x = highest_label['line2_x']
        y_indices_pos = y_limits[1] - (y_range * 0.15)
        
        # Only show position labels if lines are sufficiently separated to avoid overlap
        if abs(line2_x - line1_x) > 0.1:
            ax2.text(line1_x, y_indices_pos, f'{int(line1_x)}', 
                    horizontalalignment='center', verticalalignment='center',
                    fontsize=7, fontweight='bold', color='black',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='white', alpha=0.9, edgecolor='black'))
            
            ax2.text(line2_x, y_indices_pos, f'{int(line2_x)}', 
                    horizontalalignment='center', verticalalignment='center',
                    fontsize=7, fontweight='bold', color='black',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='white', alpha=0.9, edgecolor='black'))
        
        # Position maximum value labels directly above their corresponding dots
        max_pos_before = highest_label['max_pos_before']
        max_val_before = highest_label['max_before_first']
        max_pos_between = highest_label['max_pos_between']
        max_val_between = highest_label['max_between']
        
        # Calculate vertical offset for labels (8% of range)
        label_offset = y_range * 0.08
        
        # Blue label positioning (maximum before first mr)
        blue_label_y = max_val_before + label_offset
        # Ensure label stays within plot boundaries
        if blue_label_y > y_limits[1] - (y_range * 0.25):
            blue_label_y = max_val_before - label_offset
            va_blue = 'top'
        else:
            va_blue = 'bottom'
        
        ax2.text(max_pos_before, blue_label_y, f'{max_val_before}', 
                horizontalalignment='center', verticalalignment=va_blue,
                fontsize=8, fontweight='bold', color='blue',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9, edgecolor='blue'))
        
        # Red label positioning (maximum between mr occurrences)
        red_label_y = max_val_between + label_offset
        # Ensure label stays within plot boundaries
        if red_label_y > y_limits[1] - (y_range * 0.25):
            red_label_y = max_val_between - label_offset
            va_red = 'top'
        else:
            va_red = 'bottom'
        
        ax2.text(max_pos_between, red_label_y, f'{max_val_between}', 
                horizontalalignment='center', verticalalignment=va_red,
                fontsize=8, fontweight='bold', color='red',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9, edgecolor='red'))
        
        # Handle label overlap by adding horizontal offset when necessary
        if abs(max_pos_before - max_pos_between) < 1.0 and abs(max_val_before - max_val_between) < label_offset:
            # Apply horizontal displacement for overlapping labels
            if max_pos_before < max_pos_between:
                blue_x_offset = -0.3
                red_x_offset = 0.3
            else:
                blue_x_offset = 0.3
                red_x_offset = -0.3
            
            # Find and reposition the blue and red labels
            blue_text = None
            red_text = None
            for text in ax2.texts:
                if text.get_color() == 'blue':
                    blue_text = text
                elif text.get_color() == 'red':
                    red_text = text
            
            if blue_text:
                blue_text.set_position((max_pos_before + blue_x_offset, blue_label_y))
            if red_text:
                red_text.set_position((max_pos_between + red_x_offset, red_label_y))
    
    ax2.set_xlabel('Number of steps (from 0)')
    ax2.set_ylabel('m Values')
    ax2.set_title('m-Transform Sequences Reversed (with mr-pair Analysis)')
    ax2.grid(True, alpha=0.3)
    
    # Configure Y-axis scaling and ticks for right panel
    all_m_values = []
    for i, num in enumerate(numbers):
        try:
            collatz_seq, m_sequence = simple_m_sequence(num)
            reversed_m_sequence = m_sequence[::-1]
            all_m_values.extend(reversed_m_sequence)
        except Exception:
            continue
    
    if all_m_values:
        y_min = min(all_m_values)
        y_max = max(all_m_values)
        
        # Adaptive tick spacing based on value range
        import numpy as np
        range_size = y_max - y_min
        
        if range_size <= 20:
            ticks = list(range(y_min, y_max + 1))
        elif range_size <= 100:
            step = 5 if range_size <= 50 else 10
            ticks = list(range(y_min, y_max + step, step))
        else:
            ticks = np.linspace(y_min, y_max, 10, dtype=int)
            ticks = list(set(ticks))
            ticks.sort()
        
        ax2.set_yticks(ticks)
        margin = max(1, range_size * 0.02)
        ax2.set_ylim(y_min - margin, y_max + margin)
    
    # Prevent scientific notation on Y-axis
    ax2.ticklabel_format(style='plain', axis='y')
    
    # Add descriptive overall title
    fig.suptitle(f'Collatz Sequence Analysis: mr-class {highest_mr}', fontsize=12, fontweight='bold')
    
    # Optimize layout for readability
    plt.tight_layout()
    
    # Save as high-quality PDF with descriptive filename
    with PdfPages(pdf_file, keep_empty=False) as pdf:
        pdf.savefig(fig, bbox_inches='tight', orientation='landscape', dpi=600)
        print(f"High-resolution PDF saved as: {pdf_file}")
    
    plt.show()

def main():
    """
    Command-line interface for the Collatz sequence visualization tool.
    
    Parses command-line arguments to accept a comma-separated list of positive integers
    and generates comprehensive visualizations of their Collatz sequences and m-transforms.
    
    The tool validates input and provides helpful error messages for common mistakes.
    """
    parser = argparse.ArgumentParser(
        description='Visualize Collatz sequences and their m-transforms with mr-pair analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python collatz_plotter.py "3,7,12,27"     # Basic usage
  python collatz_plotter.py "3, 7, 12, 27"  # Spaces after commas are OK
  python collatz_plotter.py "5, 10, 15"     # Analyze different starting points
  python collatz_plotter.py "1,2,3,4,5"     # Compare sequential numbers

Output:
  - Console: Detailed numerical analysis of sequences and mr-pairs
  - PDF: High-quality dual-panel visualization saved automatically
  - Display: Interactive matplotlib window for immediate viewing
        """
    )
    
    parser.add_argument('numbers', type=str, 
                       help='Positive integers separated by commas (spaces optional)')
    
    args = parser.parse_args()
    
    # Parse and validate the comma-separated number list
    try:
        # Handle both "1,2,3" and "1, 2, 3" formats
        if ', ' in args.numbers:
            number_strings = [x.strip() for x in args.numbers.split(', ')]
        else:
            number_strings = [x.strip() for x in args.numbers.split(',')]
        
        # Convert to integers, filtering out empty strings
        numbers = [int(x) for x in number_strings if x]
        
    except ValueError:
        print("Error: List must contain only integers separated by commas")
        print("Example: '3,7,12,27' or '3, 7, 12, 27'")
        sys.exit(1)
    
    # Validate that at least one number was provided
    if not numbers:
        print("Error: You must provide at least one number")
        parser.print_help()
        sys.exit(1)
    
    # Validate that all numbers are positive (Collatz conjecture domain)
    if any(n <= 0 for n in numbers):
        print("Error: All numbers must be positive integers")
        sys.exit(1)
    
    print(f"Generating Collatz analysis for: {numbers}")
    
    try:
        plot_collatz_sequences(numbers)
    except Exception as e:
        print(f"Error generating visualization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()