import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Perfilamiento Préstamos", layout="wide")

st.title("Perfilamiento de Clientes - Thera Bank")
st.markdown("###Objetivo")
st.markdown("Identificar visualmente el perfil de los clientes que aceptan préstamos personales, para mejorar el enfoque de las campañas de marketing.")
st.markdown("###Hipótesis")
st.markdown("Los clientes con mayor ingreso, gasto en tarjeta de crédito y productos como banca online o cuentas CD son más propensos a aceptar el préstamo.")


#carga y preparacion de datos
@st.cache_data
def load_data():
    return pd.read_excel("Bank_Personal_Loan_Modelling.xlsx", sheet_name="Data")

df = load_data()
df = df.drop(columns=["ID", "ZIP Code"])
df["Education_label"] = df["Education"].map({1: "Undergrad", 2: "Graduate", 3: "Advanced"})


# Distribución de objetivo
st.header("¿Cuántos aceptaron el préstamo?")

col1, col2 = st.columns([2, 1]) 

with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    loan_dist = df["Personal Loan"].value_counts(normalize=True) * 100
    sns.barplot(x=["No", "Sí"], y=loan_dist.values, palette="Set2", ax=ax)
    ax.set_ylabel("% de clientes")
    ax.set_title("Distribución general del objetivo")
    st.pyplot(fig)

with col2:
    st.markdown("**Comentario:**")
    st.markdown("""
    La distribución muestra un desbalance claro: aproximadamente el 9% de los clientes aceptaron el préstamo, mientras que el 91% lo rechazó.  
    Este comportamiento sugiere que el producto financiero ofrecido no es atractivo para la mayoría del público, o lo mas probable es que no se está segmentando adecuadamente.

    Por ello, se hará un perfilamiento visual y analítico que permita identificar qué características tienen en comun los clientes que sí aceptaron.  
    Así, se podrá diseñar una estrategia de marketing más precisa y eficiente, focalizando los recursos en quienes tienen mayor probabilidad de conversión.
    """)


# 1. ¿Cómo se distribuyen los ingresos por grupo?
st.subheader("1. ¿Cómo se distribuyen los ingresos por grupo?")
col3, col4 = st.columns(2)

with col3:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.kdeplot(data=df, x="Income", hue="Personal Loan", fill=True, ax=ax, palette="coolwarm")
    ax.set_title("Densidad de ingreso por grupo")
    st.pyplot(fig)

with col4:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x="Personal Loan", y="Income", palette="coolwarm", ax=ax)
    ax.set_xticklabels(["No", "Sí"])
    ax.set_title("Boxplot de ingreso")
    st.pyplot(fig)

st.markdown("**Comentario:**")
st.markdown("""
 - En el primer gráfico de densidad se evidencia que los clientes que no aceptaron el préstamo tienen una alta concentración en ingresos bajos (entre 40k y 80k), mientras que quienes sí lo aceptaron tienen distribuciones mas desplazadas a la derecha, es decir, hacia ingresos mucho más altos (más de 120k), aunque en menor cantidad.

 - En el segundo gráfico (boxplot) se observa que los clientes que aceptaron préstamos tienen una mediana de ingresos significativamente mayor (alrededor de 140k), mientras que quienes no aceptaron se concentran en ingresos inferiores a 80k.
            Además, solo el grupo que no acepto presenta muchos valores atípicos, lo que indica que dentro de este segmento existen algunos clientes con ingresos altos que, sin embargo, no tomaron el préstamo. Esto podría reflejar falta de interés, necesidades distintas o desajustes en la estrategia de marketing.

En conclusion, ambos gráficos complementan visualmente un patron, el cual es de que el ingreso es una variable altamente discriminante para la aceptación del préstamo. Este hallazgo valida la hipótesis y confirma que debe considerarse como una variable clave para el perfilamiento de clientes.
""")


# 2. Gasto en tarjeta 
st.subheader("2️. ¿Existe una diferencia significativa en el gasto con tarjeta de crédito entre quienes aceptan y no aceptan el préstamo?")
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.violinplot(data=df, x="Personal Loan", y="CCAvg", palette="Purples", ax=ax)
    ax.set_xticklabels(["No", "Sí"])
    ax.set_title("Distribución del gasto en tarjeta de crédito")
    st.pyplot(fig)

