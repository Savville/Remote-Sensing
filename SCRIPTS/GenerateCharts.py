"""
Generate publication-quality charts for Spectral Unmixing paper
Creates all figures referenced in the IEEE GRSS manuscript

Data sources:
- Narok_Crops Soil Veg and Shadow Dynamics.csv
- Kajiado_Shrub Soil Veg and Shadow Dynamics.csv
- Turkana_Bare Soil Veg and Shadow Dynamics.csv
- *_Model Accuracy RMSE.csv files

Outputs:
- FIGURE 3: Narok Temporal Dynamics (4-panel time series)
- FIGURE 4: Multi-Site Comparison (6-panel comparison)
- Additional individual site charts
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Windows
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from pathlib import Path
import numpy as np

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['legend.frameon'] = False
plt.rcParams['legend.fontsize'] = 9

# Define paths relative to script location
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / 'DATA'
OUTPUT_DIR = SCRIPT_DIR / 'IMAGES'
OUTPUT_DIR.mkdir(exist_ok=True)


def load_data():
    """Load all CSV data files"""
    data = {}
    
    # Load fraction dynamics
    data['narok_dynamics'] = pd.read_csv(
        DATA_DIR / 'Narok_Crops Soil Veg and Shadow Dynamics.csv',
        parse_dates=['system:time_start']
    )
    data['kajiado_dynamics'] = pd.read_csv(
        DATA_DIR / 'Kajiado_Shrub Soil Veg and Shadow Dynamics.csv',
        parse_dates=['system:time_start']
    )
    data['turkana_dynamics'] = pd.read_csv(
        DATA_DIR / 'Turkana_Bare Soil Veg and Shadow Dynamics.csv',
        parse_dates=['system:time_start']
    )
    
    # Load RMSE accuracy
    data['narok_rmse'] = pd.read_csv(
        DATA_DIR / 'Narok_Crops Model Accuracy_RMSE.csv',
        parse_dates=['system:time_start']
    )
    data['kajiado_rmse'] = pd.read_csv(
        DATA_DIR / 'Kajiado_Shrub Model Accuracy RMSE.csv',
        parse_dates=['system:time_start']
    )
    data['turkana_rmse'] = pd.read_csv(
        DATA_DIR / 'Turkana_Bare Model Accuracy RMSE.csv',
        parse_dates=['system:time_start']
    )
    
    return data


def create_figure3_narok_temporal(data):
    """
    FIGURE 3: Narok Temporal Dynamics with RMSE
    Four-panel time series showing:
    (A) Soil fraction (red)
    (B) Vegetation fraction (green)
    (C) Shadow fraction (blue)
    (D) RMSE (black)
    """
    narok_dyn = data['narok_dynamics']
    narok_rmse = data['narok_rmse']
    
    # Merge RMSE with dynamics data
    merged = pd.merge(
        narok_dyn, narok_rmse,
        on='system:time_start',
        how='left'
    )
    
    # Create figure with 4 subplots (stacked vertically)
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    fig.suptitle('Narok Agricultural Zone: Temporal Dynamics 2023', 
                 fontsize=14, fontweight='bold', y=0.995)
    
    # Define phenological event dates
    long_rains_onset = pd.Timestamp('2023-03-04')
    harvest = pd.Timestamp('2023-08-01')
    el_nino_onset = pd.Timestamp('2023-11-29')
    
    # (A) Soil fraction
    ax = axes[0]
    ax.plot(merged['system:time_start'], merged['Soil'], 
            color='#D2691E', linewidth=2, marker='o', markersize=4, label='Soil')
    ax.fill_between(merged['system:time_start'], merged['Soil'], 
                     alpha=0.3, color='#D2691E')
    ax.set_ylabel('Soil Fraction', fontweight='bold')
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right')
    
    # Add event markers
    ax.axvline(long_rains_onset, color='blue', linestyle='--', alpha=0.6, linewidth=1.5)
    ax.axvline(harvest, color='orange', linestyle='--', alpha=0.6, linewidth=1.5)
    ax.axvline(el_nino_onset, color='green', linestyle='--', alpha=0.6, linewidth=1.5)
    
    # (B) Vegetation fraction
    ax = axes[1]
    ax.plot(merged['system:time_start'], merged['Veg'], 
            color='#228B22', linewidth=2, marker='s', markersize=4, label='Vegetation')
    ax.fill_between(merged['system:time_start'], merged['Veg'], 
                     alpha=0.3, color='#228B22')
    ax.set_ylabel('Vegetation Fraction', fontweight='bold')
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right')
    
    # Add event markers
    ax.axvline(long_rains_onset, color='blue', linestyle='--', alpha=0.6, linewidth=1.5)
    ax.axvline(harvest, color='orange', linestyle='--', alpha=0.6, linewidth=1.5)
    ax.axvline(el_nino_onset, color='green', linestyle='--', alpha=0.6, linewidth=1.5)
    
    # (C) Shadow fraction
    ax = axes[2]
    ax.plot(merged['system:time_start'], merged['Shadow'], 
            color='#4169E1', linewidth=2, marker='^', markersize=4, label='Shadow')
    ax.fill_between(merged['system:time_start'], merged['Shadow'], 
                     alpha=0.3, color='#4169E1')
    ax.set_ylabel('Shadow Fraction', fontweight='bold')
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right')
    
    # Add event markers
    ax.axvline(long_rains_onset, color='blue', linestyle='--', alpha=0.6, linewidth=1.5)
    ax.axvline(harvest, color='orange', linestyle='--', alpha=0.6, linewidth=1.5)
    ax.axvline(el_nino_onset, color='green', linestyle='--', alpha=0.6, linewidth=1.5)
    
    # (D) RMSE
    ax = axes[3]
    ax.plot(merged['system:time_start'], merged['RMSE'], 
            color='black', linewidth=2, marker='D', markersize=4, label='RMSE')
    ax.axhline(y=0.10, color='red', linestyle=':', linewidth=2, 
               alpha=0.7, label='Good Fit Threshold (0.10)')
    ax.fill_between(merged['system:time_start'], merged['RMSE'], 
                     alpha=0.2, color='gray')
    ax.set_ylabel('RMSE', fontweight='bold')
    ax.set_xlabel('Date (2023)', fontweight='bold', fontsize=11)
    ax.set_ylim(0, 0.20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right')
    
    # Add event markers
    ax.axvline(long_rains_onset, color='blue', linestyle='--', alpha=0.6, 
               linewidth=1.5, label='Long Rains')
    ax.axvline(harvest, color='orange', linestyle='--', alpha=0.6, 
               linewidth=1.5, label='Harvest')
    ax.axvline(el_nino_onset, color='green', linestyle='--', alpha=0.6, 
               linewidth=1.5, label='El Niño')
    
    # Format x-axis
    axes[3].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    axes[3].xaxis.set_major_locator(mdates.MonthLocator())
    plt.setp(axes[3].xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Add panel labels
    for i, label in enumerate(['(A)', '(B)', '(C)', '(D)']):
        axes[i].text(0.01, 0.95, label, transform=axes[i].transAxes,
                    fontsize=12, fontweight='bold', va='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    # Save figure
    output_path = OUTPUT_DIR / 'Figure3_Narok_Temporal_Dynamics.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    
    # Also save as high-res version for publication
    output_path_hires = OUTPUT_DIR / 'Figure3_Narok_Temporal_Dynamics_HighRes.tiff'
    plt.savefig(output_path_hires, dpi=600, bbox_inches='tight')
    print(f"✓ Saved: {output_path_hires}")
    
    plt.close()


def create_figure4_multisite_comparison(data):
    """
    FIGURE 4: Multi-Site Comparison Charts
    Six-panel figure showing:
    (A) Narok Soil+Veg time series
    (B) Narok RMSE
    (C) Kajiado Soil+Veg time series
    (D) Kajiado RMSE
    (E) Turkana Soil+Veg time series
    (F) Turkana RMSE
    """
    fig, axes = plt.subplots(3, 2, figsize=(16, 12))
    fig.suptitle('Multi-Site Comparative Analysis: Narok, Kajiado, Turkana (2023)', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    sites = [
        ('narok', 'Narok Agricultural Cropland', '#8B4513', '#2E8B57'),
        ('kajiado', 'Kajiado Acacia Shrubland', '#CD853F', '#3CB371'),
        ('turkana', 'Turkana Arid Rangeland', '#DEB887', '#90EE90')
    ]
    
    for i, (site_key, site_name, soil_color, veg_color) in enumerate(sites):
        dyn_data = data[f'{site_key}_dynamics']
        rmse_data = data[f'{site_key}_rmse']
        
        # Left column: Soil + Vegetation fractions
        ax_left = axes[i, 0]
        
        # Plot Soil
        ax_left.plot(dyn_data['system:time_start'], dyn_data['Soil'],
                    color=soil_color, linewidth=2.5, marker='o', markersize=5,
                    label='Soil', alpha=0.9)
        ax_left.fill_between(dyn_data['system:time_start'], dyn_data['Soil'],
                            alpha=0.2, color=soil_color)
        
        # Plot Vegetation
        ax_left.plot(dyn_data['system:time_start'], dyn_data['Veg'],
                    color=veg_color, linewidth=2.5, marker='s', markersize=5,
                    label='Vegetation', alpha=0.9)
        ax_left.fill_between(dyn_data['system:time_start'], dyn_data['Veg'],
                            alpha=0.2, color=veg_color)
        
        ax_left.set_ylabel('Fractional Cover', fontweight='bold', fontsize=11)
        ax_left.set_ylim(0, 1.0)
        ax_left.grid(True, alpha=0.3, linestyle='--')
        ax_left.legend(loc='upper left', fontsize=10)
        ax_left.set_title(f'{site_name}', fontweight='bold', fontsize=12, pad=10)
        
        # Format x-axis
        ax_left.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax_left.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        
        if i == 2:  # Bottom row
            ax_left.set_xlabel('Date (2023)', fontweight='bold', fontsize=11)
            plt.setp(ax_left.xaxis.get_majorticklabels(), rotation=45, ha='right')
        else:
            ax_left.set_xticklabels([])
        
        # Right column: RMSE
        ax_right = axes[i, 1]
        
        ax_right.plot(rmse_data['system:time_start'], rmse_data['RMSE'],
                     color='black', linewidth=2.5, marker='D', markersize=5,
                     label='RMSE', alpha=0.9)
        ax_right.fill_between(rmse_data['system:time_start'], rmse_data['RMSE'],
                             alpha=0.15, color='gray')
        
        # Add threshold line
        ax_right.axhline(y=0.10, color='red', linestyle=':', linewidth=2.5,
                        alpha=0.7, label='Good Fit (≤0.10)')
        
        # Calculate and display statistics
        mean_rmse = rmse_data['RMSE'].mean()
        median_rmse = rmse_data['RMSE'].median()
        pct_good = (rmse_data['RMSE'] <= 0.10).sum() / len(rmse_data) * 100
        
        stats_text = f'Mean: {mean_rmse:.3f}\nMedian: {median_rmse:.3f}\n{pct_good:.1f}% ≤0.10'
        ax_right.text(0.98, 0.97, stats_text, transform=ax_right.transAxes,
                     fontsize=9, va='top', ha='right',
                     bbox=dict(boxstyle='round', facecolor='white', 
                              edgecolor='gray', alpha=0.9))
        
        ax_right.set_ylabel('RMSE', fontweight='bold', fontsize=11)
        ax_right.set_ylim(0, 0.25)
        ax_right.grid(True, alpha=0.3, linestyle='--')
        ax_right.legend(loc='upper left', fontsize=10)
        ax_right.set_title(f'Reconstruction Accuracy', fontweight='bold', 
                          fontsize=12, pad=10)
        
        # Format x-axis
        ax_right.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax_right.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        
        if i == 2:  # Bottom row
            ax_right.set_xlabel('Date (2023)', fontweight='bold', fontsize=11)
            plt.setp(ax_right.xaxis.get_majorticklabels(), rotation=45, ha='right')
        else:
            ax_right.set_xticklabels([])
        
        # Add panel labels
        panel_labels = [('A', 'B'), ('C', 'D'), ('E', 'F')]
        for j, ax in enumerate([ax_left, ax_right]):
            label = f'({panel_labels[i][j]})'
            ax.text(0.02, 0.98, label, transform=ax.transAxes,
                   fontsize=13, fontweight='bold', va='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    plt.tight_layout()
    
    # Save figure
    output_path = OUTPUT_DIR / 'Figure4_MultiSite_Comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    
    # High-res version
    output_path_hires = OUTPUT_DIR / 'Figure4_MultiSite_Comparison_HighRes.tiff'
    plt.savefig(output_path_hires, dpi=600, bbox_inches='tight')
    print(f"✓ Saved: {output_path_hires}")
    
    plt.close()


def create_individual_site_charts(data):
    """Create individual detailed charts for each site"""
    
    sites = [
        ('narok', 'Narok Agricultural Cropland'),
        ('kajiado', 'Kajiado Acacia Shrubland'),
        ('turkana', 'Turkana Arid Rangeland')
    ]
    
    for site_key, site_name in sites:
        dyn_data = data[f'{site_key}_dynamics']
        rmse_data = data[f'{site_key}_rmse']
        
        # Create combined chart with all fractions + RMSE
        fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True,
                                gridspec_kw={'height_ratios': [2, 1]})
        fig.suptitle(f'{site_name}: Complete Temporal Analysis 2023',
                    fontsize=14, fontweight='bold')
        
        # Top: All three fractions stacked area chart
        ax1 = axes[0]
        ax1.fill_between(dyn_data['system:time_start'], 0, dyn_data['Soil'],
                        label='Soil', color='#D2691E', alpha=0.7)
        ax1.fill_between(dyn_data['system:time_start'], dyn_data['Soil'],
                        dyn_data['Soil'] + dyn_data['Veg'],
                        label='Vegetation', color='#228B22', alpha=0.7)
        ax1.fill_between(dyn_data['system:time_start'], 
                        dyn_data['Soil'] + dyn_data['Veg'],
                        1.0,
                        label='Shadow', color='#4169E1', alpha=0.7)
        
        ax1.set_ylabel('Fractional Cover (Cumulative)', fontweight='bold')
        ax1.set_ylim(0, 1.0)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
        ax1.set_title('Endmember Fractions (Stacked)', fontsize=11, pad=5)
        
        # Bottom: RMSE
        ax2 = axes[1]
        
        # Merge to align dates
        merged = pd.merge(dyn_data, rmse_data, on='system:time_start', how='left')
        
        ax2.plot(merged['system:time_start'], merged['RMSE'],
                color='black', linewidth=2, marker='o', markersize=4, label='RMSE')
        ax2.axhline(y=0.10, color='red', linestyle=':', linewidth=2,
                   alpha=0.7, label='Acceptable Threshold (0.10)')
        ax2.fill_between(merged['system:time_start'], merged['RMSE'],
                        alpha=0.2, color='gray')
        
        ax2.set_ylabel('RMSE', fontweight='bold')
        ax2.set_xlabel('Date (2023)', fontweight='bold')
        ax2.set_ylim(0, max(0.25, merged['RMSE'].max() * 1.1))
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
        ax2.set_title('Model Reconstruction Accuracy', fontsize=11, pad=5)
        
        # Format x-axis
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax2.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Save
        safe_name = site_key.capitalize()
        output_path = OUTPUT_DIR / f'{safe_name}_Complete_Analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
        
        plt.close()


def create_rmse_comparison_chart(data):
    """Create comparative RMSE box plots for all sites"""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data for box plot
    rmse_data = [
        data['narok_rmse']['RMSE'],
        data['kajiado_rmse']['RMSE'],
        data['turkana_rmse']['RMSE']
    ]
    
    labels = ['Narok\nCropland\n(n=65)', 'Kajiado\nShrubland\n(n=21)', 'Turkana\nRangeland\n(n=42)']
    
    # Create box plot
    bp = ax.boxplot(rmse_data, tick_labels=labels, patch_artist=True,
                    widths=0.6, showmeans=True,
                    meanprops=dict(marker='D', markerfacecolor='red', markersize=8),
                    medianprops=dict(color='black', linewidth=2))
    
    # Color boxes
    colors = ['#90EE90', '#FFD700', '#FF6347']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Add threshold line
    ax.axhline(y=0.10, color='red', linestyle='--', linewidth=2,
              alpha=0.7, label='Operational Threshold (0.10)')
    
    # Add statistics as text
    for i, (rmse_vals, x_pos) in enumerate(zip(rmse_data, [1, 2, 3])):
        mean_val = rmse_vals.mean()
        median_val = rmse_vals.median()
        pct_good = (rmse_vals <= 0.10).sum() / len(rmse_vals) * 100
        
        stats_text = f'μ={mean_val:.3f}\nMd={median_val:.3f}\n{pct_good:.0f}%≤0.10'
        ax.text(x_pos, ax.get_ylim()[1] * 0.95, stats_text,
               ha='center', va='top', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='white', 
                        edgecolor='gray', alpha=0.9))
    
    ax.set_ylabel('RMSE (Reconstruction Error)', fontweight='bold', fontsize=12)
    ax.set_xlabel('Study Site', fontweight='bold', fontsize=12)
    ax.set_title('Multi-Site RMSE Comparison: Algorithm Performance Across Biomes',
                fontweight='bold', fontsize=13, pad=15)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax.legend(loc='upper right', fontsize=10)
    ax.set_ylim(0, 0.26)
    
    plt.tight_layout()
    
    # Save
    output_path = OUTPUT_DIR / 'RMSE_MultiSite_BoxPlot.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    
    plt.close()


def create_summary_table(data):
    """Create summary statistics table as image"""
    
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')
    
    # Calculate statistics
    stats = []
    for site in ['narok', 'kajiado', 'turkana']:
        rmse_vals = data[f'{site}_rmse']['RMSE']
        dyn_vals = data[f'{site}_dynamics']
        
        stats.append([
            site.capitalize(),
            len(rmse_vals),
            f"{rmse_vals.mean():.3f}",
            f"{rmse_vals.median():.3f}",
            f"{rmse_vals.std():.3f}",
            f"{rmse_vals.min():.3f}",
            f"{rmse_vals.max():.3f}",
            f"{(rmse_vals <= 0.10).sum() / len(rmse_vals) * 100:.1f}%"
        ])
    
    # Add overall
    all_rmse = pd.concat([data['narok_rmse']['RMSE'], 
                          data['kajiado_rmse']['RMSE'],
                          data['turkana_rmse']['RMSE']])
    stats.append([
        'Overall',
        len(all_rmse),
        f"{all_rmse.mean():.3f}",
        f"{all_rmse.median():.3f}",
        f"{all_rmse.std():.3f}",
        f"{all_rmse.min():.3f}",
        f"{all_rmse.max():.3f}",
        f"{(all_rmse <= 0.10).sum() / len(all_rmse) * 100:.1f}%"
    ])
    
    columns = ['Site', 'Observations', 'Mean RMSE', 'Median RMSE', 
               'Std Dev', 'Min', 'Max', '% Good Fit\n(≤0.10)']
    
    table = ax.table(cellText=stats, colLabels=columns, loc='center',
                    cellLoc='center', colWidths=[0.15, 0.12, 0.12, 0.12, 0.11, 0.09, 0.09, 0.12])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header
    for i in range(len(columns)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Style rows
    for i in range(1, len(stats) + 1):
        if i == len(stats):  # Overall row
            for j in range(len(columns)):
                table[(i, j)].set_facecolor('#E7E6E6')
                table[(i, j)].set_text_props(weight='bold')
        else:
            color = '#F2F2F2' if i % 2 == 0 else 'white'
            for j in range(len(columns)):
                table[(i, j)].set_facecolor(color)
    
    plt.title('Table 1: Multi-Site RMSE Accuracy Summary (2023)', 
             fontweight='bold', fontsize=12, pad=20)
    
    # Save
    output_path = OUTPUT_DIR / 'Table1_RMSE_Summary.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    
    plt.close()


def main():
    """Main execution function"""
    print("=" * 60)
    print("Spectral Unmixing Figure Generation Script")
    print("=" * 60)
    print()
    
    # Load data
    print("Loading data files...")
    data = load_data()
    print(f"✓ Loaded {len(data)} datasets")
    print()
    
    # Generate figures
    print("Generating figures...")
    print()
    
    create_figure3_narok_temporal(data)
    print()
    
    create_figure4_multisite_comparison(data)
    print()
    
    create_individual_site_charts(data)
    print()
    
    create_rmse_comparison_chart(data)
    print()
    
    create_summary_table(data)
    print()
    
    print("=" * 60)
    print("✓ All figures generated successfully!")
    print(f"✓ Output directory: {OUTPUT_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
