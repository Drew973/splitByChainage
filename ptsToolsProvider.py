# -*- coding: utf-8 -*-

"""
/***************************************************************************
 splitByChainage
                                 A QGIS plugin
 split linestrings by chainage
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-09-09
        copyright            : (C) 2021 by drew
        email                : drew.bennett@ptsinternational.co.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'drew'
__date__ = '2021-09-09'
__copyright__ = '(C) 2021 by drew'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import QgsProcessingProvider
from pts_tools.split_by_chainage.splitByChainage_algorithm import splitByChainageAlgorithm
from pts_tools.point_to_chainage.pointToChainage import pointToChainageAlgorithm
from pts_tools.to_examiner.toExaminer_algorithm import toExaminerAlgorithm
#from .concatenateFields_algorithm import concatenateFieldsAlgorithm

from pts_tools.distress_processor.distressProcessor import distressProcessorAlg
from pts_tools.distress_processor.process_distress_layer import processDistressLayer
from pts_tools.join_to_network.joinToNetwork import joinToNetworkAlgorithm
from pts_tools.curvature.extract_curved_alg import extractCurvedAlg
from pts_tools.curvature.estimate_curvature_alg import estimateCurvatureAlg

from pts_tools.convert_route.convert_route import convertRoute
from pts_tools.convert_route.convert_route_folder import convertRouteFolder

from pts_tools.reposition_image.reposition_image_alg import repositionImage
from pts_tools.load_mfv_images.load_mfv_images_alg import loadMfvImagesAlg

from pts_tools.load_hsrr.load_hsrr import loadHsrr
from pts_tools.load_cateyes.load_cateyes import loadCateyes

from pts_tools.add_measure.add_measure_alg import addMeasureAlg
from pts_tools.geom_from_lrs.geom_from_lrs_alg import geomFromLrsAlg




class ptsToolsProvider(QgsProcessingProvider):

    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        self.addAlgorithm(splitByChainageAlgorithm())
        self.addAlgorithm(pointToChainageAlgorithm())
        self.addAlgorithm(toExaminerAlgorithm())
    #    self.addAlgorithm(concatenateFieldsAlgorithm())
        self.addAlgorithm(distressProcessorAlg())
        self.addAlgorithm(joinToNetworkAlgorithm())
        self.addAlgorithm(processDistressLayer())
        self.addAlgorithm(extractCurvedAlg())
        self.addAlgorithm(estimateCurvatureAlg())
        self.addAlgorithm(convertRoute())
        self.addAlgorithm(convertRouteFolder())
        self.addAlgorithm(repositionImage())
        self.addAlgorithm(loadMfvImagesAlg())
        self.addAlgorithm(loadHsrr())
        self.addAlgorithm(loadCateyes())
        self.addAlgorithm(addMeasureAlg())
        self.addAlgorithm(geomFromLrsAlg())





    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'PTS tools'


    #def helpId(self):
     #   pass
        
        
    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('PTS tools')

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        return QgsProcessingProvider.icon(self)

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
