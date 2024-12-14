import numpy as np
import seaborn as sns  # Opcional para mejorar estilos
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import scipy.stats as stats
import openpyxl



# Calcular promedios, desviaciones, medianas y medias de Winsor por empleado
def calculate_winsorized_mean(series, limits=(0.05, 0.05)):
    return stats.mstats.winsorize(series, limits=limits).mean()
# Función para cargar datos generales desde un archivo Excel
def load_data():
    try:
        # Cambia 'datos_generales.xlsx' por la ruta de tu archivo Excel
        return pd.read_excel("datos_generales.xlsx")
    except Exception as e:
        st.error(f"Error al cargar datos generales: {e}")
        return pd.DataFrame()

# Función para cargar datos de empleados desde un archivo Excel
def load_employee_data():
    try:
        # Cambia 'datos_empleados.xlsx' por la ruta de tu archivo Excel
        return pd.read_excel("datos_empleados.xlsx")


    except Exception as e:
        st.error(f"Error al cargar datos de empleados: {e}")
        return pd.DataFrame()


def load_employee_data_all():
    try:
        # Cambia 'datos_empleados.xlsx' por la ruta de tu archivo Excel
        return pd.read_excel("datos_empleados_todas.xlsx")


    except Exception as e:
        st.error(f"Error al cargar datos totales de empleados : {e}")
        return pd.DataFrame()

# Cargar los datos generales
df = load_data()
df_totales =pd.read_excel("datos_empleados_todas.xlsx")


st.write("Ultima actualización: 14/12/2024")
# Título de la aplicación
st.title("Visualización de Tiempo Promedio y Desviación")

if df.empty:
    st.warning("No se pudo cargar la información del archivo Excel.")
