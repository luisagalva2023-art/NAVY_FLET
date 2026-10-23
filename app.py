import datetime
import pandas as pd
import streamlit as st
# --- SISTEMA DE AUTENTICACIÓN / LOGIN ---
def check_password():
  """Devuelve True si el usuario ingresó la contraseña correcta."""

  def password_entered():
    # Puedes cambiar "ADMIN123" por la contraseña que tú quieras
    if st.session_state["password"] == "**Fleeuyt**":
      st.session_state["password_correct"] = True
      del st.session_state["password"]  # No guardar la contraseña en memoria
    else:
      st.session_state["password_correct"] = False

  if "password_correct" not in st.session_state:
    st.text_input(
        "🔑 Ingrese la clave de acceso de seguridad (Level-5):",
        type="password",
        on_change=password_entered,
        key="password",
    )
    return False
  elif not st.session_state["password_correct"]:
    st.text_input(
        "🔑 Ingrese la clave de acceso de seguridad (Level-5):",
        type="password",
        on_change=password_entered,
        key="password",
    )
    st.error("⛔ Acceso Denegado: Contraseña incorrecta")
    return False
  else:
    return True


# Si la contraseña no es correcta, detiene la ejecución del resto de la app
if not check_password():
  st.stop()
# Configuración de página
st.set_page_config(
    page_title="US NAVY & USCG // FLEET COMMAND SYSTEM",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo visual avanzado: Escala de grises minimalista, ultra compacto y elegante estilo militar HUD
st.markdown(
    """
    <style>
    .main { background-color: #07090b; }
    html, body, [class*="st-"] {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 12px !important;
        color: #d1d5db;
    }
    .enc-header {
        font-family: 'Courier New', Courier, monospace;
        background: linear-gradient(90deg, #111827 0%, #030712 100%);
        border: 1px solid #1f2937;
        border-left: 3px solid #3b82f6;
        padding: 12px 18px;
        border-radius: 4px;
        color: #9ca3af;
        font-size: 11px;
        letter-spacing: 0.8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
    }
    h1 {
        font-size: 20px !important;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #f3f4f6;
        text-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
    }
    h3 {
        font-size: 12px !important;
        font-weight: 600;
        letter-spacing: 1px;
        color: #60a5fa;
        text-transform: uppercase;
        border-bottom: 1px solid #1f2937;
        padding-bottom: 5px;
        margin-top: 20px;
    }
    /* Estilo profesional para métricas */
    div[data-testid="metric-container"] {
        background-color: #0b0f12;
        border: 1px solid #1f2937;
        padding: 10px 15px;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Panel superior de telemetría e identificación encriptada
st.markdown(
    f"""
    <div class="enc-header">
        <b>SYS-ID:</b> USN-USCG-GLOBAL-INTEL &nbsp;&nbsp;|&nbsp;&nbsp; 
        <b>ACCESS LEVEL:</b> SECURE-5 &nbsp;&nbsp;|&nbsp;&nbsp; 
        <b>LATENCY:</b> 24ms &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>UTC TIMESTAMP:</b> {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
""",
    unsafe_allow_html=True,
)

st.title("⚓ US NAVY & USCG // GLOBAL FLEET COMMAND STATUS")


# --- CONEXIÓN EN VIVO CON GOOGLE SHEETS ---
@st.cache_data(ttl=30)
def load_data_from_cloud():
  sheet_id = "1_2k9uw4QjS-YkRT0EBlMQQ2Tnvl_r3OqOw5DOG8qFzk"
  csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
  try:
    return pd.read_csv(csv_url)
  except Exception as e:
    st.error(
        f"[ERROR DE CONEXIÓN CLOUD] No se pudo acceder al Google Sheet: {e}"
    )
    return pd.DataFrame()


# Cargar datos desde la nube
df = load_data_from_cloud()

# Controles laterales y sincronización mejorados
st.sidebar.markdown("### 🔒 SEC-OPS CONTROLS")
if st.sidebar.button("🔄 Sincronizar Base de Datos"):
  with st.spinner("Estableciendo enlace seguro con Google Sheets..."):
    st.cache_data.clear()
    df = load_data_from_cloud()
  st.sidebar.success("¡Sincronización completada con éxito!")

st.sidebar.markdown("---")
search_query = st.sidebar.text_input(
    "🔍 FILTRAR (HULL / MMSI / NOMBRE)"
).lower()

# Filtrado dinámico
if search_query and not df.empty:
  df = df[
      df["name"].str.lower().str.contains(search_query)
      | df["mmsi"].astype(str).str.contains(search_query)
      | df["hull no."].str.lower().str.contains(search_query)
  ]

# --- MAPA TÁCTICO GLOBAL ---
st.markdown("### 🌐 GLOBAL OPERATIONAL DEPLOYMENT GRID")

map_data = pd.DataFrame({
    "lat": [
        36.8508,
        32.7157,
        47.5615,
        35.2834,
        32.7767,
        21.3069,
        13.4443,
        34.0522,
    ],
    "lon": [
        -76.2859,
        -117.1611,
        -122.6462,
        139.6688,
        -79.9311,
        -157.8583,
        144.7937,
        31.2357,
    ],
    "name": [
        "Norfolk Naval Station",
        "San Diego Naval Base",
        "Bremerton Shipyard",
        "Yokosuka Base (Japan)",
        "North Charleston (USCG)",
        "Pearl Harbor Operations",
        "Guam Forward Post",
        "Middle East Sector",
    ],
})

st.map(map_data, latitude="lat", longitude="lon", zoom=1)


# Colores de estado sutiles y elegantes para la tabla
def color_status(val):
  val_lower = str(val).lower()
  if "available" in val_lower and "post" not in val_lower:
    return "background-color: #064e3b; color: #6ee7b7; font-size: 11px;"
  elif "post deployment availability" in val_lower:
    return "background-color: #78350f; color: #fcd34d; font-size: 11px;"
  elif "maintenance" in val_lower:
    return "background-color: #7f1d1d; color: #fca5a5; font-size: 11px;"
  elif "deployed" in val_lower:
    return "background-color: #1e3a8a; color: #93c5fd; font-size: 11px;"
  elif "training" in val_lower:
    return "background-color: #374151; color: #e5e7eb; font-size: 11px;"
  return ""


# Visualización de la Base de Datos
st.markdown("### 📋 REGISTRO DE UNIDADES NAVALES, LOGÍSTICAS Y USCG")
if not df.empty:
  styled_df = df.style.map(color_status, subset=["status"])
  st.dataframe(styled_df, hide_index=True)
else:
  st.warning("No hay registros disponibles en la nube.")

# Indicadores de estado inferiores rediseñados tipo HUD militar
st.markdown("---")
st.markdown("### 📊 ESTADO DE NODOS DE RED Y FLOTA")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("AVAILABLE", "🟢 STBY", "Nominal")
m2.metric("POST-DEPLOY", "🟠 REST", "Rotación")
m3.metric("MAINTENANCE", "🔴 DRYDOCK", "Reparación")
m4.metric("DEPLOYED", "🔵 ACTIVE", "En Misión")
m5.metric("TRAINING", "⚪ COMP", "Maniobras")