st.markdown("**Comentario:**")
st.markdown("""
- El gráfico muestra que los clientes que no aceptaron el préstamo tienen un gasto mensual con tarjeta de crédito (CCAvg) concentrado principalmente por debajo de 2.5k, con una densidad alta en valores bajos y baja dispersión.

- Por otro lado, los clientes que sí aceptaron el préstamo presentan una distribución más uniforme y extendida, con una mediana de gasto claramente superior y un rango que se extiende hasta los 10k.

Se puede inferir que los clientes que aceptan préstamos tienen un comportamiento financiero más activo, probablemente tienen una mayor capacidad crediticia o estilo de vida más orientado al consumo. Esta variable es útil para segmentar perfiles con mayor probabilidad de aceptación.
""")




# 3. ¿Qué variables numéricas están más relacionadas?
st.subheader("3️. ¿Qué variables numéricas están más relacionadas y aportan al perfilamiento del cliente?")

left_pad, center_col, right_pad = st.columns([1, 2, 1])  

with center_col:
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    num_vars = ["Age", "Experience", "Income", "CCAvg", "Mortgage"]
    corr = df[num_vars].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=ax)
    ax.set_title("Matriz de correlación entre variables numéricas")
    st.pyplot(fig)

    st.markdown("""
    **Comentario:**

    - Se observa una correlación casi perfecta entre edad y experiencia (0.99), lo que sugiere que aportan información redundante. Podría considerarse una sola para simplificar el perfil.

    - También hay una correlación moderada (0.65) entre ingreso y gasto promedio con tarjeta (CCAvg), lo que refuerza la idea de que clientes con mayor capacidad económica también tienden a consumir más.

    """)



# 5. Productos digitales
st.subheader("5️.  ¿Influyen los productos digitales?")

col6, col7 = st.columns(2)
for col, var, label in zip([col6, col7], ["Online", "CD Account"], ["Banca Online", "Cuenta CD"]):
    with col:
        fig, ax = plt.subplots(figsize=(5.5, 4))
        df_group = pd.crosstab(df[var], df["Personal Loan"], normalize='index') * 100
        df_group.plot(kind="bar", stacked=True, colormap="cool", ax=ax, legend=False)
        ax.set_title(f"Aceptación por {label}")
        ax.set_ylabel("% dentro del grupo")
        ax.legend(["No", "Sí"])
        st.pyplot(fig)
        st.markdown(f"**Comentario:** Clientes con {label.lower()} muestran mayor aceptación.")

# 6. Explorador interactivo 
st.subheader("6️. Aceptacion de prestamos segun diferentes variables")
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    opciones = st.selectbox("Selecciona variable para comparar:", ["Education_label", "Family", "CreditCard", "Securities Account"])

    fig, ax = plt.subplots(figsize=(6, 4))
    ct = pd.crosstab(df[opciones], df["Personal Loan"], normalize='index') * 100
    ct.plot(kind="bar", stacked=True, ax=ax, colormap="Paired")
    ax.set_ylabel("% dentro del grupo")
    ax.set_title(f"Aceptación según {opciones}")
    ax.legend(["No", "Sí"])
    st.pyplot(fig)

    st.markdown("'''**Comentario:** Del análisis interactivo por variables categóricas como nivel educativo, tamaño de familia, uso de tarjeta de crédito y cuenta de valores, se observa que los clientes con mayor nivel educativo (“Graduate” y “Advanced”) tienen una mayor tasa de aceptación del préstamo. Asimismo, las familias con 3 o 4 miembros muestran también mayor disposición, lo cual puede estar vinculado a necesidades económicas más amplias. Además, los clientes que ya poseen productos financieros como tarjetas de crédito o cuentas de valores tienen una mayor tasa de aceptación, lo que sugiere familiaridad con productos bancarios o mejor perfil financiero. Este análisis aporta información clave para segmentar campañas según características demográficas y de comportamiento financiero.'''")



# Conclusión final
st.header("Conclusión")
st.markdown("""
El perfilamiento visual permitió validar la hipótesis planteada: los clientes que aceptan préstamos personales en Thera Bank tienden a tener características financieras y demográficas claramente diferenciadas. En particular, destacan por tener mayores ingresos, gastos más altos en tarjetas de crédito, uso de productos digitales como banca online o cuentas CD, así como niveles educativos superiores y familias más numerosas. Además, las correlaciones entre variables indican que edad, experiencia e ingreso están vinculados, lo que refuerza el perfil de un cliente económicamente consolidado. Esta información es valiosa para dirigir con mayor precisión los esfuerzos de marketing, optimizando recursos y aumentando la tasa de aceptación al enfocarse en los segmentos más propensos al préstamo.
""")
