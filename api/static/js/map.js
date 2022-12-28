
import Map from '../assets/ol/Map.js';
import OSM from '../assets/ol/source/OSM.js';
import TileLayer from '../assets/ol/layer/Tile.js';
import View from '../assets/ol/View.js';


const map = new Map({
    target: 'map',
    layers: [
        new TileLayer({
            source: new OSM(),
        }),
    ],
    view: new View({
        center: [0, 0],
        zoom: 2,
    }),
});