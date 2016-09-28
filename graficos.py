from matplotlib.collections import PathCollection
from mpl_toolkits.basemap import Basemap
from country import Country
import matplotlib.pyplot as plt
import math
import numpy as np


def get_marker_color(ageplayers, league):
    if ageplayers < 25:
        return 'go'
    elif ageplayers < 5.0:
        return 'yo'
    else:
        return 'ro'


def groupData(dataByCombo, leagues, seasons, banHome=False):

    countryToData = {}
    for (country, league, season) in dataByCombo:
        if league in leagues and season in seasons:
            if banHome and ((league == 'premier' and country == 'United Kingdom') or (
                            league == 'bundes' and country == 'Germany') or (
                            league == 'seriea' and country == 'Italy') or (
                            league == 'spain' and country == 'Spain')):
                continue

            lat, lon, age, players = dataByCombo[(country, league, season)]
            if country in countryToData:
                countryToData[country].append((float(age), int(players)))
            else:
                countryToData[country] = [(float(age), int(players))]

    return countryToData


def aggregateData(countryToData, countries):

    lats, lons = [], []
    ages, counts = [], []

    for country in countryToData:
        # if country == 'United Kingdom':
        #     continue
        meanage = 0
        totalplayers = 0
        for age, players in countryToData[country]:
            meanage += age * players
            totalplayers += players
        if totalplayers > 0:
            meanage /= totalplayers
        lats.append(countries[country].lat)
        lons.append(countries[country].lon)
        counts.append(totalplayers)
        ages.append(meanage)

    return lats, lons, ages, counts


def run():

    data = open('tabla_completa.csv', 'r')
    data.readline()
    dataByCombo = {}
    countries = {}

    # se leen los datos del archivo csv y se guardan en un diccionario para luego ser ordenados
    for line in data:
        country, lat, lon, age, league, season, players = line.replace('\n', '').split(',')
        dataByCombo[(country, league, int(season))] = lat, lon, age, players
        if country not in countries:
            countries[country] = Country(('NN', lat, lon, country))

    # se define la forma en que se agruparán los datos
    leagues = ['premier', 'seriea', 'spain', 'bundes']
    seasons = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]

    # se agrupan los datos
    countryToData = groupData(dataByCombo, ['premier'], seasons, banHome=True)
    lats, lons, ages, counts = aggregateData(countryToData, countries)

    # Se grafican los datos
    plt.figure(figsize=(25, 20))
    eq_map = Basemap(projection='merc', resolution='l', area_thresh=1000.0,
                     lat_0=0, lon_0=0, llcrnrlon=-120, llcrnrlat=-56,
                     urcrnrlon=+150, urcrnrlat=70)
    eq_map.drawcoastlines()
    eq_map.drawcountries()
    eq_map.fillcontinents(color='gray')
    # eq_map.drawmapboundary()

    # TODO: ELegir qué gráficos mostrar y estamos listos
    maxs = max(counts)

    xs = []
    ys = []
    sizes = []
    colors = []

    # Se obtienen las coordenadas y valores
    for lat, lon, age, count in zip(lats, lons, ages, counts):
        x, y = eq_map(lon, lat)
        xs.append(x)
        ys.append(y)
        colors.append(age)
        sizes.append(getMarkerSize(count, maxs))

    # para chequear q el tamaño del marcador represente el área y no el radio
    # x1, y1 = eq_map(-75, -35)
    # x2, y2 = eq_map(-75, -33.6)
    # x3, y3 = eq_map(-75, -36.5)
    # xs = [x1, x2, x3]
    # ys = [y1, y2, y3]
    # colors = [25, 27, 30]
    # sizes = [800, 200, 200]
    pathCollection = eq_map.scatter(xs, ys, marker='o', c=colors, cmap='jet', s=sizes)
    pathCollection.set_zorder(2)
    plt.colorbar()

    # Título
    title_string = "Jugadores extranjeros en la Premier League\n"
    title_string += "temporadas %d a %d" % (seasons[0], seasons[-1])
    plt.title(title_string)

    plt.show()


def colorTest():
    # Have colormaps separated into categories:
    # http://matplotlib.org/examples/color/colormaps_reference.html

    cmaps = [('Sequential', ['Blues', 'BuGn', 'BuPu',
                             'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                             'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
                             'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']),
             ('Sequential (2)', ['afmhot', 'autumn', 'bone', 'cool',
                                 'copper', 'gist_heat', 'gray', 'hot',
                                 'pink', 'spring', 'summer', 'winter']),
             ('Diverging', ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
                            'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
                            'seismic']),
             ('Qualitative', ['Accent', 'Dark2', 'Paired', 'Pastel1',
                              'Pastel2', 'Set1', 'Set2', 'Set3']),
             ('Miscellaneous', ['gist_earth', 'terrain', 'ocean', 'gist_stern',
                                'brg', 'CMRmap', 'cubehelix',
                                'gnuplot', 'gnuplot2', 'gist_ncar',
                                'nipy_spectral', 'jet', 'rainbow',
                                'gist_rainbow', 'hsv', 'flag', 'prism'])]

    nrows = max(len(cmap_list) for cmap_category, cmap_list in cmaps)
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    def plot_color_gradients(cmap_category, cmap_list):
        fig, axes = plt.subplots(nrows=nrows)
        fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99)
        axes[0].set_title(cmap_category + ' colormaps', fontsize=14)

        for ax, name in zip(axes, cmap_list):
            ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
            pos = list(ax.get_position().bounds)
            x_text = pos[0] - 0.01
            y_text = pos[1] + pos[3] / 2.
            fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)

        # Turn off *all* ticks & spines, not just the ones with colormaps.
        for ax in axes:
            ax.set_axis_off()

    for cmap_category, cmap_list in cmaps:
        plot_color_gradients(cmap_category, cmap_list)

    plt.show()


def getMarkerSize(count, maxs):
    maxradius = 450
    # maxmark = maxradius * math.sqrt(count / maxs)
    # # return count * maxmark / maxs
    return count * maxradius / maxs


if __name__ == '__main__':
    run()