else:
    # Creación de filtros
    st.sidebar.header("Filtros")

    producto_filter = st.sidebar.multiselect(
        "Filtrar por Producto",
        options=df["producto"].unique(),
        default=["Didi V1"]
    )

    # Filtrar dinámicamente las opciones de Subparte basadas en Producto
    filtered_df = df[df["producto"].isin(producto_filter)] if producto_filter else df

    subparte_filter = st.sidebar.multiselect(
        "Filtrar por Subparte",
        options=filtered_df["subparte"].unique(),
        default=[]
    )

    filtered_df = filtered_df[filtered_df["subparte"].isin(subparte_filter)] if subparte_filter else filtered_df
    maquina_options = filtered_df["maquina"].unique() if not filtered_df.empty else []
    # Filtro por máquina en la barra lateral
    # Filtro por Máquina
    maquina_filter = st.sidebar.multiselect(
        "Filtrar por Máquina",
        options=maquina_options,
        default=[]  # No seleccionar ninguna máquina por defecto
    )

    operaciones_filter = st.sidebar.multiselect(
        "Filtrar por Operaciones",
        options=df[
            (df["producto"].isin(producto_filter) if producto_filter else True) &
            (df["subparte"].isin(subparte_filter) if subparte_filter else True)&
            (df["maquina"].isin(maquina_filter) if maquina_filter else True)

            ]["operaciones"].unique()
    )

    st.sidebar.write("**Nota:**")
    st.sidebar.write("El modelo calcula tiempos basado en un horario de 7:00 am hasta las 5:00 pm")

    # Filtrar los datos
    filtered_data = df[
        (df["producto"].isin(producto_filter) if producto_filter else True) &
        (df["subparte"].isin(subparte_filter) if subparte_filter else True) &
        (df["maquina"].isin(maquina_filter) if maquina_filter else True) &
        (df["operaciones"].isin(operaciones_filter) if operaciones_filter else True)
    ]

    filtered_df_totales = df_totales[
        (df_totales["producto"].isin(producto_filter) if producto_filter else True) &
        (df_totales["subparte"].isin(subparte_filter) if subparte_filter else True) &
        (df_totales["maquina"].isin(maquina_filter) if maquina_filter else True) &
        (df_totales["operaciones"].isin(operaciones_filter) if operaciones_filter else True)
        ]

    # Calcular la mediana agrupando por las columnas deseadas
    median_by_group = (
        filtered_df_totales
        .groupby(["producto", "subparte", "operaciones"])["tiempo_para_500_en_horas"]
        .median()
        .reset_index()  # Opcional: convierte el resultado en un DataFrame
    )



    # Convertir id_operaciones_subparte_producto a int si es necesario
    if "id_operaciones_subparte_producto" in filtered_data.columns:
        filtered_data["id_operaciones_subparte_producto"] = filtered_data[
            "id_operaciones_subparte_producto"
        ].astype(int)
    if "id_operaciones_subparte_producto" in median_by_group.columns:
        median_by_group["id_operaciones_subparte_producto"] = median_by_group[
            "id_operaciones_subparte_producto"
        ].astype(int)





    # Mostrar datos filtrados
    st.write("Datos filtrados:")
    st.dataframe(filtered_data)

    if operaciones_filter:
        ids_operaciones = filtered_data["id_operaciones_subparte_producto"].dropna().unique()


        promedio_operacion = filtered_data["promedio_500unds_en_horas"].dropna().mean()
        promedio_operacion_mediana=median_by_group["tiempo_para_500_en_horas"].dropna().mean()


        if len(ids_operaciones) >= 1:  # Solo cargar si hay un único id seleccionado
            id_operacion = ids_operaciones[0]
            st.write(f"ID de operación seleccionada: {id_operacion}")
            #st.write(f"promedio: {promedio_operacion}")
            #st.write(f"promedio por media: {promedio_operacion_mediana}")

            # Convertir lista de operaciones seleccionadas en una cadena separada por comas
            operaciones_seleccionadas = ", ".join(operaciones_filter)

            # Código actualizado para mostrar el promedio sin corchetes
            st.markdown(f"""
                <style>
                .card {{
                    background-color: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                    text-align: center;
                    margin: 20px 0;
                }}
                .card h3 {{
                    margin: 0;
                    font-size: 1.5em;
                    color: #333;
                }}
                .card p {{
                    margin: 5px 0 0;
                    font-size: 1.2em;
                    color: #666;
                }}
                </style>
                <div class="card">
                    <h3>Promedio de Tiempo Operación seleccionada: {operaciones_seleccionadas}</h3>
                    <p>{promedio_operacion:.2f} horas promedio</p>
                    <p>{promedio_operacion_mediana:.2f} horas mediana</p>
                </div>
            """, unsafe_allow_html=True)

            employee_data = load_employee_data()
            employee_data_all = load_employee_data_all()


            if not employee_data.empty:
                # Filtrar los datos de empleados por `id_operaciones_subparte_producto`
                employee_data = employee_data[
                    employee_data["id_operaciones_subparte_producto"] == id_operacion
                ]

                # Combinar 'nombre' y 'Apellidos' para mostrar el nombre completo
                employee_data["Nombre Completo"] = employee_data["nombre"] + " " + employee_data["Apellidos"]

                # Crear un filtro múltiple para 'Nombre Completo'
                selected_names = st.sidebar.multiselect(
                    "Filtrar por Nombre Completo:",
                    options=employee_data["Nombre Completo"].unique(),
                    default=employee_data["Nombre Completo"].unique()  # Seleccionar todos por defecto
                )

                # Filtrar los datos por los nombres seleccionados
                filtered_employee_data = employee_data[
                    employee_data["Nombre Completo"].isin(selected_names)
                ]

                if len(selected_names) == 1:  # Si solo hay un nombre seleccionado
                    st.write("Promedio de tiempos por empleado:")
                    st.dataframe(filtered_employee_data)

                else:
                    st.write("Promedio de tiempos por empleado:")
                    st.dataframe(filtered_employee_data)


                if len(selected_names) > 1:  # Si hay varios nombres seleccionados
                    st.write("Comparación de tiempos promedio por empleado")

                    # Asegurarse de que la columna `promedio_500unds_en_horas` sea numérica
                    filtered_employee_data["promedio_500unds_en_horas"] = pd.to_numeric(
                        filtered_employee_data["promedio_500unds_en_horas"], errors='coerce'
                    )

                    # Eliminar filas con valores NaN en la columna
                    filtered_employee_data = filtered_employee_data.dropna(subset=["promedio_500unds_en_horas"])

                    if not filtered_employee_data.empty:
                        # Agrupar los datos por 'Nombre Completo' y calcular promedios y desviaciones estándar
                        comparison_data = filtered_employee_data.groupby("Nombre Completo")[
                            "promedio_500unds_en_horas"].agg(
                            promedio="mean",
                            desviacion="std"
                        )

                        # Calcular el promedio general de todos los empleados seleccionados
                        overall_mean = comparison_data["promedio"].mean()

                        # Crear el gráfico
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.bar(
                            comparison_data.index,
                            comparison_data["promedio"],
                            yerr=comparison_data["desviacion"],  # Agregar barras de error
                            capsize=5,
                            alpha=0.75,
                            color='skyblue',
                            edgecolor='black'
                        )

                        # Dibujar la línea del promedio general
                        ax.axhline(overall_mean, color='red', linestyle='--', linewidth=2,
                                   label=f'Promedio General: {overall_mean:.2f}')

                        ax.set_title("Comparación de Tiempos Promedio por Empleado ")
                        ax.set_xlabel("Empleado")
                        ax.set_ylabel("Tiempo Promedio (horas)")
                        ax.set_xticklabels(comparison_data.index, rotation=45, ha='right', fontsize=9)
                        ax.legend()

                        st.pyplot(fig)




                    else:
                        st.warning("No hay datos válidos para graficar después de filtrar.")
            else:
                st.warning("No se encontraron datos adicionales para la operación seleccionada.")

            plt.style.use("ggplot")  # Puedes usar otros estilos como 'seaborn' o 'fivethirtyeight'

            # Verificar que hay datos en `employee_data_all`
            if not employee_data_all.empty:
                if "id_operaciones_subparte_producto" in employee_data_all.columns and \
                        "nombre" in employee_data_all.columns and "Apellidos" in employee_data_all.columns:

                    # Filtrar los datos de empleados por `id_operaciones_subparte_producto`
                    employee_data_all = employee_data_all[
                        employee_data_all["id_operaciones_subparte_producto"] == id_operacion
                        ]

                    # Crear columna de nombre completo
                    employee_data_all["Nombre Completo"] = employee_data_all["nombre"] + " " + employee_data_all[
                        "Apellidos"]


                    # Filtrar nombres
                    #selected_names = st.sidebar.multiselect(
                     #   "Filtrar por Nombre Completo:",
                      #  options=employee_data_all["Nombre Completo"].unique(),
                       # default=employee_data_all["Nombre Completo"].unique(),
                        #key="unique_key_selected_names"  # Evitar conflictos
                    #)

                    # Filtrar los datos por los nombres seleccionados
                    filtered_employee_data_all = employee_data_all[
                        employee_data_all["Nombre Completo"].isin(selected_names)
                    ]

                    st.write("Tiempos de la Operación seleccionada")
                    st.dataframe(employee_data_all)

                    if len(selected_names) > 1:  # Si hay varios nombres seleccionados
                        st.write("Comparación de tiempos promedio por empleado con ajustes para valores dispersos:")

                        if "tiempo_para_500_en_horas" in filtered_employee_data_all.columns:
                            filtered_employee_data_all["tiempo_para_500_en_horas"] = pd.to_numeric(
                                filtered_employee_data_all["tiempo_para_500_en_horas"], errors='coerce'
                            )
                            filtered_employee_data_all = filtered_employee_data_all.dropna(
                                subset=["tiempo_para_500_en_horas"]
                            )

                            if not filtered_employee_data_all.empty:
                                # Identificar y eliminar outliers usando percentiles
                                q_low = filtered_employee_data_all["tiempo_para_500_en_horas"].quantile(0.05)
                                q_high = filtered_employee_data_all["tiempo_para_500_en_horas"].quantile(0.95)
                                adjusted_data = filtered_employee_data_all[
                                    (filtered_employee_data_all["tiempo_para_500_en_horas"] >= q_low) &
                                    (filtered_employee_data_all["tiempo_para_500_en_horas"] <= q_high)
                                    ]

                                # Calcular promedios y medianas por empleado

                                #comparison_data = adjusted_data.groupby("Nombre Completo")[
                                 #   "tiempo_para_500_en_horas"
                                #].agg(promedio="mean", desviacion="std", mediana="median").reset_index()



                                comparison_data = filtered_employee_data_all.groupby("Nombre Completo")[
                                    "tiempo_para_500_en_horas"
                                ].agg(promedio="mean", desviacion="std", mediana="median").reset_index()

                                # Calcular el promedio general y la mediana general
                                promedio_general = adjusted_data["tiempo_para_500_en_horas"].mean()
                                promedio_general = filtered_employee_data_all["tiempo_para_500_en_horas"].mean()
                                mediana_general = adjusted_data["tiempo_para_500_en_horas"].median()

                                # Gráfico principal con datos ajustados
                                fig, ax = plt.subplots(figsize=(12, 6))
                                bar_positions = range(len(comparison_data))

                                # Dibujar barras
                                bars = ax.bar(
                                    comparison_data["Nombre Completo"],
                                    comparison_data["promedio"],
                                    yerr=comparison_data["desviacion"],
                                    capsize=5,
                                    alpha=0.8,
                                    color=sns.color_palette("pastel", len(comparison_data)),
                                    edgecolor="black",
                                    linewidth=1.2
                                )

                                # Dibujar línea del promedio general
                                ax.axhline(promedio_general, color="red", linestyle="--", linewidth=2,
                                           label="Promedio General")

                                # Dibujar línea de la mediana general
                                ax.axhline(mediana_general, color="blue", linestyle=":", linewidth=2,
                                           label="Mediana General")

                                # Agregar la mediana de cada empleado como un punto sobre las barras
                                for i, name in enumerate(comparison_data["Nombre Completo"]):
                                    mediana_empleado = \
                                    comparison_data.loc[comparison_data["Nombre Completo"] == name, "mediana"].values[0]
                                    ax.scatter(
                                        i, mediana_empleado,
                                        color="purple", s=100, zorder=5,
                                        label="Mediana por Empleado" if i == 0 else None
                                    )
                                    ax.text(
                                        i, mediana_empleado + 0.5, f"{mediana_empleado:.2f}",
                                        color="purple", fontsize=10, ha="center", va="bottom"
                                    )

                                # Agregar puntos de dispersión con jitter reducido
                                for i, name in enumerate(comparison_data["Nombre Completo"]):
                                    puntos_empleado = adjusted_data[
                                        adjusted_data["Nombre Completo"] == name
                                        ]["tiempo_para_500_en_horas"]

                                    x_jitter = np.random.normal(loc=i, scale=0.1, size=len(puntos_empleado))
                                    ax.scatter(
                                        x_jitter,
                                        puntos_empleado,
                                        color="darkblue",
                                        alpha=0.7,
                                        s=15,
                                        edgecolor="white",
                                        linewidth=0.5,
                                        label="Dispersión" if i == 0 else None
                                    )

                                # Configurar ejes y leyenda
                                ax.set_title("Comparación de Tiempos Promedio y Mediana por Empleado (Ajustado)",
                                             fontsize=14, weight="bold")
                                ax.set_xlabel("Empleado", fontsize=12)
                                ax.set_ylabel("Tiempo Promedio (horas)", fontsize=12)
                                ax.set_xticks(bar_positions)
                                ax.set_xticklabels(comparison_data["Nombre Completo"], rotation=45, ha="right",
                                                   fontsize=10)
                                ax.legend(loc="upper left", fontsize=10)

                                st.pyplot(fig)

                                # **1. Análisis de Distribución de Tiempos**
                                st.write("### Análisis de Distribución de Tiempos")
                                fig, ax = plt.subplots(figsize=(10, 6))
                                sns.histplot(filtered_employee_data["promedio_500unds_en_horas"], kde=True, ax=ax,
                                             color='skyblue')
                                ax.set_title("Distribución de Tiempos Promedio")
                                ax.set_xlabel("Tiempo Promedio (horas)")
                                ax.set_ylabel("Frecuencia")
                                st.pyplot(fig)

                                # **5. Heatmap de Tiempos Promedio**
                                st.write("### Mapa de Calor de Tiempos Promedio por Operación")
                                if "id_operaciones_subparte_producto" in filtered_employee_data.columns:
                                    heatmap_data = filtered_employee_data.pivot_table(
                                        values="promedio_500unds_en_horas",
                                        index="Nombre Completo",
                                        columns="id_operaciones_subparte_producto",
                                        aggfunc="mean"
                                    )
                                    fig, ax = plt.subplots(figsize=(10, 8))
                                    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
                                    ax.set_title("Mapa de Calor de Tiempos Promedio")
                                    st.pyplot(fig)

                                # Cuadro de entrada para establecer la meta
                                meta = st.number_input("Establece la meta en horas:", min_value=0.0, step=0.1,
                                                       value=5.0)








                            else:
                                st.warning("No hay datos válidos para graficar después de filtrar.")
                        else:
                            st.warning("La columna 'tiempo_para_500_en_horas' no está presente en los datos.")
                else:
                    st.error(
                        "El archivo de empleados no contiene las columnas requeridas: 'id_operaciones_subparte_producto', 'nombre', o 'Apellidos'."
                    )
            else:
                st.warning("El archivo de datos de empleados está vacío.")






        else:
            st.warning("Por favor, asegúrate de seleccionar una única operación para ver detalle promedio Empleados")

    # Visualización de gráficos
    if not filtered_data.empty:


        st.write("Gráficos de datos filtrados:")

        # Input para la cantidad de unidades
        cantidad_unidades = st.number_input("Ingresa la cantidad de unidades:", min_value=1, value=500, step=1)

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Operaciones por Producto", "promedio por producto","Sección", "Máquinas", "Predicción de tiempos"])

        with tab1:


            if "promedio_500unds_en_horas" in filtered_data.columns and "desviacion_estandar_en_horas" in filtered_data.columns:
                # Ajustar las columnas de datos al valor dinámico ingresado
                filtered_data["promedio_por_unds_en_horas"] = filtered_data["promedio_500unds_en_horas"] * (
                            cantidad_unidades / 500)
                filtered_data["desviacion_por_unds_en_horas"] = filtered_data["desviacion_estandar_en_horas"] * (
                            cantidad_unidades / 500)

                # Agrupar los datos por producto y operación
                grouped_data = filtered_data.groupby(["producto", "operaciones"])[
                    ["promedio_por_unds_en_horas", "desviacion_por_unds_en_horas"]
                ].mean().reset_index()

                # Crear un gráfico de barras para mostrar operaciones separadas por productos
                fig, ax = plt.subplots(figsize=(12, 6))

                # Obtener lista de operaciones únicas y productos únicos
                unique_operations = grouped_data["operaciones"].unique()
                unique_products = grouped_data["producto"].unique()

                # Definir colores para los productos
                colors = plt.cm.tab10(range(len(unique_products)))

                # Ancho de cada barra
                bar_width = 0.8 / len(unique_products)  # Distribuir barras en un rango fijo

                # Coordenadas x para las operaciones
                x_positions = range(len(unique_operations))

                # Dibujar barras para cada producto
                for i, product in enumerate(unique_products):
                    product_data = grouped_data[grouped_data["producto"] == product]

                    # Alinear datos con las operaciones únicas para evitar problemas de shape
                    aligned_data = pd.DataFrame({"operaciones": unique_operations}).merge(
                        product_data,
                        on="operaciones",
                        how="left"
                    ).fillna(0)  # Llenar con 0 para operaciones no presentes en el producto

                    # Ajustar las posiciones en x para este producto
                    product_x_positions = [x + (i * bar_width) for x in x_positions]

                    ax.bar(
                        product_x_positions,
                        aligned_data["promedio_por_unds_en_horas"],
                        yerr=aligned_data["desviacion_por_unds_en_horas"],
                        width=bar_width,
                        label=product,
                        capsize=5,
                        alpha=0.75,
                        color=colors[i],
                        edgecolor='black'
                    )

                # Etiquetas y configuraciones del gráfico
                ax.set_xlabel("Operaciones")
                ax.set_ylabel(f"Promedio (horas) para {cantidad_unidades} unidades")
                ax.set_title("Promedio por Operaciones Separadas por Producto")
                ax.set_xticks([x + (bar_width * (len(unique_products) / 2 - 0.5)) for x in x_positions])
                ax.set_xticklabels(unique_operations, rotation=45, ha='right', fontsize=9)
                ax.legend(title="Productos")

                # Mostrar el gráfico
                st.pyplot(fig)
            else:
                st.warning(
                    "No se encontraron las columnas necesarias para el gráfico ('promedio_500unds_en_horas', 'desviacion_estandar_en_horas')."
                )

        with tab2:





            if "promedio_500unds_en_horas" in filtered_data.columns:
                # Ajustar los datos al valor dinámico ingresado
                filtered_data["promedio_por_unds_en_horas"] = filtered_data["promedio_500unds_en_horas"] * (
                        cantidad_unidades / 500)

                # Sumar tiempos ajustados por producto
                suma_por_producto = filtered_data.groupby("producto")["promedio_por_unds_en_horas"].sum()

            # Ajustar los datos para la mediana si existe 'tiempo_para_500_en_horas'
            if "tiempo_para_500_en_horas" in median_by_group.columns:
                median_by_group["tiempo_por_unds_en_horas"] = median_by_group["tiempo_para_500_en_horas"] * (
                        cantidad_unidades / 500)
                suma_por_producto_mediana = median_by_group.groupby("producto")["tiempo_por_unds_en_horas"].sum()
            else:
                suma_por_producto_mediana = None

                # Mostrar las sumas ajustadas
                st.write(f"Suma de tiempos ajustados por producto (promedio) para {cantidad_unidades} unidades:")
                st.bar_chart(suma_por_producto)

            if suma_por_producto_mediana is not None:
                st.write(f"Suma de tiempos ajustados por producto (mediana) para {cantidad_unidades} unidades:")
                st.bar_chart(suma_por_producto_mediana)

            if suma_por_producto_mediana is not None:
                st.write("Suma de tiempos ajustados por producto (mediana):")
                st.bar_chart(suma_por_producto_mediana)





        with tab3:
            if "promedio_500unds_en_horas" in filtered_data.columns:
                # Ajustar los datos al valor dinámico ingresado
                filtered_data["promedio_por_unds_en_horas"] = filtered_data["promedio_500unds_en_horas"] * (
                        cantidad_unidades / 500)

                # Sumar tiempos ajustados por subparte
                suma_por_subparte = filtered_data.groupby("subparte")["promedio_por_unds_en_horas"].sum()

                # Mostrar la suma ajustada por subparte
                st.write(f"Suma de tiempos ajustados por subparte para {cantidad_unidades} unidades:")
                st.bar_chart(suma_por_subparte)

            # Gráfico de torta para tiempos ajustados por subparte
            st.write(
                f"Distribución porcentual de tiempos ajustados por subparte para {cantidad_unidades} unidades:")
            fig_subparte, ax_subparte = plt.subplots()
            ax_subparte.pie(
                suma_por_subparte,
                labels=suma_por_subparte.index,
                autopct='%1.1f%%',
                startangle=90,
                colors=plt.cm.tab20.colors
            )
            ax_subparte.axis('equal')  # Asegura que el gráfico sea un círculo perfecto
            st.pyplot(fig_subparte)

        with tab4:
    #if "promedio_500unds_en_horas" in filtered_data.columns:


                # Gráfico de barras: Suma de tiempos por máquina


                # Gráfico de torta para tiempos por máquina



            if "promedio_500unds_en_horas" in filtered_data.columns:
                # Ajustar los datos al valor dinámico ingresado
                filtered_data["promedio_por_unds_en_horas"] = filtered_data["promedio_500unds_en_horas"] * (
                        cantidad_unidades / 500)

                # Sumar tiempos ajustados por máquina
                suma_por_maquina = filtered_data.groupby("maquina")["promedio_por_unds_en_horas"].sum()

                # Mostrar la suma ajustada por máquina
                st.write(f"Suma de tiempos ajustados por máquina para {cantidad_unidades} unidades:")
                st.bar_chart(suma_por_maquina)





            if "promedio_500unds_en_horas" in filtered_data.columns:
                # Ajustar los datos al valor dinámico ingresado
                filtered_data["promedio_por_unds_en_horas"] = filtered_data["promedio_500unds_en_horas"] * (
                            cantidad_unidades / 500)

                # Sumar tiempos ajustados por máquina
                suma_por_maquina = filtered_data.groupby("maquina")["promedio_por_unds_en_horas"].sum()

                # Gráfico de torta: Distribución porcentual de tiempos por máquina
                st.write(f"Distribución porcentual de tiempos ajustados por máquina para {cantidad_unidades} unidades:")
                fig_maquina, ax_maquina = plt.subplots()
                ax_maquina.pie(
                    suma_por_maquina,
                    labels=suma_por_maquina.index,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=plt.cm.tab20.colors
                )
                ax_maquina.axis('equal')  # Asegura que el gráfico sea un círculo perfecto
                st.pyplot(fig_maquina)

        with tab5:

            # Crear un diccionario para almacenar las cantidades personalizadas
            cantidades = {}

            st.markdown("### Introduce las cantidades para cada producto seleccionado:")
            for producto in suma_por_producto.index:
                cantidades[producto] = st.number_input(
                    f"Cantidad para {producto}:",
                    min_value=1,
                    value=500,
                    step=1,
                    help=f"Ingresa la cantidad de unidades para el producto {producto}."
                )

            # Calcular los tiempos totales ajustados para cada producto
            total_horas_por_producto = {
                producto: (suma_por_producto[producto] / 500) * cantidades[producto]
                for producto in suma_por_producto.index
            }
            # Calcular los tiempos totales ajustados para cada producto usando la mediana
            total_horas_por_producto_mediana = {
                producto: (suma_por_producto_mediana.get(producto, 0) / 500) * cantidades[producto]
                for producto in suma_por_producto.index
            }


            # Agregar estilos CSS con st.markdown antes del bucle de los productos
            st.markdown("""
                <style>
                .card {
                    background-color: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                    text-align: center;
                    margin: 20px 0;
                }
                .card h3 {
                    margin: 0;
                    font-size: 1.5em;
                    color: #333;
                }
                .card p {
                    margin: 5px 0 0;
                    font-size: 1.2em;
                    color: #666;
                }
                </style>
            """, unsafe_allow_html=True)

            # Generar los cards para cada producto
            for producto, total_horas in total_horas_por_producto.items():
                promedio_por_mediana = suma_por_producto_mediana.get(producto, 0)  # Obtén el promedio basado en la mediana
                st.markdown(f"""
                    <div class="card">
                        <h3>{producto}</h3>
                        <p>Promedio basado en la media: {total_horas:.2f} horas para {cantidades[producto]} unidades</p>
                         <p>Promedio basado en la mediana: {promedio_por_mediana:.2f} horas para {cantidades[producto]} unidades</p>
                    </div>
                """, unsafe_allow_html=True)

            # Calcular el total consolidado de horas
            total_consolidado = sum(total_horas_por_producto.values())
            # Calcular el total consolidado basado en la mediana
            total_consolidado_mediana = sum(total_horas_por_producto_mediana.values())


            # Agregar un margen del 10% al total consolidado
            margen_error = total_consolidado * 0.10
            total_consolidado_con_margen = total_consolidado + margen_error

            # Agregar un margen del 10% al total consolidado por mediana
            margen_error_mediana = total_consolidado_mediana * 0.10
            total_consolidado_mediana_con_margen = total_consolidado_mediana + margen_error_mediana

            # Mostrar el total consolidado con margen
            st.markdown(f"""
                <div class="card">
                    <h3>Total Consolidado</h3>
                    <p>{total_consolidado:.2f} horas (Estimado por Media)</p>
                    <p>{total_consolidado_con_margen:.2f} horas (Con Margen del 10% por Media)</p>
                    <hr>
                    <p>{total_consolidado_mediana:.2f} horas (Estimado por Mediana)</p>
                    <p>{total_consolidado_mediana_con_margen:.2f} horas (Con Margen del 10% por Mediana)</p>
                </div>
            """, unsafe_allow_html=True)

            # Inputs: Número de Trabajadores y Horas al Día
            st.markdown("### Parámetros del Proyecto")
            numero_empleados = st.number_input(
                "Número de Empleados:",
                min_value=1,
                value=5,  # Número por defecto
                step=1,
                help="Cantidad de empleados disponibles para trabajar en el proyecto."
            )

            horas_por_dia = st.number_input(
                "Horas por Día:",
                min_value=1,
                max_value=24,
                value=8,  # Horas por defecto
                step=1,
                help="Número de horas que cada empleado trabaja por día."
            )

            # Calcular los días requeridos
            if numero_empleados > 0 and horas_por_dia > 0:
                dias_requeridos = total_consolidado_con_margen / (numero_empleados * horas_por_dia)
                dias_requeridos_mediana = total_consolidado_mediana_con_margen /(numero_empleados * horas_por_dia)
            else:
                dias_requeridos = float("inf")  # Manejar caso de división por 0
                dias_requeridos
            # Mostrar el resultado en un card
            st.markdown(f"""
                <div class="card">
                    <h3>Tiempo Requerido (media)</h3>
                    <p><b>{dias_requeridos:.2f} días</b> requeridos para completar el proyecto</p>
                    <p>Con {numero_empleados} empleados trabajando {horas_por_dia} horas al día.</p>
                    <h3>Tiempo Requerido (Mediana)</h3>
                    <p><b>{dias_requeridos_mediana:.2f} días</b> requeridos para completar el proyecto</p>
                    <p>Con {numero_empleados} empleados trabajando {horas_por_dia} horas al día.</p>
                </div>
            """, unsafe_allow_html=True)









    else:
        st.warning("No hay datos para los filtros seleccionados.")
