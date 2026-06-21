import streamlit as st
import pandas as pd
from datetime import datetime
import math

# Configuración de pantalla ancha y estilo visual premium
st.set_page_config(page_title="Variedades JAW - Sistema Inteligente", page_icon="⚡", layout="wide")

# Inicialización de bases de datos internas en memoria
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {} 
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame(
        columns=["Fecha", "Año", "Mes", "Día", "Producto", "Cantidad", "Precio ($)", "Registrado Por"]
    )
if 'ventas' not in st.session_state:
    st.session_state.ventas = pd.DataFrame(
        columns=["Hora/Fecha", "Producto Vendido", "Cant. Vendida", "Total Recaudado ($)", "Vendedor"]
    )
if 'ajustes_caja' not in st.session_state:
    st.session_state.ajustes_caja = pd.DataFrame(
        columns=["Hora/Fecha", "Tipo", "Descripción", "Monto ($)", "Responsable"]
    )
if 'chat' not in st.session_state:
    st.session_state.chat = [{"usuario": "Sistema", "mensaje": "¡Bienvenidos al panel inteligente de Variedades JAW! 🚀"}]
if 'ordenes_admin' not in st.session_state:
    st.session_state.ordenes_admin = []  
if 'laborando' not in st.session_state:
    st.session_state.laborando = True
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = ""
if 'rol_actual' not in st.session_state:
    st.session_state.rol_actual = ""
# MEMORIA DE PANTALLA DIGITAL DE LA CALCULADORA
if 'pantalla_calc' not in st.session_state:
    st.session_state.pantalla_calc = ""

# --- TIEMPO REAL ---
ahora = datetime.now()
hora_reloj = ahora.strftime("%I:%M:%S %p")
dia_act = ahora.strftime("%d")
mes_act = ahora.strftime("%m")
ano_act = ahora.strftime("%Y")
fecha_completa = ahora.strftime("%Y-%m-%d")

