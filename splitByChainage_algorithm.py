# -*- coding: utf-8 -*-


__author__ = 'drew'
__date__ = '2021-09-09'
__copyright__ = '(C) 2021 by drew'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from PyQt5.QtCore import QVariant

from qgis.PyQt.QtCore import QCoreApplication


from qgis.core import (QgsProcessing,
                       QgsFeature,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterBoolean,
                       QgsExpression,
                       QgsExpressionContext,
                       QgsExpressionContextUtils,
                       QgsField)


#from . import splitFeature
from . import split
from . import substring

#import logging# logging doesn't seem to work well with this
#import sys




class splitByChainageAlgorithm(QgsProcessingAlgorithm):


    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    #OUTPUT = 'OUTPUT'
    #INPUT = 'INPUT'
    #FIELD = None
    #STEP = 'step'
    
    
    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """


        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                #self.INPUT,
                name = 'INPUT'
                ,description = self.tr('Input layer')
                ,types = [QgsProcessing.TypeVectorLine]
            )
        )


        self.addParameter(
            QgsProcessingParameterDistance(
                name = 'STEP'
                ,description = self.tr('step between start and end chainages. Negative for reverse direction.')
                ,defaultValue = 10.0
                ,parentParameterName = 'INPUT'#linked to crs of input
            )
        )
                                                      

        #field with section length
        self.addParameter(QgsProcessingParameterField(name = 'FIELD'
                                                      ,description = self.tr('Treat section length as this field. Same units as step.')
                                                      ,optional = True
                                                     ,parentLayerParameterName='INPUT'
                                                     ,type = QgsProcessingParameterField.Numeric
                                                      ))

       #field with Reverse direction bool
        #self.addParameter(QgsProcessingParameterBoolean(name = 'REVERSE',description = self.tr('Reverse direction.')))

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                name = 'OUTPUT'
                #,self.tr('Output layer')
                ,description = 'Output layer'
            )
        )




        
        

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(parameters, 'INPUT', context)
        
        fields = source.fields()
        fields.append(QgsField('source_id', QVariant.Int))
        fields.append(QgsField('start_chainage', QVariant.Double))
        fields.append(QgsField('end_chainage', QVariant.Double))

        
        (sink, dest_id) = self.parameterAsSink(parameters, 'OUTPUT',
                context, fields, source.wkbType(), source.sourceCrs())


        fieldsParam = self.parameterAsFields(parameters,'FIELD',context)
        #parameterAsString
        if fieldsParam:
            field = fieldsParam[0]
        else:
            field = None
        
        
        if field is None:
            step = self.parameterAsDouble(parameters,'STEP',context)#converts to crs units.
        else:
            step = float(self.parameterAsString(parameters,'STEP',context))#unchanged spinbox value
                
        
        
        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()
        
        for current, feature in enumerate(features):
           
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            if field is None:
                length = feature.geometry().length()
                scale = 1
            else:
                length = feature[field]
                scale = feature.geometry().length()/length
                
            #geometry chainage = geometry length*nominal chainage/nominal length
            
            atts = feature.attributes()  #feature.attributes() is slow
            fid = feature.id()
            
            for startChain,endChain in split.split(length=length,step=step):
                f = QgsFeature(fields)
                f.setAttributes(atts+[fid,float(startChain),float(endChain)])
                f.setGeometry(substring.substring(feature.geometry(),startChain*scale,endChain*scale))
                sink.addFeatures([f])


            # Update the progress bar
            feedback.setProgress(int(current * total))
            

            #context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(vl))


        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {'OUTPUT': dest_id}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'split_by_chainage'


    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Split by chainage')



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
        return splitByChainageAlgorithm()


    def helpUrl(self):
        help_path = os.path.join(os.path.dirname(__file__),'help','split_by_chainage.html')
        return 'file:/'+os.path.abspath(help_path)
        
        
        
        
        
