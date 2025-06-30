import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize

# Datos simulados de tonelaje por hora para el circuito de chancado UNTUCA
# Notación: 'Origen -> Destino' : Toneladas por hora (tph)
flujos_tph = {
    "Tolva Gruesos -> Zaranda Primaria": 84,
    "Zaranda Primaria Oversize -> Chancadora Primaria": 60,
    "Zaranda Primaria Undersize -> Zaranda Secundaria": 24,
    "Chancadora Primaria -> Zaranda Secundaria": 60,
    "Zaranda Secundaria Oversize -> Chancadora Secundaria": 30,
    "Zaranda Secundaria Undersize -> Zaranda Terciaria": 54,
    "Chancadora Secundaria -> Zaranda Terciaria": 30,
    "Zaranda Terciaria Oversize -> Chancadora Terciaria": 10,
    "Zaranda Terciaria Undersize -> Faja 04A": 52,
    "Chancadora Terciaria -> Zaranda Terciaria": 10,
    "Faja 04A -> Tolva Finos #1": 26,
    "Faja 04B -> Tolva Finos #2": 26,
    "Zaranda Terciaria Undersize -> Faja 04B": 26,
}

# Crear DataFrame
df_flujos = pd.DataFrame([
    {"Desde": origen.split(" -> ")[0], "Hacia": origen.split(" -> ")[1], "Ton/h": tph}
    for origen, tph in flujos_tph.items()
])

# Mostrar tabla de flujos al usuario
import ace_tools as tools; tools.display_dataframe_to_user(name="Balance de Masa - Chancado UNTUCA", dataframe=df_flujos)

# Crear grafo de red para visualización
G = nx.DiGraph()
for _, row in df_flujos.iterrows():
    G.add_edge(row["Desde"], row["Hacia"], weight=row["Ton/h"])

# Layout y colores por tonelaje
pos = nx.spring_layout(G, seed=42)
edges = G.edges(data=True)
weights = [edata['weight'] for _, _, edata in edges]
norm = Normalize(vmin=min(weights), vmax=max(weights))
colors = [cm.viridis(norm(w)) for w in weights]

# Graficar red de flujo de mineral
plt.figure(figsize=(14, 10))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue',
        arrowsize=20, edge_color=colors, width=2, font_size=10)
edge_labels = {(u, v): f'{d["weight"]} tph' for u, v, d in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
plt.title("Diagrama de Flujo de Masa - Circuito de Chancado UNTUCA")
plt.axis('off')
plt.tight_layout()
plt.show()

