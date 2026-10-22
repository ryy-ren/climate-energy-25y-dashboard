"""
全球气候变化与能源转型可视化平台
=================================
基于 Streamlit + Plotly 构建的交互式大数据可视化作品

数据集: Global Climate & Energy Transition 2000-2026
来源: Kaggle (CC0 Public Domain)
链接: https://www.kaggle.com/datasets/sergionefedov/global-climate-and-energy-transition-2000-2026

运行: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="全球气候变化与能源转型可视化",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 数据加载
# ============================================================
@st.cache_data
def load_data():
    """加载所有CSV数据集"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')

    temp_df = pd.read_csv(os.path.join(data_dir, 'temperature_anomaly_monthly.csv'))
    co2_df = pd.read_csv(os.path.join(data_dir, 'co2_emissions_yearly.csv'))
    energy_df = pd.read_csv(os.path.join(data_dir, 'energy_mix_yearly.csv'))
    events_df = pd.read_csv(os.path.join(data_dir, 'climate_events.csv'))
    carbon_df = pd.read_csv(os.path.join(data_dir, 'carbon_prices_daily.csv'))

    # 数据预处理
    temp_df['year_month'] = pd.to_datetime(temp_df['year_month'], format='%Y-%m')
    carbon_df['date'] = pd.to_datetime(carbon_df['date'])
    events_df['date'] = pd.to_datetime(events_df['date'])

    return temp_df, co2_df, energy_df, events_df, carbon_df

# 加载数据
temp_df, co2_df, energy_df, events_df, carbon_df = load_data()

