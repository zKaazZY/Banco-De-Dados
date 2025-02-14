import folium
import pandas as pd
from folium.plugins import PolyLineTextPath

# Carregar os dados
file_path = "/mnt/data/trajetorias_filtradas.csv"
df = pd.read_csv(file_path)

# Filtrar apenas trajetórias que chegam ou saem de SBGL
df_sbgl = df[(df['plan_arr'] == 'SBGL') | (df['plan_dep'] == 'SBGL')]

# Criar um mapa centralizado no SBGL
sbgl_coords = (-22.809999, -43.250556)
mapa = folium.Map(location=sbgl_coords, zoom_start=8)

# Agrupar por trajetória (identificada pelo indicat)
for indicat, trajeto in df_sbgl.groupby('indicat'):
    coordenadas = list(zip(trajeto['lat'], trajeto['lon']))
    
    # Adicionar linha representando a trajetória
    folium.PolyLine(coordenadas, color='blue', weight=2.5, opacity=0.7).add_to(mapa)
    
    # Adicionar marcadores no início e no fim
    if not trajeto.empty:
        folium.Marker(coordenadas[0], popup=f"Início {indicat}", icon=folium.Icon(color='green')).add_to(mapa)
        folium.Marker(coordenadas[-1], popup=f"Fim {indicat}", icon=folium.Icon(color='red')).add_to(mapa)

# Salvar o mapa em um arquivo HTML
mapa.save("mapa_interativo_sbgl.html")

print("Mapa gerado e salvo como 'mapa_interativo_sbgl.html'")
