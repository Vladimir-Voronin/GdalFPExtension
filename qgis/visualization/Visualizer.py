import datetime
import os

from pathlib import Path
from qgis.core import *
from osgeo import ogr


class Visualizer:
    @staticmethod
    def update_layer_by_extended_points(address, points: list, include_id=False):
        layer = QgsVectorLayer(address)
        layer.dataProvider().truncate()

        feats = []
        for point in points:
            feat = QgsFeature(layer.fields())
            if include_id:
                feat.setId(point.id)
            feat.setGeometry(point.point)
            feats.append(feat)

        layer.dataProvider().addFeatures(feats)
        layer.triggerRepaint()

    @staticmethod
    def create_new_layer_points(address, points: list):
        layer = QgsVectorLayer(address, 'points', 'ogr')

        layer.dataProvider().truncate()

        feats = []
        for point in points:
            point = QgsGeometry.fromPointXY(point)
            feat = QgsFeature(layer.fields())
            feat.setGeometry(point)
            feats.append(feat)

        layer.dataProvider().addFeatures(feats)
        layer.triggerRepaint()

        QgsProject.instance().addMapLayer(layer)
        return True

    @staticmethod
    def update_layer_by_geometry_objects(address, objects: list):
        layer = QgsVectorLayer(address)
        layer.dataProvider().truncate()
        feats = []
        id_number = 0
        for obj in objects:
            id_number += 1
            feat = QgsFeature(layer.fields())
            feat.setId(id_number)
            feat.setGeometry(obj)
            feats.append(feat)
        layer.dataProvider().addFeatures(feats)
        layer.triggerRepaint()

    @staticmethod
    def update_layer_by_feats_objects(address, feats: list):
        layer = QgsVectorLayer(address)
        layer.dataProvider().truncate()
        layer.dataProvider().addFeatures(feats)
        layer.triggerRepaint()

    @staticmethod
    def create_and_add_new_final_path(project, path_to_add, feats):
        name = 'Final_path'
        now = datetime.datetime.now()
        full_name = name + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) \
                    + '_' + str(now.minute) + '_' \
                    + str(now.second)

        fn = path_to_add + '/' + full_name + '.shp'
        layerFields = QgsFields()

        crs = project.crs()
        save_options = QgsVectorFileWriter.SaveVectorOptions()
        transform_context = QgsProject.instance().transformContext()
        writer = QgsVectorFileWriter.create(fn, layerFields, QgsWkbTypes.LineString, crs,
                                            transform_context,
                                            save_options)

        writer.addFeatures(feats)
        del writer

        my_gpkg = fn + '.gpkg'
        Visualizer.add_gpkg_to_layer_and_change_style(project, my_gpkg, 'final_path_style.qml')

    @staticmethod
    def create_and_add_new_default_graph(project, path_to_add, feats):
        name = 'default_graph'
        now = datetime.datetime.now()
        full_name = name + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) \
                    + '_' + str(now.minute) + '_' \
                    + str(now.second)

        fn = path_to_add + '/' + full_name + '.shp'
        layerFields = QgsFields()

        crs = project.crs()
        save_options = QgsVectorFileWriter.SaveVectorOptions()
        transform_context = QgsProject.instance().transformContext()
        writer = QgsVectorFileWriter.create(fn, layerFields, QgsWkbTypes.LineString, crs,
                                            transform_context,
                                            save_options)

        writer.addFeatures(feats)
        del writer

        my_gpkg = fn + '.gpkg'
        Visualizer.add_gpkg_to_layer_and_change_style(project, my_gpkg, 'default_graph.qml')

    @staticmethod
    def create_and_add_new_path_short_tree(project, path_to_add, feats):
        name = 'short_tree'
        now = datetime.datetime.now()
        full_name = name + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) \
                    + '_' + str(now.minute) + '_' \
                    + str(now.second)

        fn = path_to_add + '/' + full_name + '.shp'
        layerFields = QgsFields()

        crs = project.crs()
        save_options = QgsVectorFileWriter.SaveVectorOptions()
        transform_context = QgsProject.instance().transformContext()
        writer = QgsVectorFileWriter.create(fn, layerFields, QgsWkbTypes.LineString, crs,
                                            transform_context,
                                            save_options)

        writer.addFeatures(feats)
        del writer

        my_gpkg = fn + '.gpkg'
        Visualizer.add_gpkg_to_layer_and_change_style(project, my_gpkg, 'graph_short_tree.qml')

    @staticmethod
    def create_and_add_new_default_points(project, path_to_add, feats):
        name = 'default_points'
        now = datetime.datetime.now()
        full_name = name + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) \
                    + '_' + str(now.minute) + '_' \
                    + str(now.second)

        fn = path_to_add + '/' + full_name + '.shp'
        layerFields = QgsFields()

        crs = project.crs()
        save_options = QgsVectorFileWriter.SaveVectorOptions()
        transform_context = QgsProject.instance().transformContext()
        writer = QgsVectorFileWriter.create(fn, layerFields, QgsWkbTypes.Point, crs,
                                            transform_context,
                                            save_options)

        writer.addFeatures(feats)
        del writer

        my_gpkg = fn + '.gpkg'
        Visualizer.add_gpkg_to_layer_and_change_style(project, my_gpkg, 'default_points.qml')

    @staticmethod
    def add_gpkg_to_layer_and_change_style(project, path_to_gpkg, relative_style_path):
        gpkg_layers = [l.GetName() for l in ogr.Open(path_to_gpkg)]
        layer = QgsVectorLayer(path_to_gpkg + "|layername=" + gpkg_layers[0], gpkg_layers[0], 'ogr')

        path_to_the_style_folder = os.path.dirname(__file__)
        path_to_the_style_folder = Path(path_to_the_style_folder).parents[1]
        style_path = os.path.join(path_to_the_style_folder, r'Styles', relative_style_path)
        layer.loadNamedStyle(style_path)
        layer.triggerRepaint()
        project.addMapLayer(layer)
