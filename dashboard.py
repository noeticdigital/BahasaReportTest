import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from assets.css import *

# Set Streamlit page configuration
st.set_page_config(
    page_title="Mellysa Salon Dashboard",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(main_style, unsafe_allow_html=True)
st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 25px;
}
</style>
""",
    unsafe_allow_html=True,
)

# Define options for filters
all_month = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']
quarter_months = {
    'Q1': ['January', 'February', 'March'],
    'Q2': ['April', 'May', 'June'],
    'Q3': ['July', 'August', 'September'],
    'Q4': ['October', 'November', 'December']
}

all_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

year_option = [2022, 2023]

now_year = 2023

def load_data(path: str):
    data = pd.read_csv(path)
    return data

df = load_data("./dataset/dataset_cleaned.csv")

def main_info(selected_months: list):
    month_filtered = df[df["Bulan"].isin(selected_months)]
    total_pendapatan_yearan = month_filtered.groupby('year')["Harga"].sum().reset_index()
    total_kedatangan_yearan = month_filtered.groupby('year')["Harga"].count().reset_index()
    tp_23 = int(total_pendapatan_yearan[total_pendapatan_yearan["year"]==2023]["Harga"].values[0])
    tp_22 = int(total_pendapatan_yearan[total_pendapatan_yearan["year"]==2022]["Harga"].values[0])
    tk_23 = int(total_kedatangan_yearan[total_kedatangan_yearan["year"]==2023]["Harga"].values[0])
    tk_22 = int(total_kedatangan_yearan[total_kedatangan_yearan["year"]==2022]["Harga"].values[0])

    service_pendapatan_yearan = month_filtered.groupby(['Nama Service', 'year'])["Harga"].sum().reset_index()
    service_pendapatan_year_2023 = service_pendapatan_yearan[service_pendapatan_yearan['year'] == 2023]
    service_pendapatan_year_2023_sorted = service_pendapatan_year_2023.sort_values(by='Harga', ascending=False)
    p_nama_service_tertinggi_2023 = service_pendapatan_year_2023_sorted.iloc[0]['Nama Service']
    service_pendapatan_year_2022 = service_pendapatan_yearan[
        (service_pendapatan_yearan['year'] == 2022) &
        (service_pendapatan_yearan['Nama Service'] == p_nama_service_tertinggi_2023)
    ]
    service_diminati_yearan = month_filtered.groupby(['Nama Service', 'year'])["Harga"].count().reset_index()
    service_diminati_year_2023 = service_diminati_yearan[service_diminati_yearan['year'] == 2023]
    service_diminati_year_2023_sorted = service_diminati_year_2023.sort_values(by='Harga', ascending=False)
    k_nama_service_tertinggi_2023 = service_diminati_year_2023_sorted.iloc[0]['Nama Service']
    service_diminati_year_2022 = service_diminati_yearan[
        (service_diminati_yearan['year'] == 2022) &
        (service_diminati_yearan['Nama Service'] == k_nama_service_tertinggi_2023)
    ]

    sp_23 = int(service_pendapatan_year_2023_sorted.iloc[0]['Harga'])
    sp_22 = int(service_pendapatan_year_2022.iloc[0]['Harga'])
    sk_23 = int(service_diminati_year_2023_sorted.iloc[0]['Harga'])
    sk_22 = int(service_diminati_year_2022.iloc[0]['Harga'])
    st.subheader("Total year 2023")
    st.metric("Pendapatan", f"{tp_23:,} (IDR)", f"{(tp_23-tp_22):,} (IDR)")
    st.metric("Kedatangan", f"{tk_23} (Pendatang)", f"{tk_23-tk_22} (Pendatang)")
    st.metric(f"Pendapatan Service Tertinggi ({p_nama_service_tertinggi_2023})", f"{sp_23:,} (IDR)", f"{(sp_23-sp_22):,} (IDR)")
    st.metric(f"Pembelian Service Tertinggi ({k_nama_service_tertinggi_2023})", f"{sk_23} (Pendatang)", f"{sk_23-sk_22} (Pendatang)")

def daily_year_trend(selected_months: list, selected_opsi):
    if selected_opsi == "Jumlah_Kedatangan":
        title_ops = "Kedatangan"
    elif selected_opsi == "Total_Pendapatan":
        title_ops = "Pendapatan"
    month_filtered = df[df["Bulan"].isin(selected_months)]
    grouped_data = month_filtered.groupby(["Hari", "year"]).agg({
        "Harga": ["count", "sum"]
    }).reset_index()
    # Rename the columns for clarity
    grouped_data.columns = ["Hari", "year", "Jumlah_Kedatangan", "Total_Pendapatan"]
    grouped_data['Hari'] = pd.Categorical(grouped_data['Hari'], categories=all_day, ordered=True)
    grouped_data = grouped_data.sort_values('Hari')
    grouped_data['year'] = grouped_data['year'].astype(str)

    fig = px.bar(grouped_data, x='Hari', y=selected_opsi, color="year", orientation='v', text=selected_opsi, barmode="group",
                labels={'Jumlah_Kedatangan': 'Jumlah Kedatangan'})

    # Menambahkan judul dan mengatur layout
    fig.update_layout(title_text=f'Jumlah {title_ops} per Hari', height=415)

    st.plotly_chart(fig, use_container_width=True)

def plot_trend_year(year: list,selected_months: list, selected_opsi):
    if selected_opsi == "Jumlah_Kedatangan":
        title_ops = "Kedatangan"
    elif selected_opsi == "Total_Pendapatan":
        title_ops = "Pendapatan"
    year_filtered = df[df["year"].isin(year)]
    month_filtered = year_filtered[year_filtered["Bulan"].isin(selected_months)]
    if selected_opsi == "Total_Pendapatan":
        sales_data = month_filtered.groupby(['year', 'Bulan'])['Harga'].sum().reset_index()
    elif selected_opsi == "Jumlah_Kedatangan":
        sales_data = month_filtered.groupby(['year', 'Bulan'])['Harga'].count().reset_index()
    sales_data['Bulan'] = pd.Categorical(sales_data['Bulan'], categories=all_month, ordered=True)
    sales_data = sales_data.sort_values('Bulan')
    sales_data.columns = ['year', 'Bulan', 'Pendapatan']
    fig = px.line(
        sales_data,
        x="Bulan",
        y="Pendapatan",
        color="year",
        markers=True,
        text="Pendapatan",
        title=f"Trend {title_ops} Dalam Seyear"
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(legend=dict(title=dict(text="year"), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), height=420)

    st.plotly_chart(fig, use_container_width=True)

def service_top_rank(selected_opsi: str, year: list, month=None):
    top_rank = df[df["year"].isin(year)]
    if month != None:
        top_rank = top_rank[top_rank["Bulan"].isin(month)]
    grouped_data = top_rank.groupby("Nama Service").agg({
        "Harga": ["count", "sum"]
        }).reset_index()
    grouped_data.columns = ["Nama Layanan", "Jumlah_Kedatangan", "Total_Pendapatan"]
    grouped_data['Total_Pendapatan'] = grouped_data['Total_Pendapatan'] / 1000000
    grouped_data = grouped_data.sort_values(selected_opsi, ascending=False, ignore_index=True)
    #top_rank = top_rank.loc[:]
    grouped_data['Total_Pendapatan'] = grouped_data['Total_Pendapatan'].astype(float)
    pendapatan_max = grouped_data["Total_Pendapatan"].max()
    st.markdown("##### Layanan Teratas")
    st.dataframe(
        grouped_data,
        column_config={
            "Nama Layanan": st.column_config.Column(
                "Nama Layanan",
                width="medium",
                required=True,
            ),
            "Jumlah_Kedatangan": st.column_config.NumberColumn(
                "Jumlah Pembelian",
                help="Jumlah customer yang memilih layanan",
                width="small",
                step=1,
                format="%d Orang",
            ),
            "Total_Pendapatan": st.column_config.ProgressColumn(
                "Volum Pendapatan",
                help="Volum Pendapatan Service dengan Total Pendapatan (IDR)",
                format="Rp %fjt",
                width="medium",
                min_value=0,
                max_value=pendapatan_max
            ),
        },
        hide_index=True,
        height=390,
    )

def daily_trend(year: list, month: str, selected_opsi: str):
    daily_trend = df[df["year"].isin(year)]
    if  month.lower() == "Idul Fitri".lower():
        daily_trend = daily_trend[
            ((daily_trend['Tanggal'] >= '4/2/2022') & (daily_trend['Tanggal'] <= '5/8/2022')) |
            ((daily_trend['Tanggal'] >= '3/22/2023') & (daily_trend['Tanggal'] <= '4/28/2023'))
        ]
    else:
        daily_trend = daily_trend.loc[daily_trend["Bulan"]==month]
    if selected_opsi == "Pendapatan":
        service_totals = daily_trend.groupby("Nama Service")["Harga"].sum().reset_index()
        top_services = service_totals.nlargest(9, "Harga")["Nama Service"].tolist()
        daily_trend.loc[~daily_trend["Nama Service"].isin(top_services), "Nama Service"] = "etc"
        daily_trend_grouped = daily_trend.groupby(["Nomor Hari", "Nama Service"])["Harga"].sum().reset_index()
    elif selected_opsi == "Kedatangan":
        service_totals = daily_trend.groupby("Nama Service")["Harga"].count().reset_index()
        top_services = service_totals.nlargest(9, "Harga")["Nama Service"].tolist()
        daily_trend.loc[~daily_trend["Nama Service"].isin(top_services), "Nama Service"] = "etc"
        daily_trend_grouped = daily_trend.groupby(["Nomor Hari", "Nama Service"])["Harga"].count().reset_index()
    fig = px.bar(
        daily_trend_grouped,
        x="Nomor Hari",
        y="Harga",
        color="Nama Service",
        title=f"Grafik {selected_opsi} Harian year 2023",
        labels={"Nomor Hari": "Tanggal", "Harga": "Pendapatan"},
    )
    total_per_day = daily_trend_grouped.groupby("Nomor Hari")["Harga"].sum().reset_index()
    fig.add_trace(
        go.Scatter(
            x=total_per_day["Nomor Hari"],
            y=total_per_day["Harga"],
            mode="lines+markers",
            name="",
            line=dict(color="rgba(0, 0, 0, 0.5)"),
            marker=dict(color="rgba(0, 0, 0, 0.7)"),
            text="Total Pendapatan"
        )
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_days_trend(options_viz: str, month=None):
    days_dist = df.copy()
    days_dist['year'] = days_dist['year'].astype(str)
    if  month.lower() == "Idul Fitri".lower():
        days_dist = days_dist[
            ((days_dist['Tanggal'] >= '4/2/2022') & (days_dist['Tanggal'] <= '5/8/2022')) |
            ((days_dist['Tanggal'] >= '3/22/2023') & (days_dist['Tanggal'] <= '4/28/2023'))
        ]
    else:
        days_dist = days_dist.loc[days_dist["Bulan"]==month]
    grouped_data = days_dist.groupby(["Hari", "year"]).agg({
        "Harga": ["count", "sum"]
    }).reset_index()
    # Rename the columns for clarity
    grouped_data.columns = ["Hari", "year", "Jumlah_Kedatangan", "Total_Pendapatan"]
    grouped_data["Total_Pendapatan"] = grouped_data["Total_Pendapatan"] / 1000
    grouped_data['Hari'] = pd.Categorical(grouped_data['Hari'], categories=all_day, ordered=True)
    grouped_data = grouped_data.sort_values('Hari')
    if options_viz == "Pendapatan":
        viz_text = "Total_Pendapatan"
    elif options_viz == "Kedatangan":
        viz_text = "Jumlah_Kedatangan"
    fig = px.bar(
        grouped_data,
        x='Hari',
        y=viz_text,
        title=f'Perbandingan {options_viz} year 2022 vs 2023',
        color="year",
        barmode="group",
        text=viz_text)
    fig.update_layout(
        legend=dict(title=dict(text="year"), orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

def info_month(month, selected_opsi):
    info_month = df.copy()
    if  month.lower() == "Idul Fitri".lower():
        info_month = info_month[
            ((info_month['Tanggal'] >= '4/2/2022') & (info_month['Tanggal'] <= '5/1/2022')) |
            ((info_month['Tanggal'] >= '3/22/2023') & (info_month['Tanggal'] <= '4/21/2023'))
        ]
    else:
        info_month = info_month.loc[info_month["Bulan"]==month]
    info_month['year'] = info_month['year'].astype(str)
    grouped_data = info_month.groupby(["Hari", "year"]).agg({
        "Harga": ["count", "sum"]
    }).reset_index()
    # Rename the columns for clarity
    grouped_data.columns = ["Hari", "year", "Jumlah_Kedatangan", "Total_Pendapatan"]
    grouped_data["Total_Pendapatan"] = grouped_data["Total_Pendapatan"] / 1000000
    grouped_data['Hari'] = pd.Categorical(grouped_data['Hari'], categories=all_day, ordered=True)
    grouped_data = grouped_data.sort_values('Hari')
    grouped_data_service = info_month.groupby(["Nama Service", "year"]).agg({
        "Harga": ["count", "sum"]
    }).reset_index()
    
    grouped_data_service.columns = ["Nama Service", "year", "Jumlah_Kedatangan", "Total_Pendapatan"]
    grouped_data_service["Total_Pendapatan"] = grouped_data_service["Total_Pendapatan"] / 1000000
    if selected_opsi == "Pendapatan":
        options_selected = "Total_Pendapatan"
    elif selected_opsi == "Kedatangan":
        options_selected = "Jumlah_Kedatangan"
    grouped_data_service = grouped_data_service.sort_values(options_selected, ascending=False, ignore_index=True)
    row1 = st.columns(4)

    total_pendapatan_month = round(grouped_data[grouped_data["year"]=="2023"]["Total_Pendapatan"].sum(),1)
    total_pendapatan_month_22 = round(grouped_data[grouped_data["year"]=="2022"]["Total_Pendapatan"].sum(),1)
    jumlah_kedatangan_month = round(grouped_data[grouped_data["year"]=="2023"]["Jumlah_Kedatangan"].sum(),1)
    jumlah_kedatangan_month_22 = round(grouped_data[grouped_data["year"]=="2022"]["Jumlah_Kedatangan"].sum(),1)
    top_ns_month = grouped_data_service[(grouped_data_service["year"] == "2023")]["Nama Service"].tolist()[0]
    top_tps_month = round(grouped_data_service[(grouped_data_service["year"] == "2023")][options_selected].tolist()[0],1)
    top_ns_month_22 = grouped_data_service[(grouped_data_service["year"] == "2022")]["Nama Service"].tolist()[0]
    top_tps_month_22 = round(grouped_data_service[(grouped_data_service["year"] == "2022")][options_selected].tolist()[0],1)
    # pt => pendapatan tinggi
    days_pt23 = ', '.join(grouped_data[grouped_data["year"] == "2023"].sort_values("Total_Pendapatan")["Hari"][:3].str[:3])
    days_pt22 = ', '.join(grouped_data[grouped_data["year"] == "2022"].sort_values("Total_Pendapatan")["Hari"][:3].str[:3])
    # pr => pendapatan rendah
    days_pr23 = ', '.join(grouped_data[grouped_data["year"] == "2023"].sort_values("Total_Pendapatan", ascending=False)["Hari"][:3].str[:3])
    days_pr22 = ', '.join(grouped_data[grouped_data["year"] == "2022"].sort_values("Total_Pendapatan", ascending=False)["Hari"][:3].str[:3])
    # kt => kedatangan tinggi
    days_kt23 = ', '.join(grouped_data[grouped_data["year"] == "2023"].sort_values("Jumlah_Kedatangan")["Hari"][:3].str[:3])
    days_kt22 = ', '.join(grouped_data[grouped_data["year"] == "2022"].sort_values("Jumlah_Kedatangan")["Hari"][:3].str[:3])
    # kr => kedatangan rendah
    days_kr23 = ', '.join(grouped_data[grouped_data["year"] == "2023"].sort_values("Jumlah_Kedatangan", ascending=False)["Hari"][:3].str[:3])
    days_kr22 = ', '.join(grouped_data[grouped_data["year"] == "2022"].sort_values("Jumlah_Kedatangan", ascending=False)["Hari"][:3].str[:3])

    with row1[0].container():
        st.markdown(f'<span class="small-font">Total Pendapatan</span>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font">{total_pendapatan_month}jt (2023)</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="medium-font">{total_pendapatan_month_22}jt (2022)</p>', unsafe_allow_html=True)
    
        st.markdown(f'<span class="small-font">Hari Dengan Pendapatan Terendah</span>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font">{days_pt23} (2023)</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="medium-font">{days_pt22} (2022)</p>', unsafe_allow_html=True)
    with row1[1].container():
        st.markdown(f'<span class="small-font">Jumlah Kedatangan</span>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font">{jumlah_kedatangan_month} (2023)</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="medium-font">{jumlah_kedatangan_month_22} (2022)</p>', unsafe_allow_html=True)

        st.markdown(f'<span class="small-font">Hari Dengan Pendapatan Tertinggi</span>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font">{days_pr23} (2023)</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="medium-font">{days_pr22} (2022)</p>', unsafe_allow_html=True)
    with row1[2].container():
        st.markdown(f'<span class="small-font">Jumlah {selected_opsi} Teratas (2023)</span>', unsafe_allow_html=True)
        if selected_opsi == "Pendapatan":
            st.markdown(f'<p class="big-font">{top_tps_month} jt</p>', unsafe_allow_html=True)
        elif selected_opsi == "Kedatangan":
            st.markdown(f'<p class="big-font">{top_tps_month}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="medium-font" style="color:black">{top_ns_month}</p>', unsafe_allow_html=True)

        st.markdown(f'<span class="small-font">Hari Dengan Kedatangan Terendah</span>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font">{days_kt23} (2023)</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="medium-font">{days_kt22} (2022)</p>', unsafe_allow_html=True)
    with row1[3].container():
        st.markdown(f'<span class="small-font">Jumlah {selected_opsi} Teratas (2022)</span>', unsafe_allow_html=True)
        if selected_opsi == "Pendapatan":
            st.markdown(f'<p class="big-font">{top_tps_month_22} jt</p>', unsafe_allow_html=True)
        elif selected_opsi == "Kedatangan":
            st.markdown(f'<p class="big-font">{top_tps_month_22}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="medium-font" style="color:black">{top_ns_month_22}</p>', unsafe_allow_html=True)
    
        st.markdown(f'<span class="small-font">Hari Dengan Kedatangan Tertinggi</span>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font">{days_kr23} (2023)</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="medium-font">{days_kr22} (2022)</p>', unsafe_allow_html=True)

def format_rupiah(angka):
    angka = int(angka.replace(",", ""))
    prefixes = ["", "rb", "rts", "jt", "B", "T"]
    for prefix in reversed(prefixes):
        if abs(angka) < 1000:
            break
        angka /= 1000
    formatted_value = f"{angka:.2f} {prefix}"
    formatted_value = formatted_value.rstrip("0").rstrip(".")
    
    return formatted_value

def distribution_q_hc_ht():
    col = st.columns([5,2.5,2.5])
    hair_tr = df[df["year"].isin([2022, 2023])]
    hair_tr['year'] = hair_tr['year'].astype(str)
    with col[0]:
        selected_cat = st.selectbox("Pilih Treatment", ["cat rambut", "smothing"], index=0)
    hair_tr = hair_tr.loc[hair_tr['Nama Service'] == selected_cat]
    total_pendapatan_yearan = hair_tr.groupby('year')["Harga"].sum().reset_index()
    total_pembelian_yearan = hair_tr.groupby('year')["Harga"].count().reset_index()
    total_pendapatan_2023 = total_pendapatan_yearan[total_pendapatan_yearan["year"] == "2023"]["Harga"].values[0]
    total_pendapatan_2022 = total_pendapatan_yearan[total_pendapatan_yearan["year"] == "2022"]["Harga"].values[0]
    total_pembelian_2023 = total_pembelian_yearan[total_pembelian_yearan["year"]=="2023"]["Harga"].values[0]
    total_pembelian_2022 = total_pembelian_yearan[total_pembelian_yearan["year"] == "2022"]["Harga"].values[0]
    col[1].metric("Total Pendapatan",
                  value=format_rupiah(str(total_pendapatan_2023)),
                  delta=format_rupiah(str(total_pendapatan_2023-total_pendapatan_2022)))
    col[2].metric("Total Pembelian",
                  value=int(total_pembelian_2023),
                  delta=int(total_pembelian_2023-total_pembelian_2022))
    fig = px.histogram(hair_tr, x='Harga', color='year', marginal="box",text_auto=True, title=None)
    fig.update_layout(
        legend=dict(title=dict(text="year"), orientation="h", yanchor="bottom", y=0.5, xanchor="right", x=1),
        margin=dict(l=0, r=0, b=2, t=0),  # Adjust the margin
        yaxis=dict(title=dict(text="Pendapatan")),
        height=300  # Adjust the yaxis title standoff
    )
    st.plotly_chart(fig, use_container_width=True)


# main functions
st.sidebar.header("Main Filter")
selected_year = st.sidebar.multiselect("Pilih year", year_option, default=[year_option[1]])
all_quarters = list(quarter_months.keys())
selected_quarters = st.sidebar.multiselect("Pilih Quarter Bulan", all_quarters, default=all_quarters,help="Satu quarter terdapat 3 bulan (ex: Q1: Jan, Feb, Mar)")
selected_months = []
for quarter in selected_quarters:
    selected_months.extend(quarter_months[quarter])
selected_opsi_ts = st.sidebar.selectbox("Pilih Opsi Untuk Sorter Data", ["Total_Pendapatan", "Jumlah_Kedatangan"])
if not selected_year or not selected_months:
    st.warning("Pilih minimal satu elemen untuk setiap opsi.")
    st.stop()
month_hr = all_month + ["Idul Fitri"]
with st.expander("Detail Report Perbulan"):
    row3 = st.columns(3)
    with row3[0]:
        selected_year = st.selectbox("Pilih year", [2022, 2023], index=1)
    with row3[1]:
        selected_month = st.selectbox("Pilih Bulan", month_hr, index=0)
    with row3[2]:
        selected_opsi = st.selectbox("Pilih Opsi Visualisasi", ["Pendapatan", "Kedatangan"], index=0)
    info_month(selected_month, selected_opsi)
    row5 = st.columns(2)
    with row5[0]:
        daily_trend([selected_year], selected_month, selected_opsi)
    with row5[1]:
        plot_days_trend(selected_opsi,selected_month)
row1 = st.columns([2.5,3.75,3.75])
with row1[0]:
    main_info(selected_months)
with row1[1]:
    service_top_rank(selected_opsi_ts, selected_year)
with row1[2]:
    daily_year_trend(selected_months, selected_opsi_ts)
st.write("---")
row2 = st.columns([6.5,3.5])
with row2[0]:
    plot_trend_year(selected_year, selected_months, selected_opsi_ts)
with row2[1]:
    distribution_q_hc_ht()
