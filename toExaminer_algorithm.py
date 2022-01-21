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

import os
import csv

from PyQt5.QtCore import QVariant

from qgis.PyQt.QtCore import QCoreApplication


from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsProcessingParameterDistance,
                       QgsField,
                       QgsProcessingParameterFileDestination,
                       QgsCoordinateTransform,
                       QgsCoordinateReferenceSystem,
                       QgsProject
                       )




#import logging# logging doesn't seem to work well with this
#import sys


'''
group mandatory?
depth optional.
examiner doesn't show features without name.

'''

class toExaminerAlgorithm(QgsProcessingAlgorithm):
    
    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """


        #input layer
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                name = 'layer'
                ,description = self.tr('Input layer')
                ,types = [QgsProcessing.TypeVectorPoint]
            )
        )



        #field with group
        self.addParameter(QgsProcessingParameterField(name = 'groupField'
                                                      ,description = self.tr('Field with annotation group')
                                                      ,optional = True
                                                     ,parentLayerParameterName='layer'
                                                      ))


        #field with name
        self.addParameter(QgsProcessingParameterField(name = 'nameField'
                                                      ,description = self.tr('Field with name')
                                                      ,optional = False
                                                     ,parentLayerParameterName='layer'
                                                      ))


        #field with depth
        self.addParameter(QgsProcessingParameterField(name = 'depthField'
                                                      ,description = self.tr('Field with depth.')
                                                      ,optional = True
                                                     ,parentLayerParameterName='layer'
                                                     ,type = QgsProcessingParameterField.Numeric
                                                      ))



        #output file
        self.addParameter(
            QgsProcessingParameterFileDestination(
                name = 'output'
                ,description = 'Output file'
                ,fileFilter  = '*.txt'
            )
        )


    def parameterAsField(self,parameters,name,context):
        fields = self.parameterAsFields(parameters,name,context)
        if fields:
            return fields[0]
        

    def processAlgorithm(self, parameters, context, feedback):

        source = self.parameterAsSource(parameters, 'layer', context)

        transform = QgsCoordinateTransform(source.sourceCrs(),QgsCoordinateReferenceSystem("EPSG:4326"), QgsProject.instance())
        

        groupField = self.parameterAsField(parameters,'groupField',context)
        nameField = self.parameterAsField(parameters,'nameField',context)
        depthField = self.parameterAsField(parameters,'depthField',context)
            
        output = self.parameterAsFileOutput(parameters,'output',context)
        
        
        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()
 
        
        with open(output,'w') as file:
            file.write('#Group	Name	Depth(m)	Latitude	Longitude\n')
            file.write('#FormatVersion=2.7\n')
            file.write('#Culture=en-GB\n')
            file.write('#CoordinateSystem=Wgs84\n')
            
            #group,name,depth,lat,lon
            fields = [groupField,nameField]


            for current, feature in enumerate(features):
               
                # Stop the algorithm if cancel button has been clicked
                if feedback.isCanceled():
                    break


                #print('\t'.join(featureToList(feature,fields)))
                file.write(writeFeature(feature,groupField,nameField,depthField,transform)+'\n')
                # Update the progress bar
                feedback.setProgress(int(current * total))


        return {'output': output}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'to_examiner'


    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('To examiner')



    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())


    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''


    def tr(self, string):
        return QCoreApplication.translate('Processing', string)


    def createInstance(self):
        return toExaminerAlgorithm()


    def helpUrl(self):
        help_path = os.path.join(os.path.dirname(__file__),'help','to_examiner.html')
        return 'file:/'+os.path.abspath(help_path)
        
        
def featureToList(feature,fields=None):
    if fields is None:
        fields = feature.fields().names()
    return [feature[f] for f in fields if f]
    
    

#feature to string (row)
#if field is null write ''
def writeFeature(feature,groupField,nameField,depthField,transform=None):
    
    p = feature.geometry().asPoint()
    if transform:
        p = transform.transform(p)
        
    fields = [groupField,nameField,depthField]
    
    r = [str(getField(feature,field,'')) for field in fields]+[str(p.y())]+[str(p.x())]#lat,lon
    
    return '\t'.join(r)
    
def getField(feature,field,default=None):
    if field:
        return feature[field]
    return default
    