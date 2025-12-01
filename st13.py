import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
import math
import re
import warnings
import base64
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
    st.session_state.language = "English"

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

    st.markdown(f'<div class="content-card"><h2>🔗 {texts["assoc"][language]}</h2></div>', unsafe_allow_html=True)

    if len(numeric_cols) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            var_x = st.selectbox(texts["x_variable"][language], numeric_cols)
        with col2:
            var_y = st.selectbox(texts["y_variable"][language], [c for c in numeric_cols if c != var_x])

        method = st.radio(texts["corr_method"][language], ["pearson", "spearman"])

        if st.button(texts["run_test"][language]):
            try:
                temp_df = df[[var_x, var_y]].copy()
                temp_df[var_x] = pd.to_numeric(temp_df[var_x], errors='coerce')
                temp_df[var_y] = pd.to_numeric(temp_df[var_y], errors='coerce')
                temp_df = temp_df.dropna()

                if len(temp_df) < 2:
                    st.warning(texts["not_enough_data"][language])
                else:
                    x_data = temp_df[var_x].values
                    y_data = temp_df[var_y].values
                    
                    if np.std(x_data) == 0 or np.std(y_data) == 0:
                        st.warning(texts["constant_values"][language])
                    else:
                        if method == "pearson":
                            corr, pval = pearsonr(x_data, y_data)
                        else:
                            corr, pval = spearmanr(x_data, y_data)
                        
                        st.success("✅ " + texts["correlation_result"][language].format(method, var_x, var_y, f"{corr:.4f}"))
                        st.info("📊 " + texts["pvalue_sample"][language].format(f"{pval:.4g}", len(temp_df)))
                        
                        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
                        ax.scatter(x_data, y_data, alpha=0.6, edgecolors='black', linewidth=0.5, color='#667eea')
                        ax.set_xlabel(var_x, fontsize=10)
                        ax.set_ylabel(var_y, fontsize=10)
                        ax.set_title(texts["scatter_title"][language].format(var_x, var_y, f"{corr:.4f}", f"{pval:.4g}"), 
                                   fontsize=11, fontweight='bold')
                        ax.grid(True, alpha=0.3)
                        plt.tight_layout()
                        st.pyplot(fig, clear_figure=True)
                        plt.close(fig)
                        
            except Exception as e:
                st.error(texts["error_corr"][language].format(str(e)))
    else:
        st.info(texts["need_two_cols"][language])

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