<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1">
<context>
    <name>GtfsShapesCreator</name>
    <message>
        <location filename="../gtfs_shapes_creator.py" line="200" />
        <source>&amp;GTFS Shapes Creator</source>
        <translation>&amp;Creador de Formas GTFS</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator.py" line="169" />
        <source>Create the shapes.txt for your GTFS</source>
        <translation>Crea el archivo shapes.txt para tu GTFS</translation>
    </message>
</context>
<context>
    <name>GtfsShapesCreatorDockWidget</name>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="204" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on files_to_delete.json</source>
        <translation>Los archivos temporales se eliminarán solo reiniciando QGIS, sus rutas se guardan en files_to_delete.json</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="222" />
        <source>Starting at {datetime.datetime.now().time().replace(microsecond=0)} the real job (..be patient, please)</source>
        <translation>A partir de {datetime.datetime.now().time().replace(microsecond=0)} el trabajo real (..por favor sé paciente)</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1750" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on {files_to_delete_next_bus_loading_json}</source>
        <translation>Los archivos temporales se eliminarán solo reiniciando QGIS, sus rutas se guardan en {files_to_delete_next_bus_loading_json}</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1184" />
        <source>at {datetime.datetime.now().time().replace(microsecond=0)} : GTFS Shapes Creator has started routing..</source>
        <translation>a {datetime.datetime.now().time().replace(microsecond=0)} : Creador de Formas GTFS ha iniciado el enrutamiento..</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1222" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on the files_to_delete.json</source>
        <translation>Los archivos temporales se eliminarán solo reiniciando QGIS, sus rutas se guardan en files_to_delete.json</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1326" />
        <source>Something wrong went creating the trips, GO BACK to step 1, remove the buses concerned and try again</source>
        <translation>Algo salió mal al crear los viajes, VUELVE al paso 1, elimina los autobuses afectados e intenta de nuevo</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1386" />
        <source>{trip} is missing</source>
        <translation>{trip} está faltando</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1409" />
        <source>at {datetime.datetime.now().time().replace(microsecond=0)} : Integrating the shapes to the GTFS file take much less time</source>
        <translation>a {datetime.datetime.now().time().replace(microsecond=0)} : La integración de las formas en el archivo GTFS toma mucho menos tiempo</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1565" />
        <source>It's DONE! Find your file in {zip_file}, CONGRATULATION!</source>
        <translation>¡Es HECHO! Encuentra tu archivo en {zip_file}, ¡FELICITACIONES!</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1717" />
        <source>you have never run the plugins with the </source>
        <translation>nunca ha ejecutado el plugin con</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1739" />
        <source>the </source>
        <translation>el</translation>
    </message>
</context>
<context>
    <name>GtfsShapesCreatorDockWidgetBase</name>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="20" />
        <source>GTFS Shapes Creator</source>
        <translation>Creador de Formas GTFS</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="42" />
        <source>Download a GTFS on opendatatransport.swiss</source>
        <translation>Descarga un GTFS en opendatatransport.swiss</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="61" />
        <source>Browse to the GTFS unzipped Folder</source>
        <translation>Busca la carpeta GTFS descomprimida</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="130" />
        <source>1st step - agencies selection</source>
        <translation>1er paso - selección de agencias</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="148" />
        <source>Update Agencies</source>
        <translation>Actualizar Agencias</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="189" />
        <source>Search the agency</source>
        <translation>Buscar la agencia</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="214" />
        <source>Load the PT lines for the selected agencies</source>
        <translation>Cargue las líneas PT para las agencias seleccionadas</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="241" />
        <source>2nd step - transports selection</source>
        <translation>2do paso - selección de transportes</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="287" />
        <source>Load the stops and create the roads/rails 
networks for the selected transports</source>
        <translation>Cargue las paradas y cree las redes de carreteras/ferrocarriles para los transportes seleccionados</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="301" />
        <source>It will take lot of time, be patient...</source>
        <translation>Tomará mucho tiempo, sé paciente...</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="314" />
        <source>Remove precedent loaded liens</source>
        <translation>Elimina las líneas cargadas anteriormente</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="328" />
        <source>3rd step - move the off-road stops</source>
        <translation>3er paso - mover las paradas fuera de carretera</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="365" />
        <source>Zoom on the selected Stop</source>
        <translation>Zoom en la parada seleccionada</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="381" />
        <source>Create the paths for each trip</source>
        <translation>Crea las rutas para cada viaje</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="395" />
        <source>4th step - correct the transports paths</source>
        <translation>4to paso - corregir las rutas de transporte</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="407" />
        <source>Display Trips</source>
        <translation>Mostrar Viajes</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="440" />
        <source>Create your shapes.txt
and 
the final GTFS .zip file !</source>
        <translation>¡Crea tu shapes.txt y el archivo GTFS .zip final!</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="455" />
        <source>you like those trips ? .. </source>
        <translation>¿te gustan esos viajes? ..</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="475" />
        <source> PUSH THE BUTTON!</source>
        <translation>¡PRESIONA EL BOTÓN!</translation>
    </message>
</context>
</TS>