import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# station names to show on a figure
VERTICES = ['西新井', 'つくば', '南栗橋', '春日部']
# lines to add manually
EDGES = ['つくばエクスプレス', '東武伊勢崎線', '東武日光線', '東武野田線', 'JR埼京線']

line = pd.read_csv('./data/line20220720free.csv')
line = line[['line_cd', 'line_name']]
station = pd.read_csv('./data/station20220720free.csv')
station = station[['station_cd', 'station_name', 'line_cd', 'address', 'lon', 'lat']]
join = pd.read_csv('./data/join20220720.csv')

def main():
    constraint = get_constraint()
    station_sub = station.query(constraint)
    join_sub = join.query(constraint)

    show(station_sub, join_sub)
    

def get_constraint():
    """return query for selected lines"""
    lines_to_go = set()
    for statioin_name in VERTICES:
        line_cds = station[station['station_name']==statioin_name]['line_cd'].values
        for cd in line_cds:
            lines_to_go.add(cd)

    lines_manual_cd = list(map(lambda l: line[line['line_name']==l]['line_cd'].values[0], EDGES))
    for cd in lines_manual_cd:
        lines_to_go.add(cd)

    constraint = ''
    assert len(lines_manual_cd) > 0
    for i, cd in enumerate(lines_to_go):
        if i > 0: constraint += ' or '
        constraint += f'line_cd == {cd}'
    return constraint

def show(station, join):
    #グラフの宣言
    G = nx.Graph()
    #頂点を駅名にする
    G.add_nodes_from(station["station_name"])
    #plotの座標を設定
    pos = {}
    for i, j, k in zip(station["station_name"], station["lon"], station["lat"]):
        pos[i] = (j, k)
    #リストeにstation_nameとstation_cdを格納し、リンクさせる
    e = []
    for i, j in zip(station["station_name"], station["station_cd"]):
        e.append([i, j])
    #グラフに辺情報を加える
    for i, j in zip(join["station_cd1"], join["station_cd2"]):
        for k in e:
            if k[1] == i:
                for l in e:
                    if l[1] == j:
                        G.add_edge(k[0], l[0])
    # g2 = nx.DiGraph(G)
    
    figsize = (8, 8)
    font_family = 'Hiragino Maru Gothic Pro'
    station_font_size = 5

    _, axs = plt.subplots(1, 1, figsize=figsize)
    axs.set_title(f'# VERTICES: {len(VERTICES)}', fontsize=20, fontname=font_family)
    nx.draw_networkx(G, pos, node_color='b', node_size=10,
                    font_size=station_font_size, font_family=font_family)
    for c in list(map(lambda p: pos[p], VERTICES)):
        circle = plt.Circle(c, .05, fill=False, color='red')
        axs.add_artist(circle)
    plt.show()

if __name__ == '__main__':
    main()