# --- DISEÑO VISUAL PREMIUM Y ESTILOS 3D ---
st.markdown("""
    <style>
    .welcome-container {
        background-image: linear-gradient(135deg, #1f2833 0%, #0b0c10 100%);
        padding: 35px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 2px solid #6C63FF;
    }
    .welcome-title { color: #ffffff; font-size: 38px; font-weight: 800; letter-spacing: 1px; }
    .reloj-style {
        background: linear-gradient(135deg, #FF4B4B, #6C63FF);
        color: white; padding: 12px; border-radius: 12px; text-align: center; font-family: monospace; font-size: 22px; font-weight: bold;
    }
    .chat-card { 
        background-color: #ffffff !important; 
        color: #111111 !important; 
        padding: 12px; 
        border-radius: 8px; 
        margin-bottom: 8px; 
        border-left: 6px solid #FF4B4B;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .chat-text { color: #222222 !important; font-size: 15px; }
    .alerta-grave { background-color: #FF4B4B; color: white; padding: 15px; border-radius: 10px; font-weight: bold; margin-bottom: 15px; border: 2px solid white; }
    .ganancia-box {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white; padding: 20px; border-radius: 15px; text-align: center; font-size: 26px; font-weight: bold; margin-top: 10px;
    }
    
    /* CHASIS CONTENEDOR 3D DE LA CALCULADORA */
    .chasis-3d {
        background: linear-gradient(135deg, #3a3d46 0%, #1e2024 100%);
        padding: 20px;
        border-radius: 18px;
        border-top: 3px solid #5a5e6b;
        border-left: 2px solid #4a4e5a;
        border-right: 4px solid #111215;
        border-bottom: 7px solid #0d0e10;
        box-shadow: 0px 15px 25px rgba(0,0,0,0.6), inset 0px 1px 3px rgba(255,255,255,0.2);
        margin-bottom: 20px;
    }
    
    /* BOTONES ESTILO REALISTA 3D */
    .stButton > button {
        width: 100% !important;
        height: 48px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        transition: all 0.05s ease-in-out !important;
    }
    
    /* Variaciones de botones inyectados por orden de fila */
    div[data-testid="stSidebar"] button {
        background: linear-gradient(180deg, #4c515f 0%, #333742 100%) !important;
        color: #ffffff !important;
        border-top: 2px solid #656c7e !important;
        border-bottom: 4px solid #1c1e24 !important;
        border-left: 1px solid #4c515f !important;
        border-right: 1px solid #1c1e24 !important;
        box-shadow: 0px 4px 5px rgba(0,0,0,0.4) !important;
    }
    div[data-testid="stSidebar"] button:active {
        border-bottom: 1px solid #1c1e24 !important;
        transform: translateY(3px) !important;
        box-shadow: 0px 1px 2px rgba(0,0,0,0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------
# PANTALLA DE ACCESO (LOGIN / REGISTRO)
# -----------------------------------------------------------------
if not st.session_state.autenticado:
    st.markdown('<div class="welcome-container"><div class="welcome-title">👋 ¡Hola, bienvenido a Variedades JAW! ✨</div></div>', unsafe_allow_html=True)
    col_cen, _ = st.columns([2, 1])
    
    with col_cen:
        if not st.session_state.usuarios:
            st.info("📢 **SISTEMA NUEVO:** Registra el primer usuario como 'Administrador' para tomar el control de Variedades JAW.")
            
        pestana_acceso = st.radio("Selecciona una opción:", ["🔐 Iniciar Sesión", "📝 Registrar Nuevo Usuario"], horizontal=True)
        st.divider()
        
        if pestana_acceso == "🔐 Iniciar Sesión":
            user_input = st.text_input("Usuario:", placeholder="Tu usuario...", key="login_user")
            pass_input = st.text_input("Contraseña:", type="password", placeholder="Tu clave...", key="login_pass")
            
            if st.button("🚀 Entrar al Sistema", use_container_width=True):
                user_key = user_input.strip().lower()
                if user_key in st.session_state.usuarios and st.session_state.usuarios[user_key]["password"] == pass_input:
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = user_input
                    st.session_state.rol_actual = st.session_state.usuarios[user_key]["role"]
                    st.rerun()
                else:
                    st.error("❌ Datos incorrectos.")
                    
        else:
            nuevo_user = st.text_input("Nombre de Usuario:", placeholder="Ej: erick_jaw", key="reg_user")
            nuevo_pass = st.text_input("Contraseña:", type="password", placeholder="Crea tu clave...", key="reg_pass")
            nuevo_rol = st.selectbox("Rol:", ["Usuario", "Administrador"])
            
            if st.button("💾 Completar Registro", use_container_width=True):
                user_key = nuevo_user.strip().lower()
                if nuevo_user.strip() == "" or nuevo_pass.strip() == "":
                    st.error("⚠️ Campos vacíos.")
                elif user_key in st.session_state.usuarios:
                    st.error("⚠️ El usuario ya existe.")
                elif nuevo_rol == "Administrador" and any(d["role"] == "Administrador" for d in st.session_state.usuarios.values()):
                    st.error("🛑 Variedades JAW ya cuenta con un Administrador principal. Regístrate como 'Usuario'.")
                else:
                    st.session_state.usuarios[user_key] = {"password": nuevo_pass, "role": nuevo_rol}
                    st.success("🎉 ¡Registrado con éxito! Ya puedes iniciar sesión.")

# -----------------------------------------------------------------
# CONTROL DE JORNADA LABORAL BLOQUEADA
# -----------------------------------------------------------------
elif not st.session_state.laborando and st.session_state.rol_actual != "Administrador":
    st.markdown('<div style="background-color:#FF4B4B; padding:40px; border-radius:15px; text-align:center; color:white;"><h1>🛑 NO ESTAMOS LABORANDO</h1><p>El Administrador de Variedades JAW cerró el sistema por el día de hoy.</p></div>', unsafe_allow_html=True)
    if st.button("🚪 Salir de la Cuenta", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

# -----------------------------------------------------------------
# PANEL PRINCIPAL (ADENTRO)
# -----------------------------------------------------------------
else:
    col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
    with col_h1:
        st.markdown(f"## 📦 Variedades JAW — Panel de {st.session_state.rol_actual.upper()}")
        st.write(f"👤 Activo: **{st.session_state.usuario_actual.upper()}**")
    with col_h2:
        st.markdown(f'<div class="reloj-style">🕒 {hora_reloj}</div>', unsafe_allow_html=True)
    with col_h3:
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.autenticado = False
            st.rerun()
            
    st.divider()

    # --- CONTROL DE ALERTAS DE 30 MINUTOS ---
    if st.session_state.ordenes_admin:
        st.markdown("### 📢 Órdenes del Administrador en Curso")
        for idx, orden in enumerate(st.session_state.ordenes_admin):
            if not orden["completada"]:
                minutos_pasados = int((datetime.now() - orden["hora_creacion"]).total_seconds() / 60)
                
                if minutos_pasados >= 30:
                    st.markdown(f"""
                        <div class="alerta-grave">
                            🚨 ¡AVISO DE INCUMPLIMIENTO! El Admin ordenó hace {minutos_pasados} minutos: 
                            "{orden['tarea']}". ¡Esto debió corregirse hace tiempo! Modifica la tabla de inmediato.
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning(f"📌 **Orden Pendiente (Hace {minutos_pasados} min):** {orden['tarea']}")
                
                if st.button(f"✅ Marcar como Solucionado: '{orden['tarea'][:20]}...'", key=f"btn_orden_{idx}"):
                    st.session_state.ordenes_admin[idx]["completada"] = True
                    st.success("¡Orden completada!")
                    st.rerun()
        st.divider()

    # --- BARRA LATERAL (HERRAMIENTAS & CALCULADORA SENCILLA TIPO TELÉFONO) ---
    st.sidebar.markdown("## ⚙️ Herramientas JAW")
    
    with st.sidebar.expander("🧮 Calculadora Sencilla", expanded=True):
        
        # Apertura de Contenedor Chasis de Plástico Físico
        st.markdown('<div class="chasis-3d">', unsafe_allow_html=True)
        
        # 🟢 PANTALLA DIGITAL LCD
        display_text = st.session_state.pantalla_calc if st.session_state.pantalla_calc else "0"
        st.markdown(f"""
            <div style="
                background-color: #0b0d10; 
                padding: 16px; 
                border-radius: 6px; 
                text-align: right; 
                font-family: 'Courier New', monospace; 
                font-size: 26px; 
                color: #00ff66; 
                text-shadow: 0 0 12px #00ff66;
                border-bottom: 3px solid #3a3d46;
                border-right: 2px solid #3a3d46;
                border-top: 4px solid #050607;
                border-left: 4px solid #050607;
                box-shadow: inset 0px 4px 10px rgba(0,0,0,0.9);
                margin-bottom: 20px;
                font-weight: bold;
                overflow-x: auto;
                white-space: nowrap;
            ">
                {display_text}
            </div>
        """, unsafe_allow_html=True)

        # Función inyectora de caracteres matemáticos
        def agregar(simbolo):
            if st.session_state.pantalla_calc == "Error":
                st.session_state.pantalla_calc = ""
            st.session_state.pantalla_calc += str(simbolo)

        # FILA 1: Comandos de Limpieza y Control Básicos
        r1 = st.columns(4)
        with r1[0]:
            if st.button("C", key="calc_c"):
                st.session_state.pantalla_calc = ""
                st.rerun()
        with r1[1]:
            if st.button("DEL", key="calc_del"):
                if st.session_state.pantalla_calc == "Error":
                    st.session_state.pantalla_calc = ""
                else:
                    st.session_state.pantalla_calc = st.session_state.pantalla_calc[:-1]
                st.rerun()
        with r1[2]:
            if st.button("√", key="calc_raiz"): agregar("sqrt("); st.rerun()
        with r1[3]:
            if st.button("÷", key="calc_div"): agregar("/"); st.rerun()

        # FILA 2: Bloque Numérico Sencillo (7, 8, 9 y Operador)
        r2 = st.columns(4)
        with r2[0]:
            if st.button("7", key="calc_7"): agregar("7"); st.rerun()
        with r2[1]:
            if st.button("8", key="calc_8"): agregar("8"); st.rerun()
        with r2[2]:
            if st.button("9", key="calc_9"): agregar("9"); st.rerun()
        with r2[3]:
            if st.button("×", key="calc_mult"): agregar("*"); st.rerun()

        # FILA 3: Bloque Numérico Sencillo (4, 5, 6 y Operador)
        r3 = st.columns(4)
        with r3[0]:
            if st.button("4", key="calc_4"): agregar("4"); st.rerun()
        with r3[1]:
            if st.button("5", key="calc_5"): agregar("5"); st.rerun()
        with r3[2]:
            if st.button("6", key="calc_6"): agregar("6"); st.rerun()
        with r3[3]:
            if st.button("-", key="calc_resta"): agregar("-"); st.rerun()

        # FILA 4: Bloque Numérico Sencillo (1, 2, 3 y Operador)
        r4 = st.columns(4)
        with r4[0]:
            if st.button("1", key="calc_1"): agregar("1"); st.rerun()
        with r4[1]:
            if st.button("2", key="calc_2"): agregar("2"); st.rerun()
        with r4[2]:
            if st.button("3", key="calc_3"): agregar("3"); st.rerun()
        with r4[3]:
            if st.button("+", key="calc_suma"): agregar("+"); st.rerun()

        # FILA 5: Base de la Calculadora (0, Punto e Igual básico)
        r5 = st.columns([2, 1, 1])
        with r5[0]:
            if st.button("0", key="calc_0"): agregar("0"); st.rerun()
        with r5[1]:
            if st.button(".", key="calc_punto"): agregar("."); st.rerun()
        with r5[2]:
            if st.button("＝", key="calc_igual_corto"):
                if st.session_state.pantalla_calc.strip() != "":
                    try:
                        diccionario_matematico = {"sqrt": math.sqrt}
                        operacion_cruda = st.session_state.pantalla_calc
                        resultado_evaluado = eval(operacion_cruda, {"__builtins__": None}, diccionario_matematico)
                        
                        if isinstance(resultado_evaluado, float) and resultado_evaluado.is_integer():
                            resultado_evaluado = int(resultado_evaluado)
                        
                        st.session_state.pantalla_calc = str(resultado_evaluado)
                        st.rerun()
                    except Exception:
                        st.session_state.pantalla_calc = "Error"
                        st.rerun()
                    
        # Cierre del chasis físico 3D
        st.markdown('</div>', unsafe_allow_html=True)

    # 👑 PODERES EXCLUSIVOS DEL ADMIN
    if st.session_state.rol_actual == "Administrador":
        st.sidebar.divider()
        st.sidebar.markdown("### 👑 Controles de Admin")
        
        st.sidebar.subheader("🔒 Estado de la Jornada")
        if st.session_state.laborando:
            if st.sidebar.button("🔴 CERRAR: YA NO ESTAMOS LABORANDO", use_container_width=True):
                st.session_state.laborando = False
                st.rerun()
        else:
            if st.sidebar.button("🟢 REABRIR JORNADA LABORAL", use_container_width=True):
                st.session_state.laborando = True
                st.rerun()
        
        st.sidebar.divider()
        st.sidebar.subheader("📣 Mandar Cambio Directo a Usuarios")
        nueva_tarea = st.sidebar.text_input("Escribe la orden (Ej: Cambiar precio de blusas):")
        if st.sidebar.button("🚀 Emitir Orden (Corre Tiempo)", use_container_width=True):
            if nueva_tarea.strip() != "":
                st.session_state.ordenes_admin.append({
                    "tarea": nueva_tarea,
                    "hora_creacion": datetime.now(),
                    "completada": False
                })
                st.sidebar.success("¡Orden enviada con tiempo límite de 30 minutos!")
                st.rerun()

        lista_usuarios = [u for u in st.session_state.usuarios.keys() if st.session_state.usuarios[u]["role"] != "Administrador"]
        if lista_usuarios:
            st.sidebar.subheader("🗑️ Eliminar Colaboradores")
            user_del = st.sidebar.selectbox("Selecciona al usuario para revocar:", lista_usuarios)
            if st.sidebar.button("❌ Eliminar Acceso", use_container_width=True):
                del st.session_state.usuarios[user_del]
                st.sidebar.success(f"Usuario {user_del} eliminado.")
                st.rerun()

    # --- PESTAÑAS DE TRABAJO ---
    tab_inv, tab_ventas, tab_chat = st.tabs(["📊 Inventario de Mercancía", "💰 Registro de Ventas y Caja", "💬 Muro de Mensajes"])
    
    # PESTAÑA 1: INVENTARIO
    with tab_inv:
        with st.expander("✨ Agregar Nueva Mercancía al Stock", expanded=True):
            with st.form("form_inventario", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                with col1: prod = st.text_input("Nombre del Artículo:")
                with col2: cant = st.number_input("Cantidad Disponible (Stock):", min_value=1, step=1)
                with col3: precio = st.number_input("Precio por Unidad ($):", min_value=0, step=500)
                
                if st.form_submit_button("🛒 Guardar en Inventario", use_container_width=True):
                    if prod.strip() != "" and precio > 0:
                        nueva_mercancia = pd.DataFrame([{
                            "Fecha": fecha_completa, "Año": ano_act, "Mes": mes_act, "Día": dia_act,
                            "Producto": prod, "Cantidad": cant, "Precio ($)": precio,
                            "Registrado Por": st.session_state.usuario_actual
                        }])
                        st.session_state.inventario = pd.concat([st.session_state.inventario, nueva_mercancia], ignore_index=True)
                        st.success(f"¡{prod} guardado en stock!")
                        st.rerun()

        st.markdown("### 📋 Tabla de Stock Actual")
        if not st.session_state.inventario.empty:
            st.session_state.inventario = st.data_editor(st.session_state.inventario, use_container_width=True, hide_index=True)
            if st.session_state.rol_actual == "Administrador" and st.button("🚨 Reiniciar Tabla de Stock"):
                st.session_state.inventario = pd.DataFrame(columns=["Fecha", "Año", "Mes", "Día", "Producto", "Cantidad", "Precio ($)", "Registrado Por"])
                st.rerun()
        else:
            st.warning("Inventario vacío.")

    # PESTAÑA 2: REGISTRO DE VENTAS
    with tab_ventas:
        col_izq, col_der = st.columns(2)
        
        with col_izq:
            st.markdown("### 💵 Registrar Movimiento de Venta")
            tipo_registro = st.radio("Método de venta:", ["✍️ Registro Manual Directo", "📦 Desde el Inventario Guardado"], horizontal=True)
            
            with st.form("form_ventas", clear_on_submit=True):
                if tipo_registro == "✍️ Registro Manual Directo":
                    v_prod = st.text_input("Escribe el nombre del artículo vendido:", placeholder="Ej: Vestido enterizo negro")
                    v_cant = st.number_input("Cantidad Vendida:", min_value=1, step=1)
                    v_precio = st.number_input("Precio Cobrado por Unidad ($):", min_value=0, step=500)
                    
                    if st.form_submit_button("💰 Registrar Venta Directa", use_container_width=True):
                        if v_prod.strip() != "" and v_precio > 0:
                            total_dinero = v_cant * v_precio
                            nueva_venta = pd.DataFrame([{
                                "Hora/Fecha": f"{fecha_completa} {hora_reloj}",
                                "Producto Vendido": v_prod,
                                "Cant. Vendida": v_cant,
                                "Total Recaudado ($)": total_dinero,
                                "Vendedor": st.session_state.usuario_actual
                            }])
                            st.session_state.ventas = pd.concat([st.session_state.ventas, nueva_venta], ignore_index=True)
                            st.success("🎉 ¡Venta manual registrada exitosamente!")
                            st.rerun()
                        else:
                            st.error("Por favor completa los datos de la venta.")
                
                else:
                    if not st.session_state.inventario.empty:
                        lista_productos_disponibles = st.session_state.inventario["Producto"].unique()
                        v_prod_inv = st.selectbox("Selecciona el producto del stock:", lista_productos_disponibles)
                        v_cant_inv = st.number_input("Cantidad Vendida:", min_value=1, step=1)
                        
                        if st.form_submit_button("💰 Confirmar y Descontar de Stock", use_container_width=True):
                            idx_prod = st.session_state.inventario[st.session_state.inventario["Producto"] == v_prod_inv].index[0]
                            stock_actual = st.session_state.inventario.at[idx_prod, "Cantidad"]
                            precio_unidad = st.session_state.inventario.at[idx_prod, "Precio ($)"]
                            
                            if v_cant_inv > stock_actual:
                                st.error(f"⚠️ ¡Error! No puedes vender {v_cant_inv} unidades. Solo tienes {stock_actual} en stock.")
                            else:
                                st.session_state.inventario.at[idx_prod, "Cantidad"] = stock_actual - v_cant_inv
                                total_dinero = v_cant_inv * precio_unidad
                                nueva_venta = pd.DataFrame([{
                                    "Hora/Fecha": f"{fecha_completa} {hora_reloj}",
                                    "Producto Vendido": v_prod_inv,
                                    "Cant. Vendida": v_cant_inv,
                                    "Total Recaudado ($)": total_dinero,
                                    "Vendedor": st.session_state.usuario_actual
                                }])
                                st.session_state.ventas = pd.concat([st.session_state.ventas, nueva_venta], ignore_index=True)
                                st.success(f"🎉 ¡Venta procesada y stock descontado!")
                                st.rerun()
                    else:
                        st.warning("No hay productos en el inventario para cruzar datos. Usa el modo manual.")
                        st.form_submit_button("Deshabilitado", disabled=True)
                        
        with col_der:
            st.markdown("### 💸 Añadir o Descontar de las Ganancias")
            st.caption("Usa esta sección para meter base, registrar gastos imprevistos, compras o retirar dinero.")
            
            with st.form("form_ajustes_caja", clear_on_submit=True):
                tipo_mov = st.radio("Acción a realizar:", ["➕ Añadir Dinero (Ingreso / Base Inicial)", "➖ Descontar Dinero (Egreso / Gasto / Retiro)"], horizontal=True)
                desc_mov = st.text_input("Descripción del movimiento:", placeholder="Ej: Pago de bolsas, Base de la mañana, Almuerzos")
                monto_mov = st.number_input("Monto en Efectivo ($):", min_value=0, step=500)
                
                if st.form_submit_button("💾 Registrar Ajuste en Caja", use_container_width=True):
                    if desc_mov.strip() != "" and monto_mov > 0:
                        tipo_limpio = "Ingreso" if "Añadir" in tipo_mov else "Egreso"
                        nuevo_ajuste = pd.DataFrame([{
                            "Hora/Fecha": f"{fecha_completa} {hora_reloj}",
                            "Tipo": tipo_limpio,
                            "Descripción": desc_mov,
                            "Monto ($)": monto_mov,
                            "Responsable": st.session_state.usuario_actual
                        }])
                        st.session_state.ajustes_caja = pd.concat([st.session_state.ajustes_caja, nuevo_ajuste], ignore_index=True)
                        st.success("📝 ¡Flujo de dinero guardado con éxito!")
                        st.rerun()
                    else:
                        st.error("Rellena la descripción y el monto válido.")

        st.divider()
        st.markdown("### 📊 Balance General de Caja en Vivo")
        
        tot_ventas = st.session_state.ventas["Total Recaudado ($)"].sum() if not st.session_state.ventas.empty else 0
        tot_ingresos = st.session_state.ajustes_caja[st.session_state.ajustes_caja["Tipo"] == "Ingreso"]["Monto ($)"].sum() if not st.session_state.ajustes_caja.empty else 0
        tot_egresos = st.session_state.ajustes_caja[st.session_state.ajustes_caja["Tipo"] == "Egreso"]["Monto ($)"].sum() if not st.session_state.ajustes_caja.empty else 0
        
        ganancia_neta_total = tot_ventas + tot_ingresos - tot_egresos
        
        m1, m2, m3 = st.columns(3)
        with m1: st.metric(label="🛍️ (+) Total por Ventas", value=f"${tot_ventas:,.0f} COP")
        with m2: st.metric(label="📥 (+) Total Dinero Añadido", value=f"${tot_ingresos:,.0f} COP")
        with m3: st.metric(label="📤 (-) Total Dinero Descontado", value=f"${tot_egresos:,.0f} COP")
        
        st.markdown(f'<div class="ganancia-box">💵 GANANCIA NETA TOTAL EN EFECTIVO: ${ganancia_neta_total:,.0f} COP</div>', unsafe_allow_html=True)
        st.divider()
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("#### 🛒 Registro Histórico de Ventas")
            if not st.session_state.ventas.empty:
                st.session_state.ventas = st.data_editor(st.session_state.ventas, use_container_width=True, num_rows="dynamic", key="tabla_ventas_editor")
            else:
                st.info("Sin registros de ventas.")
                
        with col_t2:
            st.markdown("#### 💸 Historial de Ajustes (Añadido/Descontado)")
            if not st.session_state.ajustes_caja.empty:
                st.session_state.ajustes_caja = st.data_editor(st.session_state.ajustes_caja, use_container_width=True, num_rows="dynamic", key="tabla_ajustes_editor")
            else:
                st.info("Sin movimientos de dinero extra.")

    # PESTAÑA 3: CHAT
    with tab_chat:
        st.markdown("### 💬 Muro de Coordinación Interna — Variedades JAW")
        box_mensajes = st.container(height=250)
        with box_mensajes:
            for msg in st.session_state.chat:
                st.markdown(f"""
                    <div class="chat-card">
                        <span style="color:#6C63FF; font-weight:bold;">[{msg["usuario"].upper()}]:</span> 
                        <span class="chat-text">{msg["mensaje"]}</span>
                    </div>
                """, unsafe_allow_html=True)
                
        with st.form("envio_notas", clear_on_submit=True):
            texto_nota = st.text_input("Escribe tu nota para el equipo aquí:")
            if st.form_submit_button("Mandar Nota al Muro 📌") and texto_nota.strip() != "":
                st.session_state.chat.append({"usuario": st.session_state.usuario_actual, "mensaje": texto_nota})
                st.rerun()