import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, shapiro, normaltest
import math
import re
import warnings
import base64
from scipy.stats import spearmanr as spearman_corr
warnings.filterwarnings('ignore')

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Survey Data Analyzer", layout="wide", initial_sidebar_state="collapsed")

# -------------------------
# LOAD BACKGROUND IMAGE
# -------------------------
def get_base64_image(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Ganti 'background.jpg' dengan nama file gambar Anda
bg_image = get_base64_image('background.jpg')

# -------------------------
# LANGUAGE SYSTEM
# -------------------------
if 'language' not in st.session_state:
    st.session_state.language = "Indonesia"

texts = {
    "title": {
        "Indonesia": "Analisis Data Survei", 
        "English": "Survey Data Analysis", 
        "Chinese": "调查数据分析"
    },
    "subtitle": {
        "Indonesia": "Unggah file Excel Anda untuk memulai analisis",
        "English": "Upload your Excel file to start analysis",
        "Chinese": "上传您的 Excel 文件以开始分析"
    },
    "upload": {
        "Indonesia": "Unggah File Excel", 
        "English": "Upload Excel File", 
        "Chinese": "上传 Excel 文件"
    },
    "drag_drop": {
        "Indonesia": "Seret dan lepas file di sini",
        "English": "Drag and drop file here",
        "Chinese": "将文件拖放至此"
    },
    "file_limit": {
        "Indonesia": "Maksimal 200MB • Format: XLSX, XLS",
        "English": "Limit 200MB • Format: XLSX, XLS",
        "Chinese": "单个文件大小上限200MB • 支持XLSX、XLS格式"
    },
    "browse_files": {
        "Indonesia": "Telusuri File",
        "English": "Browse Files",
        "Chinese": "浏览文件"
    },
    "preview": {
        "Indonesia": "Pratinjau Data", 
        "English": "Data Preview", 
        "Chinese": "数据预览"
    },
    "desc": {
        "Indonesia": "Analisis Deskriptif", 
        "English": "Descriptive Analysis", 
        "Chinese": "描述性分析"
    },
    "select_columns": {
        "Indonesia": "Pilih kolom untuk analisis",
        "English": "Select columns for analysis",
        "Chinese": "选择要分析的列"
    },
    "no_numeric": {
        "Indonesia": "Tidak ada kolom numerik yang ditemukan",
        "English": "No numeric columns found",
        "Chinese": "未找到数字列"
    },
    "bar_chart": {
        "Indonesia": "Grafik Batang",
        "English": "Bar Chart",
        "Chinese": "柱状图"
    },
    "histogram": {
        "Indonesia": "Histogram",
        "English": "Histogram",
        "Chinese": "直方图"
    },
    "x_group": {
        "Indonesia": "Grup X",
        "English": "X Group",
        "Chinese": "X组"
    },
    "y_group": {
        "Indonesia": "Grup Y",
        "English": "Y Group",
        "Chinese": "Y组"
    },
    "other_group": {
        "Indonesia": "Lainnya",
        "English": "Other",
        "Chinese": "其他"
    },
    "total_analysis": {
        "Indonesia": "Analisis Skor Total",
        "English": "Total Scores Analysis",
        "Chinese": "总分分析"
    },
    "total_scores": {
        "Indonesia": "Skor Total",
        "English": "Total Scores",
        "Chinese": "总分"
    },
    "summary_stats": {
        "Indonesia": "Ringkasan Statistik untuk Total",
        "English": "Summary Statistics for Totals",
        "Chinese": "总分汇总统计"
    },
    "no_xy_cols": {
        "Indonesia": "Tidak ditemukan kolom X atau Y untuk membuat total",
        "English": "No X or Y columns found to create totals",
        "Chinese": "未找到X或Y列以创建总分"
    },
    "x_total_created": {
        "Indonesia": "X_TOTAL dibuat dari {} kolom",
        "English": "X_TOTAL created from {} columns",
        "Chinese": "X_TOTAL 已从 {} 列创建"
    },
    "y_total_created": {
        "Indonesia": "Y_TOTAL dibuat dari {} kolom",
        "English": "Y_TOTAL created from {} columns",
        "Chinese": "Y_TOTAL 已从 {} 列创建"
    },
    "could_not_create": {
        "Indonesia": "Tidak dapat membuat {}: {}",
        "English": "Could not create {}: {}",
        "Chinese": "无法创建 {}: {}"
    },
    "assoc": {
        "Indonesia": "Analisis Asosiasi Dua Variabel", 
        "English": "Two-Variable Association Analysis", 
        "Chinese": "两变量关联分析"
    },
    "x_variable": {
        "Indonesia": "Variabel X",
        "English": "X Variable",
        "Chinese": "X变量"
    },
    "y_variable": {
        "Indonesia": "Variabel Y",
        "English": "Y Variable",
        "Chinese": "Y变量"
    },
    "corr_method": {
        "Indonesia": "Metode Korelasi",
        "English": "Correlation Method",
        "Chinese": "相关方法"
    },
    "run_test": {
        "Indonesia": "Jalankan Tes",
        "English": "Run Test",
        "Chinese": "运行测试"
    },
    "correlation_result": {
        "Indonesia": "Korelasi ({}) antara {} dan {}: **{}**",
        "English": "Correlation ({}) between {} and {}: **{}**",
        "Chinese": "{} 和 {} 之间的相关性 ({}): **{}**"
    },
    "pvalue_sample": {
        "Indonesia": "p-value: {} | Ukuran sampel: {}",
        "English": "p-value: {} | Sample size: {}",
        "Chinese": "p值: {} | 样本量: {}"
    },
    "scatter_title": {
        "Indonesia": "Grafik Sebaran: {} vs {}\n(r = {}, p = {})",
        "English": "Scatter Plot: {} vs {}\n(r = {}, p = {})",
        "Chinese": "散点图: {} 对 {}\n(r = {}, p = {})"
    },
    "not_enough_data": {
        "Indonesia": "Tidak cukup data berpasangan setelah menghapus nilai kosong",
        "English": "Not enough paired data after dropping NA",
        "Chinese": "删除缺失值后数据不足"
    },
    "constant_values": {
        "Indonesia": "Salah satu atau kedua variabel memiliki nilai konstan",
        "English": "One or both variables have constant values",
        "Chinese": "一个或两个变量具有恒定值"
    },
    "error_corr": {
        "Indonesia": "Error menghitung korelasi: {}",
        "English": "Error computing correlation: {}",
        "Chinese": "计算相关性时出错: {}"
    },
    "need_two_cols": {
        "Indonesia": "Minimal 2 kolom numerik diperlukan untuk analisis korelasi",
        "English": "Need at least 2 numeric columns for correlation analysis",
        "Chinese": "相关分析至少需要2个数字列"
    },
    "file_error": {
        "Indonesia": "Gagal membaca file. Pastikan file Excel valid.\n{}",
        "English": "Failed to read file. Make sure the Excel file is valid.\n{}",
        "Chinese": "读取文件失败。请确保Excel文件有效。\n{}"
    },
    "empty_file": {
        "Indonesia": "File Excel kosong",
        "English": "Excel file is empty",
        "Chinese": "Excel文件为空"
    },
    "features_title": {
        "Indonesia": "Fitur Utama",
        "English": "Key Features",
        "Chinese": "主要功能"
    },
    "feature1_title": {
        "Indonesia": "Analisis Deskriptif",
        "English": "Descriptive Analysis",
        "Chinese": "描述性分析"
    },
    "feature1_desc": {
        "Indonesia": "Ringkasan statistik lengkap dan visualisasi data survei Anda",
        "English": "Comprehensive statistical summaries and visualizations of your survey data",
        "Chinese": "全面的统计摘要和调查数据可视化"
    },
    "feature2_title": {
        "Indonesia": "Grafik Visual",
        "English": "Visual Charts",
        "Chinese": "可视化图表"
    },
    "feature2_desc": {
        "Indonesia": "Grafik batang dan histogram interaktif untuk pemahaman data yang lebih baik",
        "English": "Interactive bar charts and histograms for better data understanding",
        "Chinese": "交互式柱状图和直方图，更好地理解数据"
    },
    "feature3_title": {
        "Indonesia": "Analisis Korelasi",
        "English": "Correlation Analysis",
        "Chinese": "相关性分析"
    },
    "feature3_desc": {
        "Indonesia": "Temukan hubungan antar variabel dengan uji korelasi",
        "English": "Discover relationships between variables with correlation testing",
        "Chinese": "通过相关性测试发现变量之间的关系"
    },
    # New texts for association analysis
    "auto_assoc": {
        "Indonesia": "Analisis Asosiasi Otomatis",
        "English": "Automatic Association Analysis",
        "Chinese": "自动关联分析"
    },
    "select_var1": {
        "Indonesia": "Pilih variabel 1",
        "English": "Select variable 1",
        "Chinese": "选择变量1"
    },
    "select_var2": {
        "Indonesia": "Pilih variabel 2",
        "English": "Select variable 2",
        "Chinese": "选择变量2"
    },
    "data_type": {
        "Indonesia": "Tipe data",
        "English": "Data type",
        "Chinese": "数据类型"
    },
    "normality_test": {
        "Indonesia": "Uji Normalitas",
        "English": "Normality Test",
        "Chinese": "正态性检验"
    },
    "data_normal": {
        "Indonesia": "Data normal",
        "English": "Data normal",
        "Chinese": "数据正态"
    },
    "data_not_normal": {
        "Indonesia": "Data tidak normal",
        "English": "Data not normal",
        "Chinese": "数据非正态"
    },
    "using_spearman": {
        "Indonesia": "Data tidak normal → menggunakan Spearman Correlation",
        "English": "Data not normal → using Spearman Correlation",
        "Chinese": "数据非正态 → 使用斯皮尔曼相关"
    },
    "using_pearson": {
        "Indonesia": "Data normal → menggunakan Pearson Correlation",
        "English": "Data normal → using Pearson Correlation",
        "Chinese": "数据正态 → 使用皮尔逊相关"
    },
    "corr_result": {
        "Indonesia": "Hasil Korelasi",
        "English": "Correlation Result",
        "Chinese": "相关性结果"
    },
    "conclusion": {
        "Indonesia": "Kesimpulan",
        "English": "Conclusion",
        "Chinese": "结论"
    },
    "strong_corr": {
        "Indonesia": "Sangat kuat",
        "English": "Very strong",
        "Chinese": "非常强"
    },
    "moderate_corr": {
        "Indonesia": "Sedang",
        "English": "Moderate",
        "Chinese": "中等"
    },
    "weak_corr": {
        "Indonesia": "Lemah",
        "English": "Weak",
        "Chinese": "弱"
    },
    "no_corr": {
        "Indonesia": "Tidak ada korelasi",
        "English": "No correlation",
        "Chinese": "无相关"
    },
    "significant": {
        "Indonesia": "Signifikan",
        "English": "Significant",
        "Chinese": "显著"
    },
    "not_significant": {
        "Indonesia": "Tidak signifikan",
        "English": "Not significant",
        "Chinese": "不显著"
    },
    "both_numeric": {
        "Indonesia": "Kedua variabel numeric 😊",
        "English": "Both variables are numeric 😊",
        "Chinese": "两个变量都是数值型 😊"
    },
    "not_both_numeric": {
        "Indonesia": "Variabel tidak keduanya numeric",
        "English": "Variables are not both numeric",
        "Chinese": "变量不都是数值型"
    },
    "run_auto_analysis": {
        "Indonesia": "Jalankan Analisis Otomatis",
        "English": "Run Auto Analysis",
        "Chinese": "运行自动分析"
    },
    # New texts for conclusion
    "pos_corr": {
        "Indonesia": "positif",
        "English": "positive",
        "Chinese": "正"
    },
    "neg_corr": {
        "Indonesia": "negatif",
        "English": "negative",
        "Chinese": "负"
    },
    "no_dir_corr": {
        "Indonesia": "tidak ada",
        "English": "no",
        "Chinese": "无"
    },
    "results_show": {
        "Indonesia": "Hasil menunjukkan korelasi",
        "English": "Results show",
        "Chinese": "结果显示"
    },
    "with_strength": {
        "Indonesia": "dengan kekuatan",
        "English": "with",
        "Chinese": "相关性，强度为"
    },
    "p_value_is": {
        "Indonesia": "Nilai p =",
        "English": "P-value =",
        "Chinese": "P值 ="
    },
    "so_relationship": {
        "Indonesia": "sehingga hubungan",
        "English": "so the relationship is",
        "Chinese": "因此关系"
    }
}

# -------------------------
# MODERN STYLING
# -------------------------
# Generate CSS with base64 image
bg_css = ""
if bg_image:
    bg_css = f"""
    .stApp {{
        background: url('data:image/jpeg;base64,{bg_image}') no-repeat center center fixed;
        background-size: cover;
    }}
    """
else:
    # Fallback to gradient if image not found
    bg_css = """
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    """

st.markdown(f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    {bg_css}
    
    [data-testid="stAppViewContainer"] {{
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: none;
    }}
    
    /* Header Styling */
    .main-header {{
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .hero-section {{
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        margin: 2rem auto;
        max-width: 900px;
    }}
    
    .hero-title {{
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        line-height: 1.2;
    }}
    
    .hero-subtitle {{
        font-size: 1.3rem;
        color: #4B5563;
        font-weight: 400;
        margin-bottom: 2rem;
    }}
    
    /* File Uploader Styling */
    .stFileUploader {{
        background: white;
        border-radius: 20px;
        padding: 2rem;
        border: 3px dashed #667eea;
        transition: all 0.3s ease;
    }}
    
    .stFileUploader:hover {{
        border-color: #764ba2;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }}
    
    [data-testid="stFileUploader"] section {{
        border: none;
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }}
    
    /* Content Cards */
    .content-card {{
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin: 1.5rem 0;
    }}
    
    /* Feature Cards */
    .feature-card {{
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        height: 100%;
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }}
    
    .feature-title {{
        font-size: 1.2rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 0.5rem;
    }}
    
    .feature-desc {{
        font-size: 0.95rem;
        color: #6B7280;
        line-height: 1.6;
    }}
    
    /* Select Box */
    .stSelectbox {{
        border-radius: 12px;
    }}
    
    /* Dataframe */
    .stDataFrame {{
        border-radius: 15px;
        overflow: hidden;
    }}
    
    /* Section Headers */
    h1, h2, h3 {{
        color: #1F2937;
        font-weight: 700;
    }}
    
    /* Language Selector */
    .language-selector {{
        display: flex;
        gap: 0.5rem;
        justify-content: center;
        margin-bottom: 2rem;
    }}
    
    .lang-btn {{
        padding: 0.5rem 1rem;
        border-radius: 10px;
        background: white;
        border: 2px solid #E5E7EB;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }}
    
    .lang-btn:hover {{
        border-color: #667eea;
        background: #F3F4F6;
    }}
    
    .lang-btn.active {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: transparent;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Multiselect */
    .stMultiSelect {{
        border-radius: 12px;
    }}
    
    /* Custom styling for association analysis */
    .assoc-box {{
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        color: #333;
        font-weight: 500;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .normality-box {{
        background: #fff3cd;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid #ffeaa7;
        color: #333;
        font-size: 1.1rem;
        font-weight: 600;
    }}
    
    .result-box {{
        background: #d1ecf1;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid #bee5eb;
        color: #333;
    }}
    
    .conclusion-box {{
        background: #d4edda;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid #c3e6cb;
        color: #333;
    }}
    
    .check-mark {{
        color: #28a745;
        font-size: 1.5rem;
        font-weight: bold;
    }}
    
    .x-mark {{
        color: #dc3545;
        font-size: 1.5rem;
        font-weight: bold;
    }}
    
    .warning-text {{
        color: #dc3545;
        font-weight: 500;
    }}
    
    .info-text {{
        color: #17a2b8;
        font-weight: 500;
    }}
    
    .success-text {{
        color: #28a745;
        font-weight: 600;
    }}
    
    /* Data type display */
    .data-type-box {{
        background: #e9ecef;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        font-family: monospace;
        font-weight: 500;
    }}
    
    /* Normality test result */
    .normality-result {{
        margin-bottom: 1rem;
        padding: 0.8rem;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 3px solid #6c757d;
    }}
</style>
""", unsafe_allow_html=True)

# -------------------------
# LANGUAGE SELECTOR (Custom HTML)
# -------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="language-selector">', unsafe_allow_html=True)
    lang_col1, lang_col2, lang_col3 = st.columns(3)
    
    with lang_col1:
        if st.button("🇮🇩 Indonesia", key="lang_id", use_container_width=True):
            st.session_state.language = "Indonesia"
            st.rerun()
    
    with lang_col2:
        if st.button("🇬🇧 English", key="lang_en", use_container_width=True):
            st.session_state.language = "English"
            st.rerun()
    
    with lang_col3:
        if st.button("🇨🇳 Chinese", key="lang_cn", use_container_width=True):
            st.session_state.language = "Chinese"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

language = st.session_state.language

# -------------------------
# HERO SECTION
# -------------------------
st.markdown(f"""
<div class="hero-section">
    <h1 class="hero-title">{texts["title"][language]}</h1>
    <p class="hero-subtitle">{texts["subtitle"][language]}</p>
</div>
""", unsafe_allow_html=True)

# -------------------------
# HELPER FUNCTIONS
# -------------------------
def check_normality(data, alpha=0.05):
    """Check normality using Shapiro-Wilk test"""
    try:
        data_clean = data.dropna()
        if len(data_clean) < 3:
            return None, None  # Not enough data for normality test
        
        # Shapiro-Wilk test
        stat, p_value = shapiro(data_clean)
        return stat, p_value
    except Exception as e:
        try:
            # Alternative: D'Agostino's K^2 test
            stat, p_value = normaltest(data_clean)
            return stat, p_value
        except:
            return None, None

def get_correlation_strength(rho):
    """Get correlation strength based on absolute value"""
    abs_rho = abs(rho)
    if abs_rho >= 0.9:
        return texts["strong_corr"][language]
    elif abs_rho >= 0.7:
        return texts["strong_corr"][language]
    elif abs_rho >= 0.5:
        return texts["moderate_corr"][language]
    elif abs_rho >= 0.3:
        return texts["weak_corr"][language]
    else:
        return texts["no_corr"][language]

def format_p_value(p):
    """Format p-value nicely"""
    if p < 0.0001:
        return "0.0000"
    else:
        return f"{p:.4f}"

# -------------------------
# FILE UPLOAD
# -------------------------
uploaded_file = st.file_uploader(
    texts["upload"][language],
    type=["xlsx", "xls"],
    help=texts["file_limit"][language]
)

# Helper functions
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

PLOT_FIGSIZE = (6, 3)
PLOT_DPI = 100

def plot_barh(ax, series, max_bars=20):
    """Plot horizontal bar chart with error handling"""
    try:
        counts = series.value_counts(dropna=False)
        if len(counts) == 0:
            ax.text(0.5, 0.5, "No data", ha='center', va='center', fontsize=10, color='red')
            return
        
        if len(counts) > max_bars:
            counts = counts.nlargest(max_bars)
        counts.sort_index().plot(kind='barh', ax=ax, color='#667eea')
    except Exception as e:
        ax.text(0.5, 0.5, f"Error: {str(e)[:30]}", ha='center', va='center', fontsize=9, color='red')

def render_group_charts(df, cols, group_name):
    """Render charts for a group of columns"""
    if not cols:
        return
    
    st.markdown(f'<div class="content-card"><h3>📊 {texts["bar_chart"][language]} ({group_name})</h3></div>', unsafe_allow_html=True)
    max_per_row = 3
    
    for row in chunk_list(cols, max_per_row):
        cols_ui = st.columns(len(row))
        for i, col_name in enumerate(row):
            with cols_ui[i]:
                fig, ax = plt.subplots(figsize=PLOT_FIGSIZE, dpi=PLOT_DPI)
                try:
                    plot_barh(ax, df[col_name])
                    ax.set_title(col_name, fontsize=10, fontweight='bold')
                    ax.tick_params(axis='both', labelsize=8)
                except Exception as e:
                    ax.text(0.5, 0.5, "Chart error", ha='center', va='center', fontsize=10, color='red')
                
                plt.tight_layout()
                st.pyplot(fig, clear_figure=True)
                plt.close(fig)

    st.markdown(f'<div class="content-card"><h3>📈 {texts["histogram"][language]} ({group_name})</h3></div>', unsafe_allow_html=True)
    for row in chunk_list(cols, max_per_row):
        cols_ui = st.columns(len(row))
        for i, col_name in enumerate(row):
            with cols_ui[i]:
                fig, ax = plt.subplots(figsize=PLOT_FIGSIZE, dpi=PLOT_DPI)
                try:
                    coldata = pd.to_numeric(df[col_name], errors='coerce').dropna()
                    if len(coldata) == 0:
                        raise ValueError("no numeric data")
                    
                    num_bins = min(20, max(5, int(np.sqrt(len(coldata)))))
                    ax.hist(coldata, bins=num_bins, edgecolor='black', alpha=0.7, color='#764ba2')
                    ax.set_title(col_name, fontsize=10, fontweight='bold')
                    ax.tick_params(axis='both', labelsize=8)
                except Exception as e:
                    ax.text(0.5, 0.5, "No numeric data", ha='center', va='center', fontsize=10, color='red')
                
                plt.tight_layout()
                st.pyplot(fig, clear_figure=True)
                plt.close(fig)

# -------------------------
# MAIN LOGIC
# -------------------------
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        if df.empty:
            st.error(texts["empty_file"][language])
            st.stop()
            
    except Exception as e:
        st.error(texts["file_error"][language].format(str(e)))
        st.stop()

    st.markdown(f'<div class="content-card"><h2>📁 {texts["preview"][language]}</h2></div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    df = df.copy()

    maybe_numeric = []
    for col in df.columns:
        try:
            coerced = pd.to_numeric(df[col], errors='coerce')
            non_na_ratio = coerced.notna().sum() / max(len(coerced), 1)
            if non_na_ratio >= 0.5:
                df[col] = coerced
                maybe_numeric.append(col)
        except Exception:
            continue

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    st.markdown(f'<div class="content-card"><h2>📈 {texts["desc"][language]}</h2></div>', unsafe_allow_html=True)

    if len(numeric_cols) == 0:
        st.warning(texts["no_numeric"][language])
    else:
        selected_desc_cols = st.multiselect(
            texts["select_columns"][language],
            numeric_cols,
            default=numeric_cols[:10] if len(numeric_cols) > 10 else numeric_cols
        )

        if selected_desc_cols:
            st.write(df[selected_desc_cols].describe())

            def starts_with_letter(c, letter):
                try:
                    return bool(re.match(rf"^\s*{letter}", str(c), flags=re.I))
                except:
                    return False

            x_cols = [c for c in selected_desc_cols if starts_with_letter(c, 'x')]
            y_cols = [c for c in selected_desc_cols if starts_with_letter(c, 'y')]
            other_cols = [c for c in selected_desc_cols if c not in x_cols + y_cols]

            x_total = None
            y_total = None
            
            if x_cols:
                try:
                    x_total = df[x_cols].sum(axis=1)
                    df['X_TOTAL'] = x_total
                    st.success("✅ " + texts["x_total_created"][language].format(len(x_cols)))
                except Exception as e:
                    st.warning(texts["could_not_create"][language].format("X_TOTAL", str(e)))
            
            if y_cols:
                try:
                    y_total = df[y_cols].sum(axis=1)
                    df['Y_TOTAL'] = y_total
                    st.success("✅ " + texts["y_total_created"][language].format(len(y_cols)))
                except Exception as e:
                    st.warning(texts["could_not_create"][language].format("Y_TOTAL", str(e)))
            
            if x_cols:
                render_group_charts(df, x_cols, texts["x_group"][language])
            if y_cols:
                render_group_charts(df, y_cols, texts["y_group"][language])
            if other_cols:
                render_group_charts(df, other_cols, texts["other_group"][language])
            
            st.markdown("---")
            st.markdown(f'<div class="content-card"><h2>📊 {texts["total_analysis"][language]}</h2></div>', unsafe_allow_html=True)
            
            total_cols_to_plot = []
            if x_total is not None:
                total_cols_to_plot.append('X_TOTAL')
            if y_total is not None:
                total_cols_to_plot.append('Y_TOTAL')
            
            if total_cols_to_plot:
                render_group_charts(df, total_cols_to_plot, texts["total_scores"][language])
                st.markdown(f"### {texts['summary_stats'][language]}")
                st.write(df[total_cols_to_plot].describe())
            else:
                st.info(texts["no_xy_cols"][language])

    # ============================================
    # AUTOMATIC ASSOCIATION ANALYSIS SECTION
    # ============================================
    st.markdown(f'<div class="content-card"><h2>🤖 {texts["auto_assoc"][language]}</h2></div>', unsafe_allow_html=True)
    
    # Create two columns for variable selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {texts['select_var1'][language]}")
        var1_options = ["-- Pilih --"] + numeric_cols
        var1 = st.selectbox(
            "",
            var1_options,
            key="var1_select"
        )
    
    with col2:
        st.markdown(f"### {texts['select_var2'][language]}")
        if var1 != "-- Pilih --":
            var2_options = ["-- Pilih --"] + [col for col in numeric_cols if col != var1]
        else:
            var2_options = ["-- Pilih --"] + numeric_cols
        var2 = st.selectbox(
            "",
            var2_options,
            key="var2_select"
        )
    
    if var1 != "-- Pilih --" and var2 != "-- Pilih --":
        # Display variable information
        st.markdown("---")
        st.markdown(f"### {texts['data_type'][language]}")
        
        # Check if both are numeric
        is_var1_numeric = pd.api.types.is_numeric_dtype(df[var1])
        is_var2_numeric = pd.api.types.is_numeric_dtype(df[var2])
        
        # Display data types in separate lines
        st.markdown(f"**{var1}:**")
        st.markdown(f'<div class="data-type-box">{"Numeric" if is_var1_numeric else "Non-numeric"}</div>', unsafe_allow_html=True)
        
        st.markdown(f"**{var2}:**")
        st.markdown(f'<div class="data-type-box">{"Numeric" if is_var2_numeric else "Non-numeric"}</div>', unsafe_allow_html=True)
        
        if is_var1_numeric and is_var2_numeric:
            # Display success message in box
            st.markdown(f"""
            <div class="assoc-box">
                <span class="check-mark">✓</span>
                <span>{texts["both_numeric"][language]}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Add space before button
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Center the button
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button(f"🚀 {texts['run_auto_analysis'][language]}", type="primary", use_container_width=True):
                    # Perform normality tests
                    st.markdown("---")
                    st.markdown(f"### {texts['normality_test'][language]}")
                    
                    # Get clean data
                    data1 = pd.to_numeric(df[var1], errors='coerce').dropna()
                    data2 = pd.to_numeric(df[var2], errors='coerce').dropna()
                    
                    # Check normality
                    _, p1 = check_normality(data1)
                    _, p2 = check_normality(data2)
                    
                    # Display normality test results
                    st.markdown(f"**{var1}:**")
                    if p1 is not None:
                        # Create normality result box for var1
                        is_normal1 = p1 > 0.05
                        st.markdown(f"""
                        <div class="normality-result">
                            p = {p1:.4f}<br>
                            <span class="{'success-text' if is_normal1 else 'warning-text'}">
                                {'✓' if is_normal1 else '✗'} {texts["data_normal"][language] if is_normal1 else texts["data_not_normal"][language]}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="normality-result">Tidak cukup data untuk uji normalitas</div>', unsafe_allow_html=True)
                    
                    st.markdown(f"**{var2}:**")
                    if p2 is not None:
                        # Create normality result box for var2
                        is_normal2 = p2 > 0.05
                        st.markdown(f"""
                        <div class="normality-result">
                            p = {p2:.4f}<br>
                            <span class="{'success-text' if is_normal2 else 'warning-text'}">
                                {'✓' if is_normal2 else '✗'} {texts["data_normal"][language] if is_normal2 else texts["data_not_normal"][language]}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="normality-result">Tidak cukup data untuk uji normalitas</div>', unsafe_allow_html=True)
                    
                    # Determine correlation method
                    use_spearman = (p1 is not None and p1 <= 0.05) or (p2 is not None and p2 <= 0.05)
                    
                    st.markdown("---")
                    
                    # Display method selection box
                    if use_spearman:
                        st.markdown(f"""
                        <div class="normality-box">
                            <strong>{texts["using_spearman"][language]}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        method = "spearman"
                    else:
                        st.markdown(f"""
                        <div class="normality-box">
                            <strong>{texts["using_pearson"][language]}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        method = "pearson"
                    
                    # Perform correlation
                    try:
                        # Clean data for correlation
                        temp_df = df[[var1, var2]].copy()
                        temp_df[var1] = pd.to_numeric(temp_df[var1], errors='coerce')
                        temp_df[var2] = pd.to_numeric(temp_df[var2], errors='coerce')
                        temp_df = temp_df.dropna()
                        
                        if len(temp_df) >= 2:
                            x_data = temp_df[var1].values
                            y_data = temp_df[var2].values
                            
                            if method == "pearson":
                                corr_coef, p_value = pearsonr(x_data, y_data)
                            else:
                                corr_coef, p_value = spearmanr(x_data, y_data)
                            
                            # Display results
                            st.markdown(f"""
                            <div class="result-box">
                                <h3>{texts['corr_result'][language]}</h3>
                                <h4>{method.upper()}</h4>
                                <p style="font-size: 1.2rem; font-weight: bold;">rho = {corr_coef:.4f}</p>
                                <p style="font-size: 1.2rem; font-weight: bold;">P-value = {format_p_value(p_value)}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Display conclusion - FIXED: Menggunakan bahasa yang sesuai
                            strength = get_correlation_strength(corr_coef)
                            
                            # Determine correlation direction in selected language
                            if corr_coef > 0:
                                direction = texts["pos_corr"][language]
                            elif corr_coef < 0:
                                direction = texts["neg_corr"][language]
                            else:
                                direction = texts["no_dir_corr"][language]
                            
                            # Create conclusion text based on selected language
                            if language == "Indonesia":
                                conclusion_text = f"""
                                {texts["results_show"][language]} korelasi {direction} {texts["with_strength"][language]} <strong>{strength}</strong> (rho = {corr_coef:.4f}).<br>
                                {texts["p_value_is"][language]} {format_p_value(p_value)}, {texts["so_relationship"][language]} <strong>{texts["significant"][language] if p_value < 0.05 else texts["not_significant"][language]}</strong>.
                                """
                            elif language == "English":
                                conclusion_text = f"""
                                {texts["results_show"][language]} a {direction} correlation {texts["with_strength"][language]} <strong>{strength}</strong> strength (rho = {corr_coef:.4f}).<br>
                                {texts["p_value_is"][language]} {format_p_value(p_value)}, {texts["so_relationship"][language]} <strong>{texts["significant"][language] if p_value < 0.05 else texts["not_significant"][language]}</strong>.
                                """
                            else:  # Chinese
                                conclusion_text = f"""
                                {texts["results_show"][language]}{direction}{texts["with_strength"][language]}<strong>{strength}</strong> (rho = {corr_coef:.4f})。<br>
                                {texts["p_value_is"][language]}{format_p_value(p_value)}，{texts["so_relationship"][language]}<strong>{texts["significant"][language] if p_value < 0.05 else texts["not_significant"][language]}</strong>。
                                """
                            
                            st.markdown(f"""
                            <div class="conclusion-box">
                                <h3>{texts['conclusion'][language]}</h3>
                                <p style="font-size: 1.1rem;">{conclusion_text}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Create scatter plot
                            fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
                            
                            # Scatter plot
                            scatter = ax.scatter(x_data, y_data, alpha=0.7, color='#667eea', s=60, edgecolors='white', linewidth=0.5)
                            
                            # Add regression line if Pearson
                            if method == "pearson":
                                z = np.polyfit(x_data, y_data, 1)
                                p = np.poly1d(z)
                                ax.plot(x_data, p(x_data), color='#764ba2', linewidth=2, linestyle='--', alpha=0.8)
                            
                            # Labels and title
                            ax.set_xlabel(var1, fontsize=12, fontweight='bold')
                            ax.set_ylabel(var2, fontsize=12, fontweight='bold')
                            
                            if language == "Indonesia":
                                title = f"Grafik Sebaran: {var1} vs {var2}"
                            elif language == "English":
                                title = f"Scatter Plot: {var1} vs {var2}"
                            else:
                                title = f"sàndiǎntú: {var1} vs {var2}"
                            
                            ax.set_title(f"{title}\n({method.upper()} r = {corr_coef:.4f}, p = {format_p_value(p_value)})", 
                                       fontsize=14, fontweight='bold')
                            
                            # Add grid
                            ax.grid(True, alpha=0.3, linestyle='--')
                            
                            # Add annotation about correlation strength
                            if language == "Indonesia":
                                strength_text = f"Kekuatan: {strength}"
                            elif language == "English":
                                strength_text = f"Strength: {strength}"
                            else:
                                # Untuk Chinese
                                if strength == texts["no_corr"][language]:  # 无相关
                                    strength_text = "qiángdù: wú guānlián"  # dengan spasi
                                else:
                                    strength_text = f"qiángdù: xiāngguānxìng"
                                
                            ax.annotate(strength_text, xy=(0.05, 0.95), xycoords='axes fraction',
                                       fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close(fig)
                            
                        else:
                            st.warning(texts["not_enough_data"][language])
                            
                    except Exception as e:
                        st.error(f"Error in correlation analysis: {str(e)}")
        
        else:
            # Display warning message in box
            st.markdown(f"""
            <div class="assoc-box">
                <span class="x-mark">⚠</span>
                <span>{texts["not_both_numeric"][language]}</span>
            </div>
            """, unsafe_allow_html=True)
            st.info("Pilih dua variabel numerik untuk analisis korelasi.")

else:
    # Show features when no file uploaded
    st.markdown(f'<div class="content-card"><h2>✨ {texts["features_title"][language]}</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">{texts["feature1_title"][language]}</div>
            <div class="feature-desc">{texts["feature1_desc"][language]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">{texts["feature2_title"][language]}</div>
            <div class="feature-desc">{texts["feature2_desc"][language]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">🔗</div>
            <div class="feature-title">{texts["feature3_title"][language]}</div>
            <div class="feature-desc">{texts["feature3_desc"][language]}</div>
        </div>
        """, unsafe_allow_html=True)