# ============================================================
# 侧边栏导航
# ============================================================
with st.sidebar:
    st.title("🌍 导航目录")
    page = st.radio(
        "选择视图",
        ["📊 项目概览", "🌡️ 温度异常趋势", "💨 CO₂排放分析", "⚡ 能源结构转型",
         "💰 碳市场价格", "📅 重大气候事件"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("""
    **数据集信息**
    - 温度数据: 2000-2026 (月)
    - CO₂排放: 50国 × 27年
    - 能源结构: 50国 × 27年
    - 碳市场: 5个ETS
    - 气候事件: 50起重大事件
    """)

# ============================================================
# 页面一: 项目概览
# ============================================================
if page == "📊 项目概览":
    st.title("🌍 全球气候变化与能源转型 — 25年数据洞察")
    st.markdown("---")

    # 核心指标卡片
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # 计算2000年和2024年温度差
        global_temp = temp_df[temp_df['region'] == 'Global']
        temp_2000 = global_temp[global_temp['year'] == 2000]['temp_anomaly_c'].mean()
        temp_2024 = global_temp[global_temp['year'] == 2024]['temp_anomaly_c'].mean()
        st.metric("温度上升", f"{temp_2024 - temp_2000:.2f}°C",
                  f"+{temp_2000:.2f}°C → +{temp_2024:.2f}°C",
                  delta_color="inverse")
    with col2:
        # CO2浓度变化
        co2_2000 = global_temp[global_temp['year'] == 2000]['co2_ppm'].dropna().mean()
        co2_2024 = global_temp[global_temp['year'] == 2024]['co2_ppm'].dropna().mean()
        st.metric("CO₂浓度增长", f"{co2_2024 - co2_2000:.0f} ppm",
                  f"{co2_2000:.0f} → {co2_2024:.0f} ppm")
    with col3:
        # 排放总量
        emissions_2000 = co2_df[co2_df['year'] == 2000]['co2_emissions_mt'].sum() / 1000
        emissions_2024 = co2_df[co2_df['year'] == 2024]['co2_emissions_mt'].sum() / 1000
        st.metric("全球排放", f"{emissions_2024:.0f} Gt CO₂",
                  f"{emissions_2000:.0f} → {emissions_2024:.0f} Gt")
    with col4:
        # 重大事件数
        st.metric("重大气候事件", f"{len(events_df)} 起",
                  f"涵盖 {events_df['region'].nunique()} 个地区")

    st.markdown("---")

    # 简介
    st.header("📖 项目简介")
    st.markdown("""
    本项目基于 **2000-2026年** 的全球公开气候与能源数据，通过交互式可视化探索：

    1. **温度异常的时空演变** — 全球变暖的25年轨迹，北极放大效应的直观展示
    2. **CO₂排放格局变迁** — 50个主要排放国的总量、人均、碳排放强度对比
    3. **能源结构转型路径** — 从化石能源到可再生能源的转型速度与模式差异
    4. **碳市场价格波动** — 五大ETS交易体系的价格驱动因素与政策影响
    5. **气候事件时间线** — 50起极端天气与政策事件的时间锚点

    **目标受众**: 环境科学学生、政策制定者、ESG研究者、公众科普
    """)

    # 数据来源
    st.header("📚 数据来源")
    st.markdown("""
    所有数据均来自公开官方统计机构，采用 CC0 Public Domain 许可：
    - **温度异常**: NASA GISS GISTEMP v4 + NOAA NCEI
    - **CO₂浓度**: NOAA Mauna Loa Observatory
    - **国家排放**: EDGAR v8.0 + Our World in Data + BP Statistical Review
    - **能源结构**: IEA World Energy Statistics + Ember Climate Analytics
    - **碳市场价格**: EU ETS / California CARB / RGGI / UK ETS / China ETS
    - **气候事件**: IPCC AR6 + EM-DAT + UNFCCC COP 文件
    """)

    st.markdown("---")

    # 快速预览图: 温度+CO2 双轴图
    st.header("🎯 快速洞察: 温度与CO₂的25年联动")
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    global_temp = temp_df[temp_df['region'] == 'Global'].sort_values('year_month')
    fig.add_trace(
        go.Scatter(x=global_temp['year_month'], y=global_temp['temp_anomaly_c'],
                   name='温度异常 (°C)', line=dict(color='#e74c3c', width=2)),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=global_temp['year_month'], y=global_temp['co2_ppm'],
                   name='CO₂浓度 (ppm)', line=dict(color='#3498db', width=2)),
        secondary_y=True
    )
    fig.add_hline(y=1.5, line_dash="dash", line_color="red",
                  annotation_text="1.5°C 阈值", secondary_y=False)
    fig.update_layout(title_text="全球温度异常与CO₂浓度 (2000-2026)",
                      hovermode='x unified', height=500)
    fig.update_yaxes(title_text="温度异常 (°C)", secondary_y=False)
    fig.update_yaxes(title_text="CO₂浓度 (ppm)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# 页面二: 温度异常趋势
# ============================================================
elif page == "🌡️ 温度异常趋势":
    st.title("🌡️ 全球温度异常趋势分析")
    st.markdown("---")

    # 区域选择
    regions = temp_df['region'].unique().tolist()
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_regions = st.multiselect("选择区域", regions, default=['Global', 'Arctic', 'Europe', 'Asia'])
    with col2:
        show_trend = st.checkbox("显示趋势线", value=True)

    # 温度趋势图
    temp_filtered = temp_df[temp_df['region'].isin(selected_regions)]
    fig = px.line(temp_filtered.sort_values('year_month'),
                  x='year_month', y='temp_anomaly_c', color='region',
                  title="温度异常变化趋势 (相对于1951-1980基准)",
                  labels={'year_month': '时间', 'temp_anomaly_c': '温度异常 (°C)', 'region': '区域'})
    fig.add_hline(y=1.5, line_dash="dash", line_color="red", annotation_text="1.5°C 阈值")
    fig.update_layout(height=500, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # 年度变化柱状图（带动画）
    st.subheader("📈 年度温度异常 (全球 + 区域对比)")
    year_type = st.radio("统计粒度", ["月数据", "年平均"], horizontal=True)

    if year_type == "年平均":
        yearly_temp = temp_df.groupby(['year', 'region'])['temp_anomaly_c'].mean().reset_index()
        yearly_temp = yearly_temp[yearly_temp['region'].isin(selected_regions)]

        fig2 = px.bar(yearly_temp, x='year', y='temp_anomaly_c', color='region',
                      barmode='group',
                      title="年度平均温度异常对比",
                      labels={'year': '年份', 'temp_anomaly_c': '温度异常 (°C)', 'region': '区域'})
        fig2.update_layout(height=450)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # 区域热力图
    st.subheader("🔥 区域年度温度热力图")
    pivot_temp = temp_df[temp_df['region'].isin(selected_regions)].groupby(['year', 'region'])['temp_anomaly_c'].mean().reset_index()
    pivot_table = pivot_temp.pivot(index='region', columns='year', values='temp_anomaly_c')

    fig3 = px.imshow(pivot_table,
                     labels=dict(x="年份", y="区域", color="温度异常 (°C)"),
                     color_continuous_scale='RdYlBu_r',
                     aspect='auto',
                     title="各区域年度平均温度异常热力图")
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

    # 统计数据
    st.markdown("---")
    st.subheader("📊 关键统计")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**北极放大效应**")
        arctic = temp_df[temp_df['region'] == 'Arctic']
        global_avg = temp_df[temp_df['region'] == 'Global']
        ratio = arctic['temp_anomaly_c'].mean() / global_avg['temp_anomaly_c'].mean()
        st.metric("放大倍数", f"{ratio:.1f}×")
    with col2:
        st.write("**最热年份**")
        hottest_year = temp_df[temp_df['region'] == 'Global'].groupby('year')['temp_anomaly_c'].mean().idxmax()
        st.metric("", f"{hottest_year}年")
    with col3:
        st.write("**1.5°C突破**")
        breach = temp_df[(temp_df['region'] == 'Global') & (temp_df['temp_anomaly_c'] >= 1.5)]['year'].min()
        st.metric("首次突破", f"{breach}年" if pd.notna(breach) else "未突破")

# ============================================================
# 页面三: CO2排放分析
# ============================================================
elif page == "💨 CO₂排放分析":
    st.title("💨 CO₂排放格局与演变")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["年度排放排名", "排放动态演变 (动画)", "排放强度分析"])

    with tab1:
        year = st.slider("选择年份", 2000, 2026, 2024)
        top_n = st.slider("显示前N名", 5, 20, 15)

        year_data = co2_df[co2_df['year'] == year].nlargest(top_n, 'co2_emissions_mt')

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(year_data, x='co2_emissions_mt', y='country', orientation='h',
                         title=f"{year}年 CO₂排放量 TOP {top_n}",
                         color='region',
                         labels={'co2_emissions_mt': '排放量 (百万吨)', 'country': '国家', 'region': '地区'})
            fig.update_layout(height=550, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig2 = px.bar(year_data, x='co2_per_capita_t', y='country', orientation='h',
                          title=f"{year}年 人均CO₂排放量 TOP {top_n}",
                          color='co2_per_capita_t', color_continuous_scale='YlOrRd',
                          labels={'co2_per_capita_t': '人均排放 (吨/人)', 'country': '国家'})
            fig2.update_layout(height=550, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("🎬 CO₂排放随时间演变动画")
        top_countries = co2_df.groupby('country')['co2_emissions_mt'].sum().nlargest(15).index.tolist()
        anim_data = co2_df[co2_df['country'].isin(top_countries)]

        fig3 = px.bar(anim_data, x='co2_emissions_mt', y='country',
                      animation_frame='year', animation_group='country',
                      color='region', orientation='h',
                      range_x=[0, anim_data['co2_emissions_mt'].max() * 1.1],
                      title="15大排放国CO₂排放量动态演变 (2000-2026)",
                      labels={'co2_emissions_mt': '排放量 (百万吨)', 'country': '国家'})
        fig3.update_layout(height=600, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig3, use_container_width=True)

        st.caption("点击播放按钮观看25年排放格局的动态变化")

    with tab3:
        st.subheader("📉 碳排放强度分析")
        # co2_intensity = kg CO2 per GDP USD - 越低越好
        intensity_data = co2_df[co2_df['year'] == 2024].copy()
        intensity_data = intensity_data.nlargest(15, 'co2_emissions_mt')

        fig4 = px.scatter(intensity_data,
                          x='co2_intensity_kg_per_gdp_usd',
                          y='co2_per_capita_t',
                          size='co2_emissions_mt',
                          color='region',
                          text='country',
                          title=f"2024年 碳排放强度 × 人均排放 × 总排放量 (气泡大小)",
                          labels={
                              'co2_intensity_kg_per_gdp_usd': '碳排放强度 (kg CO₂ / USD GDP)',
                              'co2_per_capita_t': '人均排放 (吨/人)',
                              'co2_emissions_mt': '总排放量 (Mt)'
                          })
        fig4.update_layout(height=550)
        st.plotly_chart(fig4, use_container_width=True)

        st.caption("**解读**: 理想位置在左下角（低碳强度 + 低人均排放）。气泡越大代表总排放量越大。")

# ============================================================
# 页面四: 能源结构转型
# ============================================================
elif page == "⚡ 能源结构转型":
    st.title("⚡ 能源结构转型路径分析")
    st.markdown("---")

    # 国家选择
    major_countries = co2_df.groupby('country')['co2_emissions_mt'].sum().nlargest(20).index.tolist()
    country = st.selectbox("选择国家/地区", major_countries, index=0)

    country_energy = energy_df[energy_df['country'] == country].sort_values('year')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"📊 {country} 能源结构演变 (堆叠面积)")
        energy_cols = ['coal_pct', 'oil_pct', 'gas_pct', 'nuclear_pct',
                       'hydro_pct', 'solar_pct', 'wind_pct', 'other_renewables_pct']
        energy_labels = ['煤炭', '石油', '天然气', '核能', '水电', '太阳能', '风能', '其他可再生']
        energy_colors = ['#2c3e50', '#8e44ad', '#e67e22', '#34495e', '#3498db', '#f1c40f', '#27ae60', '#1abc9c']

        fig = go.Figure()
        for col, label, color in zip(energy_cols, energy_labels, energy_colors):
            fig.add_trace(go.Scatter(x=country_energy['year'], y=country_energy[col],
                                     stackgroup='one', name=label,
                                     line=dict(color=color, width=0.5),
                                     fillcolor=color, opacity=0.9))
        fig.update_layout(title=f"{country} 一次能源结构 (2000-2026)",
                          yaxis_title="占比 (%)", xaxis_title="年份",
                          height=500, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(f"🔄 {country} 可再生能源转型速度")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=country_energy['year'],
                              y=country_energy['fossil_total_pct'],
                              name='化石能源', marker_color='#95a5a6'))
        fig2.add_trace(go.Bar(x=country_energy['year'],
                              y=country_energy['renewables_total_pct'],
                              name='可再生能源', marker_color='#2ecc71'))
        fig2.update_layout(barmode='stack',
                           title=f"{country} 化石能源 vs 可再生能源占比",
                           yaxis_title="占比 (%)", height=500)
        st.plotly_chart(fig2, use_container_width=True)

        # 计算转型速度
        renew_2000 = country_energy[country_energy['year'] == 2000]['renewables_total_pct'].values[0]
        renew_2024 = country_energy[country_energy['year'] == 2024]['renewables_total_pct'].values[0]
        growth_rate = (renew_2024 - renew_2000) / 24

        st.metric("可再生能源增长",
                  f"+{renew_2024 - renew_2000:.1f}%",
                  f"年均 {growth_rate:.2f}%")

    st.markdown("---")

    # 多国对比
    st.subheader("🌐 多国可再生能源转型对比")
    compare_countries = st.multiselect("选择对比国家", major_countries,
                                       default=['China', 'United States', 'Germany', 'India', 'United Kingdom'])

    if compare_countries:
        compare_data = energy_df[energy_df['country'].isin(compare_countries)]

        fig3 = px.line(compare_data.sort_values('year'),
                       x='year', y='renewables_total_pct', color='country',
                       title="主要国家可再生能源占比变化 (2000-2026)",
                       labels={'year': '年份', 'renewables_total_pct': '可再生能源占比 (%)', 'country': '国家'})
        fig3.update_layout(height=450)
        st.plotly_chart(fig3, use_container_width=True)

# ============================================================
# 页面五: 碳市场价格
# ============================================================
elif page == "💰 碳市场价格":
    st.title("💰 全球碳交易市场价格走势")
    st.markdown("---")

    markets = carbon_df['market'].unique().tolist()
    selected_markets = st.multiselect("选择碳市场", markets, default=markets)

    carbon_filtered = carbon_df[carbon_df['market'].isin(selected_markets)]

    # 价格走势图
    fig = px.line(carbon_filtered.sort_values('date'),
                  x='date', y='price', color='market',
                  title="五大碳交易体系价格走势",
                  labels={'date': '日期', 'price': '价格', 'market': '市场'},
                  hover_data=['currency'])
    fig.update_layout(height=500, hovermode='x unified')

    # 添加重大事件标注
    key_events = {
        '2005-04-22': ('EU ETS启动', 'EU_ETS'),
        '2008-09-25': ('RGGI启动', 'RGGI'),
        '2013-11-19': ('加州碳市场启动', 'California'),
        '2021-05-19': ('UK ETS启动', 'UK_ETS'),
        '2021-07-16': ('中国全国ETS启动', 'China_ETS'),
        '2022-08-01': ('EU ETS历史高点€100', 'EU_ETS'),
    }
    for date_str, (label, market) in key_events.items():
        try:
            fig.add_vline(x=date_str, line_dash="dot", line_color="gray", opacity=0.5)
        except:
            pass

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # 价格统计
    st.subheader("📊 各碳市场价格统计")
    stats = carbon_df.groupby('market').agg({
        'price': ['mean', 'max', 'min', 'std'],
        'currency': 'first'
    }).round(2)
    stats.columns = ['平均价', '最高价', '最低价', '波动率', '货币']
    stats = stats.reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(stats, use_container_width=True, hide_index=True)
    with col2:
        fig2 = px.box(carbon_df, x='market', y='price', color='market',
                      title="各碳市场价格分布",
                      labels={'market': '市场', 'price': '价格'})
        fig2.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# 页面六: 重大气候事件
# ============================================================
elif page == "📅 重大气候事件":
    st.title("📅 2000-2026年重大气候事件时间线")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        event_types = events_df['event_type'].unique().tolist()
        selected_types = st.multiselect("事件类型", event_types, default=event_types[:5])
    with col2:
        regions = events_df['region'].unique().tolist()
        selected_regions = st.multiselect("地区", regions, default=regions)
    with col3:
        min_severity = st.slider("最低严重程度", 1, 10, 5)

    events_filtered = events_df[
        (events_df['event_type'].isin(selected_types)) &
        (events_df['region'].isin(selected_regions)) &
        (events_df['severity_score'] >= min_severity)
    ].sort_values('date')

    # 时间线散点图
    fig = px.scatter(events_filtered, x='date', y='severity_score',
                     size='severity_score', color='event_type',
                     hover_data=['description', 'region'],
                     title="重大气候事件时间线 (气泡大小=严重程度)",
                     labels={'date': '日期', 'severity_score': '严重程度',
                             'event_type': '事件类型', 'region': '地区'})
    fig.update_layout(height=500, yaxis=dict(title='严重程度 (1-10)'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # 事件列表
    st.subheader(f"📋 筛选后的事件列表 ({len(events_filtered)} 起)")
    display_cols = ['date', 'event_type', 'region', 'severity_score', 'description']
    st.dataframe(events_filtered[display_cols].rename(columns={
        'date': '日期', 'event_type': '类型', 'region': '地区',
        'severity_score': '严重程度', 'description': '描述'
    }), use_container_width=True, hide_index=True)

    st.markdown("---")

    # 类型统计
    st.subheader("📊 事件类型分布")
    col1, col2 = st.columns(2)
    with col1:
        type_counts = events_df['event_type'].value_counts()
        fig2 = px.pie(values=type_counts.values, names=type_counts.index,
                      title="事件类型分布", hole=0.4)
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        year_counts = events_df.groupby('year').size().reset_index(name='count')
        fig3 = px.bar(year_counts, x='year', y='count',
                      title="各年度重大事件数量",
                      labels={'year': '年份', 'count': '事件数量'})
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
